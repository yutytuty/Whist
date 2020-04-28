import random
import pygame

new_player_order = None


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = None
        self.assign_picture()

    def assign_picture(self):
        if self.value < 11:
            self.image = f"assets/{self.value}{self.suit[0]}.png"

        if self.value == 11:
            self.image = f"assets/J{self.suit[0]}.png"

        elif self.value == 12:
            self.image = f"assets/Q{self.suit[0]}.png"

        elif self.value == 13:
            self.image = f"assets/K{self.suit[0]}.png"

        elif self.value == 14:
            self.image = f"assets/A{self.suit[0]}.png"

    def __str__(self):
        if self.value < 11:
            return f"{self.value} of {self.suit}"
        elif self.value == 11:
            return f"Jack of {self.suit}"
        elif self.value == 12:
            return f"Queen of {self.suit}"
        elif self.value == 13:
            return f"King of {self.suit}"
        elif self.value == 14:
            return f"Ace of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []

    def draw(self):
        return self.cards.pop()

    def show(self):
        for card in self.cards:
            print(card)

    def build(self):
        for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            for value in range(2, 15):
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.take_num = 0
        self.declaration = None

    def show_hand(self):
        for card in self.hand:
            print(card)

    def draw(self, deck, num):
        for i in range(num):
            self.hand.append(deck.draw())

    def sort_hand(self):
        def bubble_sort(arr):
            swapped = False

            def swap(z, j):
                arr[z], arr[j] = arr[j], arr[z]

            pointer = 1

            for f in range(pointer, len(arr)):
                if arr[f].value < arr[f - 1].value:
                    swap(f, f - 1)
                    swapped = True

            if not swapped:
                return arr

            return bubble_sort(arr)

        sorted_hand = [
            [],
            [],
            [],
            []
        ]

        for card in self.hand:
            if card.suit == "Spades":
                sorted_hand[0].append(card)
            elif card.suit == "Hearts":
                sorted_hand[1].append(card)
            elif card.suit == "Clubs":
                sorted_hand[2].append(card)
            elif card.suit == "Diamonds":
                sorted_hand[3].append(card)

        for i in sorted_hand:
            bubble_sort(i)

        self.hand = sum(sorted_hand, [])

    def play_card(self, table, card_id, round_suit=None):
        round_suit = round_suit
        card_suit = self.hand[card_id].suit
        if not round_suit:
            round_suit = self.hand[card_id].suit

        elif card_suit != round_suit:
            suits = [i.suit for i in self.hand]
            if round_suit in suits:
                print(f"Please play a card with a suit of {round_suit}")
                return self.play_card(table, round_suit)

            else:
                table.on_table.append(self.hand.pop(card_id))
                return round_suit

        table.on_table.append(self.hand.pop(card_id))
        return round_suit


class Table:
    def __init__(self):
        self.on_table = []

    def show(self):
        # TODO: remove when done debugging
        print("On table: }")
        for card in self.on_table:
            print(card)

    def take(self, trump):
        # --------------------------------------------------------------------------------------------------------------
        global new_player_order

        def shift(arr, new_first):
            head_arr = arr[new_first:]
            tail_arr = arr[:new_first]
            arr = head_arr + tail_arr
            return arr

        # --------------------------------------------------------------------------------------------------------------

        if len(self.on_table) == 4:
            largest_card = self.on_table[0]
            largest_trump = None
            for card in self.on_table:
                if card.suit == trump:
                    largest_trump = card

                if card.value > largest_card.value and card.suit == self.on_table[0].suit:
                    largest_card = card

            if not largest_trump:
                players[self.on_table.index(largest_card)].take_num += 1
                print(f'\n"{players[self.on_table.index(largest_card)].name}" takes!')
                new_player_order = shift(players, self.on_table.index(largest_card))
                self.on_table = []

            elif largest_trump:
                players[self.on_table.index(largest_trump)].take_num += 1
                print(f'\n"{players[self.on_table.index(largest_trump)].name}" takes!')
                new_player_order = shift(players, self.on_table.index(largest_trump))
                self.on_table = []

            return new_player_order


# players = [Player("Player 1"), Player("Player 2"), Player("Player 3"), Player("Player 4")]
players = []
