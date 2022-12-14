class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, pos):
        if isinstance(pos, Pos):
            self.x += pos.x
            self.y += pos.y

        if isinstance(pos, list) or isinstance(pos, tuple):
            self.x += pos[0]
            self.y += pos[1]

    def __sub__(self, pos):
        if isinstance(pos, Pos):
            self.x -= pos.x
            self.y -= pos.y

        if isinstance(pos, list) or isinstance(pos, tuple):
            self.x -= pos[0]
            self.y -= pos[1]

    def __mul__(self, value: (int, float, list, tuple)):
        if isinstance(value, int) or isinstance(value, float):
            self.x *= value
            self.y *= value

        if isinstance(value, list) or isinstance(value, tuple):
            self.x *= value[0]
            self.y *= value[1]