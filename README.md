# Сравнение производительности различных ORM (Object-Relational Mapping) библиотек: Django ORM, SQLAlchemy и Tortoise ORM

### <ins>Установка программы</ins>

1. Клонирование репозитория
В консоли ввести команду:
`git clone https://github.com/MVerseau/ORMs`
2. Перейти в директорию ORMs
`cd ORMs`
3. Создать и активировать виртуальное окружение:
`python -m venv venv`, `source venv/bin/activate`
4. Установить зависимости проекта:
`pip install -r requirements.txt`
5. Запустить программу:
`python manage.py runserver`
6. Перейти по ссылке (обычно это [http://127.0.0.1:8000/](http://127.0.0.1:8000/))

### <ins>Использованные навыки</ins>

- работа с Django (настройка приложения, маршрутов отображения, настройка работы со сравниваемыми библиотеками ORM);
- создание моделей для каждой ORM, реазиация функций запросов для каждой из ORM;
- работа с HTML: реализация визуализации данных, фильтрация данных, форматирование вывода;
- использования ООП и функционального программирования;
- работа с декораторами: создание встроенных декораторов Django и реализация и применение своих;
- работа с файлами: в ходе реализации приложения возникла необходимость выборки определённых данных в отдельный файл для анализа корректности выполнения кода.

### <ins>Результат выполнения программы</ins>
Были протестированы запросы к БД при помощи ORM-инструментов Django ORM, SQLAlchemy, Tortoise ORM на созданном наборе данных.
Для оценки производительности была выбрана скорость обработки запросов. Для большей репрезентативности результатов каждый из запросов повторялся 100 раз. В качестве результата использовано суммарное время всех 100 итераций по каждому из запросов.
Также для возможной оценки в будущем реализована возможность сбора тестовых данных по загрузке CPU и RAM. Их сравнение не выявлило какие-либо значимые отличия.
БД представляет собой 2 таблицы без связывания, однако с едиными полями для удобства связывания. БД содержит информацию о виртуальных покупателях игр и самих играх.

Визуализация результатов выполнения программы реализована на базе HTML шаблона.
![Скорость обработки запросов](https://github.com/MVerseau/ORMs/blob/f28042b01ffe915c1b1aeade43069f96cda58331/time.jpg)
![Загрузка ЦПУ](https://github.com/MVerseau/ORMs/blob/f28042b01ffe915c1b1aeade43069f96cda58331/CPU.jpg)
![ОЗУ](https://github.com/MVerseau/ORMs/blob/f28042b01ffe915c1b1aeade43069f96cda58331/RAM.jpg)

