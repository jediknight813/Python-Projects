import time
import random


class game():
    def __init__(self, turn=0, gameover=False, current_turn="player", player_board=None, computer_board=None):
        self.turn = turn
        self.gameover = gameover
        self.current_turn = current_turn
        self.player_board = player_board
        self.computer_board = computer_board

        
def game_manager(): #starts and manages the game
    game_class = game()
    game_class.player_board = gameboard("player", create_board(0, 10), 0, None, 4)
    game_class.computer_board =  gameboard("computer", create_board(0, 10), 0, create_board("?", 10), 5)
    game_class.computer_board.board = place_ships_randomly_on_board(game_class.computer_board.board, [3,2])
    print_board(game_class.player_board.board)
    game_class.player_board.board = pick_ship_location(game_class.player_board.board, [4])


    while game_class.gameover == False:
        game_class.gameover = check_for_winner(game_class.player_board) #handles the players turn
        if game_class.current_turn == "player" and game_class.gameover == False:
            print("current turn: " + str(game_class.turn))
            print(game_class.player_board.name + " turn")
            attack(game_class.computer_board)
            game_class.current_turn = "computer"
            game_class.turn += 1


        game_class.gameover = check_for_winner(game_class.computer_board) #handles the computers turn
        if game_class.current_turn == "computer" and game_class.gameover == False:
            print("current turn: " + str(game_class.turn))
            computer_attack(game_class.player_board)
            game_class.current_turn = "player"
            game_class.turn += 1
    

def create_board(character, size): #creates the board dynamically 
    grid = []
    for i in range(size):
        grid.append([])
        for b in range(size):
            grid[i].append(character)

    return grid


class gameboard(): #class for the gameboard

    def __init__(self, name, board, hits, hidden_board, ship_value, MissesAndHits=[]):
         self.name = name
         self.board = board
         self.hits = hits
         self.hidden_board = hidden_board
         self.MissesAndHits = MissesAndHits
         self.ship_value = ship_value


class ship(): #prototype ship class

    def __init__(self, position, ship_type, length, placed):
        self.position = position #positon = [[1,2], [1,3], [1,4]]
        self.ship_type = ship_type #battleship
        self.length = length # 4
        self.placed =  placed
        if ship_type == "battleship":
            self.health = 4
        elif ship_type == "cruiser":
            self.health = 3
        elif ship_type == "patrol boat":
            self.health = 2

    def check_if_sunk(self):
        if self.health < 0:
            return True
        else:
            return False


    def ship_hit(self):
        self.health -= 1
    

    def is_placed(self):
        self.placed = True



def check_for_winner(gameboard): #takes a gameboard and checks for winner
    if int(gameboard.hits) >= int(gameboard.ship_value):
        print(gameboard.name + " has lost the game")
        return True
    else:
        return False


def pick_ship_location(board, ships): #allows the player to pick where they want to place their ships
    ship_list = ships #length of eatch ships, can add as many as you want
    correct_x_y = False
    
    while correct_x_y == False:
        x, y = get_correct_x_y()
        if y < 9 and x+ship_list[0] < 9 and y > -1 and x > -1:
            if board[y][x] != 2:
                if ship_list != []:
                    board = place_ship(x, y, board, ship_list[0])
                    ship_list.remove(ship_list[0])
                    print("place ships")
                    print_board(board)
                    if ship_list == []:
                        correct_x_y = True
            else:
                print("incorrect x, y try again")
    
    return board


def get_correct_x_y(): #makes sure the x, y is correct
    correct_x_y = False
    while correct_x_y == False:
        x = input("enter x value: ")
        y = input("enter y value: ")
        if x.isdigit() == True:
            if y.isdigit() == True:
                x = int(x)
                y = int(y)
                return(x, y)


def place_ship(x, y, board, ship): #places the ship on the gameboard
    length = ship

    board[y][x] = 2
    if length > 1:
        board[y][x+1] = 2
        if length > 2:
            board[y][x+2] = 2
            if length > 3:
                board[y][x+3] = 2

    return board


def place_ships_randomly_on_board(board, ship_list): #randomly places all the ships on the passed board
    correct_x_y = False

    while correct_x_y == False:
        x = random.randrange(-1, 10)
        y = random.randrange(-1, 10)
        if y < 9 and x+ship_list[0] < 9 and y > -1 and x > -1:
            if board[y][x] != 2:
                if ship_list != []:
                    board = place_ship(x, y, board, ship_list[0])
                    ship_list.remove(ship_list[0])
                    print("computer place ships")
                    print_board(board)
                    if ship_list == []:
                        correct_x_y = True
            else:
                print("incorrect x, y try again")
    
    return board


def computer_attack(gameboard): #attacks a random position on the board that has not been attacked
    move_tried = False
    correct_x_y = False
    while correct_x_y == False:
        x = random.randrange(-1, 10)
        y = random.randrange(-1, 10)
        if y < 9 and x < 9 and y > -1 and x > -1:
            for i in gameboard.MissesAndHits:
                if i == [y, x]:
                    move_tried = True
            if gameboard.board[y][x] == 2 and move_tried == False:
                gameboard.hits += 1
                gameboard.MissesAndHits += [[y, x]]
                gameboard.board[y][x] = "X"
                correct_x_y = True
            elif move_tried == False:
                gameboard.board[y][x] = "M"
                gameboard.MissesAndHits += [[y, x]]
                correct_x_y = True


    print("computer turn")
    print_board(gameboard.board)
    time.sleep(2)


def attack(gameboard): #lets the player pick where they want to attack
    move_tried = False
    correct_x_y = False

    print_board(gameboard.hidden_board)

    while correct_x_y == False:
        x, y = get_correct_x_y()
        if y < 9 and x < 9 and y > -1 and x > -1:
            for i in gameboard.MissesAndHits:
                if i == [y, x]:
                    move_tried = True
            if gameboard.board[y][x] == 2 and move_tried == False:
                gameboard.hits += 1
                gameboard.MissesAndHits += [[y, x]]
                gameboard.hidden_board[y][x] = "X"
                correct_x_y = True

            elif move_tried == False:
                gameboard.hidden_board[y][x] = "O"
                gameboard.MissesAndHits += [[y, x]]
                correct_x_y = True

            else:
                print("you already tried that attack")
                move_tried = False
                

    print("player attack")
    print_board(gameboard.hidden_board)
    time.sleep(2)


def print_board(board): #prints the game board
    header = len(board[0]*2)-1
    x = "" 
    for i in range(header):
         x += "-"

    print(x)

    for i in board:
        print (' '.join(str(n) for n in i))

    print(x)

game_manager()



