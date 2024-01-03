import os
import numpy as np

## 핸드데이터 불러와서 정리하기
poker_hand_data = []
directory_path = 'Holdem\HandData'

for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file: # 파일을 읽어서 리스트에 추가
            file_contents = file.read()
            poker_hand_data.append(file_contents)

hand_data_list = []

for poker_hand in poker_hand_data: # 핸드데이터 한줄씩 2차원 리스트로 정리
    hand_data = [line.strip() for line in poker_hand.strip().split('\n\n')]

    hand_data_list = hand_data_list + hand_data

import pandas as pd
import re

hero_hands = [] # DataFrame을 저장할 리스트

for hand_data in hand_data_list: # 각 포커 핸드 데이터에 대한 반복
    hand_date = hand_data.split('\n')[0]
    
    date_pattern = r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}" # 날짜를 추출하는 정규 표현식 패턴
    
    match = re.search(date_pattern, hand_date)

    FlopCard = []

    if match:
        extracted_date = match.group()
        
    for line in hand_data.split('\n'):
        if "Dealt to Hero" in line:
            hero_hand = line.split('[')[1].split(']')[0] # [Ad 5h]
        if "*** FLOP ***" in line:
            FlopCard = line.split('[')[1].split(']')[0] # [8h As 9d]

    hero_hands.append([extracted_date, hero_hand, FlopCard]) #날짜, 홀카드, 플랍

df = pd.DataFrame(hero_hands, columns=['Date', 'Hero Hand', 'FlopCard']) # DataFrame 생성
df['Date'] = pd.to_datetime(df['Date']) # 'Date' 열을 datetime 자료형으로 변환
df = df.sort_values(by='Date') # 날짜를 기준으로 DataFrame을 정렬

## 홀카드 + 플랍 조합 분석

Flop = df[df['FlopCard'].apply(len) > 0] # FlopCard값이 존재하면 추출

rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
rank_mapping = {'A': 0, 'K': 1, 'Q': 2, 'J': 3, 'T': 4, '9': 5, '8': 6, '7': 7, '6': 8, '5': 9, '4': 10, '3': 11, '2': 12}

Quads = np.zeros((13,13), dtype=int)
FullHouse = np.zeros((13,13), dtype=int)
Flush = np.zeros((13,13), dtype=int)
Straight = np.zeros((13,13), dtype=int)
Set = np.zeros((13,13), dtype=int)
Trips = np.zeros((13,13), dtype=int)
Onepair = np.zeros((13,13), dtype=int)
TwoPair = np.zeros((13,13), dtype=int)
OverPair = np.zeros((13,13), dtype=int)
TopPair = np.zeros((13,13), dtype=int)
MiddlePair = np.zeros((13,13), dtype=int)
LowPair = np.zeros((13,13), dtype=int)

HighCard = np.zeros((13,13), dtype=int)

FlushDraw = np.zeros((13,13), dtype=int)
Openended = np.zeros((13,13), dtype=int)
Gutshot = np.zeros((13,13), dtype=int)

for index, row in Flop.iterrows():

    Date = row['Date']
    Hand = row['Hero Hand']
    Flop = row['FlopCard']

    hand = Hand.split() # ['Ad', '2s']
    flop = Flop.split() # ['3d', '4h', '8h']

    hand_rank1, hand_rank2 = hand[0][0], hand[1][0] # ['A'] / ['2']
    hand_suit1, hand_suit2 = hand[0][1], hand[1][1] # ['d'] / ['s']

    flop_rank1, flop_rank2, flop_rank3 = flop[0][0], flop[1][0], flop[2][0] # ['3'] / ['4'] / ['8']
    flop_suit1, flop_suit2, flop_suit3 = flop[0][1], flop[1][1], flop[2][1] # ['d'] / ['h'] / ['h']
        
    ranks = [hand_rank1, hand_rank2, flop_rank1, flop_rank2, flop_rank3] # [3, A, Q, T, 7]
    suits = [hand_suit1, hand_suit2, flop_suit1, flop_suit2, flop_suit3] # [d, h, d, d, s]

    # 홀카드 좌표 인식
    if hand_suit1 == hand_suit2:
        x = min(rank_mapping[hand_rank1], rank_mapping[hand_rank2])
        y = max(rank_mapping[hand_rank1], rank_mapping[hand_rank2])
    else:
        x = max(rank_mapping[hand_rank1], rank_mapping[hand_rank2])
        y = min(rank_mapping[hand_rank1], rank_mapping[hand_rank2])

    ##풀하우스 판별
    if len(set(ranks)) == 2:
        FullHouse[x, y] += 1
        continue

    ##플러쉬 판별
    if len(set(suits)) == 1:
        Flush[x, y] += 1
        continue

    ##스트레이트 판별
    rank_numbers = [rank_values[rank] for rank in ranks]

    # rank_numbers 리스트에 A가 포함되어 있으면 1을 리스트에 추가
    if 14 in rank_numbers:
        rank_numbers.append(1)
    rank_numbers.sort()

    # 스트레이트 여부 확인
    consecutive_count = 0
    for i in range(len(rank_numbers) - 1):
        if rank_numbers[i] + 1 == rank_numbers[i + 1]:
            consecutive_count += 1
            if consecutive_count >= 4:
                Straight[x, y] += 1
        elif rank_numbers[i] != rank_numbers[i + 1]:
            consecutive_count = 0

    ##페어 확인

    hand_rank = [rank_values[hand_rank1], rank_values[hand_rank2]]
    flop_rank = [rank_values[flop_rank1], rank_values[flop_rank2], rank_values[flop_rank3]]

    #포켓일 경우
    if len(set(hand_rank)) == 1:
        if flop_rank.count(hand_rank[0]) == 0:
            sort = sorted(flop_rank + [hand_rank[0]], reverse=True)
            position = sort.index(hand_rank[0])
            if position == 0:
                OverPair[x, y] += 1
            elif position == 1:
                TopPair[x, y] += 1
            elif position == 2:
                MiddlePair[x, y] += 1
            elif position == 3:
                LowPair[x, y] += 1
        elif flop_rank.count(hand_rank[0]) == 1:
            Set[x, y] += 1
        elif flop_rank.count(hand_rank[0]) == 2:
            Quads[x, y] += 1
            
    #포켓이 아닐 경우
    from collections import Counter

    hand_flop_rank = hand_rank + flop_rank

    if len(set(hand_rank)) == 2:
        if len(set(flop_rank)) == 3 and len(set(hand_flop_rank)) == 5:
            HighCard[x, y] += 1
        if len(set(flop_rank)) == 3 and len(set(hand_flop_rank)) == 4:
            onepair = Counter(hand_flop_rank).most_common(1)
            sort = sorted(hand_flop_rank, reverse=True)
            position = sort.index(onepair[0][0])
            if position == 0:
                TopPair[x, y] += 1
            elif position == 1:
                MiddlePair[x, y] += 1
            elif position == 2:
                LowPair[x, y] += 1
        if len(set(flop_rank)) == 3 and len(set(hand_flop_rank)) == 3:
            TopPair[x, y] += 1
        if len(set(flop_rank)) == 2 and len(set(hand_flop_rank)) == 4:
            HighCard[x, y] += 1
        if len(set(flop_rank)) == 2 and len(set(hand_flop_rank)) == 3:
            trips = Counter(hand_flop_rank).most_common(1)
            if trips[0][1] == 3:
                Trips[x, y] += 1
            elif trips[0][1] == 2:
                Onepair[x, y] += 1
        if len(set(flop_rank)) == 1 and len(set(hand_flop_rank)) == 3:
            HighCard[x, y] += 1


    ##드로판별 투핸드 드로만 체크

    #플러쉬드로 판별
    hand_suit = [hand_suit1, hand_suit2]

    if len(set(hand_suit)) == 1 and len(set(suits)) == 2:
        FlushDraw[x, y] += 1

    #양차 판별
    rank_numbers = [rank_values[rank] for rank in ranks]

    # 양차 여부 확인
    consecutive_count = 0
    for i in range(len(rank_numbers) - 1):
        if 14 in rank_numbers: # A있으면 양차 불가능
            break

        if rank_numbers[i] + 1 == rank_numbers[i + 1]:
            consecutive_count += 1
            if consecutive_count >= 3:
                Openended[x, y] += 1
        elif rank_numbers[i] != rank_numbers[i + 1]:
            consecutive_count = 0

    #것샷 판별(비슷한거 포함)
    gutshot_list = [
        ['A','2','3','4'], ['A','2','3','5'], ['A','2','4','5'], ['A','3','4','5'],
        ['2','3','4','6'], ['2','3','5','6'], ['2','4','5','6'],
        ['3','4','5','7'], ['3','4','6','7'], ['3','5','6','7'],
        ['4','5','6','8'], ['4','5','7','8'], ['4','6','7','8'],
        ['5','6','7','9'], ['5','6','8','9'], ['5','7','8','9'],
        ['6','7','8','T'], ['6','7','9','T'], ['6','8','9','T'],
        ['7','8','9','J'], ['7','8','T','J'], ['7','9','T','J'],
        ['8','9','T','Q'], ['8','9','J','Q'], ['8','T','J','Q'],
        ['9','T','J','K'], ['9','T','Q','K'], ['9','J','Q','K'],
        ['T','J','Q','A'], ['T','J','K','A'], ['T','Q','K','A'], ['T','J','Q','K']
        ]

    hand_rank = [hand_rank1, hand_rank2]
    flop_rank = [flop_rank1, flop_rank2, flop_rank3]
    hand_flop_rank = hand_rank + flop_rank

    for gutshot in gutshot_list:
        if all(item in gutshot for item in hand_rank): #투핸드 것샷인지 판별
            if all(item in hand_flop_rank for item in gutshot):
                Gutshot[x, y] += 1
