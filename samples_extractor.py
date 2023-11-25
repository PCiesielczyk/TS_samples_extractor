import logging
import os

from PIL import Image

from TSI.recognition.detection.detection_model import DetectionModel


# filter to ignore specific watermarks on video frames
def match_filter(x1, y1, x2, y2):
    upper_right_x1 = 1060
    lower_right_y2 = 220

    upper_left_x2_1 = 170
    lower_left_y2_1 = 80

    upper_left_x2_2 = 90
    lower_left_y2_2 = 90

    upper_y1 = 660

    if x1 > upper_right_x1 and y2 < lower_right_y2:
        return True
    if x2 < upper_left_x2_1 and y2 < lower_left_y2_1:
        return True
    if x2 < upper_left_x2_2 and y2 < lower_left_y2_2:
        return True
    if y1 > upper_y1:
        return True
    else:
        return False


class SamplesExtractor:
    def __init__(self, images_dir_path: str, confidence_threshold: float):
        logging.basicConfig(level=logging.INFO)
        self.images_dir_path = images_dir_path
        self._detection_model = DetectionModel(confidence_threshold=confidence_threshold)

        if not os.path.isdir('temp'):
            os.mkdir('temp')

    def extract_samples(self) -> None:
        filename_index = 1

        for image_filename in os.listdir(self.images_dir_path):
            image_filename_path = os.path.join(self.images_dir_path, image_filename)
            image = Image.open(image_filename_path).convert('RGB')

            detected_traffic_signs = self._detection_model.detect_traffic_signs(image_filename_path)
            count = len(detected_traffic_signs)

            for traffic_sign in detected_traffic_signs:
                x1, y1 = traffic_sign.x_min, traffic_sign.y_min
                x2, y2 = traffic_sign.x_max, traffic_sign.y_max

                if match_filter(x1, y1, x2, y2):
                    count -= 1
                    continue

                cropped_image = image.crop((x1, y1, x2, y2))

                output_filename = str(filename_index).zfill(6) + '.jpg'
                logging.info(f'x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}')
                logging.info(f'From {image_filename_path} saved to {output_filename}')
                output_file_path = os.path.join('temp', output_filename)

                cropped_image.save(output_file_path)
                filename_index += 1

            logging.info(f'Extracted {count} samples in {image_filename_path}')
