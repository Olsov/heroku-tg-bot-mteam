import telebot
import requests
import datetime
# для группы -100(номер группы(от{c} и до {_}))
TOKEN = '455147225:AAHSOf6baU9TQ8u-KJhnK7pJsuPvU9TUWCA' # полученный у @BotFather
bot = telebot.TeleBot(TOKEN)
commandsText = '/contact  - Связаться с нами!\r\n/info - Про нас\r\n/help - Все команды\r\n/question - Задать вопрос в Telegram\r\n'
class AnswerClass:
	def setChatId(self,chatId):
		self.chatId = chatId
class Contact:
	def setName(self,name):
		self.name = name
	def setEmail(self,email):
		self.email = email
	def setText(self,text):
		self.text = text
	def returnInfo(self):
		return "Имя:\r\n \r\n"+self.name+"\r\n \r\nПочта:\r\n \r\n"+self.email+"\r\n \r\nТекст:\r\n \r\n"+self.text
	def sendMessageToSite(self):
		r = requests.post('http://beerin.m-team.com.ua/',data={'name':self.name,'email':self.email,'message':self.text})
		return r.text
	def sendTest(self):
		r = requests.post('http://beerin.m-team.com.ua/')
		return 'r.text'
	def returnInfoToChanel(self):
		now = datetime.datetime.now()
		currentTimeText =now.strftime("%Y-%m-%d %H:%M")
		return "Новая заявка с телеграма!\r\n \r\nИмя:\r\n \r\n"+self.name+"\r\n \r\nПочта:\r\n \r\n"+self.email+"\r\n \r\nТекст:\r\n \r\n"+self.text+"\r\n \r\nДата:\r\n \r\n"+currentTimeText
newContact = Contact()
newAnswer = AnswerClass()
@bot.message_handler(commands=['start'])
def start (message):

	sent = bot.send_message(message.chat.id,'Здравствуйте! Мы молодая веб-студия: Mteam\r\n \r\n[Наш сайт:](http://m-team.com.ua/)\r\n \r\nКоманды:\r\n \r\n'+commandsText)

# спрашивай простой вопрос 
@bot.message_handler(commands=['question'])
def question (message):
	sent = bot.send_message(message.chat.id,'Спросите и мы ответим вам в телеграме')
	bot.register_next_step_handler(sent,sendQuestion)
def sendQuestion(message):
	messageText = message.text
	chatId = message.chat.id
	now = datetime.datetime.now()
	currentTimeText =now.strftime("%Y-%m-%d %H:%M")
	bot.send_message(message.chat.id,'Спасибо за вопрос! Мы ответим вам в ближайшее время\r\n \r\n')
	bot.send_message('-1001281509825','Чат:\r\n \r\n{id} \r\n \r\nВопрос:\r\n \r\n{text}\r\n\r\nДата:\r\n \r\n{date}'.format(id=chatId,text=messageText,date =currentTimeText))
# отвечаем на простой вопрос
@bot.message_handler(commands=['answer'])
def answer (message):
	newAnswer = AnswerClass()
	sent = bot.send_message(message.chat.id,'Впишите Id чата')
	bot.register_next_step_handler(sent,sendAnswer)
def sendAnswer(message):
	messageId = message.text
	newAnswer.setChatId(message.text)
	sent = bot.send_message(message.chat.id,'Напишите ответ')
	bot.register_next_step_handler(sent,sendFullAnswer)
def sendFullAnswer(message):
	bot.send_message(message.chat.id,"Ваш ответ отправлен!")
	bot.send_message(newAnswer.chatId,"Вам ответ!\r\n \r\n{text}".format(text=message.text))
#отправяем все полученные данные
@bot.message_handler(commands=['contact'])
def contact (message):
	newContact = Contact()
	sent = bot.send_message(message.chat.id,'Введите Данные по очереди, сначала ФИО')
	bot.register_next_step_handler(sent,setMessageName)
#сохраняем фио - переходим дальше
def setMessageName(message):
	newContact.setName(message.text)
	sent = bot.send_message(message.chat.id,'Ваш имя - {name}. Введите почту:'.format(name=message.text))
	bot.register_next_step_handler(sent,setMessageEmail)
# сохраняем эмеил - переходим дальше
def setMessageEmail(message):
	newContact.setEmail(message.text)
	sent = bot.send_message(message.chat.id,'Ваша почта - {name}. Введите cообщение:'.format(name=message.text))
	bot.register_next_step_handler(sent,setMessageText)

def setMessageText(message):
	# сохраняем сообщение - отправлем запрос на сервер и потом возвращаем ответ, так же постим в группу 
	newContact.setText(message.text)
	# пост в группу
	bot.send_message('-1001281509825',newContact.returnInfoToChanel()+'\r\n \r\nТелеграм:\r\n\r\n@{name}'.format(name=message.from_user.username))
	# ответ
	bot.send_message(message.chat.id,	newContact.sendMessageToSite())

@bot.message_handler(commands=['help'])
def help (message):
	bot.send_message(message.chat.id,'Комманды:\r\n \r\n'+commandsText)
@bot.message_handler(commands=['info'])
def info(message):
	bot.send_message(message.chat.id,'Наши услуги. Решение задач любой сложности\r\n \r\nLanding Page, Интернет Магазин, Корпоративный Сайт, Индивидуальный проект\r\n \r\nЧем мы полезны?\r\n \r\nСтудия интернет-маркетинга M-Team предлагает услуги лидогенерации (привлечение потенциальных клиентов), комплексной рекламы и разработки сайтов любой сложности включая поддержку и обслуживание. Работая с нами Вам не нужно вникать во многие технические подробности, не понятные термины и т.д. Мы предлагаем готовые решения для любого бизнеса выходящего в сеть Интернет. Вы получаете готовый проект "под ключ", который гарантированно приносит Вам доход. Именно этот факт является показателем качества и добросовестного подхода к нашей работе.\r\n \r\nКонтактные данные\r\n \r\nemail - mteam.digital@gmail.com\r\n \r\nViber/WhatsApp/Telegram - +380 (66) 970-97-91')
bot.polling()

