
import random

import asyncio
from django.db.models import Count
from django.shortcuts import render
# import time
from django.db import connection
from django.template.defaulttags import register
from .models import *
from .views_SQLA import *
from .views_SQLA import sql_alchem
from .views_Tortoise import tortoise_main


def results(request):
    title = "Сравнение библиотек ORM"
    head = "Сравнительная таблица"
    data = {'SELECT buyer50 FROM Buyer': [0, 0, 0],
            'SELECT buyer101 FROM Buyer': [0, 0, 0],
            'SELECT * FROM Buyer ORDER BY balance': [0, 0, 0],
            'SELECT age FROM Buyer GROUP BY age': [0, 0, 0],
            'SELECT COUNT(age) FROM Buyer WHERE age=?': [0, 0, 0],
            'SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name': [0, 0, 0],
            'INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)': [0, 0, 0],
            'UPDATE Buyer SET name ="TEST" WHERE name = "test2"': [0, 0, 0],
            'DELETE FROM Buyer WHERE name like "% ?%"': [0, 0, 0],
            }
    perf = Dj()

    for i in range(100):
        data = calculation_of_indicators(data, perf).copy()
        data = sql_alchem(data).copy()
        data = asyncio.run(tortoise_main(data))

    for key,value in data.items():
        data[key].append(['Django ORM', 'SQLAlchemy', 'Tortoise ORM'][data[key].index(min(data.get(key)))])


    context = {
        'title': title,
        'head': head,
        'data': data,

    }
    return render(request, 'results.html', context)

@register.filter
def is_string(val):
    return isinstance(val, str)
def calculation_of_indicators(data: dict, perf):
    rez = round(perf.query_get_record_found(True), 5)
    data['SELECT buyer50 FROM Buyer'][0] += rez

    rez = perf.query_get_record_found(False)
    data['SELECT buyer101 FROM Buyer'][0] += rez

    rez = perf.group_by()
    data['SELECT age FROM Buyer GROUP BY age'][0] += rez

    rez = perf.sorting()
    data['SELECT * FROM Buyer ORDER BY balance'][0] += rez
    #
    rez = perf.count_elems()
    data['SELECT COUNT(age) FROM Buyer WHERE age=?'][0] += rez
    #
    rez = perf.joining()
    data['SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name'][0] += rez

    rez = perf.add_record()
    data['INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)'][0] += rez
    #
    rez = perf.update_records()
    data['UPDATE Buyer SET name ="TEST" WHERE name = "test2"'][0] += rez

    rez = perf.del_all_data()
    data['DELETE FROM Buyer WHERE name like "% ?%"'][0] += rez
    # # print(data)
    return data


class Dj():

    def fill_in_buyers(self):
        start = time.time()
        for i in range(100):
            Buyer.objects.create(
                name=f'buyer{i}',
                balance=random.randint(0, 100),
                age=random.randint(1, 100)
            )
        end = time.time()
        return f"{(end - start):.3f} сек."


    def fill_in_games(self):

        start = time.time()
        for i in range(100):
            Game.objects.create(
                title=f'game{i}',
                cost=random.randint(0, 100),
                size=random.randint(1, 100),
                description=f'description of game{i}',
                age_limited=[True, False][random.randint(0, 1)],
                buyer=Buyer.objects.get(id=random.randint(1, 100)).name

            )

        end = time.time()
        return f"{(end - start):.3f} сек."

    def query_get_record_found(self, find_yes: bool):
        start = time.time()
        if find_yes:
            Buyer.objects.get(name='buyer50')
        else:
            Buyer.objects.filter(name='buyer101')
        end = time.time()
        return end - start


    def group_by(self):
        start = time.time()
        Buyer.objects.values('age').annotate(total_posts=Count('age')).order_by('age')
        end = time.time()
        return end - start

    def sorting(self):
        start = time.time()
        Buyer.objects.all().order_by('balance')
        end = time.time()
        return end - start

    def count_elems(self):
        start = time.time()
        Buyer.objects.all().filter(age=random.randint(0, 100)).aggregate(Count('age'))
        end = time.time()
        return end - start

    def add_record(self):
        start = time.time()
        new_record = Buyer.objects.create(name="test DJ", balance=1000, age=101)
        new_record.save()
        end = time.time()
        return end - start

    def del_all_data(self):
        start = time.time()
        Buyer.objects.filter(name__contains='DJ').delete()
        end = time.time()
        return end - start

    def joining(self):

        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("""
                    Select sole_game.title, sole_buyer.name from sole_game JOIN sole_buyer ON
                     sole_game.buyer = sole_buyer.name
                """)

        end = time.time()
        return end - start

    def update_records(self):
        start = time.time()
        query_for_filter = Buyer.objects.filter(name='test DJ')
        query_for_filter.update(name=('test DJ') + ' Updated')
        end = time.time()
        return end - start

    # def del_all_data(self):
    #     start = time.time()
    #     Buyer.objects.filter(name__contains='test').delete()
    #     end = time.time()
    #     return end - start