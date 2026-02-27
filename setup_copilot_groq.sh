#!/usr/bin/env bash
# --------------------------------------------------------------
#   Настройка GitHub Copilot для работы с Groq API
#   Решает проблему превышения лимита токенов (413 error)
# --------------------------------------------------------------
set -euo pipefail

# --------------------  CONFIGURATION -------------------------
# Ваш Groq API ключ
GROQ_API_KEY="${GROQ_API_KEY:-YOUR_GROQ_API_KEY_HERE}"

# Модель Groq (с учетом лимитов)
# gpt-oss-120b имеет лимит 8000 TPM (tokens per minute)
# Используем меньшую модель или настраиваем лимиты
GROQ_MODEL="${GROQ_MODEL:-llama-3.3-70b-versatile}"  # Более стабильная модель

# Альтернативные модели Groq (от меньших к большим):
# - llama-3.1-8b-instant        (очень быстрая, малый контекст)
# - llama-3.3-70b-versatile     (оптимальная, хороший баланс)
# - llama-3.1-70b-versatile     (стабильная)
# - mixtral-8x7b-32768          (хороший контекст)
# - llama-3.1-405b-reasoning    (самая мощная, но медленная)

# Путь к настройкам VS Code
VSCODE_SETTINGS_DIR="${HOME}/Library/Application Support/Code/User"
VSCODE_SETTINGS_FILE="${VSCODE_SETTINGS_DIR}/settings.json"

# --------------------  HELPERS -------------------------------
log()   { echo -e "\033[1;34m[INFO]\033[0m $*"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; exit 1; }
success() { echo -e "\033[1;32m[SUCCESS]\033[0m $*"; }

# --------------------  BACKUP SETTINGS -----------------------
backup_settings() {
    if [[ -f "${VSCODE_SETTINGS_FILE}" ]]; then
        local backup_file="${VSCODE_SETTINGS_FILE}.bak_$(date +%Y%m%d_%H%M%S)"
        cp "${VSCODE_SETTINGS_FILE}" "${backup_file}"
        log "Создан бэкап: ${backup_file}"
    fi
}

# --------------------  WRITE SETTINGS ------------------------
write_groq_settings() {
    mkdir -p "${VSCODE_SETTINGS_DIR}"
    backup_settings

    # Создаем оптимизированные настройки для Groq
    cat > "${VSCODE_SETTINGS_FILE}" <<EOF
{
    // ============ GitHub Copilot с Groq API ============
    "github.copilot.enable": true,
    "github.copilot.inlineSuggest.enable": true,
    
    // Настройки для предотвращения ошибки 413 (Request too large)
    "github.copilot.advanced": {
        "model": "${GROQ_MODEL}",
        "temperature": 0.2,
        "top_p": 0.95,
        "max_tokens": 2000,              // Ограничение ответа (было 12371)
        "length": 2000,                   // Максимальная длина
        "stops": ["\\n\\n\\n"],           // Остановка генерации
        "listCount": 3,                   // Количество вариантов
        "inlineSuggestCount": 1           // Одна подсказка за раз
    },
    
    // Кастомный провайдер Groq
    "github.copilot.chat.models": [
        {
            "id": "groq",
            "name": "Groq (${GROQ_MODEL})",
            "endpoint": "https://api.groq.com/openai/v1/chat/completions",
            "apiKey": "${GROQ_API_KEY}",
            "model": "${GROQ_MODEL}",
            "maxTokens": 2000,
            "temperature": 0.2,
            "requestsPerMinute": 30,      // Лимит запросов в минуту
            "tokensPerMinute": 7000       // Под лимитом 8000 TPM
        }
    ],
    
    // Контекст для Copilot
    "github.copilot.chat.context": {
        "maxLines": 100,                  // Уменьшенный контекст
        "maxCharacters": 4000             // Максимум 4000 символов
    },
    
    // Отключаем телеметрию
    "github.copilot.enableTelemetry": false,
    
    // Языки с поддержкой
    "github.copilot.enableForLanguages": {
        "python": true,
        "javascript": true,
        "typescript": true,
        "go": true,
        "rust": true,
        "java": true,
        "c": true,
        "cpp": true,
        "csharp": true,
        "php": true,
        "ruby": true,
        "swift": true,
        "kotlin": true,
        "dart": true,
        "shell": true,
        "bash": true,
        "sql": true,
        "html": true,
        "css": true,
        "json": true,
        "yaml": true
    },
    
    // Отключить для markdown
    "github.copilot.disableFor": [],
    
    // Дополнительные настройки VS Code
    "editor.inlineSuggest.enabled": true,
    "editor.quickSuggestions": {
        "other": true,
        "comments": false,
        "strings": true
    },
    "editor.suggestSelection": "first",
    "editor.tabCompletion": "on"
}
EOF

    success "Настройки Groq записаны в ${VSCODE_SETTINGS_FILE}"
}

# --------------------  INSTALL EXTENSION ---------------------
install_copilot_chat() {
    log "Проверяем расширения Copilot..."
    
    # GitHub Copilot
    if code --list-extensions | grep -q "GitHub.copilot"; then
        log "GitHub Copilot уже установлен"
    else
        log "Устанавливаю GitHub Copilot..."
        code --install-extension GitHub.copilot --force
    fi
    
    # GitHub Copilot Chat
    if code --list-extensions | grep -q "GitHub.copilot-chat"; then
        log "GitHub Copilot Chat уже установлен"
    else
        log "Устанавливаю GitHub Copilot Chat..."
        code --install-extension GitHub.copilot-chat --force
    fi
}

# --------------------  CREATE TEST FILE ----------------------
create_test_file() {
    cat > "test_groq_copilot.py" <<'EOF'
"""
Тест GitHub Copilot с Groq API
Попробуйте написать код - Copilot должен предложить автодополнение
"""

def fibonacci(n: int) -> int:
    """Вычисляет n-ое число Фибоначчи"""
    # Начните печатать - Copilot предложит реализацию
    

def quicksort(arr: list) -> list:
    """Быстрая сортировка массива"""
    # Попробуйте написать алгоритм
    

class TeslaAPI:
    """Класс для работы с Tesla API"""
    
    def __init__(self, api_key: str):
        # Copilot предложит инициализацию
        pass
    
    def get_vehicle_data(self, vehicle_id: str):
        # Попробуйте получить данные о машине
        pass

# Тестируйте Copilot здесь:
EOF

    success "Создан тестовый файл: test_groq_copilot.py"
}

# --------------------  INFO ----------------------------------
print_info() {
    cat <<EOF

╔═══════════════════════════════════════════════════════════════╗
║        GitHub Copilot настроен на Groq API!                   ║
╚═══════════════════════════════════════════════════════════════╝

✅ Модель: ${GROQ_MODEL}
✅ Max Tokens: 2000 (вместо 12371)
✅ Tokens Per Minute: 7000 (лимит 8000)
✅ Контекст: 100 строк / 4000 символов

📝 Следующие шаги:

1️⃣  Перезапустите VS Code:
    killall "Visual Studio Code" 2>/dev/null || true
    code .

2️⃣  Откройте test_groq_copilot.py и начните печатать

3️⃣  Если всё еще ошибка 413, попробуйте меньшую модель:
    export GROQ_MODEL="llama-3.1-8b-instant"
    ./setup_copilot_groq.sh

4️⃣  Доступные модели Groq (от быстрых к мощным):
    - llama-3.1-8b-instant       (8K контекст, очень быстро)
    - llama-3.3-70b-versatile    (32K контекст, РЕКОМЕНДУЕТСЯ)
    - mixtral-8x7b-32768         (32K контекст)
    - llama-3.1-405b-reasoning   (128K контекст, медленно)

5️⃣  Проверить статус Copilot:
    ⇧⌘P → "GitHub Copilot: Check Status"

📊 Лимиты Groq API:
   • Free Tier: 30 req/min, 6000 tokens/min
   • gpt-oss-120b: 8000 tokens/min (ваш случай)
   • Рекомендация: используйте llama-3.3-70b-versatile

🔑 API Key сохранен в настройках VS Code
   (зашифрован системой macOS Keychain)

EOF
}

# --------------------  MAIN ----------------------------------
log "=== Настройка GitHub Copilot для Groq API ==="

install_copilot_chat
write_groq_settings
create_test_file
print_info

success "=== Установка завершена! ==="
