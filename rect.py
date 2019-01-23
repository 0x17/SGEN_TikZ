class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def overlaps(self, other):
        if self.w == 0 or self.h == 0:
            return False

        return self.x + self.w > other.x and \
               self.x < other.x + other.w and \
               self.y + self.h > other.y and \
               self.y < other.y + other.h

    def __str__(self):
        return str([self.x, self.y, self.w, self.h])
