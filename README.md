# Price_List_Analyzer

## Описание:

Это Python-программа для загрузки данных о товарах из CSV-файлов, поиска товаров по их названиям и экспорта результатов в HTML-формат. <br>
Программа позволяет пользователям:
- Загружать данные о товарах из CSV-файлов, содержащих информацию о названии, цене и весе товаров.
- Искать товары по их названиям с учетом регистра.
- Экспортировать результаты поиска в HTML-файл для удобного просмотра.

## Установка:
git clone https://github.com/gostok/Price_List_Analyzer.git <br>
cd Price_List_Analyzer 

## Использование:
1. Поместите CSV-файлы с данными о товарах в директорию проекта. Файлы должны содержать слово "price" в названии и иметь следующие столбцы:
- Название товара
- Цена
- Вес

2. Запустите программу:
   - py project.py

3. Введите текст для поиска товаров или введите 'exit' для выхода.

4. Результаты поиска будут отображены в консоли и экспортированы в HTML-файл output.html.