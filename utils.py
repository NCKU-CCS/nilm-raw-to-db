import os
import csv


def read_csv_file(f):
    content = []
    with open(f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                content.append(row)
        return content

def loop_csv_files(file_path_list, callback):
    for path in file_path_list:
        filename = os.path.splitext(path.split('/')[-1])[0]
        print(f'Insert {path}...')
        callback(filename, read_csv_file(path))

def rpartial(func, *args):
    return lambda *a: func(*(a + args))


def safe_cast(to_type, val, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
