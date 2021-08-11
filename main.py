# -*- coding: utf-8 -*-
import sys
import os
import json
from script import *
from sys import argv

__author__ = 'Ahat Mullabaev'


if __name__ == '__main__':
    # Получаем настройки
    with open("settings.json") as json_file:
        dataMap = json.load(json_file)
    # Берем из настроек декор и список сайтов для случайной статьи
    headerDecor = dataMap['border']
    sites = dataMap['sites']
    # Создаем экземпляр парсера и передаем в конструктор декор
    script = NewsParser(headerDecor)
    # первым идет имя скрипта
    if '--random' in argv:
        # Режим случайной статьи, берет случайную статью из сайта указанного в списке сайтов
        site = script.random_url(random.choice(sites))
        script.work_cycle(site)
    else:
        # Обычный режим, параметр должен содержать ссылку
        script.work_cycle(argv[1])
