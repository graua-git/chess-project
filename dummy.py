class Move:
    def __init__(self, notation):
        self.notation = notation
    
    def __eq__(self, other):
        return other == self.notation
    

move = 'Rf2'
move_list = [Move('Nb2'), Move('Ke1'), Move('Rf2'), Move('Qh3'), Move('Bb5'), Move('e4')]
print(move_list.index(move))