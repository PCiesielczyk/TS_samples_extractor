import os

master_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.dirname(master_dir)
project_dir = os.path.dirname(module_dir)
archive_dir = os.path.join(project_dir, 'TSI', 'archive')


def meta_file_path(class_id: int) -> str:
    return os.path.join(archive_dir, 'Meta', str(class_id) + '.png')


def sample_train_dir_path(class_id: int) -> str:
    return os.path.join(archive_dir, 'Train', str(class_id))


def sample_filenames() -> list:
    return os.listdir(os.path.join(module_dir, 'temp'))


def sample_file_path(sample_filename: str) -> str:
    return os.path.join(module_dir, 'temp', sample_filename)


def no_class_meta_path() -> str:
    return os.path.join(master_dir, 'no_image_selected.jpg')
