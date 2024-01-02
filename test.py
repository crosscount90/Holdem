import random

# 카드 덱 초기화
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

# 카드 섞기
random.shuffle(deck)

# 플레이어와 딜러 초기 패 설정
player1_hand = [deck.pop(), deck.pop()]
player2_hand = [deck.pop(), deck.pop()]

# 커뮤니티 카드 초기화
community_cards = [deck.pop() for _ in range(5)]

# print(community_cards)

"""
for card in community_cards:
    print(community_cards)
    print(f"{card['rank']} of {card['suit']}")
"""

print(deck[0]['rank'])
