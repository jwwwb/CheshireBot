# -*- coding: utf-8 -*-

'''
#to-do: promotion
        try on different architecture
'''


import numpy as np
import pyopencl as cl
import time

# consts
LOC_SIZE = 128
BOARD_SIZE = 128
MOVES_SIZE = 128
PIECE_SIZE = 16
PIECE_OFFSET = 8
NUM_FLAGS = 4
CHECK_OFFSET = 120
MATE_OFFSET = 121
COLOR_OFFSET = 122
PASSANT_OFFSET = 123


class ChessBoardCL:
    def __init__(self, state=None):
        if state:
            self.state = state
        else:
            self.state = np.asarray([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                     -1,  5,  3,  4,  6,  7,  4,  3,  5, -1,
                                     -1,  2,  2,  2,  2,  2,  2,  2,  2, -1,
                                     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1,
                                     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1,
                                     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1,
                                     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1,
                                     -1, -2, -2, -2, -2, -2, -2, -2, -2, -1,
                                     -1, -5, -3, -4, -6, -7, -4, -3, -5, -1,
                                     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                                     0, 0, 1, 0, 0, 0, 0, 0], dtype=np.int32)  # default board, last row is flags:
            # check, mate, turn color, en passant field, white a castle, h castle, black a castle, h castle ruled out

    def output(self):
        symcon = u' x♙♘♗♖♕♔;:♚♛♜♝♞♟x'
        print('   _______________________________')
        for rank in range(8, 0, -1):
            if rank % 2:
                line = str(rank)+' |['
            else:
                line = str(rank)+' | '
            for file_ in range(1, 9):
                field = self.state[10+rank*10+file_]
                if (rank+file_) % 2:
                    if file_ < 8:
                        line += symcon[field]+' |['
                    else:
                        line += symcon[field]+' | '
                else:
                    line += symcon[field]+']| '
            print(line)
        print('   ‾A‾‾‾B‾‾‾C‾‾‾D‾‾‾E‾‾‾F‾‾‾G‾‾‾H‾')

    def get_all_legal_moves(self, color='white'):
        pass

    def set_fen_state(self, fen):
        print fen
        int_piece = {'K': 7, 'Q': 6, 'R': 5, 'B': 4, 'N': 3, 'P': 2, 'k': -7, 'q': -6, 'r': -5, 'b': -4, 'n': -3, 'p': -2}
        board, flags = fen.split(' ', 1)
        board = board.split('/')
        rank = 8
        for row in board:
            file_ = 1
            for field in row:
                if field.isdigit():
                    self.state[10+10*rank+file_:10+10*rank+file_+int(field)] = 0
                    file_ += int(field)
                else:
                    self.state[10+10*rank+file_] = int_piece[field]
                    # print('setting state[{}] to {}.'.format(10+10*rank+file_), int_piece[field])
                    file_ += 1
            rank -= 1
        flags = flags.split(' ')
        self.state[COLOR_OFFSET] = {'w': 1, 'b': -1}[flags[0]]
        self.state[BOARD_SIZE-NUM_FLAGS+0] = 0 if 'K' in flags[1] else 1
        self.state[BOARD_SIZE-NUM_FLAGS+1] = 0 if 'Q' in flags[1] else 1
        self.state[BOARD_SIZE-NUM_FLAGS+2] = 0 if 'k' in flags[1] else 1
        self.state[BOARD_SIZE-NUM_FLAGS+3] = 0 if 'q' in flags[1] else 1
        if flags[2] != '-':
            self.state[ord(flags[2][0])-86+10*int(flags[2][1])] = 8 if flags[2][1] == '3' else -8

    def get_fen_state(self):
        fen_state = ''
        chr_piece = '  PNBRQKkqrbnp '
        for rank in range(90, 10, -10):
            empty_counter = 0
            for file_ in range(1, 9, 1):    # loop from 1 to 8
                if self.state[rank+file_] in (0, 8, -8):    # if nothing there simply increment
                    empty_counter += 1
                else:                       # if something is there
                    if empty_counter:
                        fen_state += str(empty_counter)     # first dump the counter if there is one
                        fen_state += chr_piece[self.state[rank+file_]]      # then print the item
                    else:
                        fen_state += chr_piece[self.state[rank+file_]]      # then print the item
                    empty_counter = 0
            if empty_counter > 0:           # if there's something in the counter at the end
                fen_state += str(empty_counter)             # dump it to the string
            if rank > 20:
                fen_state += '/'
        fen_state += ' '
        fen_state += 'w ' if self.state[COLOR_OFFSET] else 'b '
        if self.state[BOARD_SIZE-NUM_FLAGS+1] == 0:
            fen_state += 'K'
        if self.state[BOARD_SIZE-NUM_FLAGS+0] == 0:
            fen_state += 'Q'
        if self.state[BOARD_SIZE-NUM_FLAGS+3] == 0:
            fen_state += 'k'
        if self.state[BOARD_SIZE-NUM_FLAGS+2] == 0:
            fen_state += 'q'
        if fen_state[-1] == ' ':
            fen_state += '-'
        fen_state += ' '
        if self.state[PASSANT_OFFSET]:
            fen_state += string_loc(self.state[PASSANT_OFFSET])
        else:
            fen_state += '-'
        return fen_state


class MoveArray:
    def __init__(self, move_array):
        self.move_array = move_array

    def convert(self):
        start_array = (self.move_array//LOC_SIZE) % LOC_SIZE
        goal_array = self.move_array % LOC_SIZE
        out = np.array([start_array, goal_array])
        return out.transpose()

    def convert2(self):
        start_array = (self.move_array//LOC_SIZE) % LOC_SIZE
        goal_array = self.move_array % LOC_SIZE
        return start_array, goal_array


class PerfTester:
    def __init__(self):
        self.game = ChessBoardCL()
        self.colors = ['none', 'white', 'black']
        # pre initialized just to make pycharm's pep8 checker happy:
        self.depth = 0
        self.depth_limit = 1
        self.perft_res = 0
        self.store_final = False
        # import the opencl code
        self.context = cl.create_some_context()
        self.queue = cl.CommandQueue(self.context)
        f = open('opencl.cl', 'r')
        self.program = cl.Program(self.context, ''.join(f.readlines())).build()

    def apply_move(self, move):
        moves = np.zeros(MOVES_SIZE, dtype=np.int32)
        moves[0] = move
        new_states = self.apply_moves(self.game.state, moves)
        self.game.state = new_states[0:BOARD_SIZE]

    def get_legal_moves(self, states=None):
        if states is None:
            states = self.game.state
        mf = cl.mem_flags
        local_states = states.copy()
        counter = np.arange(len(states)//BOARD_SIZE, dtype=np.int32)
        moves = np.empty_like(local_states)
        count_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=counter)
        state_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=local_states)
        output_buffer = cl.Buffer(self.context, mf.WRITE_ONLY, local_states.nbytes)
        self.program.find_moves(self.queue, counter.shape, None, count_buffer, state_buffer, output_buffer)
        cl.enqueue_copy(self.queue, moves, output_buffer)
        return moves

    def apply_moves(self, states, moves):
        mf = cl.mem_flags
        local_states = states.copy()
        counter = np.arange(len(states)//BOARD_SIZE, dtype=np.int32)
        moves = moves.copy()
        count_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=counter)
        state_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=local_states)
        moves_buffer = cl.Buffer(self.context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=moves)
        new_state_buffer = cl.Buffer(self.context, mf.WRITE_ONLY, BOARD_SIZE*states.nbytes)
        self.program.apply_moves(self.queue, counter.shape, None, count_buffer, state_buffer, moves_buffer, new_state_buffer)
        new_states = np.zeros(len(moves)*BOARD_SIZE, dtype=np.int32)
        cl.enqueue_copy(self.queue, new_states, new_state_buffer)
        return new_states

    def split_perft(self, depth, state=None):
        if state is None:
            state = self.game.state
        raw_moves = self.get_legal_moves(state)
        raw_new_states = self.apply_moves(state, raw_moves)
        raw_new_states = raw_new_states.reshape(len(raw_new_states)//BOARD_SIZE, BOARD_SIZE)
        moves = raw_moves[raw_moves != 0]
        new_states = raw_new_states[raw_moves != 0]
        total_per = 0
        for i in range(len(moves)):
            per = self.perft(depth-1, new_states[i])
            total_per += per
            print '{}: {} moves'.format(string_move(moves[i]), per)
        print 'Total: {} moves'.format(total_per)

    def deep_split_perft(self, depth, state=None):
        if state is None:
            state = self.game.state
        raw_moves = self.get_legal_moves(state)
        raw_new_states = self.apply_moves(state, raw_moves)
        raw_new_states = raw_new_states.reshape(len(raw_new_states)//BOARD_SIZE, BOARD_SIZE)
        moves = raw_moves[raw_moves != 0]
        new_states = raw_new_states[raw_moves != 0]
        total_per = 0
        for i in range(len(moves)):
            per = self.deep_perft(depth-6, 5, new_states[i])
            total_per += per
            print '{}: {} moves'.format(string_move(moves[i]), per)
        print 'Total: {} moves'.format(total_per)

    def deep_perft(self, depth1, depth2, state=None):
        self.store_final = True
        self.perft(depth1, state)
        res = 0
        # print(len(self.final_states))
        for substate in self.final_states:
            res += self.perft(depth2, substate)
        return res

    def perft(self, depth, state=None):
        if state is None:
            state = self.game.state
        self.depth = 1
        self.depth_limit = depth
        self.recurse(state)
        return self.perft_res

    def recurse(self, states):
        self.depth += 1
        moves = self.get_legal_moves(states)
        if self.depth <= self.depth_limit:
            new_states = self.apply_moves(states, moves)
            reshape = new_states.reshape(len(new_states)//BOARD_SIZE, BOARD_SIZE)
            pruned = reshape[moves != 0]
            self.recurse(pruned.flatten())
        else:
            self.perft_res = len(moves[moves != 0])
            if self.store_final:
                new_states = self.apply_moves(states, moves)
                reshape = new_states.reshape(len(new_states)//BOARD_SIZE, BOARD_SIZE)
                self.final_states = reshape[moves != 0]
                # print 'Final states array size: {}'.format(self.final_states.nbytes)
                self.store_final = False


'''
main function:
'''


def main3():
    perft = PerfTester()
    # perft.deep_split_perft(7)

    print('Applying move G1-F3 and repeating')
    perft.apply_move(int_move('G1-F3'))
    perft.split_perft(6)


def main():
    import os
    os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
    os.environ['PYOPENCL_CTX'] = '0:0'
    perft = PerfTester()
    for i in range(1, 6):
        print('Perft for depth={} is: {}'.format(i, perft.perft(i)))
    i = 1
    j = 5
    print('Deep perft for depth={} is: {}'.format(i+j, perft.deep_perft(i, j)))
    i = 2
    print('Deep perft for depth={} is: {}'.format(i+j, perft.deep_perft(i, j)))


def main1():
    perft = PerfTester()
    perft.split_perft(4)

    print('Applying move B1-C3 and repeating')
    perft.apply_move(int_move('B1-C3'))
    perft.split_perft(3)

    print('Applying move E7-E5 and repeating')
    perft.apply_move(int_move('E7-E5'))
    perft.split_perft(2)

    print('Applying move C3-D5 and repeating')
    perft.apply_move(int_move('C3-D5'))
    temp = perft.get_legal_moves()
    moves = temp[temp != 0]
    print len(moves)
    output_moves(moves)
    print 'If E8-E7 is in here, that means the king is moving into the knights check. Fix it!'


def main4():
    board = ChessBoardCL()
    board.output()
    # board.set_fen_state('3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1')
    board.set_fen_state('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -')
    board.output()


'''
helper functions:
'''


def output_moves(moves):
    out = []
    pro = '   NBRQ'
    for move in moves:
        if move > LOC_SIZE * LOC_SIZE:
            promotion = move // (LOC_SIZE * LOC_SIZE)
            move %= (LOC_SIZE * LOC_SIZE)
            out.append('{}{}-{}{}{}'.format(chr(move//BOARD_SIZE % 10+64), move//BOARD_SIZE//10-1,
                                      chr(move % BOARD_SIZE % 10+64), move % BOARD_SIZE//10-1, pro[promotion]))
        else:
            out.append('{}{}-{}{}'.format(chr(move//BOARD_SIZE % 10+64), move//BOARD_SIZE//10-1,
                                      chr(move % BOARD_SIZE % 10+64), move % BOARD_SIZE//10-1))
    print out


def string_loc(loc):
    return '{}{}'.format(chr(loc % 10 + 64), loc//10-1)


def string_move(move):
    if move > LOC_SIZE * LOC_SIZE:
        pro = '   NBRQ'
        promotion = move // (LOC_SIZE * LOC_SIZE)
        move %= (LOC_SIZE * LOC_SIZE)
        return '{}{}-{}{}{}'.format(chr(move//BOARD_SIZE % 10+64), move//BOARD_SIZE//10-1,
                                      chr(move % BOARD_SIZE % 10+64), move % BOARD_SIZE//10-1, pro[promotion])
    else:
        return '{}{}-{}{}'.format(chr(move//BOARD_SIZE % 10+64), move//BOARD_SIZE//10-1,
                              chr(move % BOARD_SIZE % 10+64), move % BOARD_SIZE//10-1)


def int_move(move):
    return (ord(move[0])-54+10*int(move[1]))*BOARD_SIZE+(ord(move[3])-54+10*int(move[4]))


def output_board(board):
    if len(board) != BOARD_SIZE:
        print("Invalid Board.")
    else:
        symcon = u' x♙♘♗♖♕♔.,♚♛♜♝♞♟x'
        print('   _______________________________')
        for rank in range(8, 0, -1):
            if rank % 2:
                line = str(rank)+' |['
            else:
                line = str(rank)+' | '
            for file_ in range(1, 9):
                field = board[10+rank*10+file_]
                if (rank+file_) % 2:
                    if file_ < 8:
                        line += symcon[field]+' |['
                    else:
                        line += symcon[field]+' | '
                else:
                    line += symcon[field]+']| '
            print(line)
        print('   ‾A‾‾‾B‾‾‾C‾‾‾D‾‾‾E‾‾‾F‾‾‾G‾‾‾H‾')


if __name__ == '__main__':
    main()
