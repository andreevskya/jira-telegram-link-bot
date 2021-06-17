import traceback
import settings
import telebot
import re
import logging
from jira import JIRA, JIRAError

jira_issue_regex = re.compile('%s/browse/[a-zA-Z]+-[0-9]+' % settings.JIRA_URL, re.IGNORECASE)
jira = None

def get_jira_issue_caption(jira_client, issue_tag):
    try:
        return jira_client.issue(issue_tag).fields.summary
    except JIRAError as je:
        return "ERROR: " + je.text
    except:
        print("Unexpected error:", traceback.format_exc())
        return "ERROR"

def extract_jira_issues(jira_client, message_text):
    jira_links = jira_issue_regex.findall(message_text)
    issues = []
    for link in jira_links:
        tag = link[link.rfind('/') + 1:]
        title = get_jira_issue_caption(jira_client, tag)
        issues.append((tag, link, title))
    return issues

def compose_message(jira_link_tuples):
    if not jira_link_tuples:
        return None
    return "\n".join(map(lambda x: '[%s](%s) "%s"' % x, jira_link_tuples))
    

def handle_message(message):
    if not settings.TELEGRAM_TARGET_GROUP_CHAT_ID:
        print('Received message "%s" from chat "%s" with id "%s"' % (message.text, message.chat.title, message.chat.id))
        return
    if settings.TELEGRAM_TARGET_GROUP_CHAT_ID != str(message.chat.id) and settings.TELEGRAM_TARGET_GROUP_CHAT_ID != '*':
        print('WARNING: received a message "%s" from an unknown chat' % message)
        return
    jira_links = extract_jira_issues(jira, message.text)
    if not jira_links:
        return
    reply_text = compose_message(jira_links)
    if reply_text:
        bot.send_message(chat_id=message.chat.id, text=reply_text, parse_mode="MARKDOWN")

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
