class Game:
    def __init__(self):
        self.board = [['.' for i in range(7)] for i in range(7)]
        self.tiles = {(0, 0), (0, 3), (0, 6), (1, 1), (1, 3), (1, 5), (2, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2),
                      (3, 4), (3, 5), (3, 6), (4, 2), (4, 3), (4, 4), (5, 1), (5, 3), (5, 5), (6, 0), (6, 3), (6, 6)}
        self.placed = 0
        self.white = 0
        self.black = 0
        self.player = 'W'
        self.history = []

    def start(self):
        self.board = [['.' for i in range(7)] for i in range(7)]
        self.placed = 0
        self.white = 0
        self.black = 0
        self.player = 'W'
        self.history = []

    def switch(self):
        if self.player == 'W':
            self.player = 'B'
        else:
            self.player = 'W'

    def place(self, x, y):
        if self.placed > 17 or (x, y) not in self.tiles or self.board[y][x] != '.':
            return False
        self.board[y][x] = self.player
        self.placed += 1
        if self.player == 'W':
            self.white += 1
        else:
            self.black += 1
        self.history.append((x, y, None, None))
        return True

    def move(self, x, y, nx, ny):
        if (self.placed < 18 or (x, y) not in self.tiles or (nx, ny) not in self.tiles
                or self.board[y][x] != self.player or self.board[ny][nx] != '.'):
            return False
        self.board[y][x] = '.'
        self.board[ny][nx] = self.player
        self.history.append((x, y, nx, ny))
        return True
    
    def undo(self):
        if not self.history:
            return False
        x, y, nx, ny = self.history.pop()
        if nx is None:
            self.board[y][x] = '.'
            self.placed -= 1
            if self.player == 'W':
                self.white -= 1
            else:
                self.black -= 1
        else:
            self.board[y][x] = self.player
            self.board[ny][nx] = '.'


def main():
    print("Welcome to the Mill Game Solver!")


if __name__ == "__main__":
    main()
