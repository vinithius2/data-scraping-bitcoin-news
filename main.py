import os

import colorama
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from webdriver_manager.chrome import ChromeDriverManager

import constants
from bcolors import bcolors

os.system('cls')
colorama.init()


def main():
    """
    Iniciar aplicação.
    """
    driver = __config()
    result_list = __get_news(driver)
    sentiment, sentiment_count_dict, sentiment_news_dict = __get_sentiment(result_list)
    __output_action(sentiment)
    __print_output(sentiment_count_dict, sentiment_news_dict)


def __config():
    """
    Configuração inicial para o navegador Chrome.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(), options=chrome_options)
    print(f'\n{bcolors.BOLD}{bcolors.OKBLUE}Waiting browser...{bcolors.ENDC}{bcolors.ENDC}\n')
    driver.get("https://news.bitcoin.com/")
    return driver


def __get_news(driver):
    """
    Raspagem dos dados e usar somente as notícias das últimas horas.
    """
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
    """
    Avaliar o sentimento das notícias e definir se é negativo ou positivo.
    """
    analyser = SentimentIntensityAnalyzer()
    sentiment_count_dict = {"negative": 0, "positive": 0}
    sentiment_news_dict = {"negative": list(), "positive": list()}
    for title in result_list:
        sentiment = analyser.polarity_scores(title)
        compound = sentiment.get("compound")
        if compound >= 0.05:
            sentiment_news_dict["positive"].append(title)
            sentiment_count_dict["positive"] = sentiment_count_dict["positive"] + 1
        elif compound <= -0.05:
            sentiment_news_dict["negative"].append(title)
            sentiment_count_dict["negative"] = sentiment_count_dict["negative"] + 1
    return max(sentiment_count_dict, key=sentiment_count_dict.get), sentiment_count_dict, sentiment_news_dict


def __output_action(sentiment):
    """
    Saida do resultado se é positivo ou negativo.
    """
    if sentiment == "positive":
        print(constants.positive)
        print(constants.bitcoin_up)
    elif sentiment == "negative":
        print(constants.negative)
        print(constants.bitcoin_down)


def __print_output(sentiment_count_dict, sentiment_news_dict):
    """
    Saida das notícias usadas na lógica de sentimento.
    """
    print(constants.news)
    for key, value in sentiment_news_dict.items():
        if key == "positive":
            print(
                f'{bcolors.BOLD}{bcolors.OKGREEN}{key.capitalize()}{bcolors.ENDC}{bcolors.ENDC} ({sentiment_count_dict["positive"]})')
        else:
            print(
                f'{bcolors.BOLD}{bcolors.FAIL}{key.capitalize()}{bcolors.ENDC}{bcolors.ENDC} ({sentiment_count_dict["negative"]})')
        count = 0
        for item in value:
            count = count + 1
            print(f'{count} - {bcolors.OKCYAN}{item}{bcolors.ENDC}')


if __name__ == '__main__':
    main()
