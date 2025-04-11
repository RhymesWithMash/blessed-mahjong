# Math modeling final project: MAHJONG
# 12.10.2024
# Will Sullivan

import random
from collections import Counter
from tqdm import tqdm

yonma_tiles = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', # sou
               'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', # pin
               'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', # man
               'n0', 'e0', 'z0', 'w0', 'r0', 'g0', 'w0']             # honors

sanma_tiles = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', # sou
               'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', # pin
               'm1', 'm9',                                           # man
               'n0', 'e0', 'z0', 'w0', 'r0', 'g0', 'w0']             # honors

kokushi_musou = {'s1', 's9', 'p1', 'p9', 'm1', 'm9', 'n0', 'e0', 'z0', 'w0', 'r0', 'g0', 'w0'}

def main():
    iterations = 500_000
    # stats = simulate_sanma_sp(iterations)
    # print(stats)

    # hand = ['p2', 'p3', 'p4',      'p3', 'p4', 'p5',      'p6', 'p7', 'p8',       's6', 's9',    's7', 's8', 's9']

    # print(can_call_riichi_yonma(hand))

    tenhous = simulate_sanma_sp(iterations)

    print(tenhous)

# Loops simulate_yonma_round
def simulate_many_yonma_rounds(iterations):
    stats = {"tenhou": 0,
             "chiihou": 0,
             "renhou": 0,
             "none": 0}
    
    for _ in tqdm(range(iterations)):
        result = simulate_yonma_round()
        stats.update({result: stats[result] + 1})

    return stats

# Loops simulate_sanma_round
def simulate_many_sanma_rounds(iterations):
    stats = {"tenhou": 0,
             "chiihou": 0,
             "renhou": 0,
             "none": 0}
    
    for _ in tqdm(range(iterations)):
        result = simulate_sanma_round()
        stats.update({result: stats[result] + 1})

    return stats

# Simulates the first round of a 4 player game
def simulate_yonma_round():
    players = [[], [], [], []]
    wall = generate_yonma_wall()
    
    # Deal 13 tiles to each player
    for i in range(4):
        players[i] = wall[:13]
        del wall[:13]
    
    for i in range(len(players)): # let each player take a turn
        draw = wall.pop()
        for j in range(i, len(players)): # for each player that has not gone yet (including the player who is taking their turn)
            players[j].append(draw)      # give the opportunity to call ron (to get renhou)
            if check_valid_hand(players[j]):
                if(i == j):                # if it's a someone's turn and they are the one to get the valid hand, it's chiihou
                    if(i == 0):            # unless it's the dealer, then it's tenhou
                        # print("TH")
                        return "tenhou"
                    # print("CH")
                    return "chiihou"
                else:                      # if someone else's hand is completed by a discard, it's renhou
                    # print("RH")
                    return "renhou"
            players[j].remove(draw)
    return "none"

# Simulates the first round of a 3 player game.
def simulate_sanma_round():
    players = [[], [], []]

    wall = generate_sanma_wall()
    
    # Deal 13 tiles to each player
    for i in range(3):
        players[i] = wall[:13]
        del wall[:13]
    
    for i in range(len(players)): # let each player take a turn
        draw = wall.pop()
        for j in range(i, len(players)): # for each player that has not gone yet (including the player who is taking their turn)
            players[j].append(draw)      # give the opportunity to call ron (to get renhou)
            if check_valid_hand(players[j]):
                if(i == j):                # if it's a someone's turn and they are the one to get the valid hand, it's chiihou
                    if(i == 0):            # unless it's the dealer, then it's tenhou
                        # print("TH")
                        return "tenhou"
                    # print("CH")
                    return "chiihou"
                else:                      # if someone else's hand is completed by a discard, it's renhou
                    # print("RH")
                    return "renhou"
            players[j].remove(draw)
    return "none"

# Simulates drawing sanma tiles and checks for valid hands ("single player")
def simulate_sanma_sp(iterations):
    tenhous = 0

    for _ in tqdm(range(iterations), leave = False):
        wall = generate_sanma_wall()

        player_hand = random.sample(wall, 14)
        player_hand.sort()
        if(can_call_riichi_sanma(player_hand)):
            tenhous += 1
    
    return tenhous

# Simulates drawing yonma tiles and checks for valid hands ("single player")
def simulate_yonma_sp(iterations):
    tenhous = 0

    for _ in tqdm(range(iterations), leave = False):
        wall = generate_yonma_wall()

        player_hand = random.sample(wall, 14)
        player_hand.sort()
        if(can_call_riichi_yonma(player_hand)):
            tenhous += 1
    
    return tenhous

def generate_yonma_wall():
    wall = []
    for _ in range(4):
        wall.extend(yonma_tiles)
    random.shuffle(wall)
    return wall

def generate_sanma_wall():
    wall = []
    for _ in range(4):
        wall.extend(sanma_tiles)
    random.shuffle(wall)
    return wall

# Check if any tiles repeat more than n times (used in generate_valid_hand())
def tile_occurs_more_than_n_times(hand, n):
    counts = Counter(hand)
    return any(count > n for count in counts.values())

# Used for testing check_valid_hand()
def generate_valid_hand():
    hand = []
    suits = ["s", "p", "m"]
    nums = ['1', '2', '3', '4', '5', '6', '7']
    for i in range(4):
        suit = random.choice(suits)
        num = random.choice(nums)
        hand.append(suit + num)
        if(random.random() < 0.5):
            hand.append(suit + num)
            hand.append(suit + num)
        else:
            inc = str(int(num) + 1)
            hand.append(suit + inc)
            inc = str(int(inc) + 1)
            hand.append(suit + inc)

    suit = random.choice(suits)
    num = random.choice(nums)

    hand.append(suit + num)
    hand.append(suit + num)

    if(tile_occurs_more_than_n_times(hand, 4)): # if you make an impossible hand, regenerate
        hand = generate_valid_hand()
        
    return hand

# Checks if a 14-tile hand fits the fomat of 4 melds plus a pair
def check_valid_hand(hand):
    hand.sort()
    if(check_chiitoitsu(hand) or check_kokushi(hand)): return True
    
    triplet_blocks = []
    
    for i in range(len(hand)):
        working_hand = hand[:]   # reset hand
        try:
            pair_block, remainder = find_pair(working_hand, i)
        except LookupError: # pair not found
            return False
        

        triplet_blocks = []
        for i in range(4):
            try:
                block, remainder = split_block(remainder)
            except KeyError:
                break
            triplet_blocks.append(block)
        
        if(len(triplet_blocks) == 4):
            return True
    return False

# Searches a hand for pairs, starting from start_index
def find_pair(hand, start_index):
    possible_remainder_sets = [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
    pair_block = []

    hand_sum = sum(int(tile[1]) for tile in hand)
    remainder_set = possible_remainder_sets[hand_sum % 3]

    for i in range(start_index, len(hand) - 1): # sliding window!
        for rem in remainder_set:
            if int(hand[i][1]) == rem and int(hand[i + 1][1]) == rem and hand[i][0] == hand[i+1][0]: 
                pair_block = [hand.pop(i), hand.pop(i)]
                break
        else:
            continue
        break

    if(len(pair_block) == 0):
        raise LookupError("Pair not found!")

    return pair_block, hand

# Assumes a block exists to be split off. Otherwise, raises a KeyError.
def split_block(hand):
    for i in range(len(hand) - 2): # start with the lowest value
        if(hand.count(hand[i]) >= 3): # if it occurs three or more times, it must be in a triplet
            # Split a triplet
            tile1 = hand[i]
            tile2 = hand[i + 1]
            tile3 = hand[i + 2]

            if(tile1 == tile2 and tile1 == tile3): # triplet
                return [hand.pop(i), hand.pop(i), hand.pop(i)], hand
        else: # otherwise, it must be the start of a sequence
            # Split a sequence
            tile1 = hand[i]
            tile2 = tile1[0] + str(int(tile1[1]) + 1)
            tile3 = tile2[0] + str(int(tile2[1]) + 1)
            if tile2 in hand and tile3 in hand:
                hand.remove(tile1)
                hand.remove(tile2)
                hand.remove(tile3)
                return [tile1, tile2, tile3], hand

    raise KeyError("Unable to split off a block.")

# Checks if a hand is chiitoitsu
def check_chiitoitsu(hand):
    i = 0
    while(i < 13):
        j = i + 1
        if(hand[i] != hand[j]):
            return False
        i += 2
    return True

# Checks if a hand is kokushi musou
def check_kokushi(hand):
    hand_set = set(hand)
    return hand_set == kokushi_musou

# HERE LIES MY VALIANT ATTEMPT AT CHECKING FOR DOUBLE RIICHI IN AN EFFICIENT MANNER. 
# I TRIED FOR HOURS BEFORE RESIGNING TO THE SIMPLE BRUTE FORCE SOLUTION.
# RIP EFFICIENCY
[
# def check_double_riichi(hand):
#     def analyze_last_three(remainder):
#         if(len(remainder) > 3):
#             return False

#         # If we have a pair
#         if remainder[0] == remainder[1] or remainder[1] == remainder[2]: # no need to check if 0 != 2 because the hand is sorted
#             return True
#         # If we have two consecutive tiles or separated by 1
#         if are_consecutive_tiles(remainder[0], remainder[1]) or are_consecutive_tiles(remainder[1], remainder[2]): # same deal as above if statement
#             return True

#         # If we don't have either, then we dont have a wait
#         return False

#     hand.sort()
#     triplet_blocks = []
    
#     for i in range(len(hand)):
#         # First, look for tanki wait
#         working_hand = hand[:]   # reset hand
#         try:
#             pair_block, remainder = find_pair_stupid(working_hand, i)
#         except LookupError: # pair not found, therefore we must have tanki wait with all sequences (or invalid)
#             for i in range(4):
#                 try:
#                     block, remainder = split_block(working_hand)
#                 except KeyError:
#                     return False # no pair and no blocks. invalid
#                 triplet_blocks.append(block)
#             return True # if we get here, we've found 4 sequences, therefore the last two make a tanki wait. valid!

#         # If we reach this code, we have a pair. Try to make 3 triplets out of 4
#         triplet_blocks = []
#         for i in range(3):
#             try:
#                 block, remainder = split_block_dr(remainder)
#             except KeyError:
#                 continue # move on
#             triplet_blocks.append(block)
        
#         if(analyze_last_three(remainder)):
#             return True
#     return False

# def are_consecutive_tiles(tile1, tile2):
#     if tile1[0] != tile2[0]: return False
#     if int(tile1[1]) + 1 == int(tile2[1]): return True
#     if int(tile1[1]) - 1 == int(tile2[1]): return True
#     if int(tile1[1]) + 2 == int(tile2[1]): return True
#     if int(tile1[1]) - 2 == int(tile2[1]): return True
#     return False

# def split_block_dr(hand):
#     for i in range(len(hand) - 2): # start with the lowest value
#         if(hand.count(hand[i]) >= 3): # if it occurs three or more times, it must be in a triplet
#             # Split a triplet
#             tile1 = hand[i]
#             tile2 = hand[i + 1]
#             tile3 = hand[i + 2]
#             if(tile1 == tile2 and tile1 == tile3): # triplet
#                 return [hand.pop(i), hand.pop(i), hand.pop(i)], hand
#         else:
#             # Split a sequence
#             tile1 = hand[i]
#             tile2 = tile1[0] + str(int(tile1[1]) + 1)
#             tile3 = tile2[0] + str(int(tile2[1]) + 1)
#             if(tile1 in hand and tile2 in hand and tile3 in hand):
#                 hand.remove(tile1)
#                 hand.remove(tile2)
#                 hand.remove(tile3)
#                 return [tile1, tile2, tile3], hand

#     raise KeyError("Unable to split off a block.")

# def find_pair_stupid(hand, start_index):
#     pair_block = []

#     for i in range(start_index, len(hand) - 1): # sliding window!
#         if int(hand[i][1]) == int(hand[i + 1][1]) and hand[i][0] == hand[i+1][0]:
#             pair_block = [hand.pop(i), hand.pop(i)]
#             break
    
#     if(len(pair_block) == 0):
#         raise LookupError("Pair not found!")
    
#     return pair_block, hand
]

# Checks if a 13-tile hand is tenpai (yonma)
def is_tenpai_yonma(hand):
    for tile in yonma_tiles:  # Simulate drawing each possible tile
        temp_hand = hand.copy()
        temp_hand.append(tile)
        if check_valid_hand(temp_hand):
            return True  # The hand can win by drawing this tile
    return False

# Checks if a 13-tile hand is tenpai (sanma)
def is_tenpai_sanma(hand):
    for tile in sanma_tiles:  # Simulate drawing each possible tile
        temp_hand = hand.copy()
        temp_hand.append(tile)
        if check_valid_hand(temp_hand):
            return True  # The hand can win by drawing this tile
    return False

# Checks if a sanma hand can call riichi
def can_call_riichi_sanma(hand):    
    for tile in set(hand):  # Test each possible tile to discard
        temp_hand = hand.copy()
        temp_hand.remove(tile)  # Remove one tile
        if is_tenpai_sanma(temp_hand):
            return True  # If hand becomes tenpai after discarding one tile
    return False

# Checks if a yonma hand can call riichi
def can_call_riichi_yonma(hand):    
    for tile in set(hand):  # Test each possible tile to discard
        temp_hand = hand.copy()
        temp_hand.remove(tile)  # Remove one tile
        if is_tenpai_yonma(temp_hand):
            return True  # If hand becomes tenpai after discarding one tile
    return False

main()