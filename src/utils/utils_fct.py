import time
import pyautogui as pg


def wait_click_on(image: str, confidence: float = 0.8, max_timer: float = 5, offset_x=0, offset_y=0):
    pos = None
    start = time.time()
    while pos is None:
        if time.time() - start >= max_timer:
            return False
        pos = pg.locateOnScreen(image, confidence=confidence)

    pg.click(pos[0] + offset_x, pos[1] + offset_y)
    return True


def display_mouse(self):
    while True:
        print(pg.position(), end='\r')
