# write your code here
import textwrap
import random
import math
import time


def get_cells(cells="_________"):
    scells = textwrap.wrap(cells, 3)
    separator = " "
    out_cells = "---------\n"
    for n in range(3):
        out_cells += "| {0} |\n"\
            .format(separator.join([cell if cell == "X" or cell == "O" else " " for cell in scells[n][0:3]]))
    out_cells += "---------\n"
    return out_cells


def get_leading_diagonal(_lines):
    return [row[i] for i, row in enumerate(_lines)]


def get_even_diagonal(_lines):
    return [row[-i-1] for i, row in enumerate(_lines)]


def are_numbers(icoordinates):
    for letter in icoordinates:
        if not letter.isdecimal() and letter != " ":
            return False
    return True


def in_tiktaktoe_bounds(icoordinates):
    for digit in icoordinates.split():
        if int(digit) > 3 or int(digit) < 1:
            return False
    return True


class TikTakToe:
    def __init__(self, cells="_________"):
        self.cells = cells
        self.coordinates = {"1 3": 0, "2 3": 1, "3 3": 2, "1 2": 3, "2 2": 4, "3 2": 5, "1 1": 6, "2 1": 7, "3 1": 8}
        self.move = "1 1"
        self.levels = ["user", "easy", "medium", "hard"]
        self.winner = "none"

    def print_cells(self):
        print(get_cells(self.cells))

    def game(self):
        test = 0
        file = open('wins.txt', 'a', encoding='utf-8')
        while True:
            # command = input("Input command: ")
            command = "start hard hard"
            if command == "exit":
                break
            elif len(command.split()) == 3 and command.split()[0] == "start" \
                    and self.correct_level(command.split()[1]) \
                    and self.correct_level(command.split()[2]):
                levels = [command.split()[1], command.split()[2]]
                self.print_cells()
                flag = False
                while True:
                    for level in levels:
                        if self.play_game(level):
                            flag = True
                            break

                    if flag:
                        file.write(str(test) + " " + self.winner + "\n")
                        test += 1
                        break

            else:
                print("Bad parameters!")
            self.cells = "_________"
            if test == 100:
                file.close()
                self.check_ai()
                break

    def check_ai(self):
        file = open('wins.txt', 'r', encoding='utf-8')
        results = file.readlines()
        file.close()
        results = str(" ".join(results))
        print("Hard: {}".format(str(results.count("hard"))))
        print("Medium: {}".format(str(results.count("medium"))))
        print("Easy: {}".format(str(results.count("easy"))))
        print("Draw: {}".format(str(results.count("Draw"))))
        open('wins.txt', 'w').close()

    def play_game(self, level):
        while True:
            if level == "user":
                while True:
                    self.move = input("Enter the coordinates: ")
                    if self.check_coordinates(self.move):
                        self.cells = self.make_turn(self.cells, self.move)
                        self.print_cells()
                        return self.check_state_end(self.cells)
            if level == "easy":
                self.level_easy()
                self.print_cells()
                self.winner = "easy"
                return self.check_state_end(self.cells)
            if level == "medium":
                self.level_medium()
                self.print_cells()
                self.winner = "medium"
                return self.check_state_end(self.cells)
            if level == "hard":
                self.level_hard()
                self.print_cells()
                self.winner = "hard"
                return self.check_state_end(self.cells)

    def correct_level(self, level):
        if level in self.levels:
            return True
        return False

    def level_easy(self):
        print('Making move level "easy"')
        not_occupied = self.get_not_occupied_coordinates(self.cells)
        self.cells = self.make_turn(self.cells, random.choice(not_occupied))

    def level_medium(self):
        print('Making move level "medium"')
        not_occupied = self.get_not_occupied_coordinates(self.cells)
        for i in range(len(not_occupied)):
            ai_turn = not_occupied[i]
            state = self.get_game_state(self.make_turn(self.cells, ai_turn))
            if state == "X wins"\
                    or state == "O wins":
                self.cells = self.make_turn(self.cells, ai_turn)
                return
        for i in range(len(not_occupied)):
            ai_turn = not_occupied[i]
            for j in range(len(not_occupied)):
                block = self.make_turn(self.cells, ai_turn)
                user_turn = not_occupied[j]
                state2 = self.get_game_state(self.make_turn(block, user_turn))
                if state2 == "X wins" \
                        or state2 == "O wins":
                    self.cells = self.make_turn(self.cells, user_turn)
                    return
        self.cells = self.make_turn(self.cells, random.choice(not_occupied))

    def get_hard(self):
        return self.get_which_tictactoe(self.cells)

    def get_oponnent(self):
        return "X" if self.get_hard() == "O" else "O"

    def level_hard(self):
        print('Making move level "hard"')
        # then = time.time()
        if len(self.get_not_occupied_coordinates(self.cells)) == 9:
            self.cells = self.make_turn(self.cells, 0)
        else:
            self.cells = self.make_turn(self.cells,
            self.minimax(self.cells, self.get_hard())["index"])
        # print("--- %s seconds ---" % (time.time() - then))

    def minimax(self, newboard, player):
        availSpots = self.get_not_occupied_coordinates(newboard)
        state = self.get_game_state(newboard)
        if self.get_oponnent() in state:
            return {"score": -10}
        if self.get_hard() in state:
            return {"score": 10}
        if state == "Draw":
            return {"score": 0}
        moves = []
        for not_occupied in availSpots:
            move = {"index": self.coordinates[not_occupied],
                    "score": self.minimax(self.make_turn(newboard, not_occupied), self.get_oponnent())["score"]
                    if player == self.get_hard()
                    else self.minimax(self.make_turn(newboard, not_occupied), self.get_hard())["score"]}
            moves.append(move)
        best_move = {}
        if player == self.get_hard():
            best_score = -math.inf
            for move in moves:
                if move["score"] > best_score:
                    best_score = move["score"]
                    best_move = move
        else:
            best_score = math.inf
            for move in moves:
                if move["score"] < best_score:
                    best_score = move["score"]
                    best_move = move
        return best_move

    def get_which_tictactoe(self, cells):
        x = cells.count("X")
        o = cells.count("O")
        if x <= o:
            return "X"
        return "O"

    def make_turn(self, cells, turn):
        x = cells.count("X")
        o = cells.count("O")
        cells_list = list(cells)
        if type(turn) == str:
            if x <= o:
                cells_list[self.coordinates[str(turn)]] = "X"
            else:
                cells_list[self.coordinates[str(turn)]] = "O"
        else:
            if x <= o:
                cells_list[turn] = "X"
            else:
                cells_list[turn] = "O"
        cells = "".join(cells_list)
        return cells

    def check_state_end(self, cells):
        state = self.get_game_state(cells)
        if state == "X wins" or state == "O wins" or state == "Draw":
            print(state)
            return True
        return False

    def get_game_state(self, cells):
        lines = textwrap.wrap(cells, 3)
        columns = []
        for j in range(3):
            columns.append([])
            for i in range(j, 9, 3):
                columns[j].append(cells[i])
        diagonals = [get_leading_diagonal(textwrap.wrap(cells, 3)),
                     get_even_diagonal(textwrap.wrap(cells, 3))]
        for line in lines + columns + diagonals:
            if line.count("X") == 3:
                return "X wins"
            elif line.count("O") == 3:
                return "O wins"
        if "".join(lines).count("X") + "".join(lines).count("O") == 9:
            self.winner = "Draw"
            return "Draw"
        else:
            return "Game not finished"

    def get_not_occupied_coordinates(self, cells):
        not_occupied = [coordinate for coordinate in self.coordinates if cells[self.coordinates[coordinate]] == "_"]
        return not_occupied

    def not_occupied(self, icoordinates):
        if self.cells[self.coordinates[str(icoordinates)]] == "X" \
                or self.cells[self.coordinates[str(icoordinates)]] == "O":
            return False
        return True

    def check_coordinates(self, icoordinates):
        try:
            if not are_numbers(icoordinates):
                raise Exception("You should enter numbers!")
            elif not in_tiktaktoe_bounds(icoordinates):
                raise Exception("Coordinates should be from 1 to 3!")
            elif not self.not_occupied(icoordinates):
                raise Exception("This cell is occupied! Choose another one!")
            return icoordinates
        except Exception as err:
            print(err)
            return None



# input_cells = input("Enter cells: ")[0:9]
test = TikTakToe()
test.game()
