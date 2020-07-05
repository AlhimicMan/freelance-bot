import configparser
import telebot
import scrapy
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
import logging

class HabrFreelanceTaskHandler():
    login = ""
    password = ""
    _initial_url = "https://freelance.habr.com/tasks"

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def authenticate(self):
        #TODO: Make authentication on habr freelance
        print("Authenticating on habr freelance")


    def hfreelance_crawler():
        """
            Scrapy crawler for Habr freelance.
        """
        print("Crawling habr freelance")

class HabrFreelanceSpider(scrapy.Spider):
    name = 'habr_freelance'
    _initial_url = "https://freelance.habr.com/tasks"

    def start_requests(self):
        yield scrapy.Request(url=self._initial_url, callback=self.parse)

    def parse(self, response):
        print("parsing")
        task_containers = response.css('.content-list__item')
        print(task_containers)


print("Init")

def crawler(bot, chat_id):
    """
        Scrapy freelance crawler.
    """

    process = CrawlerProcess({'FEED_EXPORT_ENCODING': 'utf-8', 'LOG_ENABLED': False})
    spider = HabrFreelanceSpider
    process.crawl(spider)
    process.start()




# Getting bot config parameters
active_users = []
config = configparser.ConfigParser()
config.read_file(open('config.ini'))

# Connecting to Telegram API
bot = telebot.TeleBot(token=config['DEFAULT']['token'])


print ('Starting Crawler...')
#Starting crawler
p = Process(target=crawler, args=(bot, active_users))
p.start()

# Starting bot
# print ('Starting Bot...')
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#
# bot.polling()

