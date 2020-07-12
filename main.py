import configparser
import telebot
import scrapy
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
import queue
import logging

tasks_q = queue.Queue()

class FreelanceTask():
    """
    Class for storing scraped freelance tasks
    """
    title: str = ""
    description: str = ""
    price: str = ""
    tags = []
    link: str = ""

    def __init__(self, title, price, tags, link):
        self.title = title
        self.price = price
        self.tags = tags
        self.link = link

    def add_description(self, description):
        self.description = description


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
        yield scrapy.Request(url=self._initial_url, callback=self.parse_tasks_list)

    def parse_tasks_list(self, response):
        print("parsing")
        task_containers = response.css('.content-list__item')
        for task in task_containers:
            task_link = task.css(".task__title a")
            url = task_link.attrib["href"]
            task_name = task_link.xpath("text()").get()
            tags = task.css(".tags .tags__item_link::text").getall()
            print(tags)
            price_container = task.css(".task__price")
            price_text = price_container.css(".negotiated_price::text").get()
            if price_text is None:
                count_price_store = price_container.css(".count")
                count_price = count_price_store.xpath("text()").get()
                count_price_comment = count_price_store.css(".suffix::text").get()
                price_text = "%s %s" % (count_price, count_price_comment)
                print(count_price_store)

            task_link = response.urljoin(url)
            scraped_task = FreelanceTask(task_name, price_text, tags, task_link)
            print(price_text)
            yield scrapy.Request(task_link, callback=self.parse_task_page, meta={'current_item': scraped_task})

    def parse_task_page(self, response):
        print("parsing task page")
        scraped_task: FreelanceTask = response.meta.get('current_item')
        description = response.css(".task__description")
        if len(description) > 0:
            description_text = description[0].get()
        print(description_text)
        description_text = description_text.replace("<div class=\"task__description\">", "").replace("</div>", "").replace("<br>", "\n")
        scraped_task.add_description(description_text)
        tasks_q.put(scraped_task)


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

