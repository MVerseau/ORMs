import os
import time
import random

import psutil
from tortoise import Tortoise
from .models_Tortoise import T_Game, T_Buyer
from tortoise.functions import Count
from .utils import cpu_interval


async def tortoise_init():
    await Tortoise.init(
        db_url=r"sqlite://db.sqlite3",
        modules={'models': ['sole.models_Tortoise']},
    )
    await Tortoise.generate_schemas()


async def tortoise_main(data: dict):
    await tortoise_init()
    await t_simple_query(data, True)
    await t_simple_query(data, False)
    await t_group_by(data)
    await t_sort(data)
    await t_filter(data)
    await t_join(data)
    await t_add_record(data)
    await t_update_records(data)
    await t_delete_records(data)
    await Tortoise.close_connections()
    return data


async def t_simple_query(data: dict, find_yes: bool):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    if find_yes:
        await T_Buyer.filter(name='buyer50').first()
        end = time.time()
        mem_after = p.memory_info().rss
        for i in range(3):
            data['SELECT buyer50 FROM Buyer'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]
    else:
        await T_Buyer.filter(name='buyer101').first()
        end = time.time()
        mem_after = p.memory_info().rss
        for i in range(3):
            data['SELECT buyer101 FROM Buyer'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_group_by(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.all().group_by("age").annotate(count=Count('age')).values('age', 'count')
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['SELECT age FROM Buyer GROUP BY age'][2][i] += \
        [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_sort(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.all().order_by("balance")
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['SELECT * FROM Buyer ORDER BY balance'][2][i] += \
        [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][
            i]


async def t_filter(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.filter(age=random.randint(0, 100)).annotate(count=Count('age')).count()
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['SELECT COUNT(age) FROM Buyer WHERE age=?'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_join(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    connection = Tortoise.get_connection("default")
    await connection.execute_query_dict(
        "Select sole_game.title, sole_buyer.name from sole_game JOIN sole_buyer ON sole_game.buyer = sole_buyer.name")
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_add_record(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.create(
        name="test T",
        balance=1000,
        age=101,
    )
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_update_records(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.filter(name='test T').update(name='TEST T')
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['UPDATE Buyer SET name ="TEST" WHERE name = "test2"'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]


async def t_delete_records(data: dict):
    p = psutil.Process(os.getpid())
    mem_before = p.memory_info().rss
    start = time.time()
    await T_Buyer.filter(name__contains=' T').delete()
    end = time.time()
    mem_after = p.memory_info().rss
    for i in range(3):
        data['DELETE FROM Buyer WHERE name like "% ?%"'][2][i] += \
            [end - start, p.cpu_percent(interval=cpu_interval), mem_after - mem_before][i]
