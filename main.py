import os

import numpy as np
from PIL import Image


class ImageSlicer:
    RESULT_DIR_NAME = "sliced_images"

    def __init__(self, height: int, part_height: int):
        self.max_height = height
        self.part_height = part_height

    def slice(self, path: str):
        self._prepare_folder()

        if os.path.isdir(path):
            for file in os.listdir(path):
                self._slice(os.path.join(file, file))
        else:
            self._slice(path)

    def _slice(self, image_name):
        image = np.array(Image.open(image_name))
        image_name = os.path.split(image_name)[1].split(".")[0]
        flag = True
        counter = 0
        while flag:
            counter += 1
            if len(image) > self.max_height:
                index = self._find_row_for_slice(image)      
            else:
                index = len(image)
                flag = False
            new_image = image[:index]
            image = image[index:]
            self._save_image(new_image, f"{image_name}_{counter}")

    def _find_row_for_slice(self, image):
        counter = 0
        index = self._check_row(image, self.max_height)
        if not index:
            index = self._check_row(image, self._first_false_row(image, self.max_height), step=1)

        return index

    def _check_row(self, image, index, step: int = -1) -> int:
        counter = 0
        edge = 0 if step == -1 else len((image))
        for j in range(index, edge, step):
            if self._check_pixels_in_row(image[j]):
                counter += 1
                if counter == self.part_height:
                    return j
            else:
                counter = 0
        return 0

    def _first_false_row(self, image, index):
        for j in range(index, 0, -1):
            if not self._check_pixels_in_row(image[j]):
                return j
        return 0


    def _check_pixels_in_row(self, pixels: list):
        for i in range(len(pixels)-1):
            if list(pixels[0]) != list(pixels[i]):
                return False
        return True

    def _save_image(self, image, name):
        file_name = name + ".png"
        image = Image.fromarray(image)
        image.save(os.path.join(self.RESULT_DIR_NAME, file_name))

    def _prepare_folder(self):
        if not os.path.exists(self.RESULT_DIR_NAME):
            os.mkdir(self.RESULT_DIR_NAME)


if __name__ == "__main__":
    slicer = ImageSlicer(1500, 30)
    # slicer.slice("imgs")
    # slicer.slice("imgs/1.jpg")