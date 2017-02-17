import random
import pdb

PILES = 7

class Card:
    def __init__(self, suit, rank, visable):
        self.rank = rank
        self.suit = suit
        self.visable = visable

    def __str__(self):
        if self.visable:
            v = "*"
        else:
            v = ""
        return self.suit[0] + ":" + self.rank + v

    def __repr__(self):
        return self.__str__()

def make_deck():
    all_cards = []
    for suit in ['spade', 'heart', 'club', 'diamond']:
        for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
            all_cards.append(Card(suit, rank, False))
    return all_cards

def initial_deal():
    deck = make_deck()
    # shuffle fn mutates deck
    random.shuffle(deck)
    piles = []

    cur_pile = []
    pile_size = 1
    for pile in range(0, PILES):
        for i in range(0, pile_size):
            visable = False
            if i == pile_size - 1:
                visable = True
            card = deck.pop()
            card.visable = visable
            cur_pile.append(card)
        piles.append(cur_pile)
        pile_size += 1
        cur_pile = []

    return (piles, deck, [], [[], [], [], []])

def pad(n):
    return n * " "

# state is tuple of draw pile and piles, and drawn card (starts as empty list)
def print_state(state):
    piles = state[0]
    draw_pile = state[1]
    drawn_cards = state[2]
    victory_piles = state[3]
    state_repr = ""

    state_repr += " -- DRAW PILE -- " + str(len(draw_pile)) + " cards... -> " + str(drawn_cards) + "\n"
    state_repr += " -- Victory Piles -> " + str(victory_piles) + "\n"

    max_pile_depth = max(map(lambda x: len(x), piles))

    max_width = 7
    left_pad = 5

    state_repr += pad(left_pad) + "|"
    for col in range(0, len(piles)):
        col_str = str(col)
        p = max_width - len(col_str)
        state_repr += str(col) + pad(p) + "||" 
    state_repr += "\n"

    state_repr += pad(left_pad) + "|"
    for col in range(0, len(piles)):
        state_repr += ("-" * (max_width ) + "||")
    state_repr += "\n"

    for cur_depth in range(0, max_pile_depth):
        state_repr += str(cur_depth) + " -> "
        for pile in piles:
            if cur_depth < len(pile):
                card = pile[cur_depth]
                card_str = str(card)
                buf = max_width - len(card_str)
                state_repr += "|" + str(card) + (buf * " ")+ "|"
            else:
                state_repr += "|" + (max_width * " ") + "|"
        state_repr += "\n"
    return state_repr

def is_ace(card):
    return card.rank == 'A'

def perform_move(state, move):
    print "You picked: " + move
    piles = state[0]
    victory_piles = state[3]
    if move == 'd':
        print "performing draw"
        drawn_card = state[1].pop()
        drawn_cards = state[2]
        drawn_cards.append(drawn_card)
        return (state[0], state[1], drawn_cards, victory_piles)
    else:
        # assume move is col number
        col = int(move)
        print piles[col]
        card = piles[col].pop()
        # Check victory piles to see if it goes there
        moved = False
        if is_ace(card):
            for v_pile in victory_piles:
                if len(v_pile) == 0:
                    v_pile.append(card)
                    moved = True
                    break
        # Otherwise check normal piles

        if moved == True:
            piles[col][-1].visable = True
        else:
            piles[col].append(card)

    return state

state = initial_deal()
while(True):
    print print_state(state)
    move = raw_input("move? [num of col or d for draw] > ")
    state = perform_move(state, move)
