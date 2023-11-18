import csv
import os
import logging
from TSI.data_storage.file_loader import classes_csv_file_path, train_dir_path
from TS_samples_extractor.utilities.file_loader import sample_file_path, sample_train_dir_path

logging.basicConfig(level=logging.INFO)


def append_dataset(class_id: int, class_name: str):
    append_meta(class_id, class_name)
    append_train_dir(class_id)


def append_meta(class_id: int, class_name: str) -> None:
    with open(classes_csv_file_path, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator='\n')
        new_row = [str(class_id), class_name]
        csv_writer.writerow(new_row)


def append_train_dir(class_id: int):
    os.mkdir(sample_train_dir_path(class_id))


def determine_new_class_id() -> int:
    sorted_dir_list = sorted(os.listdir(train_dir_path), key=lambda d: int(d))
    last_element = sorted_dir_list[-1]
    dir_name = int(last_element) + 1
    return dir_name


def determine_new_filename(class_id):
    sample_train_dir_path_val = sample_train_dir_path(class_id)
    elements_len = len(os.listdir(sample_train_dir_path_val)) + 1
    new_sample_filename = str(elements_len) + '.jpg'

    while os.path.exists(os.path.join(sample_train_dir_path_val, new_sample_filename)):
        elements_len += 1
        new_sample_filename = str(elements_len) + '.jpg'

    return new_sample_filename


def move_sample_to_dataset(sample_filename: str, class_id: int) -> None:
    sample_path = sample_file_path(sample_filename)
    sample_train_dir_path_val = sample_train_dir_path(class_id)

    if not os.path.exists(sample_path):
        logging.error(f'File {sample_path} does not exist')
        return

    if not os.path.exists(sample_train_dir_path_val):
        logging.error(f'File {sample_train_dir_path_val} does not exist')
        return

    os.rename(sample_path, os.path.join(sample_train_dir_path_val, determine_new_filename(class_id)))


def remove_sample(sample_filename: str) -> None:
    sample_path = sample_file_path(sample_filename)
    os.remove(sample_path)
