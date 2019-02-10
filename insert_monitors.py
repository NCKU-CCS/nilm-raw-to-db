
import sys
from functools import partial

import xlrd
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from model import (
    Base,
    Monitor,
    Estimation,
    Appliance,
    engine,
)


def loop_monitor_list(path, callback):
    workbook = xlrd.open_workbook(path)
    booksheet = workbook.sheet_by_index(0)
    for n in range(booksheet.nrows):
        callback(booksheet.row_values(n))

def insert_monitor(session, row):
    try:
        session.add(
            Monitor(
                id=row[0],
                members_number=row[1],
                architectural_area_m2=row[2]
            )
        )
        session.commit()
    except IntegrityError:
        session.rollback()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        monitor_list_xlsx_path = sys.argv[1]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        loop_monitor_list(monitor_list_xlsx_path, partial(insert_monitor, session))
        print('done.')
    else:
        print('python insert_monitors.py <monitor_list_xlsx_path>')