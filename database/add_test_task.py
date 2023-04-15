import datetime

from sqlalchemy.orm import Session

from database.db import engine, Task


task1: Task = Task(title='1я',
             target_time=str(datetime.time(hour=12, minute=0, second=0)),
             last_send = datetime.datetime(2023, 4, 13))
#
task2: Task = Task(title='2я',
             target_time=str(datetime.time(hour=15, minute=0, second=0)),
             last_send = datetime.datetime(2023, 4, 13))

task3: Task = Task(title='3я',
             target_time=str(datetime.time(hour=16, minute=0, second=0)),
             last_send = datetime.datetime(2023, 4, 13))

task4: Task = Task(title='4я',
                   target_time=str(datetime.time(hour=17, minute=0, second=0)),
                   last_send = datetime.datetime(2023, 4, 13))

session = Session(bind=engine)

with session:
    session.add_all([task1, task2, task3, task4])
    session.commit()