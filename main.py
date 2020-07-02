import configparser
import telebot

import logging

def main():
    # Getting bot config parameters
    config = configparser.ConfigParser()
    config.read_file(open('/app/config.ini'))

    # Connecting to Telegram API
    bot = telebot.TeleBot(token=config['DEFAULT']['token'])

    # Starting
    print ('Starting Bot...')
