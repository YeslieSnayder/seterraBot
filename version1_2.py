"""
The script with bot for online game 'Seterra'.

:Author YeslieSnayder
:Version 1.3
"""

import sys
import csv
from enum import Enum
from configparser import ConfigParser
import keyboard

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# site_continents = 'https://online.seterra.com/ru/vgp/3111'
# continents = [
#     ('Австралия', 'Australia', 'AREA_OCEANIA'),
#     ('Азия', 'Asia', 'AREA_ASIA'),
#     ('Африка', 'Africa', 'AREA_AFRICA'),
#     ('Европа', 'Europe', 'AREA_EUROPE', 40, 10),
#     ('Северная Америка', 'North America', 'AREA_NORTHAMERICA'),
#     ('Южная Америка', 'South America', 'AREA_SOUTHAMERICA')
# ]


class ConfigError(Exception):
    pass


class Mode(Enum):
    CONTINENTS = 0
    COUNTRIES_150 = 1


def get_elements(file, language: str):
    elem = {}
    if language == 'en':
        uid = 2
    elif language == 'ru':
        uid = 3
    else:
        raise Exception("No such language: " + language)

    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'id':
                continue
            if row[-2] == '' and row[-1] == '':
                elem[row[uid]] = (row[1], row[2], row[3])
            elif row[-2] == '':
                elem[row[uid]] = (row[1], row[2], row[3], 0, int(row[-1]))
            elif row[-1] == '':
                elem[row[uid]] = (row[1], row[2], row[3], int(row[-2]), 0)
            else:
                elem[row[uid]] = (row[1], row[2], row[3], int(row[-2]), int(row[-1]))
    return elem


class SeterraGame:
    config_file = '../config.ini'   # file with configuration of the application

    def __init__(self, mode: Mode):
        self.mode = mode

        config = ConfigParser()
        if not config.read(self.config_file):
            raise ConfigError("Config file is empty")

        self._language = config['DEFAULT'].get('language')
        self._driver_file = config['DEFAULT'].get('driver_file')
        self._history_file = config['DEFAULT'].get('history_file')

        file_name = ''
        if mode == Mode.CONTINENTS:
            self._site = config['DEFAULT'].get('site_continents')
            file_name = config['DEFAULT'].get('continents_file')
        elif mode == Mode.COUNTRIES_150:
            # TODO: add category for 150 countries
            pass
        self._elements = get_elements(file_name, self._language)

    def play(self):
        history = []
        with webdriver.Chrome(executable_path=self._driver_file) as driver:
            driver.get(self._site)
            print('Please, press \'s\' to start a SeterraBot')
            while True:
                try:
                    if keyboard.is_pressed('s'):
                        break
                except:
                    break
            try:
                while True:
                    if keyboard.is_pressed('b'):
                        break

                    question = driver.find_element_by_id('currQuestion').text[9:]
                    if question == '':
                        break
                    history.append(question)
                    element_id = self._elements[question]
                    element = driver.find_element_by_id(element_id[0])
                    if len(element_id) > 3:  # if element has the 'offset' parameter
                        el = webdriver.ActionChains(driver).move_to_element(element)
                        el.move_by_offset(element_id[-2], element_id[-1])
                        el.click().perform()
                    else:
                        element.click()
                    driver.implicitly_wait(10)
            except NoSuchElementException:  # the algorithm has done
                driver.implicitly_wait(1000)

            print('Please, press \'b\' on a keyboard to break the program!')
            while True:
                try:
                    if keyboard.is_pressed('b'):
                        break
                except:
                    break
        self.write_history(history)

    def write_history(self, arr: list):
        with open(self._history_file, 'w') as file:
            for s in arr:
                file.write(s + '\n')


def main(argv: list):
    mode = Mode.CONTINENTS
    if len(argv) > 1:
        if argv[0] == '-m' or argv[0] == '--mode':
            if argv[1] is str and argv[1] == 'continents' or argv[1] is int and argv[1] == 0:
                mode = Mode.CONTINENTS
            elif argv[1] is str and argv[1] == 'countries' or argv[1] is int and argv[1] == 1:
                mode = Mode.COUNTRIES_150
            else:
                raise Exception("Incorrect params!")
    game = SeterraGame(mode)
    game.play()


if __name__ == '__main__':
    main(sys.argv[1:])
