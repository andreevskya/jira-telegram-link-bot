# JIRA-link Telegram bot
Простейший бот, чтобы постить в конференцию название задачи по ссылке на неё.
# Зачем
Потому что публичный доступ в *Jira* может быть ограничен, соответственно для её урлов превью не генерится.
# Зависимости

- *Python 3.8*
- See *requirements.txt* for the list of dependencies.

# Запуск
1. Завести в *Telegram* через *BotFather* бота с отключенными настройками приватности.
2. Перед запуском бота в переменные окружения добавить:
    ```
    export JIRA_URL="Урл JIRA, без / в конце"
    export JIRA_USER="логин пользователя Jira"
    export JIRA_PASSWORD="пароль пользователя Jira"
    export TELEGRAM_BOT_TOKEN="токен бота"
    export TELEGRAM_TARGET_GROUP_CHAT_ID="*"
    ```

3. `python3.8 jira-link-telegram-bot.py`
4. Добавить бота в конференцию.
5. Сделать его админом (так он сможет слушать сообщения в конференции).

Чтобы бот реагировал только в пределах какой-то одной конференции, прописать её идентификатор в переменной окружения `TELEGRAM_TARGET_GROUP_CHAT_ID` (если там `*`, бот выводит в лог идентификатор конференции).

