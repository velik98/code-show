import csv

def start():
    print("Welcome to the Dungeons and Pythons")
    print()
    print("_" * 35)
    name = input("Please enter your heroic name:")
    character = input("Choose your character (mage/hunter) :")
    difficulty = input("Tell me how difficult your journey should be? (e/ m/ h) :")
    
    if (character == "mage" or character == "hunter") and (difficulty == "e" or difficulty == "m" or difficulty == "h"):
         return name, character, difficulty

    else:
        print("Please insert valid options!")
        start()
#start()



    




class Player:
    def __init__(self, name, HP, EP, equipped_weapon, skills):
        self.name = name
        self.HP = HP
        self.EP = EP
        self.equipped_weapon = equipped_weapon
        self.skills = skills

class Monster:
    def __init__(self, name, HP, EP, skills):
        self.name = name
        self.HP = HP
        self.EP = EP
        self.skills = skills

class Skill:
    def __init__(self, name, damage, energy_cost, probability):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
        self.probability = probability

    def __repr__(self):
        return "name:" + self.name + "damage:" + self.damage + "energy cost:" + self.energy_cost + "probability:" + self.probability

    def add_skill(self, skill):
        self.skills
skills_dic = {}
with open("skills.csv", "r") as skills:
    skills = skills.readlines()
    for row in skills:
        row = row.strip().split(",")
        skills_dic[row[0]] = Skill(row[0], row[1], row[2], row[3])
print(Skill)

class Room:
    def __init__(self):
        self.set = 1

class Weapon:
    def __init__(self, name, damage, probability):
        self.name = name
        self.damage = damage
        self.probability = probability
