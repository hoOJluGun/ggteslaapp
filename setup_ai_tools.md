# Настройка AI инструментов для ggteslaapp

## Установленные инструменты

### 1. OpenAI Python SDK
**Версия:** 0.27.7  
**Документация:** https://platform.openai.com/docs/api-reference

#### Использование:
```python
import openai

# Установите API ключ
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# Пример запроса
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### 2. GitHub Copilot CLI
**Установлен:** ✅  
**Путь:** `/usr/local/Cellar/node/24.10.0/bin/github-copilot-cli`

#### Настройка:
```bash
# Авторизация (требуется GitHub аккаунт с Copilot)
github-copilot-cli auth
```

#### Использование:
```bash
# Объяснить команду
github-copilot-cli explain "git rebase -i HEAD~3"

# Предложить команду
github-copilot-cli suggest "найти все файлы .py в текущей папке"
```

### 3. Shell GPT (sgpt)
**Установлен:** ✅  
**Требуется:** OpenAI API ключ

#### Настройка:
```bash
# Установить API ключ через переменную окружения
export OPENAI_API_KEY="ваш-ключ-здесь"

# Или через конфигурацию
sgpt --install-integration
```

#### Использование:
```bash
# Простой запрос
sgpt "как создать Flask приложение"

# Выполнить команду
sgpt --shell "показать использование диска"

# Генерация кода
sgpt --code "функция для сортировки массива Python"
```

## Получение API ключей

### OpenAI API Key
1. Зайдите на https://platform.openai.com/api-keys
2. Нажмите "Create new secret key"
3. Скопируйте ключ и сохраните в `.env` файл

### GitHub Copilot
1. Нужна подписка GitHub Copilot
2. Выполните: `github-copilot-cli auth`
3. Следуйте инструкциям в браузере

## Рекомендуемая настройка для проекта

Создайте файл `.env` в корне проекта:
```bash
OPENAI_API_KEY=your-key-here
```

Добавьте в `.gitignore`:
```
.env
```

## Примеры использования для Tesla App

### Генерация API клиента
```bash
sgpt --code "создать Python класс для работы с Tesla API"
```

### Помощь с командами Git
```bash
github-copilot-cli suggest "создать новую ветку для фичи"
```

### Поиск решений
```bash
sgpt "как подключиться к Tesla API используя OAuth"
```
