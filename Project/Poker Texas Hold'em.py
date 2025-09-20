def poker():
    import random
    ranks = list(range(2,15))
    # suits = ['C','D','H','S']  #C -> Clubs, D-> Diamonds, H-> Hearts, S -> Spades
    ranks_string = {11: 'J',12: 'Q',13: 'K',14: 'A'}
    # suits_icon = {'C': '♣', 'D': '♦', 'H': '♥', 'S': '♠'}
    suits = ['♣','♦','♥','♠']

    CATEGORY_NAME = {
        10: "Royal Flush",
        9: "Straight Flush",
        8: "Four of a Kind",
        7: "Full House",
        6: "Flush",
        5: "Straight",
        4: "Three of a Kind",
        3: "Two Pair",
        2: "One Pair",
        1: "High Card",
    }

    # Pack of cards
    def new_pack():
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append((rank,suit))
        return deck
    pack_of_cards = new_pack()
    random.shuffle(pack_of_cards)
    #Card
    # a = random.choice(pack_of_cards)

    def card_str(card):
        r, s = card
        return f"{ranks_string.get(r, r)}{s}"

    def deal(n):
        return [pack_of_cards.pop() for _ in range(n)]
    your_cards = deal(2)
    # print(your_cards)
    bot_cards = deal(2)
    Flop = deal(3)
    Turn = deal(1)
    River = deal(1)

    # print(' - '.join(card_str(i)for i in your_cards)) -> Card output
    def show(x):
        y = (' - '.join(card_str(c) for c in x))
        return y
    ##Draw
    def ascii_card(rank, suit):
        suit_symbol = {
            '♠': '♠',
            '♥': '♥',
            '♦': '♦',
            '♣': '♣'
        }
        rank_str = {11: "J", 12: "Q", 13: "K", 14: "A"}.get(rank, str(rank))
        s = suit_symbol[suit]

        return [
            "┌───────┐",
            f"│{rank_str:<2}     │",
            f"│   {s}   │",
            f"│     {rank_str:>2}│",
            "└───────┘"
        ]

    def show_hand(cards):
        ascii_cards = [ascii_card(r, s) for (r, s) in cards]
        for row in zip(*ascii_cards):
            print("  ".join(row))

    # board = [show(Flop), show(Turn), show(River)]
    board = [Flop, Turn, River]
    street = []
    idx = -1
    #Main Gameplay
    print('[PRE-FLOP]')
    print('Your card: ')

    # print('Your cards: ',show(your_cards))
    show_hand(your_cards)
    while True:
        idx = idx + 1
        lst = ['FLOP', 'TURN', 'RIVER']
        for i in board[idx]:
            street.append(i)
        # street.append(board[idx])
        if input('Press enter to continue...: ') == '':

            print(f'{lst[idx]}')
            print('Your card: ')
            show_hand(your_cards)
            print('Board: ')
            show_hand(street)
            # print(f'Board: {street}')
            if idx == 2:
                break
    #Whole
    your_whole = your_cards + Flop + Turn + River
    # for i in your_cards:
    #     whole.append(i)
    # for i in Flop:
    #     whole.append(i)
    # for i in Turn:
    #     whole.append(i)
    # for i in River:
    #     whole.append(i)
    # print('whole=',your_whole)

    from collections import Counter

    ranks7 = [r for r, s in your_whole]
    suits7 = [s for r, s in your_whole]

    rc = Counter(ranks7)   #Count by rank
    sc = Counter(suits7)   #Count by suit
    # print('ranks7=',rc)
    # print('suits7=',sc)
    #Pair
    pair = [r for r, c in rc.items() if c >= 2]
    # print('pair=',pair)
    #Triple
    triple = [r for r,c in rc.items() if c >= 3]
    # print('triple=',triple)
    #Four of a Kind
    four = [r for r,c in rc.items() if c ==4]
    # print('four=',four)
    #Flush
    flush = [s for s,c in sc.items() if c >= 5]
    # print('flush=',flush)
    pairs = sorted([r for r,c in rc.items() if c == 2], reverse=True)
    trips = sorted([r for r,c in rc.items() if c == 3], reverse=True)
    # Straight
    r = []
    s = []
    for i in your_whole:
        a, b = i
        r.append(a)
        s.append(b)
    r = set(r)
    s = set(s)
    r = list(r)
    s = list(s)
    r.sort(reverse=True)

    # print('r=',r)
    def straight():
        for fs in flush:
            suit_ranks = sorted({rr for (rr, ss) in your_whole if ss == fs}, reverse=True) #To get the number with the same suit by flush
            for i in range(len(suit_ranks) - 4):
                w = suit_ranks[i:i + 5]
                if all(w[j] - 1 == w[j + 1] for j in range(4)):
                    if w[0] == 14:
                        return 'Royal Flush', 14, w
                    else:
                        return 'Straight Flush', w[0], w
        for i in range(len(r) - (5 - 1)):
            window = r[i:i + 5]
            if all(window[j] - 1 == window[j + 1] for j in range(4)):
                return 'Normal straight', window[0], window
        else:
                return 'Not Straight', r[0], r

    #Main mechanic of game
    ##What you got
    if straight()[0] == 'Royal Flush':
        Bool, High, Straight = straight()
        rank = 10,High
    elif straight()[0] == 'Straight Flush':
        Bool, High, Straight = straight()
        rank = 9, High
    elif len(four) >=1:
        rest = sorted(set(ranks7), reverse=True)
        rest.remove(four[0])
        kicker = rest[0]
        rank = 8, max(four), kicker
    elif len(trips) >= 2:
            rank = (7, trips[0], trips[1])  # Highest trips + Next Trips
    elif trips and pairs:
            rank = (7, trips[0], pairs[0])  # trips + Highest pair
    elif len(flush) >=1:
        for fs in flush:
            rank_in_fs = [r for (r, s) in your_whole if s == fs]
            rank_in_fs.sort(reverse=True)
            rank = 6, rank_in_fs[:5]
    elif straight()[0] == 'Normal straight':
        Bool, High, Straight = straight()
        rank = 5, High
    elif len(triple) >=1:
        rest = sorted(set(ranks7), reverse=True)
        rest.remove(triple[0])
        kicker = rest[:2]
        k1, k2 = kicker
        rank = 4, max(triple), k1, k2
    elif len(pair) >= 2:
        rest = sorted(set(ranks7), reverse=True)
        pair.sort(reverse=True)
        rest.remove(pair[0])
        rest.remove(pair[1])
        rank = 3, pair[0],pair[1],max(rest)
    elif len(pair) >= 1:
        rest = sorted(set(ranks7), reverse=True)
        rest.remove(pair[0])
        kicker = rest[:3]

        rank = 2, pair[0], kicker
    else:
        card = r[:5]
        rank = 1, card

    # print(50*'=')
    # print(f'Bot cards {show(bot_cards)}')
    ##What Bot Got
    #Bot Whole
    bot_whole = bot_cards + Flop + Turn + River

    # print('Bot whole=',bot_whole)

    from collections import Counter

    ranksbots7 = [r for r, s in bot_whole]
    suitsbots7 = [s for r, s in bot_whole]

    rcbot = Counter(ranksbots7)
    scbot = Counter(suitsbots7)
    # print('ranks7=',rcbot)
    # print('suits7=',scbot)
    #Pair
    pairbot = [r for r, c in rcbot.items() if c >= 2]
    # print('pairbot=',pairbot)
    #Triple
    triplebot = [r for r,c in rcbot.items() if c >= 3]
    # print('triplebot=',triplebot)
    #Four of a Kind
    fourbot = [r for r,c in rcbot.items() if c ==4]
    # print('fourbot=',fourbot)
    #Flush
    flushbot = [s for s,c in scbot.items() if c >= 5]
    # print('flushbot=',flushbot)
    pairsbot = sorted([r for r,c in rcbot.items() if c == 2], reverse=True)
    tripsbot = sorted([r for r,c in rcbot.items() if c == 3], reverse=True)
    # Straight
    rbot = []
    sbot = []
    for i in bot_whole:
        a, b = i
        rbot.append(a)
        sbot.append(b)
    rbot = set(rbot)
    sbot = set(sbot)
    rbot = list(rbot)
    sbot = list(sbot)
    rbot.sort(reverse=True)
    # print('r=',r)
    def straightbot():
        for fs in flushbot:
            suit_ranks = sorted({rr for (rr, ss) in bot_whole if ss == fs}, reverse=True)
            for i in range(len(suit_ranks) - 4):
                w = suit_ranks[i:i + 5]
                if all(w[j] - 1 == w[j + 1] for j in range(4)):
                    if w[0] == 14:
                        return 'Royal Flush', 14, w
                    else:
                        return 'Straight Flush', w[0], w
        for i in range(len(rbot) - (5 - 1)):
            window = rbot[i:i + 5]
            if all(window[j] - 1 == window[j + 1] for j in range(4)):
                return 'Normal straight', window[0], window
        else:
                return 'Not Straight', rbot[0], rbot
    if straightbot()[0] == 'Royal Flush':
        Bool, High, Straight = straightbot()
        rankbot = 10,High
    elif straightbot()[0] == 'Straight Flush':
        Bool, High, Straight = straightbot()
        rankbot = 9, High
    elif len(fourbot) >=1:
        rest = sorted(set(ranksbots7), reverse=True)
        rest.remove(fourbot[0])
        kicker = rest[0]
        rankbot = 8, max(fourbot), kicker
    elif len(tripsbot) >= 2:
            rankbot = (7, tripsbot[0], tripsbot[1])  # Highest trips + Next Trips
    elif tripsbot and pairsbot:
            rankbot = (7, tripsbot[0], pairsbot[0])  # trips + Highest pair
    elif len(flushbot) >=1:
        for fs in flushbot:
            rank_in_fs = [r for (r, s) in bot_whole if s == fs]
            rank_in_fs.sort(reverse=True)
            rankbot = 6, rank_in_fs[:5]
    elif straightbot()[0] == 'Normal straight':
        Bool, High, Straight = straightbot()
        rankbot = 5, High
    elif len(triplebot) >=1:
        rest = sorted(set(ranksbots7), reverse=True)
        rest.remove(triplebot[0])
        kicker = rest[:2]
        k1, k2 = kicker
        rankbot = 4, max(triplebot), k1, k2
    elif len(pairbot) >= 2:
        rest = sorted(set(ranksbots7), reverse=True)
        pairbot.sort(reverse=True)
        rest.remove(pairbot[0])
        rest.remove(pairbot[1])
        rankbot = 3, pairbot[0], pairbot[1], max(rest)
    elif len(pairbot) >= 1:
        rest = sorted(set(ranksbots7), reverse=True)
        rest.remove(pairbot[0])
        kicker = rest[:3]
        rankbot = 2, pairbot[0], kicker
    else:
        card = rbot[:5]
        rankbot = 1, card

    print(f'You have got a/an {CATEGORY_NAME.get(rank[0])}')
    print(f'Bot has got a/an {CATEGORY_NAME.get(rankbot[0])}')
    print(f'Bot Cards: {show(bot_cards)}')
    #Comparison
    if rank[0:] > rankbot[0:]:
        print("Congratulations! You won!")
    elif rank[0:] < rankbot[0:]:
        print("Hahahaha Loserrrr ")
    elif rank[0:] == rankbot[0:]:
        print('DRAWW')
    # print('rank =',rank)
    # print('rankbot=',rankbot)
    # show(bot_cards)
poker()


