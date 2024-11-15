import asyncio
from django.shortcuts import render
from .views_Django import *
from .views_SQLA import sql_alchem
from .views_Tortoise import tortoise_main
from .utils import iter, adjustment  # , file


def results(request, iter=iter):
    # file.truncate()
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

    for i in range(iter):
        data = dj_collect_data(data, perf).copy()
        data = sql_alchem(data, i).copy()
        data = asyncio.run(tortoise_main(data)).copy()

    data = adjustment(data)

    context = {
        'title': title,
        'head': head,
        'data': data,
    }
    # file.close()
    return render(request, 'results.html', context)

