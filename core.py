import pyautogui
import numpy as np
import asyncio
import os
import time
from random import random
import cv2

BASE_DIR = os.path.abspath(f'{os.path.dirname(os.path.dirname(__file__))}/fruitBot')
BASE_DIR_TEMPLATES = BASE_DIR + '\\templates'
CORDS = []


class Screen:
    def make_screen(self):
        self.image_screen = pyautogui.screenshot(region=(0, 0, 750, 500))
        #self._convert_image()
        self._change_image()
        #self._load_screen()
        self._save_current_screen()

        return self.finally_image_screen

    def _change_image(self):
        self.finally_image_screen = cv2.cvtColor(np.array(self.image_screen), cv2.COLOR_BGR2GRAY)

    def _convert_image(self):
        img_screen = self.image_screen
        self.image_now = np.array(img_screen.getdata(), dtype='uint8').reshape((img_screen.size[1], img_screen.size[0], 3))
        self.image_now = cv2.cvtColor(self.image_now, cv2.COLOR_BGR2GRAY)

    def _load_screen(self):
        self.load_screen = cv2.imread(f'{BASE_DIR}/tempScreen/1.png', 0)
        self.load_screen = cv2.cvtColor(self.load_screen, cv2.COLOR_BGR2GRAY)
        print(self.load_screen)
        print(self.load_screen.astype(np.uint8))

        return self.load_screen.astype(np.uint8)

    def _save_current_screen(self):
        name = str(random())[4:8]
        cv2.imwrite(f'{BASE_DIR}/tempScreen/game_{name}_now.png', self.finally_image_screen)


class Template:
    async def search_on_image(self, image, template):
        try:
            result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

            location_result = np.where(result >= 0.8)
            print(location_result)

            if len(location_result) != 0:
                print('Found')
                (min_Val, max_Val, minLoc, maxLoc) = cv2.minMaxLoc(result)

                coordinates = zip(*location_result[::-1])
                for pt in coordinates:
                    loc_x = int(pt[0])
                    loc_y = int(pt[1])
                    print(loc_x, '|||', loc_y)
                    CORDS.append([loc_x, loc_y])

        except Exception as e:
            print(e)

    def load_templates(self):
        lst_temp = []
        templates = os.listdir(BASE_DIR_TEMPLATES)
        for temp in templates:
            path = BASE_DIR_TEMPLATES + f'\\{temp}'
            template = cv2.imread(path, 0)
            lst_temp.append(template)

        return lst_temp


class Movement:
    @staticmethod
    def focus_on_fruit(x, y):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right', x=x+15, y=y+15)


def view_image(image):
    cv2.imshow('Image', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    screen = Screen()
    loop = asyncio.get_event_loop()
    template = Template()
    lst_temp = template.load_templates()

    start = input("Enter to start: ")
    if start or start == '':
        time.sleep(3)
        while True:
            try:
                picture_gray = screen.make_screen()
                tasks = [
                    loop.create_task(template.search_on_image(picture_gray, lst_temp[0])),
                    loop.create_task(template.search_on_image(picture_gray, lst_temp[1])),
                    loop.create_task(template.search_on_image(picture_gray, lst_temp[2])),
                    loop.create_task(template.search_on_image(picture_gray, lst_temp[3]))
                ]
                loop.run_until_complete(asyncio.wait(tasks))
                print(CORDS)

                time.sleep(1)
            except Exception as e:
                print(e)
                print("Ошибка")
