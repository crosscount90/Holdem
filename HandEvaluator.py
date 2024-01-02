import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

class Player:
    def __init__(self, chips):
        self.hand = []
        self.chips = chips

    def bet(self, amount):
        self.chips -= amount

class PokerGame:
    def __init__(self, num_players, starting_chips):
        self.deck = Deck()
        self.players = [Player(starting_chips) for _ in range(num_players)]
        self.pot = 0

    def start_hand(self):
        for player in self.players:
            player.hand = self.deck.deal(2)

    # This function is a placeholder for the actual game logic
    def play_round(self):
        pass

# Example usage
game = PokerGame(num_players=4, starting_chips=100)
game.start_hand()
game.players[0].hand, game.players[1].hand, game.players[2].hand, game.players[3].hand

from itertools import combinations

class HandEvaluator:
    @staticmethod
    def best_hand(cards):
        """ Determine the best poker hand from 7 cards """
        best_rank = 0
        best_hand = None

        for combo in combinations(cards, 5):
            rank = HandEvaluator.evaluate_hand(list(combo))
            if rank > best_rank:
                best_rank = rank
                best_hand = combo

        hand_name = HandEvaluator.rank_to_name(best_rank)
        return hand_name, best_hand

    @staticmethod
    def evaluate_hand(cards):
        """ Evaluate the hand strength """
        if HandEvaluator.is_royal_flush(cards):
            return 10
        elif HandEvaluator.is_straight_flush(cards):
            return 9
        elif HandEvaluator.is_four_of_a_kind(cards):
            return 8
        elif HandEvaluator.is_full_house(cards):
            return 7
        elif HandEvaluator.is_flush(cards):
            return 6
        elif HandEvaluator.is_straight(cards):
            return 5
        elif HandEvaluator.is_three_of_a_kind(cards):
            return 4
        elif HandEvaluator.is_two_pair(cards):
            return 3
        elif HandEvaluator.is_one_pair(cards):
            return 2
        else:
            return 1

    @staticmethod
    def is_royal_flush(cards):
        return HandEvaluator.is_straight_flush(cards) and max(HandEvaluator.card_values(cards)) == 14

    @staticmethod
    def is_straight_flush(cards):
        return HandEvaluator.is_straight(cards) and HandEvaluator.is_flush(cards)

    @staticmethod
    def is_four_of_a_kind(cards):
        values = HandEvaluator.card_values(cards)
        return any(values.count(x) == 4 for x in values)

    @staticmethod
    def is_full_house(cards):
        values = HandEvaluator.card_values(cards)
        return any(values.count(x) == 3 for x in values) and any(values.count(x) == 2 for x in values)

    @staticmethod
    def is_flush(cards):
        suits = [card.suit for card in cards]
        return any(suits.count(suit) >= 5 for suit in suits)

    @staticmethod
    def is_straight(cards):
        values = sorted(set(HandEvaluator.card_values(cards)))
        for i in range(len(values) - 4):
            if values[i] + 4 == values[i + 4]:
                return True
        return False

    @staticmethod
    def is_three_of_a_kind(cards):
        values = HandEvaluator.card_values(cards)
        return any(values.count(x) == 3 for x in values)

    @staticmethod
    def is_two_pair(cards):
        values = HandEvaluator.card_values(cards)
        pairs = [x for x in values if values.count(x) == 2]
        return len(set(pairs)) >= 2

    @staticmethod
    def is_one_pair(cards):
        values = HandEvaluator.card_values(cards)
        return any(values.count(x) == 2 for x in values)

    @staticmethod
    def card_values(cards):
        """ Convert card values to numerical values for easier comparison """
        value_map = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        return [value_map[card.value] for card in cards]

    @staticmethod
    def rank_to_name(rank):
        """ Convert hand rank to name """
        return {
            10: "Royal Flush",
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card"
        }.get(rank, "Unknown")

# Test the evaluator with a sample hand
sample_cards = [
    Card("Hearts", "10"), Card("Hearts", "J"),
    Card("Hearts", "Q"), Card("Hearts", "K"),
    Card("Hearts", "A"), Card("Diamonds", "8"),
    Card("Clubs", "2")
]

best_hand_name, best_hand = HandEvaluator.best_hand(sample_cards)
print(best_hand_name, best_hand)

