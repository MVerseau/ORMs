import os
import time
import random
from sqlalchemy import create_engine
from .models_SQLAlchemy import *
from sqlalchemy import func
from sqlalchemy.orm import Session
from .utils import ps_utils  # ,#file


def sql_alchem(data: dict, i):
    # file.write(f'iter {i}: ')
    engine = create_engine(r'sqlite:///db.sqlite3', echo=True)
    with Session(autoflush=False, bind=engine) as db:
        rez = sqla.a_query_get_record_found(db, True)
        for i in range(len(rez)):
            data['SELECT buyer50 FROM Buyer'][1][i] += rez[i]
        rez = sqla.a_query_get_record_found(db, False)
        for i in range(len(rez)):
            data['SELECT buyer101 FROM Buyer'][1][i] += rez[i]
        rez = sqla.al_group_by(db)
        for i in range(len(rez)):
            data['SELECT age FROM Buyer GROUP BY age'][1][i] += rez[i]
        rez = sqla.a_sort(db)
        for i in range(len(rez)):
            data['SELECT * FROM Buyer ORDER BY balance'][1][i] += rez[i]
        rez = sqla.a_filter(db)
        for i in range(len(rez)):
            data['SELECT COUNT(age) FROM Buyer WHERE age=?'][1][i] += rez[i]
        rez = sqla.a_join(db)
        for i in range(len(rez)):
            data['SELECT * FROM Buyer\nJOIN Game ON Game.buyer=Buyer.name'][1][i] += rez[i]
        rez = sqla.a_add_record(db)
        for i in range(len(rez)):
            data['INSERT INTO Buyer (name, balance, age) VALUES (test2,1000, 101)'][1][i] += rez[i]
        rez = sqla.a_update_records(db)
        for i in range(len(rez)):
            data['UPDATE Buyer SET name ="TEST" WHERE name = "test2"'][1][i] += rez[i]
        rez = sqla.a_delete(db)
        for i in range(len(rez)):
            data['DELETE FROM Buyer WHERE name like "% ?%"'][1][i] += rez[i]

    db.close()
    return data


class SQLA():
    @ps_utils
    def a_query_get_record_found(self, db: Session, find_yes: bool):
        start = time.time()
        if find_yes:
            db.query(A_Buyer).filter(A_Buyer.name == 'buyer50').first()
        else:
            db.query(A_Buyer).filter(A_Buyer.name == 'buyer101').first()

        end = time.time()
        return end - start

    @ps_utils
    def al_group_by(self, db: Session):
        start = time.time()
        db.query(A_Buyer.age, func.count(A_Buyer.age)).group_by(A_Buyer.age)

        end = time.time()
        return end - start

    @ps_utils
    def a_sort(self, db: Session):
        start = time.time()
        db.query(A_Buyer).order_by(A_Buyer.balance).all()
        end = time.time()
        return end - start

    @ps_utils
    def a_filter(self, db: Session):
        start = time.time()
        db.query(A_Buyer, func.count(A_Buyer.age)).filter(A_Buyer.age == random.randint(0, 100)).all()
        end = time.time()
        return end - start

    @ps_utils
    def a_join(self, db: Session):
        start = time.time()
        db.query(A_Buyer).filter(A_Buyer.name == A_Game.buyer).all()
        end = time.time()
        # file.write(f'{end-start=}\n')
        return end - start

    @ps_utils
    def a_add_record(self, db: Session):
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

    @ps_utils
    def a_update_records(self, db: Session):
        start = time.time()

        db.query(A_Buyer).filter(A_Buyer.name == 'test A').update({'name': 'TEST A'},
                                                                  synchronize_session='fetch')
        db.commit()

        end = time.time()
        return end - start

    @ps_utils
    def a_delete(self, db: Session):
        start = time.time()

        db.query(A_Buyer).filter(A_Buyer.name.contains('_A')).delete()
        db.commit()

        end = time.time()
        return end - start


sqla = SQLA()
