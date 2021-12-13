# This is a sample Python script.
import os

import colorama
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from webdriver_manager.chrome import ChromeDriverManager

import constants

os.system('cls')
colorama.init()


def main():
    driver = __config()
    result_list = __get_news(driver)
    sentiment = __get_sentiment(result_list)
    __output_action(sentiment)


def __config():
    """
    Configuração inicial para o navegador Chrome.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=chrome_options)
    driver.get("https://news.bitcoin.com/")
    driver.maximize_window()
    return driver


def __get_news(driver):
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, 'html.parser')
    story_list = soup.findAll('div', {'class': ['story']})
    result_list = list()
    for story in story_list:
        title_h6 = story.find('h6', {'class': ['story__title']})
        title_h5 = story.find('h5', {'class': ['story__title']})
        footer = story.find('div', {'class': ['story__footer']})
        footer = footer.text.strip().split("|")[1]
        footer = footer.split(" ")
        if "hours" in footer or "hour" in footer:
            title = title_h6 or title_h5
            result_list.append(title.text.strip())
    return result_list


def __get_sentiment(result_list):
    analyser = SentimentIntensityAnalyzer()
    sentiment_dict = {"negativo": 0, "positivo": 0}
    for title in result_list:
        sentiment = analyser.polarity_scores(title)
        compound = sentiment.get("compound")
        if compound >= 0.05:
            sentiment_dict["positivo"] = sentiment_dict["positivo"] + 1
        elif compound <= -0.05:
            sentiment_dict["negativo"] = sentiment_dict["negativo"] + 1
    print(sentiment_dict)
    return max(sentiment_dict, key=sentiment_dict.get)


def __output_action(sentiment):
    if sentiment == "positivo":
        print(constants.positivo)
        print(constants.bitcoin_up)
    elif sentiment == "negativo":
        print(constants.negativo)
        print(constants.bitcoin_down)


if __name__ == '__main__':
    main()
