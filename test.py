import pyautogui as pg
import pytesseract

from src.enum.positions import Positions

pg.moveTo(*Positions.INVENTORY_PODS_BAR_MIDDLE)
img = pg.screenshot(region=Positions.INVENTORY_PODS_VALUE_REG)

value = pytesseract.image_to_string(img, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')

print(value)
img.show()