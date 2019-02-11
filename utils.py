import os
import csv

def search_files_in_folder(folder, filter_fn=lambda f: True):
    searched_files = list()
    for f_dir, _, files in os.walk(folder):
        for file in files:
            if filter_fn(file):
                searched_files.append(os.path.join(f_dir, file))
    return searched_files

def read_csv_file(file_path):
    content = []
    with open(file_path) as csv_file:
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
