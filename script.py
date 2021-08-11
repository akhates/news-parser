# -*- coding: utf-8 -*-
import os
import io
import urllib.request
import re
import textwrap
import random

__author__ = 'Ahat Mullabaev'


class NewsParser:
    def __init__(self, border):
        self.headerBorder = border

    def check_url(self, article):
        """
        Метод проверки статьи на содержание ссылок и ненужных тегов
        :param article: string
        :return: string
        """
        # Если встречаем ссылку - берем ее в квадратные скобки
        url = ''
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', article)
        if urls:
            for ur in urls:
                url = '[' + ur + ']'
        # Очищаем параграф от лишних тегов
        link = ''
        links = re.findall(r'<a[^>]*>(.*?)</a>', article)
        if links:
            for lin in links:
                link = lin
        if re.search("<a[^>]*>(.*?)</a>", article, re.IGNORECASE):
            r = re.compile(r'<a[^>]*>(.*?)</a>', re.IGNORECASE)
            article = r.sub(r'' + link + ' ' + url, article)
        if re.search("<span[^>]*>(.*?)</span>", article, re.IGNORECASE):
            r = re.compile(r'<span[^>]*>(.*?)</span>', re.IGNORECASE)
            article = r.sub(r'', article)
        if re.search("<b[^>]*>(.*?)</b>", article, re.IGNORECASE):
            r = re.compile(r'<b[^>]*>(.*?)</b>', re.IGNORECASE)
            article = r.sub(r'', article)
        if re.search("<em[^>]*>(.*?)</em>", article, re.IGNORECASE):
            r = re.compile(r'<em[^>]*>(.*?)</em>', re.IGNORECASE)
            article = r.sub(r'', article)
        return article

    def create_path(self, path):
        """
        Метод создания пути по из ссылки
        :param path: string
        :return: string
        """
        way = path.split('/')
        if 'http:' in way:
            way.remove('http:')
        if 'https:' in way:
            way.remove('https:')
        if '' in way:
            way.remove('')
        name = way.pop()
        if name == '':
            name = way.pop()
        testpath = '/'.join(way[0:])
        if not os.path.exists(testpath):
            os.makedirs(testpath)
        return testpath + '\\' + name + '.txt'

    def formate_to_read(self, string):
        """
        Метод форматирования параграфа
        :param string: string
        :return: string
        """
        prewords = self.check_url(string)
        words = re.findall(r'\S+', prewords)
        res = ''  # .encode('utf_8')
        for word in words:
            # Убираем спецтеги
            if '&nbsp;' in word:
                word = word.replace('&nbsp;', ' ')
            elif '&laquo;' in word:
                word = word.replace('&laquo;', '')
            if '&raquo;' in word:
                word = word.replace('&raquo;', '')
            if '&mdash;' in word:
                word = word.replace('&mdash;', '')
            if '&minus;' in word:
                word = word.replace('&minus;', '-')
            res += word + ' '
        # Определяем длинну строки не более 80 символов
        rw = textwrap.fill(res, 80)
        return rw

    def get_page(self, index):
        """
        Метод получения html страницы
        :param index: string
        :return: string
        """
        with urllib.request.urlopen(index) as f:
            html = f.read().decode(f.headers.get_content_charset())
        return html

    def random_url(self, site):
        """
        Метод получения ссылки на случайную новости из сайта
        :param site: string
        :return: string
        """
        print(site)
        with urllib.request.urlopen(site) as f:
            urlContent = f.read().decode(f.headers.get_content_charset())
        # Получаем списко всех ссылок с главное страницы
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', urlContent)
        # Берем только которые: содержат /, длинна больше 10 и меньше 36 символов и первые 5 символов не http:
        # так-как переходы на новость обычно не содержат прямой ссылки
        validUrls = [s for s in urls if '/' in s and 10 < len(s) < 36 and s[0:5] != 'http:']
        rndLink = (random.choice(validUrls))
        # Собираем ссылку на новость из адреса сайта и ссылки на новость
        if site[-1] == '/' and rndLink[0] == '/':
            site = site[:-1]
            resl = site + rndLink
        else:
            resl = site + rndLink
        return resl

    def work_cycle(self, link):
        """
        Основной рабочий метод
        :param link: string
        :return: None
        """
        # Готовим имя для файла
        filename = self.create_path(link)
        # Получаем страничку
        npage = self.get_page(link)
        # Берем заголовок и статью
        header = re.findall(r'<title>(.+?)</title>', npage)
        article = re.findall(r'<p>(.*?)</p>', npage)
        res = ''
        # Форматируем и добавляем в результат заголовок и декор
        if header:
            for head in header:
                res += self.formate_to_read(head)
                if '\n' in self.headerBorder:
                    res += self.headerBorder
                else:
                    res += '\n' + str(self.headerBorder * 80) + '\n'
        # Форматируем и добавляем в результат статью
        if article:
            for art in article:
                if len(art.split()) > 2:
                    res += self.formate_to_read(art) + '\n'
        # Записываем все в файл
        with io.open(filename, "w", encoding="utf-8") as f:
            f.write(res)
