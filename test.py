import pyautogui


# list all windows
all_windows = pyautogui.getAllWindows()


# get only dofus windows
windows = []
for window in all_windows:
    if "Dofus" in window.title:
        windows.append(window)
        window.maximize()   # make sure that all windows are maximized

windows[0].activate()