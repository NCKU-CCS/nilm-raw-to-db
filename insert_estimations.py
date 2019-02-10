import sys
import os
from functools import partial
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from model import (
    Base,
    Monitor,
    Estimation,
    Appliance,
    engine,
)

from utils import (
    loop_csv_files,
    read_csv_file,
    rpartial,
    safe_cast,
    search_files_in_folder,
)

MIN_NUM_DATA_COL = 4
NUM_APPLIANCE_COL = 4

def is_estimation_file(file):
    if file.endswith('.csv') and not file.endswith('st.csv'):
        return True
    return False

def loop_estimations(filename, content, callback):
    created_date, monitor_id = filename.split('_')
    for row in content:
        if len(row) > MIN_NUM_DATA_COL:
            callback(created_date, monitor_id, row)
        else:
            print(f'{filename} has an incomplete row', row)

def insert_data(session, created_date, monitor_id, row):
    new_estimation = insert_estimation(session, created_date, monitor_id, row)
    row_len = len(row)
    counter = MIN_NUM_DATA_COL - 1
    while (counter + NUM_APPLIANCE_COL) < row_len:
        insert_appliance(
            new_estimation,
            safe_cast(int, row[counter]), # Appliance Type ID
            safe_cast(int, row[counter+1]), # Appliance ID
            row[counter+2], # Appliance Name
            row[counter+3] # estimated power
        )
        counter += NUM_APPLIANCE_COL


def insert_estimation(session, created_date, monitor_id, row):
    monitor = session.query(Monitor).get(monitor_id)
    try:
        new_estimation = Estimation(
            id=f'{monitor_id}_{row[0]}',
            timestamp=datetime.utcfromtimestamp(int(row[0])),
            total_power=row[1] or None,
            mac_address=row[2],
            created_date=datetime.strptime(created_date, '%Y%m%d'),
            monitor=monitor,
        )
        session.add(new_estimation)
    except IntegrityError:
        session.rollback()
    return new_estimation

def insert_appliance(estimation, type_id, appliance_id, name, power):
    session.add(
        Appliance(
            appliance_id=safe_cast(int, appliance_id),
            appliance_type_id=safe_cast(int, type_id),
            appliance_name=name,
            estimated_power=safe_cast(float, power),
            estimation=estimation
        )
    )

if __name__ == '__main__':
    if len(sys.argv) > 1:
        nilm_folder_path = sys.argv[1]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        insert_data_with_session = partial(insert_data, session)
        loop_csv_files(
            search_files_in_folder(nilm_folder_path, is_estimation_file),
            rpartial(loop_estimations, insert_data_with_session)
        )
        session.commit()
        print('done.')
    else:
        print('python insert_estimations.py <nilm_folder_path>')