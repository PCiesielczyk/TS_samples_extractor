import os
import cv2
import logging


class VideoProcessor:

    def __init__(self, video_file_path: str, output_path: str, frame_interval: int):
        logging.basicConfig(level=logging.INFO)
        self.video_file_path = video_file_path
        self.output_path = output_path
        self.frame_interval = frame_interval

    def extract_frames(self) -> None:
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        if not os.path.exists(self.video_file_path):
            logging.error(f'file {self.video_file_path} doesnt exist')
            return

        filename_index = 1

        video_cap = cv2.VideoCapture(self.video_file_path)
        success, image = video_cap.read()
        count = 0

        while success:
            if count % self.frame_interval == 0 and count > 150:
                output_filename = str(filename_index).zfill(6) + '.jpg'
                cv2.imwrite(os.path.join(self.output_path, output_filename), image)
                logging.info(f'saved frame to {output_filename}')
                filename_index += 1

            success, image = video_cap.read()
            count += 1
