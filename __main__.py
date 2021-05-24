"""
The script with bot for online game 'Seterra'.

:Author: YeslieSnayder
:Version: 1.3
"""

import sys
import csv
from enum import Enum
from configparser import ConfigParser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Mode(Enum):
    CONTINENTS = 0
    COUNTRIES_150 = 1


class SeterraGame:
    config_file = 'config.ini'   # file with configuration of the application

    def __init__(self, mode: Mode):
        self.mode = mode

        config = ConfigParser()
        if not config.read(self.config_file):
            raise Exception("Config file is empty")

        self._language = config['DEFAULT'].get('language')
        self._driver_file = config['DEFAULT'].get('driver_file')
        self._history_file = config['DEFAULT'].get('history_file')

        file_name = ''
        if mode == Mode.CONTINENTS:
            self._site = config['DEFAULT'].get('site_continents')
            file_name = config['DEFAULT'].get('continents_file')
        elif mode == Mode.COUNTRIES_150:
            self._site = config['DEFAULT'].get('site_countries')
            file_name = config['DEFAULT'].get('countries_file')
        self._elements = self._init_elements(file_name)

    def _init_elements(self, file):
        if self._language == 'en':
            uid = 2
        elif self._language == 'ru':
            uid = 3
        else:
            raise Exception("No such language: " + self._language)

        elem = {}
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

    def play(self):
        with webdriver.Chrome(executable_path=self._driver_file) as driver:
            print('Loading page...')
            driver.get(self._site)

            # Remove ads
            driver.execute_script("""
            var element = document.getElementById(\"mainbanner\");element.remove();
            var element = document.getElementById(\"panGameList\");element.remove();
            var element = document.getElementById(\"divAd_Panorama1\");
            if (element)
                element.remove();
            """)

            print('Start game!')
            history = []
            try:
                driver.find_element_by_id('cmdRestart').click()
                while True:
                    question = driver.find_element_by_id('currQuestion').text[9:]
                    if question == '':
                        break

                    history.append(question)
                    element_id = self._elements[question]
                    element = driver.find_element_by_id(element_id[0])
                    # if element has the 'offset' parameter
                    if len(element_id) > 3:
                        webdriver.ActionChains(driver).move_to_element(element)\
                            .move_by_offset(element_id[-2], element_id[-1])\
                            .click().perform()
                    else:
                        element.click()

                result = driver.find_element_by_id('lblFinalScore2').text
                progress = 'Progress: {}, Time: {}\n'.format(result[:5].strip(), result[5:].strip())
                history.insert(0, progress)
            except NoSuchElementException:
                driver.implicitly_wait(1000)
            finally:
                self.write_history(history)

            input('Press \'Enter\' to exit the program!')

    def write_history(self, arr: list):
        with open(self._history_file, 'w') as file:
            for s in arr:
                file.write(s + '\n')


def main(argv: list):
    mode = Mode.CONTINENTS
    if len(argv) > 1:
        if argv[0] == '-m' or argv[0] == '--mode':
            if argv[1] == 'continents' or argv[1] == '0':
                mode = Mode.CONTINENTS
            elif argv[1] == 'countries' or argv[1] == '1':
                mode = Mode.COUNTRIES_150
            else:
                raise Exception("Incorrect params!")
    game = SeterraGame(mode)
    game.play()


if __name__ == '__main__':
    main(sys.argv[1:])
