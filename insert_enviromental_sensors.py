import sys
import os
from functools import partial
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from model import (
    Base,
    Monitor,
    EnvironmentalSensor,
    engine,
)

from utils import (
    loop_csv_files,
    read_csv_file,
    rpartial,
    safe_cast,
)

def get_all_sensors_files(path):
    files = list()
    for r, _, f in os.walk(path):
        for file in f:
            if file.endswith('st.csv'):
                files.append(os.path.join(r, file))
    return files

def loop_sensors(filename, content, callback):
    created_date, mintor_id, _ = filename.split('_')
    for row in content[1:]:
        if len(row) == 7:
            callback(created_date, mintor_id, row)
        else:
            print(f'{filename} has incompleted row', row)

def insert_sensor(session, created_date, monitor_id, row):
    monitor = session.query(Monitor).get(monitor_id)
    try:
        session.add(
            EnvironmentalSensor(
                id=f'{monitor_id}_{row[0]}',
                timestamp=datetime.utcfromtimestamp(int(row[0])),
                time=datetime.strptime(row[1], '%Y/%m/%d %H:%M'),
                temperature=safe_cast(float, row[2]),
                humidity=safe_cast(int, row[3]),
                co2_concentration=safe_cast(int, row[4]),
                sound_pressure=safe_cast(int, row[5]),
                air_pressure=safe_cast(float, row[6]),
                monitor=monitor,
            )
        )
    except IntegrityError:
        session.rollback()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        nilm_folder_path = sys.argv[1]
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        insert_sensor_with_session = partial(insert_sensor, session)
        loop_csv_files(
            get_all_sensors_files(nilm_folder_path),
            rpartial(loop_sensors, insert_sensor_with_session)
        )
        session.commit()
        print('done.')
    else:
        print('python insert_enviromental_sensors.py <nilm_folder_path>')