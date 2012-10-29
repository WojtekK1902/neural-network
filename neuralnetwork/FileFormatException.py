class FileFormatException(Exception):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return self.pos
