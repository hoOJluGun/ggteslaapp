#!/usr/bin/env bash
# --------------------------------------------------------------
#   macOS one‑click installer for GitHub Copilot in VS Code
#   Uses a pre‑generated Copilot token (gsk_…).
# --------------------------------------------------------------
set -euo pipefail

# --------------------  CONFIGURATION -------------------------
# ВАШ COPILOT ТОКЕН (замените, если хотите хранить в переменной)
COPILOT_TOKEN="${COPILOT_TOKEN:-YOUR_COPILOT_TOKEN_HERE}"

# Прокси (если нужен). Оставьте пустым, если не используете.
HTTP_PROXY="${HTTP_PROXY:-}"          # например http://user:pwd@proxy.example.com:8080
HTTPS_PROXY="${HTTPS_PROXY:-}"        # обычно такой же, как HTTP_PROXY
NO_PROXY="${NO_PROXY:-localhost,127.0.0.1}"

# Путь к файлу настроек VS Code
VSCODE_SETTINGS_DIR="${HOME}/Library/Application Support/Code/User"
VSCODE_SETTINGS_FILE="${VSCODE_SETTINGS_DIR}/settings.json"

# --------------------  HELPERS -------------------------------
log()   { echo -e "\033[1;34m[INFO]\033[0m $*"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; exit 1; }

# --------------------  HOME‑BREW -----------------------------
install_homebrew() {
    if ! command -v brew >/dev/null; then
        log "Homebrew не найден – устанавливаю..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # Добавляем brew в PATH для текущего сеанса
        eval "$(/opt/homebrew/bin/brew shellenv)"   # Apple‑silicon
        eval "$(/usr/local/bin/brew shellenv)"    # Intel (если установлен)
    else
        log "Homebrew уже установлен, обновляю..."
        brew update
    fi
}

# --------------------  VS CODE -------------------------------
install_vscode() {
    if command -v code >/dev/null; then
        log "VS Code уже установлен – обновляю до последней версии..."
        brew upgrade --cask visual-studio-code || true
    else
        log "Устанавливаю Visual Studio Code (cask)..."
        brew install --cask visual-studio-code
    fi

    # Убедимся, что `code` в PATH (brew ставит symlink в /usr/local/bin или /opt/homebrew/bin)
    if ! command -v code >/dev/null; then
        error "Команда 'code' не попала в PATH. Перезапустите терминал и повторите."
    fi
}

# --------------------  COPILOT EXTENSION --------------------
install_copilot_extension() {
    log "Устанавливаю расширение GitHub Copilot..."
    code --install-extension GitHub.copilot --force
}

# --------------------  SETTINGS.JSON -----------------------
write_settings_json() {
    mkdir -p "${VSCODE_SETTINGS_DIR}"

    # Если файл уже существует – делаем бэкап
    if [[ -f "${VSCODE_SETTINGS_FILE}" ]]; then
        cp "${VSCODE_SETTINGS_FILE}" "${VSCODE_SETTINGS_FILE}.bak_$(date +%s)"
        log "Бэкап существующего settings.json → ${VSCODE_SETTINGS_FILE}.bak_…"
    fi

    # Базовый JSON‑объект
    cat > "${VSCODE_SETTINGS_FILE}" <<EOF
{
    "github.copilot.enable": true,
    "github.copilot.inlineSuggest.enable": true,
    "github.copilot.suggestOnTriggerCharacters": true,
    "github.copilot.editorInlineSuggest.suggestCount": 2,
    "github.copilot.disableFor": ["markdown"],
    "github.copilot.token": "${COPILOT_TOKEN}"
EOF

    # Добавляем прокси‑параметры, если они заданы
    if [[ -n "${HTTP_PROXY}" || -n "${HTTPS_PROXY}" ]]; then
        cat >> "${VSCODE_SETTINGS_FILE}" <<EOF
    ,"http.proxy": "${HTTP_PROXY}"
    ,"http.proxyStrictSSL": false
    ,"github.copilot.proxy": "${HTTPS_PROXY}"
    ,"http.noProxy": "${NO_PROXY}"
EOF
        log "Прокси‑настройки записаны."
    fi

    # Закрывающая скобка
    echo "}" >> "${VSCODE_SETTINGS_FILE}"
    log "Создан (или обновлён) ${VSCODE_SETTINGS_FILE}"
}

# --------------------  MAIN ---------------------------------
log "=== Старт установки GitHub Copilot (macOS) ==="

install_homebrew
install_vscode
install_copilot_extension
write_settings_json

log "=== Установка завершена! ==="
log "1️⃣ Перезапустите VS Code (закройте и откройте снова)."
log "2️⃣ В правом нижнем углу должно появиться «Copilot: Enabled»."
log "3️⃣ Если статус не появился → откройте палитру (⇧⌘P) и выполните «GitHub Copilot: Sign in»."
log "   (В данном скрипте токен уже записан, обычно вход происходит автоматически.)"
log "🚀 Теперь Copilot готов предлагать подсказки в любой поддерживаемой файле."
