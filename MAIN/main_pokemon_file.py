import random
from all_pokemon_list import Arceus
from all_pokemon_list import NU_Poke
from all_pokemon_list import OU_Poke
from all_pokemon_list import Uber_Poke

# test02.poker()

arceus_list = [Arceus]
wild_poke = []
evil_poke = []
class Human:
    def __init__(self, name: str, rank: str):
        self.name = name
        self.rank = rank
        self.health = 100
        self.team = []
        self.exclude = set()
        self.team_p = []
        self.exclude_p = set()
        if rank == "intern":
            for team_no in range(1):
                available_poke = []
                for poke in NU_Poke:
                    if poke not in self.exclude:
                        available_poke.append(poke)
                poke = random.choice(available_poke)
                self.team.append(poke)
                self.exclude.add(poke)
                evil_poke.append(poke)
        elif rank == "grunt":
            for team_no in range(2):
                available_poke = []
                for poke in NU_Poke:
                    if poke not in self.exclude:
                        available_poke.append(poke)
                poke = random.choice(available_poke)
                self.team.append(poke)
                self.exclude.add(poke)
                evil_poke.append(poke)
        elif rank == "manager":
            for team_no in range(3):
                available_poke = []
                for poke in OU_Poke:
                    if poke not in self.exclude:
                        available_poke.append(poke)
                poke = random.choice(available_poke)
                self.team.append(poke)
                self.exclude.add(poke)
                evil_poke.append(poke)
        elif rank == "exec":
            for team_no in range(6):
                uber_rate = random.randint(1,2)
                available_poke = []
                if uber_rate == 1:
                    for poke in Uber_Poke:
                        if poke not in self.exclude:
                            available_poke.append(poke)
                    poke = random.choice(available_poke)
                    self.team.append(poke)
                    self.exclude.add(poke)
                    evil_poke.append(poke)
                else:
                    for poke in OU_Poke:
                        if poke not in self.exclude:
                            available_poke.append(poke)
                    poke = random.choice(available_poke)
                    self.team.append(poke)
                    self.exclude.add(poke)
                    evil_poke.append(poke)


    def capture(self, pokemon):
        self.team.append(pokemon)
def into_team(player, opo, wild):
    """
    The inner function used for stealing or capturing Pokemon, the function
    creates a loop until you enter 0 that allows you to move the opposing
    pokemon into your team, and moves excess Pokemon into the wild list
    :param player: player
    :param opo: opponent whose team to check, write None if capturing wild Pokemon
    :param wild: wild pokemon, write None if battling human NPC
    :return: None
    """
    if wild == None:
        while True:
            print("Which Pokemon would you like to add to your team?")
            for index_o, poke_o in enumerate(opo.team):
                print(f"{index_o + 1}. {poke_o.name}")
            print(f"0. End")
            user_input_opo = input("Select your choice: ")
            try:
                test_1 = int(user_input_opo)
            except ValueError:
                print("Invalid input")
                continue
            if 0 < int(user_input_opo) <= len(opo.team):
                print("Which Pokemon from your team would you like to release?")
                for index_p, poke_p in enumerate(player.team):
                    print(f"{index_p + 1}. {poke_p.name}")
                print(f"0. End")
                user_input_player = input("Select your choice: ")
                try:
                    test_01 = int(user_input_player)
                except ValueError:
                    print("Invalid input")
                    continue
                if 0 < int(user_input_player) <= len(player.team):
                    player.team[int(user_input_player) - 1] = opo.team[int(user_input_opo) - 1]
                    opo.team.remove(opo.team[int(user_input_opo) - 1])
                    wild_poke.append(player.team[int(user_input_player) - 1])
                elif int(user_input_player) == 0:
                    print("Stealing ended")
                    break
                else:
                    print("Invalid input")
            elif int(user_input_opo) == 0:
                print("Stealing ended")
                break
            else:
                print("Invalid input")
    elif opo == None:
        while True:
            print("Which Pokemon from your team would you like to release?")
            for index_p, poke_p in enumerate(player.team):
                print(f"{index_p + 1}. {poke_p.name}")
            print(f"0. End")
            user_input_player = input("Select your choice: ")
            try:
                test_01 = int(user_input_player)
            except ValueError:
                print("Invalid input")
                continue
            if 0 < int(user_input_player) <= len(player.team):
                player.team[int(user_input_player) - 1] = wild
                wild_poke.remove(wild)
                wild_poke.append(player.team[int(user_input_player) - 1])
                break
            elif int(user_input_player) == 0:
                print("Capture ended")
                break
            else:
                print("Invalid input")
Ethan = Human("Ethan", "player")
Sam = Human("Sam", "exec")
Meeri = Human("Meeri", "intern")
Saara = Human("Saara", "grunt")
Kari = Human("Kari", "exec")
# into_team(Ethan, Sam, None)
def show_poke(player):
    for poke in player.team:
        print(f"{poke.name}")
