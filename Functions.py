# Definition of functions needed for our program

def convert_list_coords(coords):
    # Receives 2 ints representing 2d array list coordinates
    # Returns string chess coordinates
    # Ex. (0, 0) returns 'a1', (7, 7) returns 'h8'
    letters = 'abcdefgh'
    return letters[coords[1]] + str(coords[0] + 1)

def convert_chess_coords(coords):
    # Receives string chess coordinates
    # Returns 2 ints representing 2d array list coordinates
    # Ex. 'a1' returns '(0, 0)', 'h8' returns (7, 7)
    letters = 'abcdefgh'
    return letters.index(coords[1]), int(coords[0]) - 1