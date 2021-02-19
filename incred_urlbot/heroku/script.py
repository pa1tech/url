#https://github.com/eternnoir/pyTelegramBotAPI
import telebot,time,os,validators
from telebot import types
from github import Github
import validators
from flask import Flask, request

#Telegram Bot Token
TOKEN="TOKEN"

#Github Auth
git_token = "TOKEN"
g = Github(git_token)
repo = g.get_repo("pa1tech/url")

#Flask App
app = Flask(__name__)

@app.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url='https://incred-urlbot.herokuapp.com/' + TOKEN)
	return "!", 200

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200



start_msg = """Welcome to *!ncred Short URL*

This bot shortens URLs to the form _https://pa1tech.github.io/url/10_

Inline requests are also supported

To know more about the working of the bot : /about
"""

help_msg = """Send me the URL you want to shorten

*Inline Usage:* This bot can be added to Telegram groups and can also be used in personal chats using the inline commands
Example: [@incred_urlbot](https://telegram.me/incred_urlbot) <url>

To know more about the working of the bot : /about
"""

about_msg = """Developer: @pa1tech
Website: https://pa1tech.github.io/

*+* [Gitub Pages URL sortener](https://github.com/nelsontky/gh-pages-url-shortener)
*+* Telegram Bot API - [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
*+* Bot served from [Heroku](https://www.heroku.com)
*+* Bot source code [here](https://github.com/pa1tech/url/tree/master/incred_urlbot)
"""

#Bot settings
bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN") # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help', 'about'])
def send_welcome(message):
	if message.text == '/start':
		bot.send_message(message.chat.id, start_msg)
	elif message.text == '/help':
		bot.send_message(message.chat.id, help_msg)
	elif message.text == '/about':
		bot.send_message(message.chat.id, about_msg)

@bot.message_handler(func=lambda message: True)
def chat_handler(message):
	cid = message.chat.id
	valid=validators. url(message.text)

	if valid:
		i = repo.create_issue(
				title=message.text,
				body=".",
				labels=[]
			)
		bot.send_message(cid, "https://pa1tech.github.io/url/%d"%i.number)
	else:
		bot.reply_to(message, "Invalid URL")

n = 0
@bot.inline_handler(lambda query: len(query.query)>0 )
def query_text(inline_query):
	valid=validators. url(inline_query.query)
	try:
		if valid:
			global n
			n = n+1
			curr_n = n

			open_issues = repo.get_issues(state='open')
			num = open_issues[0].number
			rep = inline_query.query

			r = types.InlineQueryResultArticle('1', rep, input_message_content=types.InputTextMessageContent("https://pa1tech.github.io/url/%d"%(num+1)))
			
			time.sleep(5)
			bot.answer_inline_query(inline_query.id, [r],cache_time=1)
			if n==curr_n:
				i = repo.create_issue(
					title=rep,
					body=".",
					labels=[]
				)
				n = 0		
	except Exception as e:
		print(e)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))