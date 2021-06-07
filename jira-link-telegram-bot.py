import settings
import telebot
import re
import logging
from jira import JIRA, JIRAError

jira_issue_regex = re.compile('%s/browse/[a-zA-Z]+-[0-9]+' % settings.JIRA_URL, re.IGNORECASE)

def get_jira_issue_caption(jira_client, issue_tag):
    try:
        return jira_client.issue(issue_tag).fields.summary
    except JIRAError as je:
        return "ERROR: " + je.text
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "ERROR"

def handle_message(message):
    if not settings.TELEGRAM_TARGET_GROUP_CHAT_ID:
        print('Received message "%s" from chat "%s" with id "%s"' % (message.text, message.chat.title, message.chat.id))
        return
    if settings.TELEGRAM_TARGET_GROUP_CHAT_ID != str(message.chat.id) and settings.TELEGRAM_TARGET_GROUP_CHAT_ID != '*':
        print('WARNING: received a message "%s" from an unknown chat' % message)
        return
    if not settings.JIRA_URL in message.text:
        return
    jira_links = jira_issue_regex.findall(message.text)
    if not jira_links:
        return
    reply_text = ''
    for jira_link in jira_links:
        issue_tag = jira_link[jira_link.rfind('/') + 1:]
        issue_title = get_jira_issue_caption(jira, issue_tag)
        reply_text += '%s "%s"\n' % (jira_link, issue_title)
    if reply_text:
        bot.send_message(message.chat.id, reply_text)

def handle_messages(messages):
    for message in messages:
        handle_message(message)

if __name__ == '__main__':
    print('Connecting to jira...')
    jira = JIRA(server=settings.JIRA_URL, basic_auth=(settings.JIRA_USER, settings.JIRA_PASSWORD))
    print('Connected ok, starting bot')
    # Обновляем сессию раз в пять минут
    telebot.apihelper.SESSION_TIME_TO_LIVE = 5 * 60
    bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
    telebot.logger.setLevel(logging.DEBUG)
    print('Started.')
    print(bot.get_me())
    print('Polling...')
    bot.set_update_listener(handle_messages)
    bot.infinity_polling()
