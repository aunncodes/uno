# Submission by Sahil Chopra, aunngames@gmail.com


import random
import re
import time


# 0-9, numbers
# 10, skip
# 11, reverse
# 12, draw 2
# 13, wild
# 14, wild draw 4
class Card:
    def __init__(self, card, color):
        self.card = card
        self.color = color

    def __repr__(self):
        card_str = {10: 'Skip', 11: 'Reverse', 12: 'Draw Two', 13: 'Wild', 14: 'Draw Four Wild'}.get(self.card,
                                                                                                     self.card)
        return f"{self.color} {card_str}"

    def __str__(self):
        card_str = {10: 'Skip', 11: 'Reverse', 12: 'Draw Two', 13: 'Wild', 14: 'Wild Draw Four'}.get(self.card,
                                                                                                     self.card)
        return f"{self.color} {card_str}"

def shufflePile():
    global deck
    global pile
    deck.cards += pile[:-1]
    pile = [pile[-1]]

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for color in ["Red", "Yellow", "Blue", "Green"]:
            for num in range(1, 10):
                self.cards.append(Card(num, color))
                self.cards.append(Card(num, color))
            self.cards.append(Card(0, color))
            for num in [10, 11, 12]:
                self.cards.append(Card(num, color))
                self.cards.append(Card(num, color))
        for _ in range(4):
            self.cards.append(Card(13, "Black"))
            self.cards.append(Card(14, "Black"))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            if len(pile) > 1:  # Check if the pile is not empty
                shufflePile()
                self.shuffle()
            else:
                raise Exception("No more cards to draw")
            return self.draw()
        return self.cards.pop()

    def __str__(self):
        return " ".join([str(card) for card in self.cards])


def move_validation(card, pile):
    if card.card in [13, 14]:
        return True
    if card.color == pile.color or card.card == pile.card:
        return True
    return False


def ai_turn(p, draw):
    global hands
    print("\n")
    # print(f"The top card of the pile is: {pile[-1]}")
    for _ in range(draw):
        hands[p].append(deck.draw())
    if draw > 0:
        print(f"AI {p} draws {draw} cards.")
        print(f"AI {p} has {len(hands[p])} cards in hand.\n")
        return 0
    # print(f"AI {p} hand: {hands[p]}")
    time.sleep(1)
    for i in hands[p]:
        if move_validation(i, pile[-1]):
            print(f"AI {p} plays: {i}")
            if i.card == 13 or i.card == 14:
                i.color = random.choice(["Red", "Yellow", "Blue", "Green"])
            if i.card == 14 or i.card == 12:
                retval = i.card - 10
            elif i.card == 11:
                retval = "r"
            elif i.card == 10:
                retval = "s"
            else:
                retval = 0
            pile.append(i)
            hands[p].remove(i)
            if len(hands[p]) == 0:
                print(f"AI {p} wins!")
                print("Game over! :(")
                exit()
            print(f"AI {p} has {len(hands[p])} cards in hand.")
            print("\n")
            return retval

    print(f"AI {p} draws.")
    print(f"AI {p} has {len(hands[p])} cards in hand.")
    print("\n")
    hands[p].append(deck.draw())
    return 0


def preturn(draw):
    global hands
    for _ in range(draw):
        hands[0].append(deck.draw())
        if draw > 0:
            print(f"You draw {draw} cards.")
            time.sleep(0.5)
            print("Uh Oh! Your turn is skipped!")
            return 0

    return turn()


def repl_func(m):
    return m.group(1) + m.group(2).upper()


def turn():
    global hands
    global pile
    try:
        print(f"You have {len(hands[0])} cards in hand.\n")
        print("Your hand:")
        for i, card in enumerate(hands[0], 1):
            print(f"{i}. {card}")
        print(f"\n\nThe top card of the pile is: {pile[-1]}\n\n")
        ask = input("What would you like to do? ")
        if ask.strip().lower() == "d" or ask.strip().lower() == "draw":
            print("\nYou draw a card.")
            hands[0].append(deck.draw())
            return 0
        else:
            if not ask.isnumeric():
                ask = re.sub("(^|\s)(\S)", repl_func, ask)
                if ask.strip() in repr(hands[0]):
                    hand_str = repr(hands[0])
                    cards = hand_str.strip('[]').split(', ')
                    index = cards.index(ask)
                    ask = index + 1
            if not move_validation(hands[0][int(ask) - 1], pile[-1]):
                print("Invalid move. Please try again.")
                print("\n\n")
                return turn()
            else:
                if hands[0][int(ask) - 1].card == 13 or hands[0][int(ask) - 1].card == 14:
                    col = input("What color would you like to play as? (Red, Green, Blue, Yellow) ").strip().capitalize()
                    if col not in ["Red", "Green", "Blue", "Yellow"]:
                        print("Invalid color. Please try again.")
                        return turn()
                    hands[0][int(ask) - 1].color = col
                if hands[0][int(ask) - 1].card == 14 or hands[0][int(ask) - 1].card == 12:
                    retval = hands[0][int(ask) - 1].card - 10
                elif hands[0][int(ask) - 1].card == 11:
                    retval = "r"
                elif hands[0][int(ask) - 1].card == 10:
                    retval = "s"
                else:
                    retval = 0
                pile.append(hands[0][int(ask) - 1])
                hands[0].remove(hands[0][int(ask) - 1])
                if len(hands[0]) == 0:
                    print("You win!")
                    print("Gave over! :)")
                    exit()
                return retval
    except ValueError:
        print("Invalid input. Please try again.")
        print("\n\n")
        return turn()


def setup():
    global deck
    global hands
    global pile
    try:
        players = int(input("How many players? "))
    except ValueError:
        print("Invalid input. Please try again.")
        setup()
        return
    if players < 2 or players > 10:
        print("There must be between 2 and 10 players.")
        setup()
        return
    hands = [[deck.draw() for _ in range(7)] for _ in range(players)]
    print("How to play: On your turn, either type the location of the card you want to play, or type the full name of the card. If you want to draw, type 'draw' or 'd' to draw a card. \n")


def game_over():
    for i in range(1, len(hands)):
        if len(hands[i]) == 0:
            print(f"Player {i} wins!")
            return True
    return False


def main_loop():
    state = 0
    order = list(range(0, len(hands)))
    ran = False
    reverse = False
    while not game_over():
        if ran:
            i = (i - 1) % len(order)
        else:
            i = 0
            ran = True
        while i >= 0:
            if i == 0:
                action = preturn(state)
                state = 0
                if action == "r" and len(order) > 2:
                    reverse = not reverse
                elif action == "r":
                    if reverse:
                        i = (i - 1) % len(order)
                    else:
                        i = (i + 1) % len(order)
                elif action == "s":
                    if reverse:
                        i = (i - 1) % len(order)
                        print("\n")
                    else:
                        i = (i + 1) % len(order)
                        print("\n")
                else:
                    state = int(action)
            else:
                action = ai_turn(i, state)
                state = 0
                if action == "r" and len(order) > 2:
                    reverse = not reverse
                elif action == "r":
                    if reverse:
                        i = (i - 1) % len(order)
                    else:
                        i = (i + 1) % len(order)
                elif action == "s":
                    if reverse:
                        i = (i - 1) % len(order)
                    else:
                        i = (i + 1) % len(order)
                else:
                    state = int(action)
            if reverse:
                i = (i - 1) % len(order)
            else:
                i = (i + 1) % len(order)


deck = Deck()
deck.shuffle()
pile = []
hands = []

if __name__ == "__main__":
    setup()
    while True:
        top = deck.cards[-1]
        if top.card in [10, 11, 12, 13, 14]:
            deck.shuffle()
        else:
            pile.append(top)
            break
    main_loop()
