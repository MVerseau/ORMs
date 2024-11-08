import os
import random
import psutil

import asyncio
from django.db.models import Count
from django.shortcuts import render
# import time
from django.db import connection
from .models import *
from .views_SQLA import *
from .views_SQLA import sql_alchem
from .views_Tortoise import tortoise_main
from .utils import ps_utils


def results(request, iter=100):
    title = "Сравнение библиотек ORM"
    head = "Сравнительная таблица"
    data = {'SELECT buyer50 FROM Buyer': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'SELECT buyer101 FROM Buyer': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'SELECT * FROM Buyer ORDER BY balance': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'SELECT age FROM Buyer GROUP BY age': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'SELECT COUNT(age) FROM Buyer WHERE age=?': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'UPDATE Buyer SET name ="TEST" WHERE name = "test2"': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            'DELETE FROM Buyer WHERE name like "% ?%"': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            }
    perf = Dj()

    for i in range(iter):
        data = calculation_of_indicators(data, perf).copy()
        data = sql_alchem(data).copy()
        data = asyncio.run(tortoise_main(data))

    for key, value in data.items():
        for i in range(len(data[key])):
            for j in range(1, len(data[key][i])):
                print(f'{data[key][i][j]=}')
                data[key][i][j] /= iter
        timing = list(zip(value[0], value[1], value[2]))[0]
        # data[key].append(['Django ORM', 'SQLAlchemy', 'Tortoise ORM'][data[key][0].index(min(data.get(key)[0]))])
        data[key][0].append(['Django ORM', 'SQLAlchemy', 'Tortoise ORM'][timing.index(min(timing))])

    context = {
        'title': title,
        'head': head,
        'data': data,

    }
    return render(request, 'results.html', context)


def calculation_of_indicators(data: dict, perf):
    rez = perf.query_get_record_found(True)
    for i in range(len(rez)):
        data['SELECT buyer50 FROM Buyer'][0][i] += rez[i]

    rez = perf.query_get_record_found(False)
    for i in range(len(rez)):
        data['SELECT buyer101 FROM Buyer'][0][i] += rez[i]

    rez = perf.group_by()
    for i in range(len(rez)):
        data['SELECT age FROM Buyer GROUP BY age'][0][i] += rez[i]

    rez = perf.sorting()
    for i in range(len(rez)):
        data['SELECT * FROM Buyer ORDER BY balance'][0][i] += rez[i]

    rez = perf.count_elems()
    for i in range(len(rez)):
        data['SELECT COUNT(age) FROM Buyer WHERE age=?'][0][i] += rez[i]

    rez = perf.joining()
    for i in range(len(rez)):
        data['SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name'][0][i] += rez[i]

    rez = perf.add_record()
    for i in range(len(rez)):
        data['INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)'][0][i] += rez[i]

    rez = perf.update_records()
    for i in range(len(rez)):
        data['UPDATE Buyer SET name ="TEST" WHERE name = "test2"'][0][i] += rez[i]

    rez = perf.del_all_data()
    for i in range(len(rez)):
        data['DELETE FROM Buyer WHERE name like "% ?%"'][0][i] += rez[i]

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

    @ps_utils
    def query_get_record_found(self, find_yes: bool):
        start = time.time()
        if find_yes:
            Buyer.objects.get(name='buyer50')
        else:
            Buyer.objects.filter(name='buyer101')
        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

    @ps_utils
    def group_by(self):
        start = time.time()
        Buyer.objects.values('age').annotate(total_posts=Count('age')).order_by('age')
        end = time.time()
        return end - start

    @ps_utils
    def sorting(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        Buyer.objects.all().order_by('balance')
        end = time.time()
        return end - start

    @ps_utils
    def count_elems(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        Buyer.objects.all().filter(age=random.randint(0, 100)).aggregate(Count('age'))
        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

    @ps_utils
    def add_record(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        new_record = Buyer.objects.create(name="test DJ", balance=1000, age=101)
        new_record.save()
        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

    @ps_utils
    def del_all_data(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        Buyer.objects.filter(name__contains='DJ').delete()
        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

    @ps_utils
    def joining(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        with connection.cursor() as cursor:
            cursor.execute("""
                    Select sole_game.title, sole_buyer.name from sole_game JOIN sole_buyer ON
                     sole_game.buyer = sole_buyer.name
                """)

        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

    @ps_utils
    def update_records(self):
        start = time.time()
        # p = psutil.Process(os.getpid())
        query_for_filter = Buyer.objects.filter(name='test DJ')
        query_for_filter.update(name=('test DJ') + ' Updated')
        end = time.time()
        return end - start  # , p.cpu_percent(), p.memory_percent()

