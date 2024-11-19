import os
import json
import csv


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ""
        self.name_length = 0

    def load_prices(self, file_path=None):
        """
        Сканирует указанный каталог. Ищет файлы со словом price в названии.
        В файле ищет столбцы с названием товара, ценой и весом.
        Допустимые названия для столбца с товаром:
            товар
            название
            наименование
            продукт

        Допустимые названия для столбца с ценой:
            розница
            цена

        Допустимые названия для столбца с весом (в кг.)
            вес
            масса
            фасовка
        """

        if file_path is None:
            file_path = os.getcwd()

        for filename in os.listdir(file_path):
            if "price" in filename and filename.endswith(".csv"):
                with open(
                    os.path.join(file_path, filename), newline="", encoding="utf-8"
                ) as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    headers = next(reader)
                    product_index, price_index, weight_index = (
                        self._search_product_price_weight(headers)
                    )

                    for row in reader:
                        if (
                            product_index is not None
                            and price_index is not None
                            and weight_index is not None
                        ):
                            product_name = row[product_index]
                            price = float(row[price_index])
                            weight = float(row[weight_index])
                            price_per_kg = price / weight if weight > 0 else 0

                            self.data.append(
                                {
                                    "name": product_name,
                                    "price": price,
                                    "weight": weight,
                                    "file": filename,
                                    "price_per_kg": price_per_kg,
                                }
                            )

        # print(f"Загружено товаров: {len(self.data)}")
        # for item in self.data:  # Выводим все загруженные товары
        #     print(item)

    def _search_product_price_weight(self, headers):
        """
        Возвращает номера столбцов для названия товара, цены и веса.

        :param headers: Список заголовков столбцов.
        :return: Кортеж с индексами столбцов (product_index, price_index, weight_index).
        """

        product_index = next(
            (
                i
                for i, h in enumerate(headers)
                if h.lower() in ["название", "продукт", "товар", "наименование"]
            ),
            None,
        )
        price_index = next(
            (i for i, h in enumerate(headers) if h.lower() in ["цена", "розница"]), None
        )
        weight_index = next(
            (
                i
                for i, h in enumerate(headers)
                if h.lower() in ["фасовка", "масса", "вес"]
            ),
            None,
        )
        return product_index, price_index, weight_index

    def export_to_html(self, fname="output.html"):
        """
        Экспортирует данные о товарах в HTML-файл.

        :param fname: Имя выходного HTML-файла.
        """

        result = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table border="1">
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        """

        for indx, item in enumerate(self.data, start=1):
            result += f"""
                <tr>
                    <td>{indx}</td>
                    <td>{item['name']}</td>
                    <td>{item['price']}</td>
                    <td>{item['weight']}</td>
                    <td>{item['file']}</td>
                    <td>{item['price_per_kg']}</td>
                </tr>
            """

        result += """
            </table>
        </body>
        </html>
        """

        with open(fname, "w", encoding="utf-8") as f:
            f.write(result)

    def find_text(self, text):
        """
        Получает текст и возвращает список позиций, содержащий этот текст в названии продукта.

        :param text: Текст для поиска.
        :return: Список найденных товаров.
        """
        print(f"Поиск для: {text}")
        found_items = [
            item for item in self.data if text.lower() in item["name"].lower()
        ]
        print(f"Найденные товары: {len(found_items)}")
        # for item in found_items:  # Выводим найденные товары
        #     print(item)
        return found_items


def main():
    """
    Главная функция для выполнения программы.
    """

    pm = PriceMachine()
    pm.load_prices()

    while True:
        user_input = input("Введите текст для поиска (или 'exit' для выхода)  ")

        if user_input.lower() == "exit":
            print("Работа завершена.")
            break

        results = pm.find_text(user_input)
        results.sort(key=lambda x: x["price_per_kg"])

        if results:
            print(
                f"{'№':<3} {'Наименование':<40} {'Цена':<6} {'Вес, кг':<6} {'Файл':<15} {'Цена за кг.':<10}"
            )
            for idx, item in enumerate(results, start=1):
                print(
                    f"{idx:<3} {item['name']:<40} {item['price']:<6} {item['weight']:<6} {item['file']:<15} {item['price_per_kg']:.2f}"
                )
        else:
            print("Товары не найдены.")

    pm.export_to_html()


if __name__ == "__main__":
    main()
