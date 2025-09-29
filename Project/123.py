import random
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
your_whole = [(9,'♣'), (8,'♦'), (7,'♠'), (6,'♥'), (5,'♦'), (14,'♣'), (13,'♦')]
bot_whole =  [(9,'♣'), (8,'♦'), (7,'♠'), (6,'♥'), (5,'♦'), (14,'♣'), (13,'♦')]



print('whole=',your_whole)
from collections import Counter
ranks7 = [r for r, s in your_whole]
suits7 = [s for r, s in your_whole]
rc = Counter(ranks7)   # đếm theo rank
sc = Counter(suits7)   # đếm theo suit
print('rc= ',rc)
pair = [r for r, c in rc.items() if c >= 2]
print('pair=',pair)
triple = [r for r,c in rc.items() if c >= 3]
print('triple=',triple)
four = [r for r,c in rc.items() if c ==4]
print('four=',four)
flush = [s for s,c in sc.items() if c >= 5]
print('flush=',flush)
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

# r= [14, 13, 12, 11, 10, 7, 2]
# print('r=',r)
def straight():
    for i in range(len(r) - (5 - 1)):
        window = r[i:i + 5]
        if all(window[j] - 1 == window[j + 1] for j in range(4)):
            for fs in flush:
                    rank_in_fs = [r for (r, s) in your_whole if s == fs]
                    b = sorted(set(rank_in_fs), reverse=True)
                    if b == window and b[0] ==14:
                        return 'Royal Flush', b[0], b
                    elif b == window:
                        return 'Straight Flush', b[0], b
    for i in range(len(r) - (5 - 1)):
        window = r[i:i + 5]
        if all(window[j] - 1 == window[j + 1] for j in range(4)):
            return 'Normal straight', window[0], window
    else:
            return 'Not Straight', r[0], r
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
    rank = 8, four[0], kicker
elif len(triple) >=1 and len(pair) >=1:
    pair.remove(triple[0])
    rank = 7, triple[0], pair[0]
elif len(flush) >=1:
    for fs in flush:
        rank_in_fs = [r for (r, s) in your_whole if s == fs]
        rank_in_fs.sort(reverse=True)
        rank = 6, rank_in_fs
elif straight()[0] == 'Normal straight':
    Bool, High, Straight = straight()
    rank = 5, High
elif len(triple) >=1:
    rest = sorted(set(ranks7), reverse=True)
    rest.remove(triple[0])
    kicker = rest[:2]
    k1, k2 = kicker
    rank = 4, triple[0], k1, k2
elif len(pair) >= 2:
    rest = sorted(set(ranks7), reverse=True)
    rest.remove(pair[0])
    kicker = rest[0]
    pair.sort(reverse=True)
    rank = 3, pair[0],pair[1],kicker
elif len(pair) >= 1:
    rest = sorted(set(ranks7), reverse=True)
    rest.remove(pair[0])
    kicker = rest[:3]
    rank = 2, pair[0], kicker
else:
    card = r[:5]
    rank = 1, card
print(50*'=')

print('Bot whole=',bot_whole)
from collections import Counter
ranksbots7 = [r for r, s in bot_whole]
suitsbots7 = [s for r, s in bot_whole]
rcbot = Counter(ranksbots7)   # đếm theo rank
scbot = Counter(suitsbots7)   # đếm theo suit
pairbot = [r for r, c in rcbot.items() if c >= 2]
print('pairbot=',pairbot)
triplebot = [r for r,c in rcbot.items() if c >= 3]
print('triplebot=',triplebot)
fourbot = [r for r,c in rcbot.items() if c ==4]
print('fourbot=',fourbot)
flushbot = [s for s,c in scbot.items() if c >= 5]
print('flushbot=',flushbot)
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
def straightbot():
    for i in range(len(rbot) - (5 - 1)):
        window = rbot[i:i + 5]
        if all(window[j] - 1 == window[j + 1] for j in range(4)):
            for fsbot in flushbot:
                    rank_in_fs = [r for (r, s) in bot_whole if s == fsbot]
                    b = sorted(set(rank_in_fs), reverse=True)
                    if b == window and b[0] ==14:
                        return 'Royal Flush', b[0], b
                    elif b == window:
                        return 'Straight Flush', b[0], b
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
    rankbot = 8, four[0], kicker
elif len(triplebot) >=1 and len(pairbot) >=1:
    pairbot.remove(triplebot[0])
    rankbot = 7, triplebot[0], pairbot[0]
elif len(flushbot) >=1:
    for fs in flushbot:
        rank_in_fs = [r for (r, s) in bot_whole if s == fs]
        rank_in_fs.sort(reverse=True)
        rankbot = 6, rank_in_fs
elif straightbot()[0] == 'Normal straight':
    Bool, High, Straight = straightbot()
    rankbot = 5, High
elif len(triplebot) >=1:
    rest = sorted(set(ranksbots7), reverse=True)
    rest.remove(triplebot[0])
    kicker = rest[:2]
    k1, k2 = kicker
    rankbot = 4, triplebot[0], k1, k2
elif len(pairbot) >= 2:
    rest = sorted(set(ranksbots7), reverse=True)
    rest.remove(pairbot[0])
    kicker = rest[0]
    pairbot.sort(reverse=True)
    rankbot = 3, pairbot[0],pairbot[1],kicker
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

if rank[0] > rankbot[0]:
    print("Congratulations! You won!")
elif rank[0] < rankbot[0]:
    print("Hahahaha Loserrrr ")
elif rank[0] == rankbot[0]:
    if rank[0]==1:
        if rank[1]>rankbot[1]:
            print("Congratulations! You won!")
        elif rank[1]<rankbot[1]:
            print("Hahahaha Loserrrr ")
        elif rank[1]==rankbot[1]:
            print("Draw")
    elif rank[0]==2:
        if rank[1]>rankbot[1]:
            print("Congratulations! You won!")
        elif rank[1]<rankbot[1]:
            print("Hahahaha Loserrrr ")
        elif rank[1]==rankbot[1]:
            print("Draw")
    elif rank[0]==3:
        if rank[1:]>rankbot[1:]:
            print("Congratulations! You won!")
        elif rank[1:]<rankbot[1:]:
            print("Hahahaha Loserrrr ")
        elif rank[1:]==rankbot[1:]:
            print("Draw")
    elif rank[0]==4:
        if rank[1:]>rankbot[1:]:
            print("Congratulations! You won!")
        elif rank[1:]<rankbot[1:]:
            print("Hahahaha Loserrrr ")
        elif rank[1:]==rankbot[1:]:
            print("Draw")
    elif rank[0]==5:
        if rank[1]>rankbot[1]:
            print("Congratulations! You won!")
        elif rank[1]<rankbot[1]:
            print("Hahahaha Loserrrr ")
        elif rank[1]==rankbot[1]:
            print("Draw")
    elif rank[0]==6:
        if rank[1]>rankbot[1]:
            print("Congratulations! You won!")
        elif rank[1]<rankbot[1]:
            print("Hahahaha Loserrrr ")
        elif rank[1]==rankbot[1]:
            print("Draw")
    elif rank[0]==7:
        if rank[1:]>rankbot[1:]:
            print("Congratulations! You won!")
        elif rank[1:]<rankbot[1:]:
            print("Hahahaha Loserrrr ")
        elif rank[1:]==rankbot[1:]:
            print("Draw")
    elif rank[0]==8:
        if rank[1:]>rankbot[1:]:
            print("Congratulations! You won!")
        elif rank[1:]<rankbot[1:]:
            print("Hahahaha Loserrrr ")
        elif rank[1:]==rankbot[1:]:
            print("Draw")
    elif rank[0]==9:
        if rank[1:]>rankbot[1:]:
            print("Congratulations! You won!")
        elif rank[1:]<rankbot[1:]:
            print("Hahahaha Loserrrr ")
        elif rank[1:]==rankbot[1:]:
            print("Draw")
    elif rank[0]==10:
        if rank[0] == rankbot[0]:
            print("DRAW!")
        else:
            print('You win')

print(rank)
print(rankbot)
