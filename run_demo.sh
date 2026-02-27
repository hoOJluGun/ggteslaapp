#!/bin/bash
# Автоматический скрипт для демонстрации Tesla AI Assistant

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           🚗 Tesla AI Assistant - Автодемонстрация           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Проверка Python
echo "🔍 Проверка окружения..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.9+"
    exit 1
fi

echo "✅ Python3 найден: $(python3 --version)"
echo ""

# Проверка зависимостей
echo "📦 Проверка зависимостей..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден"
    exit 1
fi

echo "✅ Файл зависимостей найден"
echo ""

# Проверка установки пакетов
echo "🔧 Проверка установленных пакетов..."
missing_packages=()

python3 -c "import openai" 2>/dev/null || missing_packages+=("openai")
python3 -c "import requests" 2>/dev/null || missing_packages+=("requests")
python3 -c "import rich" 2>/dev/null || missing_packages+=("rich")

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo "⚠️  Отсутствуют пакеты: ${missing_packages[*]}"
    echo "📥 Установка..."
    pip3 install -r requirements.txt
else
    echo "✅ Все зависимости установлены"
fi
echo ""

# Проверка структуры проекта
echo "📁 Проверка структуры проекта..."
files=(
    "tesla_app/__init__.py"
    "tesla_app/tesla_client.py"
    "tesla_app/ai_assistant.py"
    "tesla_app/cli/__init__.py"
    "tesla_app/cli/main.py"
    "tests/__init__.py"
    "tests/test_tesla_app.py"
)

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Отсутствует файл: $file"
        exit 1
    fi
done

echo "✅ Структура проекта корректна"
echo ""

# Запуск демонстрации
echo "🎬 Запуск демонстрации..."
echo ""
python3 demo.py
demo_exit_code=$?

echo ""
echo "═══════════════════════════════════════════════════════════════"
if [ $demo_exit_code -eq 0 ]; then
    echo "✅ Демонстрация завершена успешно!"
else
    echo "⚠️  Демонстрация завершилась с кодом: $demo_exit_code"
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Информация о запуске приложения
echo "🚀 Для запуска интерактивного режима:"
echo ""
echo "   С AI ассистентом:"
echo "   python3 -m tesla_app.cli.main --token \$TESLA_ACCESS_TOKEN --openai-key \$OPENAI_API_KEY"
echo ""
echo "   Без AI (только управление):"
echo "   python3 -m tesla_app.cli.main --token \$TESLA_ACCESS_TOKEN"
echo ""
echo "   Или установите переменные окружения:"
echo "   export TESLA_ACCESS_TOKEN='your_token'"
echo "   export OPENAI_API_KEY='your_key'"
echo "   python3 -m tesla_app.cli.main"
echo ""

# Запуск тестов
echo "🧪 Запуск тестов..."
python3 -m pytest tests/ -v --tb=short 2>/dev/null || python3 -m unittest tests.test_tesla_app -v 2>/dev/null
test_exit_code=$?

echo ""
echo "═══════════════════════════════════════════════════════════════"
if [ $test_exit_code -eq 0 ]; then
    echo "✅ Все тесты прошли успешно!"
else
    echo "⚠️  Тесты завершились с кодом: $test_exit_code"
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "📚 Документация:"
echo "   • README.md - полное описание проекта"
echo "   • setup_ai_tools.md - настройка AI инструментов"
echo ""

echo "✨ Проект готов к использованию! ✨"
