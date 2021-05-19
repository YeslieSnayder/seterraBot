"""
The script with bot for online game 'Seterra'.

:Author YeslieSnayder
:Version 1.2
"""

import sys
import configparser

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from typing import List

history_file = ''
site = ''
elements = []

# site_continents = 'https://online.seterra.com/ru/vgp/3111'
# continents = [
#     ('Австралия', 'AREA_OCEANIA'),
#     ('Азия', 'AREA_ASIA'),
#     ('Африка', 'AREA_AFRICA'),
#     ('Европа', 'AREA_EUROPE', 40, 10),
#     ('Северная Америка', 'AREA_NORTHAMERICA'),
#     ('Южная Америка', 'AREA_SOUTHAMERICA')
# ]


def init(mode):
    global history_file, site, elements

    config = configparser.ConfigParser()
    config.read('config.cfg')
    print(config.sections())

    if len(config.sections()) == 0:
        return -1
    history_file = config['DEFAULT'].get('history_path')

    if mode == 0:
        site = config['DEFAULT'].get('site_continents')
        for key in list(config.items('CONTINENTS')):
            elements.append(key)
        print(elements)


def get_id(question: str):
    for i in range(len(elements)):
        if question == elements[i][0]:
            return elements[i]
    return None


def play():
    history = []
    with webdriver.Chrome(executable_path=r'driver/chromedriver') as driver:
        driver.get(site)
        try:
            for i in range(300):
                question = driver.find_element_by_id('currQuestion').text[9:]
                history.append(question)
                element_id = get_id(question)
                if element_id is None:
                    break

                element = driver.find_element_by_id(element_id[1])
                if len(element_id) > 2:   # if element has the 'offset' parameter
                    el = webdriver.ActionChains(driver).move_to_element(element)
                    el.move_by_offset(element_id[2], element_id[3])
                    el.click().perform()
                else:
                    element.click()
                driver.implicitly_wait(10)
        except NoSuchElementException:   # the algorithm has done
            driver.implicitly_wait(1000)
    return history


def write_history(history: List[str]):
    with open(history_file, 'w') as file:
        for s in history:
            file.write(s + '\n')


def main(argv: List[str]):
    mode = 0
    if len(argv) > 1:
        if argv[0] == '-m':
            mode = int(argv[1])
    code = init(mode)
    if code == -1:
        return
    write_history(play())


if __name__ == '__main__':
    main(sys.argv[1:])
