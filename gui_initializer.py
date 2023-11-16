import os
import logging
import numpy as np
import tkinter as tk
import logging
from utils.file_loader import meta_file_path, sample_train_dir_path, sample_filenames, sample_file_path, \
    no_class_meta_path
from utils.dataset_appender import append_dataset, move_sample_to_dataset, determine_new_class_id, remove_sample
from itertools import cycle
from tkinter import ttk, Text
from PIL import ImageTk, Image
from TSI.recognition.identification.class_mapper import ClassMapper
from TSI.recognition.identification.identification_model import IdentificationModel


class GUIInitializer:
    NEW_CLASS_OPTION = 'New class'
    logging.basicConfig(level=logging.INFO)

    def __init__(self, sample_x_size: int):
        logging.basicConfig(level=logging.INFO)
        self.sample_x_size = sample_x_size
        self._top = tk.Tk()
        self._identification_model = IdentificationModel()
        self._class_id = None
        self._current_sample = None
        self._class_id_label = ttk.Label(self._top)
        self._sample = ttk.Label(self._top)
        self._combo = ttk.Combobox(state="readonly", width=45, font=("arial", 10))
        self._meta_label = ttk.Label(self._top)
        self._class_samples_label = ttk.Label(self._top)
        self._samples_cycle = cycle(sample_filenames())
        self._new_class_text = Text(self._top, height=1, width=40)

    def _get_sample(self, sample_path) -> None:

        image = Image.open(sample_path)
        width, height = image.size
        x_ratio = self.sample_x_size / width
        sample_y_size = height * x_ratio

        image_to_identify = image.resize((32, 32))
        image = image.resize((self.sample_x_size, round(sample_y_size)))
        imageTk = ImageTk.PhotoImage(image)

        image_to_identify = np.expand_dims(image_to_identify, axis=0)
        image_to_identify = np.array(image_to_identify)
        prediction = self._identification_model.predict([image_to_identify])
        self._class_id = prediction.class_id

        self._sample.configure(image=imageTk)
        self._sample.image = imageTk
        self._sample.grid(column=1, row=1)

    def _display_combo(self) -> None:
        class_mapper = ClassMapper()
        options = list(class_mapper.classes.values())
        options.append(self.NEW_CLASS_OPTION)

        self._combo.configure(values=options)
        self._combo.set(class_mapper.map_to_text(self._class_id))

    def _display_meta(self, preview=True) -> None:
        meta_label = self._meta_label

        if not preview:
            meta_image = Image.open(no_class_meta_path())
            no_of_samples = 0
            self._new_class_text.configure()
            self._new_class_text.configure(state='normal')
            self._new_class_text.delete(1.0, 'end')
        else:
            if not os.path.exists(meta_file_path(self._class_id)):
                meta_image = Image.open(no_class_meta_path())
            else:
                meta_image = Image.open(meta_file_path(self._class_id))

            no_of_samples = len(os.listdir(sample_train_dir_path(self._class_id)))
            self._new_class_text.delete(1.0, 'end')
            self._new_class_text.insert('end', 'Select "New class" to enable')
            self._new_class_text.configure(state='disabled')

        self._class_samples_label.configure(text=f"No. of samples: {no_of_samples}",
                                            font=("arial", 12))
        self._class_samples_label.grid(column=1, row=3, pady=10, padx=10)

        self._class_id_label.configure(text=f"Class No. {self._class_id}", font=("arial", 12))
        self._class_id_label.grid(column=0, row=3, pady=10, padx=10)

        width, height = meta_image.size
        meta_x_ratio = self.sample_x_size / width
        meta_y_size = height * meta_x_ratio

        meta_image = meta_image.resize((self.sample_x_size, round(meta_y_size)))
        meta_imageTk = ImageTk.PhotoImage(meta_image)
        meta_label.configure(image=meta_imageTk)
        meta_label.image = meta_imageTk
        meta_label.grid(column=1, row=4, padx=10, pady=10)

    def _next_sample(self):
        self._current_sample = next(self._samples_cycle)
        self._get_sample(sample_file_path(self._current_sample))
        self._display_combo()
        self._display_meta()

    def _skip_sample(self):
        remove_sample(self._current_sample)
        logging.info(f'Removed {self._current_sample}')
        self._next_sample()

    def _confirm_input(self):
        if self._class_id == determine_new_class_id():
            new_class_name = self._new_class_text.get(1.0, '1.0 lineend')
            append_dataset(self._class_id, new_class_name)
            logging.info(f'Added new class: {new_class_name}')

        move_sample_to_dataset(self._current_sample, self._class_id)
        logging.info(f'Moved {self._current_sample} sample to class with {self._class_id} id')
        self._next_sample()

    def _refresh_meta(self, event):
        sign_name = event.widget.get()

        if sign_name == self.NEW_CLASS_OPTION:
            self._class_id = determine_new_class_id()
            self._display_meta(preview=False)
        else:
            self._class_id = list(ClassMapper().classes.values()).index(sign_name)
            self._display_meta(preview=True)

    def initialize_gui(self):
        self._top.geometry('580x600')
        self._top.title('TSI - Class Selector')
        self._top.configure(background='#CDCDCD')
        heading = ttk.Label(self._top, text="check traffic sign", font=('arial', 20, 'bold'))
        ttk.Label(self._top, text='Select class: ', font=("arial", 12)).grid(column=0, row=2, pady=10, padx=10)

        self._next_sample()

        self._combo.grid(column=1, row=2, padx=10, pady=10)
        self._combo.bind('<<ComboboxSelected>>', self._refresh_meta)

        self._new_class_text.insert('end', 'Select "New class" to enable')
        self._new_class_text.configure(state='disabled')
        self._new_class_text.grid(column=1, row=6, padx=10, pady=10)
        new_class_label = ttk.Label(self._top, text='Select new\nclass name: ', font=("arial", 10))
        new_class_label.grid(column=0, row=6, pady=10, padx=10)

        confirm_button = ttk.Button(self._top, text="Confirm", command=self._confirm_input)
        confirm_button.grid(column=2, row=9, padx=10, pady=10)

        skip_button = ttk.Button(self._top, text="Skip", command=self._skip_sample)
        skip_button.grid(column=0, row=9, padx=10, pady=10)

        heading.configure(background='#CDCDCD', foreground='#364156')
        heading.grid(column=1, row=0)
        self._top.mainloop()
