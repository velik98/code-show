from collections import deque
from random import randint
from random import choice
from copy import deepcopy

def print_skills(skills):
    for i in range(len(skills)):
        print(str(i) + ".", skills[i])

class Room:
    def __init__(self, monsters):
        self.monsters = monsters

    def is_empty(self):
        return not self.monsters


class Game:
    #   Handles the game.
    def __init__(self, hero, difficulty, monsters, weapons):
        self.hero = hero
        self.difficulty = difficulty
        self.monsters = monsters
        self.weapons = weapons
        self.rooms = self.generate_rooms()

    def generate_rooms(self):
        #  How much rooms and monsters in room?
        difficulty_dict = {
            "e" : { "rooms" : 4, "minmonsters" : 1, "maxmonsters" : 1 },
            "m" : { "rooms" : 6, "minmonsters" : 1, "maxmonsters" : 2 },
            "h" : { "rooms" : 8, "minmonsters" : 2, "maxmonsters" : 3 }
        }
        rooms_count = difficulty_dict[self.difficulty]["rooms"]
        rooms_deque = deque(maxlen = rooms_count)
        for _ in range(rooms_count):
            minmonsters = difficulty_dict[self.difficulty]["minmonsters"]
            maxmonsters = difficulty_dict[self.difficulty]["maxmonsters"]
            room = self.generate_room(minmonsters, maxmonsters)
            rooms_deque.append(room)
        return rooms_deque

    def generate_room(self, minmonsters, maxmonsters):
        #   Prepares room filled with monsters
        monsters = []
        for _ in range(randint(minmonsters, maxmonsters)):
            random_monster = deepcopy(choice(self.monsters))
            while random_monster in monsters:
                 random_monster = deepcopy(choice(self.monsters))
            monsters.append(random_monster)
        return Room(monsters)

    def next_room(self):
        if self.is_won():
            return print("You won! :-)")

        room = self.rooms.pop()
        enter_room(self.hero, room)

        if self.is_lost():
            return print("You lost! :-(")

        self.after_room()
        self.next_room()

    def after_room(self):
        weapon = choice(self.weapons)
        self.hero.gain_weapon(weapon)

    def is_won(self):
        return not self.rooms #    deque rooms is empty

    def is_lost(self):
        return self.hero.HP <= 0 #   hero died


class Weapon:
    def __init__(self, name, damage, probability):
        self.name = name
        self.damage = damage
        self.probability = probability

    def __str__(self):
        return (self.name + " Damage: " + str(self.damage)
                + " Chance of hit: " + str(self.probability))

class Player:
    #  Defines player (name, HP, EP, equipped weapon and skills)
    #  Handles player options (attacking, being alive, etc)

    def __init__(self, name, HP, EP, equipped_weapon, skills):
        self.name = name
        self.HP = HP
        self.EP = EP
        self.max_hp = HP
        self.max_ep = EP
        self.equipped_weapon = equipped_weapon
        self.skills = skills


    def gain_weapon(self, weapon):
        #   When room is cleared, you find a random weapon. Take it or restore your HP and EP.

        print("You found", weapon)
        response = validate_string("Do you want to equip it? (y/n): ", ["y", "n"])
        if (response == "y"):
            self.equipped_weapon = weapon
        else:
            self.heal(20)
            self.EP = self.max_ep
            print("You were healed and your energy was fully restored")

    def heal(self, amount):
        self.HP = min(self.HP + amount, self.max_hp)

    def is_alive(self):
        return self.HP > 0

    def relax(self):
        self.EP = min(self.EP + 10, self.max_ep)

    def can_perform(self, skill):
        return self.EP >= skill.energy_cost

    def available_skills(self):
        return list(filter(lambda x : self.can_perform(x), self.skills))

    def attack(self, monster):
        if not self.available_skills():
            return self.attack_meelee(monster)
        attack_type = validate_int("Press 0 if you want to attack with your weapon.\nPress 1 if you want to use your skill: ", 0, 1)
        if (attack_type == 1):
            self.attack_skill(monster)
        else:
            self.attack_meelee(monster)


    def attack_meelee(self, monster):   #   attacking with weapon
        self.try_attack(monster, self.equipped_weapon.damage, self.equipped_weapon.probability)

    def attack_skill(self, monster):   #   attacking with skill
        available_skills = self.available_skills()
        print()
        print_skills(available_skills)
        skill = validate_int("Please select skill (number): ", 0, len(available_skills) - 1)
        self.EP -= available_skills[skill].energy_cost
        self.try_attack(monster, available_skills[skill].damage, available_skills[skill].probability)

    def take_damage(self, damage):
        self.HP = max(0, self.HP - damage)

    def try_attack(self, monster, damage, probability):
        #   probabily of hiting monster
        print()
        rand = randint(0, 99)
        if rand < probability * 100:
            monster.take_damage(damage)
            print("You dealt", damage, "to", monster.name)
        else:
            print("You missed")
        print()

    def __str__(self):
        #   Returns info about player
        #   {text in this} is defined in .format()
        return (self.name + " HP: " + str(self.HP) + "/" + str(self.max_hp)
                + " EP: " + str(self.EP) + "/" + str(self.max_ep) + "\n"
                + "Your weapon: {weapon}".format(weapon = self.equipped_weapon) + "\n"
                + "Your skills:\n"
                + "\n".join(["{skill}".format(skill = skill) for skill in self.skills]))


class Monster:
    #   Defines monster (name, HP, EP, skills).
    #   Handles monster options (attack, being alive, etc.)
    #   Very similar to class Player.
    def __init__(self, name, HP, EP, skills):
        self.name = name
        self.HP = HP
        self.EP = EP
        self.max_hp = HP
        self.max_ep = EP
        self.skills = skills

    def is_alive(self):
        return self.HP > 0

    def relax(self):
        self.EP = min(self.EP + 10, self.max_ep)

    def can_perform(self, skill):
        return self.EP >= skill.energy_cost

    def available_skills(self):
        return list(filter(lambda x : self.can_perform(x), self.skills))

    def try_attack(self, hero, damage, probability):
        rand = randint(0, 99)
        if rand < probability * 100:
            hero.take_damage(damage)
            print("dealt", damage)
        else:
            print("missed")

    def attack(self, hero):
        #   What if there are no skills available? Is it even possible? I don't think so. (I'll die before.)
        skill = choice(self.available_skills())
        print(self.name, "used", skill.name, "and ", end="")
        self.try_attack(hero, skill.damage, skill.probability)
        print()

    def take_damage(self, damage):
        self.HP = max(0, self.HP - damage)

    def __str__(self):
        return (self.name + " HP: " + str(self.HP) + "/" + str(self.max_hp)
                + " EP: " + str(self.EP) + "/" + str(self.max_ep) + "\n"
                + self.name + " skills:\n"
                + "\n".join(["{skill}".format(skill = skill) for skill in self.skills]))

class Skill:
    def __init__(self, name, damage, energy_cost, probability):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
        self.probability = probability

    def __str__(self):
        return (self.name + " - Damage: " + str(self.damage)
                + " Energy cost: " + str(self.energy_cost)
                + " Chance of hit: " + str(self.probability))

def load_skills(filename):
    #   loads skills from file
    skills = []
    with open(filename, "r") as skills_file:
        lines = skills_file.readlines()
        for line in lines:
            row = line.strip().split(",")
            skills.append(Skill(row[0], int(row[1]), int(row[2]), float(row[3])))
    return skills

def find_skill(skillname, skills):
    for skill in skills:
        if skill.name == skillname:
            return skill
    return None

def load_monsters():
    #   loads monsters from file and add them skills
    skills = load_skills("skills.csv")
    monsters = []
    with open("monsters.csv", "r") as monsters_file:
        lines = monsters_file.readlines()
        for line in lines:
            row = line.strip().split(",")
            monster_skills = []
            skills_list = row[3].split(";")
            for skill in skills_list:
                monster_skills.append(find_skill(skill, skills))
            monsters.append(Monster(row[0], int(row[1]), int(row[2]), monster_skills))
    return monsters

def load_weapons():
    #   loads weapons from file
    weapons = []
    with open("weapons.csv", "r") as weapons_file:
        lines = weapons_file.readlines()
        for line in lines:
            row = line.strip().split(",")
            weapons.append(Weapon(row[0], int(row[1]), float(row[2])))
    return weapons

def validate_string(message, accepted_inputs):
    #   Checks if the input is valid.
    user_input = input(message)
    while (not user_input in accepted_inputs):
        print("Please insert valid options!")
        user_input = input(message)
    return user_input

def load_int(message, default):
    # Get user input. Bit complicated in the second part, but works for validating.
    user_input = input(message)
    try:
        number = int(user_input)
    except ValueError:
        number = default
    return number

def validate_int(message, minimum, maximum):
    #   Checks if the input is valid.
    #   if number = default that means it isn't valid option.
    number = load_int(message, maximum + 1)
    while (number < minimum or number > maximum):
        print("Please insert valid options!")
        number = load_int(message, maximum + 1)
    return number

def load_hero():
    #   Get information from player.
    #   Starting weapon set to sword, not sure if this is right.
    print("Welcome to the Dungeons and Pythons")
    print()
    print("_" * 35)
    name = input("Please enter your heroic name: ")
    skill_set = validate_string("Choose character (mage/hunter): ", ["mage", "hunter"])
    skills = load_skills(skill_set + "_skills.csv")
    starting_weapon = Weapon("Sword", 15, 0.8)
    return Player(name, 100, 100, starting_weapon, skills)

def load_difficulty():
    #   Really proud of this. It looks nice.
    return validate_string("Tell me how difficult your journey should be? (e / m / h): ", ["e", "m", "h"])

def print_monsters(room):
    #   Prints monsters in room.
    print("=== Monsters ===")
    print()
    for i in range(len(room.monsters)):
        print(i, "-  ", end="")
        print(room.monsters[i])
        print()

def player_attack(hero, room):
    #   Which monster you want to atack?
    #   Is the monster still alive after?
    print(hero)
    print()
    print_monsters(room)
    print()
    monster_index = validate_int("Please select target (number): ", 0, len(room.monsters) - 1)
    monster = room.monsters[monster_index]
    hero.attack(monster)
    if not monster.is_alive():
        room.monsters.remove(monster)
        print(monster.name, "died")

def monsters_attack(hero, room):
    for monster in room.monsters:
        monster.attack(hero)

def relax(hero, room):
    hero.relax()
    for monster in room.monsters:
        monster.relax()

def fight(hero, room):
    player_attack(hero, room)
    monsters_attack(hero, room)
    relax(hero, room)

def enter_room(hero, room):
    #  Entering room and staying until all monsters or hero die.
    print("You entered room.\n")
    fight(hero, room)
    while (hero.is_alive() and not room.is_empty()):
        print("----- NEXT ROUND -----")
        fight(hero, room)

Game(load_hero(), load_difficulty(), load_monsters(), load_weapons()).next_room()
#   Starts the game
