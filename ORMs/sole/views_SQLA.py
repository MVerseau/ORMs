import time
import random
from sqlalchemy import create_engine
from .models_SQLAlchemy import *
from sqlalchemy import func
from sqlalchemy.orm import Session


def sql_alchem(data: dict):
    engine = create_engine(r'sqlite:///db.sqlite3', echo=True)
    with Session(autoflush=False, bind=engine) as db:
        rez = a_query_get_record_found(db, True)
        data['SELECT buyer50 FROM Buyer'][1] += rez
        rez = a_query_get_record_found(db, False)
        data['SELECT buyer101 FROM Buyer'][1] += rez
        rez = al_group_by(db)
        data['SELECT age FROM Buyer GROUP BY age'][1] += rez
        rez = a_sort(db)
        data['SELECT * FROM Buyer ORDER BY balance'][1] += rez
        rez = a_filter(db)
        data['SELECT COUNT(age) FROM Buyer WHERE age=?'][1] += rez
        rez = a_join(db)
        data['SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name'][1] += rez
        rez = a_add_record(db)
        data['INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)'][1] += rez
        rez = a_update_records(db)
        data['UPDATE Buyer SET name ="TEST" WHERE name = "test2"'][1] += rez
        rez=a_delete(db)
        data['DELETE FROM Buyer WHERE name like "% ?%"'][1] += rez

    db.close()
    return data


def a_query_get_record_found(db: Session, find_yes: bool):
    start = time.time()
    if find_yes:
        db.query(A_Buyer).filter(A_Buyer.name == 'buyer50').first()
    else:
        db.query(A_Buyer).filter(A_Buyer.name == 'buyer101').first()

    end = time.time()
    return end - start


def al_group_by(db: Session):
    start = time.time()
    db.query(A_Buyer.age, func.count(A_Buyer.age)).group_by(A_Buyer.age)

    end = time.time()
    return end - start


def a_sort(db: Session):
    start = time.time()
    db.query(A_Buyer).order_by(A_Buyer.balance).all()
    end = time.time()
    return end - start


def a_filter(db: Session):
    start = time.time()
    db.query(A_Buyer, func.count(A_Buyer.age)).filter(A_Buyer.age == random.randint(0, 100)).all()
    end = time.time()
    return end - start


def a_join(db: Session):
    start = time.time()
    db.query(A_Buyer).filter(A_Buyer.name == A_Game.buyer).all()

    end = time.time()
    return end - start


def a_add_record(db: Session):
    start = time.time()
    new_record = A_Buyer(
        name="test A",
        balance=1000,
        age=101,
    )
    db.add(new_record)
    db.commit()
    end = time.time()
    return end - start


def a_update_records(db: Session):
    start = time.time()
    db.query(A_Buyer).filter(A_Buyer.name == 'test A').update({'name': 'TEST A'},
                                                             synchronize_session='fetch')
    db.commit()

    end = time.time()
    return end - start

def a_delete(db: Session):
    start = time.time()
    db.query(A_Buyer).filter(A_Buyer.name.contains('_A')).delete()
    db.commit()

    end = time.time()
    return end - start
