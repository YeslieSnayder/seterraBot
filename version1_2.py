"""
The script with bot for online game 'Seterra'.

:Author YeslieSnayder
:Version 1.2
"""

import sys
import configparser

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver

from enum import Enum


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


class SeterraGame:
    driver_file = r'driver/chromedriver'    # file for browser driver
    config_file = 'config.ini'              # file with configuration of the game
    history_file = 'log/history.log'        # file for history of the last game

    def __init__(self, mode: Mode):
        self.mode = mode
        self.elements = []

        config = configparser.ConfigParser()
        config.read(self.config_file)
        print(config.sections())

        if len(config.sections()) == 0:
            raise ConfigError("File ")

        self._history_file = config['DEFAULT'].get('history_path')
        if mode == Mode.CONTINENTS:
            self._site = config['DEFAULT'].get('site_continents')
            for key in list(config.items('CONTINENTS')):
                self.elements.append(key)
            print(self.elements)

    def get_id(self, question: str):
        for i in range(len(self.elements)):
            if question == self.elements[i][0]:
                return self.elements[i]
        return None

    def play(self):
        history = []
        with webdriver.Chrome(executable_path=self.driver_file) as driver:
            driver.get(self._site)
            try:
                for i in range(300):
                    question = driver.find_element_by_id('currQuestion').text[9:]
                    history.append(question)
                    element_id = self.get_id(question)
                    if element_id is None:
                        break

                    element = driver.find_element_by_id(element_id[1])
                    if len(element_id) > 2:  # if element has the 'offset' parameter
                        el = webdriver.ActionChains(driver).move_to_element(element)
                        el.move_by_offset(element_id[2], element_id[3])
                        el.click().perform()
                    else:
                        element.click()
                    driver.implicitly_wait(10)
            except NoSuchElementException:  # the algorithm has done
                driver.implicitly_wait(1000)
        self.write_history(history)

    def write_history(self, arr: list):
        with open(self._history_file, 'w') as file:
            for s in arr:
                file.write(s + '\n')


def main(argv: list):
    mode = Mode.CONTINENTS
    if len(argv) > 1:
        if argv[0] == '-m' or argv[1] == '--mode':
            if argv[1] is str and argv[1] == 'continents' or argv[1] is int and argv[1] == 0:
                mode = Mode.CONTINENTS
            elif argv[1] is str and argv[1] == 'countries' or argv[1] is int and argv[1] == 1:
                mode = Mode.COUNTRIES_150
            else:
                raise Exception("Incorrect params!")
    game = SeterraGame(mode)
    # game.play()
    for el in game.elements:
        print(el)


if __name__ == '__main__':
    main(sys.argv[1:])
