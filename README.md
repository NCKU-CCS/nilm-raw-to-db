## nilm-raw-to-db

Insert nilm raw data to database

### Install

```
$ pipenv install
```

### Usage

1. Donwload and save the nilm data to the project folder

2. Insert monitor list

```py
pipenv run python insert_monitors.py <monitor_list_xlsx_path>
```

3. Insert Estimation Results

```py
pipenv run python insert_estimations.py <nilm_folder_path>
```

4. Insert enviromental sensor data

```py
pipenv run python insert_enviromental_sensors.py <nilm_folder_path>
```