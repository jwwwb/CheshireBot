// This should contain a __kernel function which is the opencl implementation of a
// movegen. Considering the movegen is about 300 LoC in python, this will be a pretty
// big project to port. Data structures in C aren't really that flexible, so I may
// have to optimize along the way. perhaps represent the whole game state (board +
// flags) as a single dimension vector (something like 256 elements to describe the
// board and out of bounds regions, as well as all flags). This sequence of state
// vectors in turn needs to be flattened out into a giant 1d stream of all possible
// game states with a 256*N length

// data types:
// uint move = 128*start_field + goal_field
// int occupancy = -7:-2 for black, 2:7 for white pieces, 0 for empty, -1 for OoB
// int color = -1 if it's black's turn, 1 if it's white's turn
// int board[128] = 10 + 10*rank + file. max value 120, so we use 127 for flags.
// int flags[6] = white: A en passant, H en passant, black: A en passant, H en passant


#define LOC_SIZE 128
#define BOARD_SIZE 128
#define MOVES_SIZE 128
#define PIECE_SIZE 16
#define PIECE_OFFSET 8
#define NUM_FLAGS 4 // maximum of 8!!
#define COLOR_OFFSET 122

bool is_check(int state[], int move, int kl, int co);

bool is_check(int state[], int move, int kl, int co) {
    /*
    this function starts by making a copy of the current state from the global buffer (hopefully),
    then applies the move to it, and checks if the king is threatened from anywhere.
    variables: kl = king location, co = color of king
    */

    // apply move
    int local_state[BOARD_SIZE];
    for (int r = 0; r < BOARD_SIZE; r++) local_state[r] = state[r];
    int start = move / LOC_SIZE;
    int goal = move % LOC_SIZE;
    int flags[NUM_FLAGS];
    int b = 0;

    if (local_state[start]*co == 7) kl = goal;

    for (int f = 0; f < NUM_FLAGS; f++) flags[f] = local_state[BOARD_SIZE-NUM_FLAGS+f];

    if (local_state[goal]*co == -8 && local_state[start]*co == 2) {     // en passant
        local_state[goal-co*10] = 0;
    }
    if (local_state[start]*co == 7 && goal-start == 2) {  // short castle
        local_state[start+1] = 5*co;
        local_state[goal+1] = 0;
        flags[3-co] = 1;
    }
    if (local_state[start]*co == 7 && goal-start == -2) {  // long castle
        local_state[start-1] = 5*co;
        local_state[goal-2] = 0;
        flags[2-co] = 1;
    }
    /*      flag disables are unnecessary for checking check, as this only looks one move ahead.

    if ((start/10)*2+5*co == 11 && (goal/10)*2+co == 11 && local_state[start]*co == 2) {  // double hop
        local_state[start+10*co] = 8*co;
    }
    if (start+co*35 == 60 || start+co*35 == 63) {    // disable short castling
        flags[3-co] = 1;
    }
    if (start+co*35 == 60 || start+co*35 == 56) {    // disable long castling
        flags[2-co] = 1;
    }
    for (int e = 56+25*co; e < 64+25*co; e++) {     // remove en passant flags if we didn't take advantage
        if (local_state[e] == -8*co) {
            local_state[e] = 0;
        }
    }
    */
    local_state[goal] = local_state[start];         // finally just move the standard move, this should always be necessary
    local_state[start] = 0;
    local_state[COLOR_OFFSET] = -local_state[COLOR_OFFSET];
    // return flags to board local_state again:
    for (int f = 0; f < NUM_FLAGS; f++) local_state[BOARD_SIZE-NUM_FLAGS+f] = flags[f];

    // check for threats
    if (local_state[kl+21]*co == -3 || local_state[kl+19]*co == -3 || local_state[kl+12]*co == -3 || local_state[kl+8]*co == -3 ||
        local_state[kl-21]*co == -3 || local_state[kl-19]*co == -3 || local_state[kl-12]*co == -3 || local_state[kl-8]*co == -3) {
        return true;
    } else if (local_state[kl+9*co]*co == -2 || local_state[kl+11*co]*co == -2) { // check for pawns
        return true;
    } else if (local_state[kl+9]*co == -7 || local_state[kl+10]*co == -7 || local_state[kl+11]*co == -7 ||
                local_state[kl+1]*co == -7 || local_state[kl-10]*co == -7 || local_state[kl-11]*co == -7 ||
                local_state[kl-9]*co == -7 || local_state[kl-1]*co == -7) { // check for king
        return true;
    } else {
        b = kl;           // searching up and left
        do {
            b+=9;
            if (local_state[b]*co == -4 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching up
        do {
            b+=10;
            if (local_state[b]*co == -5 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching up and right
        do {
            b+=11;
            if (local_state[b]*co == -4 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching right
        do {
            b+=1;
            if (local_state[b]*co == -5 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching down and right
        do {
            b-=9;
            if (local_state[b]*co == -4 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching down
        do {
            b-=10;
            if (local_state[b]*co == -5 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching down and left
        do {
            b-=11;
            if (local_state[b]*co == -4 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);
        b = kl;           // searching left
        do {
            b-=1;
            if (local_state[b]*co == -5 || local_state[b]*co == -6 ) return true;
        } while (local_state[b] == 0 || local_state[b] == -8 || local_state[b] == 8);

        return false;
    }
    // to-do: check for threats other than knights.

}

__kernel void find_moves(__global int* counter, __global int* states, __global int* moves){
    /*
    this is the openCL function that analyzes all possible moves from a given state of the board.
    it is not entirely self contained, it has to call the external function is_check at every move
    in order to see if the move can be added or the user would be putting themselves into check.
    input variables:
    counter (size 1 * num_states) - unused, just gives the size
    states (size BOARD_SIZE * num_states) - all possible boards going into this move
    output variable:
    moves (size MOVES_SIZE * num_states) - all possible moves for each of the possible boards

    */
    int id = get_global_id(0);
    int attackers[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};   // initialization likely unnecessary
    int att_ind = 0;
    int state[BOARD_SIZE];
    int local_moves[MOVES_SIZE];
    int color = states[id*BOARD_SIZE+COLOR_OFFSET];
    for (int r = 0; r < BOARD_SIZE; r++) state[r] = states[id*BOARD_SIZE+r];
    int king_location = 0;
    int m = 0;  // index that loops through the moves we're computing
    // get all attacking pieces
    for (int i = 21; i < 99; i++) {   // index that loops through the fields on the board
        if (state[i]*color >= 2 && state[i]*color < 8) {
            attackers[att_ind++] = i*PIECE_SIZE + state[i]*color;
            if (state[i]*color == 7) {
                king_location = i;
            }
        }
    }

    // iterate through attacking pieces
    // to-do: replace states with state, see if local memory is faster than global.
    int flags[NUM_FLAGS];
    for (int f = 0; f < NUM_FLAGS; f++) flags[f] = state[BOARD_SIZE-NUM_FLAGS+f];
    int location = 0;
    int b = 0;
    int c = 0;
    for (int a = 0; a < att_ind; a++) {
        location = attackers[a] / PIECE_SIZE;
        if (attackers[a] % PIECE_SIZE == 2) {   // is pawn
            if (state[location+10*color] == 0) {   // field in front is empty
                if (!is_check(state, LOC_SIZE*location + location + 10*color, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location + 10*color; // add move
                }
                if (((location / 10 == 3) && color == 1) || ((location / 10 == 8) && color == -1)) {   // is still in start
                    if (state[location+20*color] == 0) {     // 2 fields ahead is empty
                        if (!is_check(state, LOC_SIZE*location + location + 20*color, king_location, color)) {
                            local_moves[m++] = LOC_SIZE*location + location + 20*color; // add move
                        }
                    }
                }
            }
            if (state[location+11*color] * color <= -2) {   // field diagonal right is occupied by opponent
                if (!is_check(state, LOC_SIZE*location + location + 11*color, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location + 11*color; // add move
                }
            }
            if (state[location+9*color] * color <= -2) {   // field diagonal left is occupied by opponent
                if (!is_check(state, LOC_SIZE*location + location + 9*color, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location + 9*color; // add move
                }
            }
        } else if (attackers[a] % PIECE_SIZE == 3) {   // is knight
            if (state[location-21] == 0 ||state[location-21]*color == 8 || state[location-21] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location-21, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location-21; // add move
                }
            }
            if (state[location-19] == 0 || state[location-19]*color == 8 || state[location-19] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location-19, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location-19; // add move
                }
            }
            if (state[location-12] == 0 || state[location-12]*color == 8 || state[location-12] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location-12, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location-12; // add move
                }
            }
            if (state[location-8] == 0 || state[location-8]*color == 8 || state[location-8] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location-8, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location-8; // add move
                }
            }
            if (state[location+8] == 0 || state[location+8]*color == 8 || state[location+8] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location+8, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location+8; // add move
                }
            }
            if (state[location+12] == 0 || state[location+12]*color == 8 || state[location+12] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location+12, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location+12; // add move
                }
            }
            if (state[location+19] == 0 || state[location+19]*color == 8 || state[location+19] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location+19, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location+19; // add move
                }
            }
            if (state[location+21] == 0 || state[location+21]*color == 8 || state[location+21] * color <= -2 ) {   // avail
                if (!is_check(state, LOC_SIZE*location + location+21, king_location, color)) {
                    local_moves[m++] = LOC_SIZE*location + location+21; // add move
                }
            }
        } else if (attackers[a] % PIECE_SIZE == 4 || attackers[a] % PIECE_SIZE == 6) {   // is bishop or queen
            b = location;           // searching up and right
            do {
                b+=11;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching up and left
            do {
                b+=9;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching down and right
            do {
                b-=9;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching down and left
            do {
                b-=11;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
        }
        if (attackers[a] % PIECE_SIZE == 5 || attackers[a] % PIECE_SIZE == 6) {   // is rook or queen
            b = location;           // searching up
            do {
                b+=10;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching right
            do {
                b+=1;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching left
            do {
                b-=1;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
            b = location;           // searching down
            do {
                b-=10;
                if (state[b] == 0 || state[b] == -8 || state[b] == 8 || state[b]*color <= -2) {
                    if (!is_check(state, LOC_SIZE*location + b, king_location, color)) {
                        local_moves[m++] = LOC_SIZE*location + b; // add move
                    }
                }
            } while (state[b] == 0 || state[b] == -8 || state[b] == 8);
        } else if (attackers[a] % PIECE_SIZE == 7) {   // is king
            for (b = -1; b<=1; b++) {
                for (c = -10; c<=10; c+=10) {
                    if (state[location+b+c]*color <= -2 || state[location+b+c] == 0 || state[location+b+c] == 8 || state[location+b+c] == -8) {
                        if (!is_check(state, LOC_SIZE*location + location+b+c, king_location, color)) {
                            local_moves[m++] = LOC_SIZE*location + location+b+c; // add move
                        }
                    }
                }
            }
            // checking castles
            if (flags[3-color] == 0 && state[location+1] == 0 && state[location+2] == 0) {
                if (!(is_check(state, LOC_SIZE*location + location+2, king_location, color) ||
                    is_check(state, LOC_SIZE*location + location+1, king_location, color) ||
                    is_check(state, LOC_SIZE*location + location, king_location, color))) {  // can't be in or pass thru
                    local_moves[m++] = LOC_SIZE*location + location+2; // add move
                }
            }
            if (flags[2-color] == 0 && state[location-1] == 0 && state[location-2] == 0
                                                                            && state[location-3] == 0) {
                if (!(is_check(state, LOC_SIZE*location + location-2, king_location, color) ||
                    is_check(state, LOC_SIZE*location + location-1, king_location, color) ||
                    is_check(state, LOC_SIZE*location + location, king_location, color))) {  // can't be in or pass thru
                    local_moves[m++] = LOC_SIZE*location + location-2; // add move
                }
            }
        }
    }
    for (int n = 0; n < m; n++) moves[id*MOVES_SIZE+n] = local_moves[n];
}

__kernel void apply_moves(__global int* counter, __global int* states, __global int* moves, __global int* new_states){
    /*
    this function applies all the generated moves to the board states, creating new states
    input variables:
    counter (size 1 * num_states) - unused, just gives the size
    states (size BOARD_SIZE * num_states) - all possible boards going into this move
    moves (size MOVES_SIZE * num_states) - all possible moves for each of the possible boards
    output variable:
    new_states (size BOARD_SIZE * MOVES_SIZE * num_states) - board states after every move applied to every state
    this might get messy fast - let's keep an eye on RAM.
    */
    int id = get_global_id(0)*BOARD_SIZE;
        // apply move
    int local_state[BOARD_SIZE];
    int local_moves[MOVES_SIZE];
    int move, start, goal, co, m, r, f, flags[NUM_FLAGS];
    for (r = 0; r < BOARD_SIZE; r++) local_state[r] = states[id+r];
    for (m = 0; m < MOVES_SIZE; m++) local_moves[m] = moves[id+m];
    for (m = 0; m < MOVES_SIZE; m++) {
        move = local_moves[m];
        if (move == 0) {
            for (r = 0; r < BOARD_SIZE; r++) new_states[id*MOVES_SIZE+m*BOARD_SIZE+r] = 0;
        } else {
            start = move / LOC_SIZE;
            goal = move % LOC_SIZE;
            co = local_state[COLOR_OFFSET];
            for (f = 0; f < NUM_FLAGS; f++) flags[f] = local_state[BOARD_SIZE-NUM_FLAGS+f];

            for (r = 0; r < BOARD_SIZE; r++) new_states[id*MOVES_SIZE+m*BOARD_SIZE+r] = local_state[r];

            if (new_states[id*MOVES_SIZE+m*BOARD_SIZE+goal]*co == -8 && new_states[id*MOVES_SIZE+m*BOARD_SIZE+start]*co == 2) {     // en passant
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+goal-co*10] = 0;
            }
            if ((start/10)*2+5*co == 11 && (goal/10)*2+co == 11 && new_states[id*MOVES_SIZE+m*BOARD_SIZE+start]*co == 2) {  // double hop
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+start+10*co] = 8*co;
            }
            if (new_states[id*MOVES_SIZE+m*BOARD_SIZE+start]*co == 7 && goal-start == 2) {  // short castle
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+start+1] = 5*co;
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+goal+1] = 0;
                flags[3-co] = 1;
            }
            if (new_states[id*MOVES_SIZE+m*BOARD_SIZE+start]*co == 7 && goal-start == -2) {  // long castle
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+start-1] = 5*co;
                new_states[id*MOVES_SIZE+m*BOARD_SIZE+goal-2] = 0;
                flags[2-co] = 1;
            }
            if (start+co*35 == 60 || start+co*35 == 63) {    // disable short castling
                flags[3-co] = 1;
            }
            if (start+co*35 == 60 || start+co*35 == 56) {    // disable long castling
                flags[2-co] = 1;
            }
            for (int e = 56+15*co; e < 64+15*co; e++) {     // remove en passant flags if we didn't take advantage
                if (new_states[id*MOVES_SIZE+m*BOARD_SIZE+e] == -8*co) {
                    new_states[id*MOVES_SIZE+m*BOARD_SIZE+e] = 0;
                }
            }
            new_states[id*MOVES_SIZE+m*BOARD_SIZE+goal] = new_states[id*MOVES_SIZE+m*BOARD_SIZE+start];         // finally just move the standard move, this should always be necessary
            new_states[id*MOVES_SIZE+m*BOARD_SIZE+start] = 0;
            new_states[id*MOVES_SIZE+m*BOARD_SIZE+COLOR_OFFSET] = -new_states[id*MOVES_SIZE+m*BOARD_SIZE+COLOR_OFFSET];     // switch color for the next turn
            // return flags to board local_state again:
            for (int f = 0; f < NUM_FLAGS; f++) new_states[id*MOVES_SIZE+m*BOARD_SIZE+BOARD_SIZE-NUM_FLAGS+f] = flags[f];
        }
    }
}