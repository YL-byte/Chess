from tkinter import *
import logic

class Tile:
    def __init__(self, master, row, column):
        self.row = row
        self.column = column
        self.tile_text = ''
        self.label = Label(master, height=int(Tile.rect_length / 2), width=Tile.rect_length, borderwidth=2,relief="solid")
        self.label.grid(row=row, column=column)
        self.label.bind('<Button-1>', self.press_tile)
        Tile.tile_list.append(self)

    is_game_active = True
    rect_length = 6
    clicked_piece = None
    chosen_tile = None
    tile_list = []
    inp = ['', ''] #this variable will store the coor of the piece the player wants to move

    def set_board(self):
        Tile.change_board_direction(Tile)
        Tile.set_tile_colors(Tile)
        for tile in Tile.tile_list:
            tile.set_tile()

    def change_board_direction(self):
        #Flip the board by reversing the tiles per turn
        for tile in Tile.tile_list:
            tile.row = 7 - tile.row

    def press_tile (self, event):
        #If the game is over there are no more moves to be made
        if Tile.is_game_active == False:
            return False

        #If the tile is green it means the player chose a piece and made a valid move
        if self.label['background'] == 'green':
            outp = [str(self.row),str(self.column)]
            is_game_over = logic.game_turn(logic.turn, Tile.inp, outp) #input and output
            logic.turn = logic.change_turn(logic.turn)
            self.set_tile()
            if self.match_piece_to_tile() != None and self.match_piece_to_tile().player == logic.turn:
                #Means that the piece in that tile is eaten
                self.match_piece_to_tile().status = False

            Tile.chosen_tile.set_tile()
            Tile.set_board(Tile)
            Tile.clicked_piece = None
            if is_game_over == True:
                #Block users from making further moves
                Tile.is_game_active = False
                notification = Tk()
                if logic.turn == '1':
                    finish_label = Label(notification, text = 'Player 1 Won')
                else:
                    finish_label = Label(notification, text='Player 2 Won')
                finish_label.pack()
                notification.mainloop()

        #Check if the player clicked an empty tile
        if self.match_piece_to_tile() == None: #Player chose an empty tile
            Tile.chosen_tile = self
            Tile.clicked_piece = self.match_piece_to_tile()
            self.highlight_possible_moves()

        #If player chose the opponents active piece
        elif self.match_piece_to_tile().player == logic.turn and self.match_piece_to_tile().status == True:
            Tile.inp[0] = str(self.row)
            Tile.inp[1] = str(self.column)
            Tile.chosen_tile.set_tile()
            Tile.chosen_tile = self
            Tile.clicked_piece = self.match_piece_to_tile()
            self.highlight_possible_moves()

    def set_tile(self):
        current_piece = self.match_piece_to_tile()
        if current_piece == None:
            self.label['text'] = ''
        else:
            self.label['text'] = current_piece.symbol
            if current_piece.player == '1':
                self.label['fg'] = 'white'
            else:
                self.label['fg'] = 'black'

    def match_piece_to_tile(self):
        current_piece = None
        for piece in logic.Piece.piece_list:
            if (self.row == piece.row) and (self.column == piece.column) and piece.status == True:
                current_piece = piece
                break
        return current_piece
    def find_piece_according_to_symbol(self, search_symbol):
        for piece in logic.Piece.piece_list:
            if piece.symbol == search_symbol:
                return piece

    def set_tile_colors(self):
        king1 = Tile.find_piece_according_to_symbol(Tile, 'K')
        king2 = Tile.find_piece_according_to_symbol(Tile, 'k')

        #Highlight if either king is in check
        for tile in Tile.tile_list:
            if [tile.row, tile.column] == [king1.row, king1.column] and [king1.row, king1.column] in logic.Piece.player_2_threatens:
                tile.label['background'] = 'orange'

            elif [tile.row, tile.column] == [king2.row, king2.column] and [king2.row, king2.column] in logic.Piece.player_1_threatens:
                tile.label['background'] = 'orange'

            elif (tile.row + tile.column) % 2 == 0:
                tile.label['background'] = 'sienna4'

            else:
                tile.label['background'] = 'sienna3'

    def highlight_possible_moves(self):
        current_piece = self.match_piece_to_tile()
        #Reset Background of each tile
        Tile.set_tile_colors(Tile)

        if current_piece != None:
            #for move in possible
            for move in current_piece.current_potential_moves:
                move_row = move[0]
                move_column = move[1]
                for tile in Tile.tile_list:
                    if tile.row == move_row and tile.column == move_column:
                        #Store Current Data to return to original board
                        original_board = logic.Piece.board
                        orig_row = current_piece.row
                        orig_column = current_piece.column

                        #Set is if move made to check if Check
                        current_piece.row = move_row
                        current_piece.column = move_column

                        #If there is a piece in potential spot - kill it and then restore it
                        is_there_a_piece = False
                        if logic.Piece.board[move_row][move_column] != '.':
                            dead_piece = logic.Piece.board[move_row][move_column]
                            dead_piece.status = False
                            is_there_a_piece = True

                        logic.Piece.set_board(logic.Piece)
                        logic.Piece.set_all_current_potential_moves(logic.Piece, logic.turn)

                        #If the king is not checked - Move is valid
                        if logic.is_check(logic.turn) == False:
                            tile.label['background'] = 'green'

                        #Restore Old Data
                        logic.Piece.board = original_board
                        current_piece.row = orig_row
                        current_piece.column = orig_column
                        if is_there_a_piece == True:
                            dead_piece.status = True
                        logic.Piece.set_board(logic.Piece)
                        logic.Piece.set_all_current_potential_moves(logic.Piece, logic.turn)

root = Tk()
board = []

#Createa Board with Empty Symbols
for row in range(0, 8):
    row = []
    for column in range (0, 8):
        row.append('.')
    board.append(row)
    row = []

#Tile Parameter
x = Tile.rect_length
y = Tile.rect_length

#Create Tiles
for row in range (0, 8):
    for column in range (0,8):
        Tile(root, row, column)

Tile.chosen_tile = Tile.tile_list[0]
Tile.set_board(Tile)
root.mainloop()