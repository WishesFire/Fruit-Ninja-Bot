import pyautogui
import numpy as np
import os
import time
import cv2

BASE_DIR = os.path.abspath(f'{os.path.dirname(os.path.dirname(__file__))}/fruitBot')
BASE_DIR_TEMPLATES = BASE_DIR + '/templates'


class Screen:
    def make_screen(self):
        self.image_now = pyautogui.screenshot(region=(0, 0, 750, 500))
        self._change_image()
        #self._save_current_screen()
        return self.img_rgb, self.img_now

    def _change_image(self):
        self.img_rgb = cv2.cvtColor(np.float32(self.image_now), cv2.COLOR_BGR2GRAY)
        self.img_now = cv2.cvtColor(np.float32(self.image_now), cv2.COLOR_BGR2RGB)

    def _save_current_screen(self):
        cv2.imwrite(f'{BASE_DIR}/game_now.png', self.img_now)


class Template:
    def search_on_image(self, image, template):
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    def load_templates(self):
        templates = os.listdir(BASE_DIR_TEMPLATES)
        for temp in templates:
            path = BASE_DIR_TEMPLATES + f'//{temp}'
            template = cv2.imread(path)
            temp_x, temp_y = template.shape[::-1]


def view_image(image):
    cv2.imshow('Image', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


class Movement:
    def slice_fruit(self):
        pass


if __name__ == '__main__':
    screen = Screen()
    template = Template()
    picture_rgb, picture_now = screen.make_screen()

