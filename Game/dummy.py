from Piece import *
from Coord import *

pawn1 = Pawn('W', Coord(0, 0))
pawn2 = Pawn('B', Coord(7, 7))

l1 = [pawn1, pawn2]
l2r = [pawn1, pawn2]

def print_pieces(pieces, piece_ref):
    for i in range(len(pieces)):
        print(pieces[i].get_position(), piece_ref[i].get_position())


def remove_pawn(pawn, list1, list_ref):
    list1.remove(pawn)
    list_ref.remove(pawn)

remove_pawn(Pawn('W', Coord(4, 4+6)), l1, l2r)

print_pieces(l1, l2r)

