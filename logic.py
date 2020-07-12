import math
import os

class Piece:
    piece_list = []
    board = [['........'] * 8]
    player_1_tool_list = ['R', 'N', 'B', 'K', 'Q', 'P']
    player_2_tool_list = ['r', 'n', 'b', 'k', 'q', 'p']
    player_1_threatens = []  # COOR's Player 1 threatns
    player_2_threatens = []  # COOR's Player 2 threatns

    def __init__(self, symbol, player, row, column):
        self.symbol = symbol
        self.player = player
        self.row = row
        self.column = column
        self.status = True
        self.count_moves_done = 0
        self.movement_type = []
        if symbol in ('R', 'r', 'Q', 'q'):
            self.movement_type.append('forward')
        if symbol in ('B', 'b', 'Q', 'q'):
            self.movement_type.append('across')
        if symbol in ('N', 'n'):
            self.movement_type.append('knight')
        if symbol in ('K', 'k'):
            self.movement_type.append('king')
        if symbol in ('P', 'p'):
            self.movement_type.append('pawn')
        self.current_potential_moves = []
        Piece.piece_list.append(self)

    def set_board(self):
        board = []
        Piece.player_1_threatens = []
        Piece.player_2_threatens = []
        for row in range(0, 8):
            temp = []
            for col in range(0, 8):
                for element in Piece.piece_list:
                    was_assigned = False
                    if element.row == row and element.column == col and element.status == True:
                        temp.append(element)
                        was_assigned = True
                        break
                if was_assigned == False:
                    temp.append('.')
            board.append(temp)
        Piece.board = board

    def print_board(self, turn):
        if turn == '1':
            if king1.check_if_king_check() == True:
                pass

            for row_index in range(0, 8):

                for col in Piece.board[7 - row_index]:
                    if col == '.':
                        pass
                    else:
                        pass

            for i in range(0, 8):
                pass
            pass
        elif turn == '2':
            if king2.check_if_king_check() == True:
                pass

            for row_index in range(0, 8):
                for col in Piece.board[row_index]:
                    if col == '.':
                        pass
                    else:
                        pass


            for i in range(0, 8):
                pass


    def append_potential_move_to_all_relevant_lists(self, potential_row, potential_col):
        self.current_potential_moves.append([potential_row, potential_col])
        if self.player == '1':
            Piece.player_1_threatens.append([potential_row, potential_col])
        else:
            Piece.player_2_threatens.append([potential_row, potential_col])

    def check_if_potential_move_is_valid(self, potential_row, potential_col):
        # If the move is not in range return False
        if potential_row not in range(0, 8) or potential_col not in range(0, 8):
            return False

        # if the move is to an empty Space return True
        elif Piece.board[potential_row][potential_col] == '.':
            return True

        # If the move is blocked by another piece of player return False
        elif Piece.board[potential_row][potential_col].player == self.player:
            return False

        # If the king is in check and the move does not prevent it return False

        # Else return True
        else:
            return True

    def add_potential_moves_for_forward_and_across(self, row_add, col_add):
        potential_row = self.row + row_add
        potential_col = self.column + col_add
        while self.check_if_potential_move_is_valid(potential_row, potential_col) == True:
            self.append_potential_move_to_all_relevant_lists(potential_row, potential_col)
            if Piece.board[potential_row][potential_col] != '.':
                if Piece.board[potential_row][potential_col].player != self.player:
                    break
            potential_row = potential_row + row_add
            potential_col = potential_col + col_add

    def add_potential_moves_for_knight(self, row_add, col_add):
        potential_row = self.row + row_add
        potential_col = self.column + col_add
        if self.check_if_potential_move_is_valid(potential_row, potential_col) == True:
            self.append_potential_move_to_all_relevant_lists(potential_row, potential_col)

    def check_if_pawn_can_eat(self, row_add, col_add):
        if (self.row + row_add) in range(0, 8) and (self.column + col_add) in range(0, 8):
            if Piece.board[self.row + row_add][self.column + col_add] != '.':
                if Piece.board[self.row + row_add][self.column + col_add].player != self.player:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def pawn_at_end_of_course(self, turn):
        self.movement_type = []
        inp = input("what piece do you want the pawn? (n,q,r,b): ")
        while inp not in ('n', 'q', 'r', 'b'):
            inp = input("INVALID INPUT - what piece do you want the pawn? (n,q,r,b): ")
        if inp == 'n' and turn == '1':
            self.symbol = 'N'
            self.movement_type.append('knight')
            self.player = '1'
        elif inp == 'n' and turn == '2':
            self.symbol = 'n'
            self.movement_type.append('knight')
            self.player = '2'
        elif inp == 'q' and turn == '1':
            self.symbol = 'Q'
            self.movement_type.append('forward')
            self.movement_type.append('across')
            self.player = '1'
        elif inp == 'q' and turn == '2':
            self.symbol = 'q'
            self.movement_type.append('forward')
            self.movement_type.append('across')
            self.player = '2'
        elif inp == 'r' and turn == '1':
            self.symbol = 'R'
            self.movement_type.append('forward')
            self.player = '1'
        elif inp == 'r' and turn == '2':
            self.symbol = 'r'
            self.movement_type.append('forward')
            self.player = '2'
        elif inp == 'b' and turn == '1':
            self.symbol = 'B'
            self.movement_type.append('across')
            self.player = '1'
        elif inp == 'b' and turn == '2':
            self.symbol = 'b'
            self.movement_type.append('across')
            self.player = '2'

    def add_potential_moves_for_pawn(self, turn):
        if self.player == '1':
            potential_row = self.row + 1
        else:
            potential_row = self.row - 1

        # Check if its the pawn's first move:
        if self.row == 1 and self.player == '1' and Piece.check_if_potential_move_is_valid(self, 2, self.column) == True:
            Piece.append_potential_move_to_all_relevant_lists(self, 2, self.column)
            if self.check_if_potential_move_is_valid(3, self.column) == True and Piece.board[3][self.column] == '.':
                self.append_potential_move_to_all_relevant_lists(3, self.column)

        # Check if it's the pawn's first move:
        elif self.row == 6 and self.player == '2' and Piece.check_if_potential_move_is_valid(self, 5, self.column) == True:
            self.append_potential_move_to_all_relevant_lists(5, self.column)
            if self.check_if_potential_move_is_valid(4, self.column) == True and Piece.board[4][self.column] == '.':
                self.append_potential_move_to_all_relevant_lists(4, self.column)

        elif self.check_if_potential_move_is_valid(potential_row, self.column) == True:
            if Piece.board[potential_row][self.column] == '.':
                self.append_potential_move_to_all_relevant_lists(potential_row, self.column)
        # Chek if pawn can eat:
        if self.player == '1':
            row_add = 1
            col_add = 1
            if self.check_if_pawn_can_eat(row_add, col_add) == True:
                self.append_potential_move_to_all_relevant_lists(self.row + row_add, self.column + col_add)
            row_add = 1
            col_add = -1
            if self.check_if_pawn_can_eat(row_add, col_add) == True:
                self.append_potential_move_to_all_relevant_lists(self.row + row_add, self.column + col_add)
        elif self.player == '2':
            row_add = -1
            col_add = 1
            if self.check_if_pawn_can_eat(row_add, col_add) == True:
                self.append_potential_move_to_all_relevant_lists(self.row + row_add, self.column + col_add)
            row_add = -1
            col_add = -1
            if self.check_if_pawn_can_eat(row_add, col_add) == True:
                self.append_potential_move_to_all_relevant_lists(self.row + row_add, self.column + col_add)

        # Check if end of pawn's course:
        if self.row == 7 and self.player == '1':
            self.pawn_at_end_of_course(turn)

        elif self.row == 0 and self.player == '2':
            self.pawn_at_end_of_course(turn)

    def add_potential_moves_for_king(self, row_add, col_add):
        potential_row = self.row + row_add
        potential_col = self.column + col_add
        if self.check_if_potential_move_is_valid(potential_row, potential_col) == True:
            if self.player == '1' and [potential_row, potential_col] not in Piece.player_2_threatens:
                self.append_potential_move_to_all_relevant_lists(potential_row, potential_col)
            if self.player == '2' and [potential_row, potential_col] not in Piece.player_1_threatens:
                self.append_potential_move_to_all_relevant_lists(potential_row, potential_col)

    def add_castling(self, rook):
        if self.count_moves_done == 0 and rook.count_moves_done == 0:
            if rook.column == 7 and self.player == '1':
                if Piece.board[0][5] == '.' and Piece.board[0][6] == '.':
                    if Piece.board[0][5] not in Piece.player_2_threatens and Piece.board[0][
                        6] not in Piece.player_2_threatens:
                        self.current_potential_moves.append([0, 6])
        if self.count_moves_done == 0 and rook.count_moves_done == 0:
            if rook.column == 0 and self.player == '1':
                if Piece.board[0][1] == '.' and Piece.board[0][2] == '.' and Piece.board[0][3] == '.':
                    if Piece.board[0][1] not in Piece.player_2_threatens and Piece.board[0][
                        2] not in Piece.player_2_threatens and Piece.board[0][3] not in Piece.player_2_threatens:
                        self.current_potential_moves.append([0, 1])
        if self.count_moves_done == 0 and rook.count_moves_done == 0:
            if rook.column == 7 and self.player == '2':
                if Piece.board[7][5] == '.' and Piece.board[7][6] == '.':
                    if Piece.board[7][5] not in Piece.player_2_threatens and Piece.board[7][
                        6] not in Piece.player_2_threatens:
                        self.current_potential_moves.append([7, 6])
        if self.count_moves_done == 0 and rook.count_moves_done == 0:
            if rook.column == 0 and self.player == '2':
                if Piece.board[7][1] == '.' and Piece.board[7][2] == '.' and Piece.board[7][3] == '.':
                    if Piece.board[7][1] not in Piece.player_2_threatens and Piece.board[7][
                        2] not in Piece.player_2_threatens and Piece.board[7][3] not in Piece.player_2_threatens:
                        self.current_potential_moves.append([7, 1])

    def change_current_potential_moves(self, turn):
        self.current_potential_moves = []
        if 'forward' in self.movement_type:
            Piece.add_potential_moves_for_forward_and_across(self, 1, 0)  # up
            Piece.add_potential_moves_for_forward_and_across(self, -1, 0)  # down
            Piece.add_potential_moves_for_forward_and_across(self, 0, 1)  # right
            Piece.add_potential_moves_for_forward_and_across(self, 0, -1)  # left
        if 'across' in self.movement_type:
            Piece.add_potential_moves_for_forward_and_across(self, 1, 1)  # up-right
            Piece.add_potential_moves_for_forward_and_across(self, 1, -1)  # up-left
            Piece.add_potential_moves_for_forward_and_across(self, -1, 1)  # down-right
            Piece.add_potential_moves_for_forward_and_across(self, -1, -1)  # down-left
        if 'knight' in self.movement_type:
            Piece.add_potential_moves_for_knight(self, 2, 1)  # up-up-right
            Piece.add_potential_moves_for_knight(self, 2, -1)  # up-up-left
            Piece.add_potential_moves_for_knight(self, -2, 1)  # down-down-right
            Piece.add_potential_moves_for_knight(self, -2, -1)  # down-down-left
            Piece.add_potential_moves_for_knight(self, 1, 2)  # up-right-right
            Piece.add_potential_moves_for_knight(self, 1, -2)  # up-left-left
            Piece.add_potential_moves_for_knight(self, -1, 2)  # down-right-right
            Piece.add_potential_moves_for_knight(self, -1, -2)  # down-left-left
        if 'pawn' in self.movement_type:
            Piece.add_potential_moves_for_pawn(self, turn)
        if 'king' in self.movement_type:
            Piece.add_potential_moves_for_king(self, 1, 0)  # up
            Piece.add_potential_moves_for_king(self, -1, 0)  # down
            Piece.add_potential_moves_for_king(self, 0, 1)  # right
            Piece.add_potential_moves_for_king(self, 0, -1)  # left
            Piece.add_potential_moves_for_king(self, 1, 1)  # up-right
            Piece.add_potential_moves_for_king(self, 1, -1)  # up-left
            Piece.add_potential_moves_for_king(self, -1, 1)  # down-right
            Piece.add_potential_moves_for_king(self, -1, -1)  # down-left
            Piece.add_castling(self, rook11)
            Piece.add_castling(self, rook12)
            Piece.add_castling(self, rook21)
            Piece.add_castling(self, rook22)

    def check_if_king_can_be_saved(self):
        for piece in Piece.piece_list:
            if self.player == piece.player and self.symbol != piece.symbol:
                original_row = piece.row
                original_col = piece.column
                original_potential_move = piece.current_potential_moves
                for potential_move in original_potential_move:
                    piece.row = potential_move[0]
                    piece.column = potential_move[1]
                    Piece.set_board(Piece)
                    Piece.set_all_current_potential_moves(Piece, turn)
                    if self.player == '1':
                        if (len(king1.current_potential_moves) > 0) or (
                                [king1.row, king1.column] not in Piece.player_2_threatens):
                            piece.row = original_row
                            piece.column = original_col
                            Piece.set_board(Piece)
                            Piece.set_all_current_potential_moves(Piece, turn)
                            return True
                    elif self.player == '2':
                        if (len(king2.current_potential_moves) > 0) or (
                                [king2.row, king2.column] not in Piece.player_1_threatens):
                            piece.row = original_row
                            piece.column = original_col
                            Piece.set_board(Piece)
                            Piece.set_all_current_potential_moves(Piece, turn)
                            return True

                piece.row = original_row
                piece.column = original_col
                Piece.set_board(Piece)
                Piece.set_all_current_potential_moves(Piece, turn)
        return False

    def check_if_king_checkmate(self):
        if self.player == '1' and len(self.current_potential_moves) == 0 and [self.row,
                                                                              self.column] in Piece.player_2_threatens and self.check_if_king_can_be_saved() == False:

            return True

        elif self.player == '2' and len(self.current_potential_moves) == 0 and [self.row,
                                                                                self.column] in Piece.player_1_threatens and self.check_if_king_can_be_saved() == False:

            return True

        else:
            return False

    def check_if_king_check(self):
        Piece.set_all_current_potential_moves(Piece, turn)
        if self.player == '1' and [self.row, self.column] in Piece.player_2_threatens:
            return True
        elif self.player == '2' and [self.row, self.column] in Piece.player_1_threatens:
            return True
        else:
            return False

    def reset_threaten_list(self):
        Piece.player_1_threatens = []
        Piece.player_2_threatens = []

    def set_all_current_potential_moves(self, turn):
        Piece.reset_threaten_list(Piece)
        for piece in Piece.piece_list:
            if piece.status == True:
                piece.change_current_potential_moves(turn)
            else:
                piece.current_potential_moves = []

def check_if_inp_is_valid(inp, turn):
    if len(inp) < 2:
        return False
    temp_row = inp[0]
    temp_col = inp[1]
    range_str = ['0', '1', '2', '3', '4', '5', '6', '7']
    if (temp_row in range_str) and (temp_col in range_str) and (len(inp) == 2):
        if Piece.board[int(temp_row)][int(temp_col)] != '.':
            if Piece.board[int(temp_row)][int(temp_col)].player == turn:
                if len(Piece.board[int(temp_row)][int(temp_col)].current_potential_moves) > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def check_if_output_is_valid(outp, chosen_piece):
    if len(outp) == 2 and outp[0] in ['0', '1', '2', '3', '4', '5', '6', '7'] and outp[1] in ['0', '1', '2', '3', '4',
                                                                                              '5', '6', '7']:
        if [int(outp[0]), int(outp[1])] in chosen_piece.current_potential_moves:
            return True
        else:
            return False
    else:
        return False


def get_input(turn):
    inp = input("What to move[row,col]:")
    # chosen_piece = check_if_inp_is_valid(inp, turn)
    while check_if_inp_is_valid(inp, turn) == False:
        inp = input("Enter valid COOR[row,col]:")
    return inp


def get_output(chosen_piece):
    outp = input("Where to move[row,col]; x for new input:")
    if outp == 'x':
        return outp
    while check_if_output_is_valid(outp, chosen_piece) == False:
        outp = input("Enter valid COOR[row,col]:")
    return outp


def turn_still_in_check(chosen_piece, previous_row, previous_col, turn):
    # Set piece back to its original row and col
    chosen_piece.row = previous_row
    chosen_piece.column = previous_col

    # Set board to the way it was in the beginning of the turn and start turn again
    Piece.set_board(Piece)
    Piece.set_all_current_potential_moves(Piece, turn)
    os.system('cls')
    Piece.print_board(Piece, turn)
    inp = get_input(turn)
    chosen_piece = Piece.board[int(inp[0])][int(inp[1])]

    outp = get_output(chosen_piece)
    if Piece.board[int(outp[0])][int(outp[1])] != '.':
        Piece.board[int(outp[0])][int(outp[1])].status = False
    previous_row = chosen_piece.row
    previous_col = chosen_piece.column
    chosen_piece.row = int(outp[0])
    chosen_piece.column = int(outp[1])
    Piece.set_board(Piece)
    Piece.set_all_current_potential_moves(Piece, turn)

def is_check(turn):
    # If the king is checked - Check if the current move is legal; i.e. if king is still in check after suggested move
    if turn == '1' and king1.check_if_king_check() == True:
        #turn_still_in_check(chosen_piece, previous_row, previous_col, turn)
        return True
    elif turn == '2' and king2.check_if_king_check() == True:
        #turn_still_in_check(chosen_piece, previous_row, previous_col, turn)
        return True
    else:
        return False

def turn_function(turn, inp, outp):
    # Set Boards and all current potential moves according to new board
    Piece.set_board(Piece)
    Piece.set_all_current_potential_moves(Piece, turn)
    # Clear screen
    os.system('cls')

    Piece.print_board(Piece, turn)
    chosen_piece = Piece.board[int(inp[0])][int(inp[1])]


    chosen_piece = Piece.board[int(inp[0])][int(inp[1])]
    if Piece.board[int(outp[0])][int(outp[1])] != '.':
        Piece.board[int(outp[0])][int(outp[1])].status = False

    # Store old row and col in case move is not legal
    previous_row = chosen_piece.row
    previous_col = chosen_piece.column

    # Set the new row and col for the chosen piece
    chosen_piece.row = int(outp[0])
    chosen_piece.column = int(outp[1])
    Piece.set_board(Piece)
    Piece.set_all_current_potential_moves(Piece, turn)

    # Define Castling:
    if 'king' in chosen_piece.movement_type and abs(previous_col - int(outp[1])) in [2, 3]:
        if chosen_piece.player == '1' and outp[1] == '1':
            rook11.column = 2
            Piece.set_board(Piece)
            Piece.set_all_current_potential_moves(Piece, turn)
        if chosen_piece.player == '1' and outp[1] == '6':
            rook12.column = 5
            Piece.set_board(Piece)
            Piece.set_all_current_potential_moves(Piece, turn)
        if chosen_piece.player == '2' and outp[1] == '1':
            rook21.column = 2
            Piece.set_board(Piece)
            Piece.set_all_current_potential_moves(Piece, turn)
        if chosen_piece.player == '2' and outp[1] == '6':
            rook22.column = 5
            Piece.set_board(Piece)
            Piece.set_all_current_potential_moves(Piece, turn)
    chosen_piece.count_moves_done = chosen_piece.count_moves_done + 1

def change_turn(turn):
    if turn == '2':
        turn = '1'
    elif turn == '1':
        turn = '2'
    return turn

def game_turn(turn, input, output):
    turn_function(turn, input, output)
    # turn = change_turn(turn)

    if king1.check_if_king_checkmate() == True or king2.check_if_king_checkmate() == True:
        Piece.set_board(Piece)
        Piece.set_all_current_potential_moves(Piece, turn)
        Piece.print_board(Piece, turn)
        return True
    else:
        return False

# Create all pieces and initialize their positions: Symbol, Player, Row, Col
rook11 = Piece('R', '1', 0, 0)
knight11 = Piece('N', '1', 0, 1)
bishop11 = Piece('B', '1', 0, 2)
queen1 = Piece('Q', '1', 0, 3)
king1 = Piece('K', '1', 0, 4) #4
bishop12 = Piece('B', '1', 0, 5)
knight12 = Piece('N', '1', 0, 6)
rook12 = Piece('R', '1', 0, 7)
pawn11 = Piece('P', '1', 1, 0)
pawn12 = Piece('P', '1', 1, 1)
pawn13 = Piece('P', '1', 1, 2)
pawn14 = Piece('P', '1', 1, 3)
pawn15 = Piece('P', '1', 1, 4)
pawn16 = Piece('P', '1', 1, 5)
pawn17 = Piece('P', '1', 1, 6)
pawn18 = Piece('P', '1', 1, 7)
rook21 = Piece('r', '2', 7, 0)
knight21 = Piece('n', '2', 7, 1)
bishop21 = Piece('b', '2', 7, 2)
queen2 = Piece('q', '2', 7, 3)
king2 = Piece('k', '2', 7, 4) #20
bishop22 = Piece('b', '2', 7, 5)
knight22 = Piece('n', '2', 7, 6)
rook22 = Piece('r', '2', 7, 7)
pawn21 = Piece('p', '2', 6, 0)
pawn22 = Piece('p', '2', 6, 1)
pawn23 = Piece('p', '2', 6, 2)
pawn24 = Piece('p', '2', 6, 3)
pawn25 = Piece('p', '2', 6, 4)
pawn26 = Piece('p', '2', 6, 5)
pawn27 = Piece('p', '2', 6, 6)
pawn28 = Piece('p', '2', 6, 7)
turn = '1'
Piece.set_board(Piece)
Piece.set_all_current_potential_moves(Piece, turn)

