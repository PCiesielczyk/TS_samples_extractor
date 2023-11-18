import os
import cv2
import logging
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_ssim(base_image: np.ndarray, compared_image: np.ndarray) -> float:
    compared_image = cv2.resize(compared_image, (base_image.shape[1], base_image.shape[0]))

    base_gray = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    compared_gray = cv2.cvtColor(compared_image, cv2.COLOR_BGR2GRAY)

    (score, diff) = ssim(base_gray, compared_gray, full=True)
    return score


class DuplicatesRemover:
    logging.basicConfig(level=logging.INFO)

    def __init__(self, similarity_threshold: float):
        self.similarity_threshold = similarity_threshold

    def remove_duplicates(self) -> None:
        samples = os.listdir('temp')

        for base_index in range(len(samples)):
            for compared_index in range(base_index + 1, len(samples)):
                base_image_path = os.path.join('temp', samples[base_index])
                compared_image_path = os.path.join('temp', samples[compared_index])

                if os.path.isfile(base_image_path) and os.path.isfile(compared_image_path):
                    base_image = cv2.imread(base_image_path)
                    compared_image = cv2.imread(compared_image_path)
                else:
                    continue

                similarity = calculate_ssim(base_image, compared_image) * 100

                if similarity >= self.similarity_threshold:
                    os.remove(compared_image_path)
                    print(f'Removed {samples[compared_index]} as duplicate of {samples[base_index]}. '
                          f'Similarity: {similarity:.2f}%')
