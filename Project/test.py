import random
import itertools

# =========================
# CONFIG & MAPPINGS
# =========================
RANKS = list(range(2, 15))        # 2..14 (A=14)
SUITS = ['C', 'D', 'H', 'S']      # Clubs, Diamonds, Hearts, Spades

RANK_TO_STR = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
SUIT_TO_SYM = {'C': '♣', 'D': '♦', 'H': '♥', 'S': '♠'}

CATEGORY_NAME = {
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

SB = 5
BB = 10
STARTING_STACK = 200
BET_SMALL = 10   # preflop & flop
BET_BIG = 20     # turn & river


# =========================
# UTILITIES
# =========================
def card_str(card):
    r, s = card
    rtxt = RANK_TO_STR.get(r, str(r))
    return f"{rtxt}{SUIT_TO_SYM[s]}"

def hand_to_str(cards):
    return ' '.join(card_str(c) for c in cards)

def new_deck():
    return [(r, s) for r in RANKS for s in SUITS]

def deal(deck, n=1):
    return [deck.pop() for _ in range(n)]


# =========================
# HAND EVALUATION (5-CARD)
# =========================
def is_straight(ranks):
    r = sorted(set(ranks), reverse=True)
    if len(r) < 5:
        return False, None

    rset = set(r)
    # A-low: A,2,3,4,5
    if {14, 5, 4, 3, 2}.issubset(rset):
        return True, 5

    for i in range(len(r) - 4):
        window = r[i:i+5]
        if all(window[j] - 1 == window[j+1] for j in range(4)):
            return True, window[0]
    return False, None

def hand_rank_5(cards5):
    ranks = sorted([r for r, _ in cards5], reverse=True)
    suits = [s for _, s in cards5]

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    groups = sorted(((c, r) for r, c in counts.items()), reverse=True)
    counts_sorted = [c for c, r in groups]
    ranks_by_group = [r for c, r in groups]

    is_flush = len(set(suits)) == 1
    straight, straight_high = is_straight(ranks)

    if is_flush and straight:
        return (9, straight_high)

    if counts_sorted[0] == 4:
        four = ranks_by_group[0]
        kicker = max([r for r in ranks if r != four])
        return (8, four, kicker)

    if counts_sorted[0] == 3 and counts_sorted[1] >= 2:
        three = ranks_by_group[0]
        pair = ranks_by_group[1]
        return (7, three, pair)

    if is_flush:
        return (6, *sorted(ranks, reverse=True))

    if straight:
        return (5, straight_high)

    if counts_sorted[0] == 3:
        three = ranks_by_group[0]
        kickers = sorted([r for r in ranks if r != three], reverse=True)[:2]
        return (4, three, *kickers)

    if counts_sorted[0] == 2 and counts_sorted[1] == 2:
        p1 = ranks_by_group[0]
        p2 = ranks_by_group[1]
        high_pair, low_pair = max(p1, p2), min(p1, p2)
        kicker = max([r for r in ranks if r not in (p1, p2)])
        return (3, high_pair, low_pair, kicker)

    if counts_sorted[0] == 2:
        pair = ranks_by_group[0]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)[:3]
        return (2, pair, *kickers)

    return (1, *sorted(ranks, reverse=True))

def best_hand_from_seven(seven_cards):
    best_rank = None
    best_combo = None
    for comb in itertools.combinations(seven_cards, 5):
        rank = hand_rank_5(list(comb))
        if best_rank is None or rank > best_rank:
            best_rank = rank
            best_combo = list(comb)
    return best_rank, best_combo

def describe_rank(rank_tuple):
    cat = rank_tuple[0]
    if cat == 9:
        high = rank_tuple[1]
        if high == 14: return "Royal Flush (Sảnh hoàng gia)"
        return f"Straight Flush, high {RANK_TO_STR.get(high, str(high))} (Sảnh đồng chất)"
    if cat == 8:
        return f"Four of a Kind ({RANK_TO_STR.get(rank_tuple[1], str(rank_tuple[1]))}x4) (Tứ quý)"
    if cat == 7:
        three, pair = rank_tuple[1], rank_tuple[2]
        return f"Full House ({RANK_TO_STR.get(three, str(three))} over {RANK_TO_STR.get(pair, str(pair))}) (Cù lũ)"
    if cat == 6:
        return "Flush (Thùng)"
    if cat == 5:
        return f"Straight, high {RANK_TO_STR.get(rank_tuple[1], str(rank_tuple[1]))} (Sảnh)"
    if cat == 4:
        return f"Three of a Kind ({RANK_TO_STR.get(rank_tuple[1], str(rank_tuple[1]))}) (Bộ ba)"
    if cat == 3:
        hp, lp = rank_tuple[1], rank_tuple[2]
        return f"Two Pair ({RANK_TO_STR.get(hp, str(hp))} & {RANK_TO_STR.get(lp, str(lp))}) (Hai đôi)"
    if cat == 2:
        pr = rank_tuple[1]
        return f"One Pair ({RANK_TO_STR.get(pr, str(pr))}) (Một đôi)"
    return "High Card (Bài cao)"


# =========================
# SIMPLE GAME STATE
# =========================
class Player:
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hole = []
        self.in_hand = True

    def bet(self, amount):
        amount = max(0, min(amount, self.stack))
        self.stack -= amount
        return amount


# =========================
# BOT (fixed: safe preflop logic)
# =========================
def bot_decide_action(street, board, bot_hole, has_bet, call_amount, bet_size):
    """
    Trả ('fold'|'check'|'call'|'bet').
    - Preflop (board < 3): dùng heuristic đơn giản, KHÔNG gọi evaluator 7 lá.
    - Từ flop trở đi: dùng evaluator (đủ ≥5 lá).
    """
    rand = random.random()

    # PRE-FLOP (và mọi trường hợp board < 3)
    if len(board) < 3:
        r1, s1 = bot_hole[0]
        r2, s2 = bot_hole[1]
        pair = (r1 == r2)
        suited = (s1 == s2)
        high = max(r1, r2)

        # Ước lượng "category" thô: đôi coi như One Pair (2), ngược lại High Card (1)
        category = 2 if pair else 1

        if has_bet:
            # Đối thủ đã bet
            if pair:
                return 'call'                 # có đôi → call
            if high >= 13 and rand < 0.35:    # A/K-high đôi lúc call nhỏ
                return 'call'
            return 'fold'                      # rác → fold đa số
        else:
            # Chưa ai bet
            if pair:
                return 'bet' if rand < 0.8 else 'check'
            if suited and high >= 12 and rand < 0.3:
                return 'bet'                   # thỉnh thoảng mở bet
            return 'check'

    # POSTFLOP (flop/turn/river): có ≥5 lá để đánh giá
    seven = bot_hole + board
    rank, _ = best_hand_from_seven(seven)
    category = rank[0]

    if has_bet:
        if category >= 2:
            return 'call'
        else:
            # thỉnh thoảng float ở flop
            if len(board) == 3 and rand < 0.15:
                return 'call'
            return 'fold'
    else:
        if category >= 2:
            return 'bet' if rand < 0.8 else 'check'
        else:
            if len(board) == 3 and rand < 0.1:
                return 'bet'
            return 'check'


# =========================
# BETTING ROUND (one-bet max per street)
# =========================
def betting_round(human_first, human: Player, bot: Player, pot, street, board):
    """
    Luật đơn giản:
    - Mỗi street tối đa 1 lần bet (không raise).
    - Người A hành động trước: check hoặc bet (bet_size cố định).
    - Nếu bet: người B chỉ có call hoặc fold.
    - Nếu check: người B có thể bet hoặc check; nếu bet -> A call hoặc fold.
    """
    bet_size = BET_SMALL if street in ('preflop', 'flop') else BET_BIG

    def ask_human_action(options):
        while True:
            ans = input(f"Chọn hành động ({'/'.join(options)}): ").strip().lower()
            if ans in options:
                return ans
            print("Nhập không hợp lệ.")

    def human_move_first():
        nonlocal pot
        print(f"\n[{street.upper()}] Bạn hành động trước. Pot={pot}, Stack bạn={human.stack}, Bot={bot.stack}")
        print(f"Bài bạn: {hand_to_str(human.hole)}")
        if board:
            print(f"Board: {hand_to_str(board)}")

        act = ask_human_action(['check', 'bet'])
        if act == 'bet':
            amt = human.bet(bet_size)
            pot += amt
            print(f"Bạn BET {amt}. Pot={pot}")
            bot_act = bot_decide_action(street, board, bot.hole, has_bet=True, call_amount=bet_size, bet_size=bet_size)
            if bot_act == 'call':
                call_amt = bot.bet(min(bet_size, bot.stack + 0))
                pot += call_amt
                print(f"Bot CALL {call_amt}. Pot={pot}")
                return pot, False
            else:
                print("Bot FOLD. Bạn thắng pot!")
                human.stack += pot
                return pot, True
        else:
            print("Bạn CHECK.")
            bot_act = bot_decide_action(street, board, bot.hole, has_bet=False, call_amount=0, bet_size=bet_size)
            if bot_act == 'bet':
                amt = bot.bet(bet_size)
                pot += amt
                print(f"Bot BET {amt}. Pot={pot}")
                act2 = ask_human_action(['call', 'fold'])
                if act2 == 'call':
                    call_amt = human.bet(min(bet_size, human.stack + 0))
                    pot += call_amt
                    print(f"Bạn CALL {call_amt}. Pot={pot}")
                    return pot, False
                else:
                    print("Bạn FOLD. Bot ăn pot.")
                    bot.stack += pot
                    return pot, True
            else:
                print("Bot CHECK.")
                return pot, False

    def bot_move_first():
        nonlocal pot
        print(f"\n[{street.upper()}] Bot hành động trước. Pot={pot}, Stack bạn={human.stack}, Bot={bot.stack}")
        print(f"Bài bạn: {hand_to_str(human.hole)}")
        if board:
            print(f"Board: {hand_to_str(board)}")

        bot_act = bot_decide_action(street, board, bot.hole, has_bet=False, call_amount=0, bet_size=bet_size)
        if bot_act == 'bet':
            amt = bot.bet(bet_size)
            pot += amt
            print(f"Bot BET {amt}. Pot={pot}")
            act = ask_human_action(['call', 'fold'])
            if act == 'call':
                call_amt = human.bet(min(bet_size, human.stack + 0))
                pot += call_amt
                print(f"Bạn CALL {call_amt}. Pot={pot}")
                return pot, False
            else:
                print("Bạn FOLD. Bot ăn pot.")
                bot.stack += pot
                return pot, True
        else:
            print("Bot CHECK.")
            act = ask_human_action(['check', 'bet'])
            if act == 'bet':
                amt = human.bet(bet_size)
                pot += amt
                print(f"Bạn BET {amt}. Pot={pot}")
                bot_act2 = bot_decide_action(street, board, bot.hole, has_bet=True, call_amount=bet_size, bet_size=bet_size)
                if bot_act2 == 'call':
                    call_amt = bot.bet(min(bet_size, bot.stack + 0))
                    pot += call_amt
                    print(f"Bot CALL {call_amt}. Pot={pot}")
                    return pot, False
                else:
                    print("Bot FOLD. Bạn thắng pot!")
                    human.stack += pot
                    return pot, True
            else:
                print("Bạn CHECK.")
                return pot, False

    if human_first:
        return human_move_first()
    else:
        return bot_move_first()


# =========================
# ONE HAND (HEADS-UP)
# =========================
def play_hand(human: Player, bot: Player, dealer_is_human=True):
    deck = new_deck()
    random.shuffle(deck)

    human.in_hand = True
    bot.in_hand = True

    # Blinds
    pot = 0
    if dealer_is_human:
        pot += human.bet(SB)
        pot += bot.bet(BB)
        print(f"\n--- Hand mới (Bạn là Dealer). SB={SB}, BB={BB} ---")
    else:
        pot += bot.bet(SB)
        pot += human.bet(BB)
        print(f"\n--- Hand mới (Bot là Dealer). SB={SB}, BB={BB} ---")

    # Deal hole cards
    human.hole = deal(deck, 2)
    bot.hole = deal(deck, 2)

    # Preflop: Dealer acts first trong heads-up
    street = 'preflop'
    human_first = dealer_is_human
    pot, ended = betting_round(human_first, human, bot, pot, street, board=[])
    if ended:
        return

    # Flop
    flop = deal(deck, 3)
    board = flop[:]
    street = 'flop'
    human_first = not dealer_is_human
    print(f"\n=== FLOP: {hand_to_str(flop)} ===")
    pot, ended = betting_round(human_first, human, bot, pot, street, board)
    if ended:
        return

    # Turn
    turn = deal(deck, 1)
    board += turn
    street = 'turn'
    print(f"\n=== TURN: {hand_to_str(turn)} | Board: {hand_to_str(board)} ===")
    pot, ended = betting_round(human_first, human, bot, pot, street, board)
    if ended:
        return

    # River
    river = deal(deck, 1)
    board += river
    street = 'river'
    print(f"\n=== RIVER: {hand_to_str(river)} | Board: {hand_to_str(board)} ===")
    pot, ended = betting_round(human_first, human, bot, pot, street, board)
    if ended:
        return

    # Showdown
    hrank, hbest = best_hand_from_seven(human.hole + board)
    brank, bbest = best_hand_from_seven(bot.hole + board)
    print("\n--- SHOWDOWN ---")
    print(f"Board: {hand_to_str(board)}")
    print(f"Bạn: {hand_to_str(human.hole)} | Best: {hand_to_str(hbest)} -> {describe_rank(hrank)} ({hrank})")
    print(f"Bot : {hand_to_str(bot.hole)} | Best: {hand_to_str(bbest)} -> {describe_rank(brank)} ({brank})")

    if hrank > brank:
        print(f"==> Bạn THẮNG pot {pot}!")
        human.stack += pot
    elif brank > hrank:
        print(f"==> Bot THẮNG pot {pot}.")
        bot.stack += pot
    else:
        share = pot // 2
        human.stack += share
        bot.stack += pot - share
        print(f"==> HÒA, chia pot: Bạn +{share}, Bot +{pot - share}.")


# =========================
# MAIN LOOP
# =========================
def main():
    print("Texas Hold'em — 1v1: Bạn vs Bot (console)")
    print("Luật cược đơn giản: mỗi street tối đa 1 lần bet, không raise.\n")

    human = Player("You", STARTING_STACK)
    bot = Player("Bot", STARTING_STACK)

    dealer_is_human = True  # Bạn là dealer ván đầu; sau đó luân phiên

    while True:
        if human.stack <= 0:
            print("\nBạn đã hết chip. GG!")
            break
        if bot.stack <= 0:
            print("\nBot đã hết chip. Bạn WIN!")
            break

        print(f"\nStacks: Bạn={human.stack}, Bot={bot.stack}")
        play_hand(human, bot, dealer_is_human=dealer_is_human)
        dealer_is_human = not dealer_is_human

        while True:
            ans = input("\nChơi tiếp? (y/n): ").strip().lower()
            if ans in ('y', 'n'):
                break
            print("Nhập 'y' hoặc 'n'.")
        if ans == 'n':
            break

    print(f"\nKết thúc. Final stacks: Bạn={human.stack}, Bot={bot.stack}")
    print("Cảm ơn đã chơi!")


if __name__ == "__main__":
    main()
