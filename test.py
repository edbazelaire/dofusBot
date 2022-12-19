import win32gui


def callback(hwnd, extra):
    name = win32gui.GetWindowText(hwnd)
    if 'Dofus' in name:
        return hwnd
    else:
        return

    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))


def main():
    win32gui.EnumWindows(callback, None)

    # test = win32gui.FindWindow(None, "Parsec")
    # win32gui.GetWindow(test)
    # print(test)


if __name__ == '__main__':
    main()