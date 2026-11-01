import time
import numpy as np
import sys
import requests
import pygame
import pokepy
from dataclasses import dataclass, field
from typing import List, Dict
import json
import random

#delay printing
def delay_print(s):
    for c in s: 
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

@dataclass(frozen=True)
class MoveData:
    name: str
    type: str
    power:int
    accuracy: int

@dataclass(frozen = True)
class SpeciesData:
    name: str
    types: List[str]
    base_stats:Dict[str,int]

with open("pokedex.json", 'r') as file:
    raw_pokedex = json.load(file)

POKEDEX: Dict[str, SpeciesData] = {}

for name, data in raw_pokedex.items(): 
    data["name"] = name
    POKEDEX[name] = SpeciesData(**data)


with open("movedex.json", 'r') as file:
    raw_movedex = json.load(file)

MOVEDEX: Dict[str, MoveData] = {}

for name, data in raw_movedex.items():
    data["name"] = name
    MOVEDEX[name] = MoveData(**data)

with open("typechart.json", 'r') as file:
    TYPECHART = json.load(file)

#class
class Pokemon:
    def __init__(self, species: SpeciesData, moves: List[MoveData]):
        self.species = species
        self.name = species.name
        self.types = species.types

        self.max_hp = species.base_stats["hp"]
        self.current_hp = self.max_hp
        self.attack = species.base_stats["atk"]
        self.defense = species.base_stats["def"]

        self.moves = moves
    

    def __str__(self):
        return self.name

    def battle(self, other):
        print()
        
        for var_name, var_value in vars(self).items():
            if var_name != 'species':
                if var_name != 'max_hp':
                    if var_name != 'moves':
                        print(f"{var_name.upper()}: {var_value}")
        print()
        for var_name, var_value in vars(other).items():
            if var_name != 'species':
                if var_name != 'max_hp':
                    if var_name != 'moves':
                        print(f"{var_name.upper()}: {var_value}")
        while self.current_hp > 0 :
            #User's turn
            print(f"\n---------------{self.name}'S TURN---------------")
            for i, move in enumerate(self.moves):
                print(f'{i+1}. {vars(move)}')

            move_number = input("(Select your move entering a number 1-4): ") 
            attack_choice = self.moves[int(move_number)-1]

            stab = attack_choice.type in self.types

            delay_print(f"\n{self.name} used {attack_choice.name}!!!")

            attack_stat = self.attack

            other.current_hp -= round(self.calculate_damage(attack_choice, attack_stat, other, stab))
            #other.current_hp = max(0, other.current_hp)

            time.sleep(1)
            delay_print(f'{other.name} FAINTED...YOU WIN!!!') if other.current_hp <= 0 else delay_print(f"{other.name} has {other.current_hp} HP remaining.")
            time.sleep(1)

            if not other.current_hp > 0:
                break
            #Ai pokemon's turn
            print(f"\n---------------{other.name}'S TURN---------------")
            
            for i, move in enumerate(other.moves):
                print(f'{i+1}. {vars(move)}')
 
            attack_choice = other.moves[random.randint(0,len(other.moves)-1)]
            stab = attack_choice.type in other.types
            delay_print(f"\n{other.name} used {attack_choice.name}!!!")

            attack_stat = other.attack
            self.current_hp -= round(self.calculate_damage(attack_choice, attack_stat, self, stab))
            #self.current_hp = max(0, self.current_hp)
            time.sleep(1)
            delay_print(f'{self.name} FAINTED...YOU LOSE') if self.current_hp <= 0 else delay_print(f"{self.name} has {self.current_hp} HP remaining.")
            time.sleep(1)
            

    def effectiveness(self, attack_type, defender_types, modifier = 1.0):
        """
        Checks if the given move type is not very effective, effective, or super effective against the other pokemon

        :param move_type: a string value that denotes the move type
        :return: 0 if not effective, 1 if effective, 2 if super effective
        """
        if attack_type not in TYPECHART:
            return modifier
        
        interactions = TYPECHART[attack_type]

        for def_type in defender_types:
            if def_type in interactions:
                modifier *= interactions[def_type]
        if modifier > 1.0:
            delay_print("It's Super Effective!!!")
        if modifier < 1.0:
            delay_print("It's Not very Effective...")
        return modifier

    def calculate_damage(self, attack_choice, attack_stat, defender, stab):
        attack_type = attack_choice.type
        if stab:
            attack_power = attack_choice.power*1.5 
        else:
            attack_power = attack_choice.power
        defender_types = defender.types
        defender_def = defender.defense
        modifier = self.effectiveness(attack_type, defender_types)
        damage = (((20+(2*attack_power*(attack_stat/defender_def))/20)+2)*modifier)*random.uniform(0.85, 1.0)
        return damage


if __name__ == "__main__":
    Charizard = Pokemon(species= POKEDEX['Charizard'], moves = [MOVEDEX['Fly'], MOVEDEX['Flamethrower'], MOVEDEX['Dragon Claw'], MOVEDEX['Brick Break']])
    Blastoise = Pokemon(species= POKEDEX['Blastoise'], moves = [MOVEDEX['Earthquake'], MOVEDEX['Hydro Pump'], MOVEDEX['Bite'], MOVEDEX['Ice Beam']])
    Venusaur = Pokemon(species= POKEDEX['Venusaur'], moves = [MOVEDEX['Body Slam'], MOVEDEX["Sludge Bomb"], MOVEDEX["Razor Leaf"], MOVEDEX["Giga Drain"]])
    Pikachu = Pokemon(species= POKEDEX['Pikachu'], moves = [MOVEDEX['Tackle'], MOVEDEX['Thunderbolt'], MOVEDEX['Iron Tail'], MOVEDEX['Quick Attack']])

    Blastoise.battle(Charizard)
    
    # pygame.init()

    # # Window setup
    # WIDTH, HEIGHT = 900, 600
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Pokemon Battle Simulator")

    # clock = pygame.time.Clock()

    # # Colors
    # WHITE = (245, 245, 235)
    # BLACK = (30, 30, 30)
    # GREEN = (70, 190, 90)
    # YELLOW = (240, 195, 50)
    # RED = (220, 65, 65)
    # BLUE = (75, 120, 210)
    # GRAY = (190, 190, 190)

    # font = pygame.font.Font(None, 30)
    # small_font = pygame.font.Font(None, 23)

    # # Temporary battle data
    # player_name = "Pikachu"
    # player_hp = 100
    # player_max_hp = 100

    # enemy_name = "Charmander"
    # enemy_hp = 100
    # enemy_max_hp = 100

    # moves = ["Thunderbolt", "Quick Attack",
    #         "Iron Tail", "Electro Ball"]

    # message = f"Go, {player_name}!"

    # def draw_text(text, x, y, color=BLACK, text_font=font):
    #     image = text_font.render(str(text), True, color)
    #     screen.blit(image, (x, y))

    # def draw_hp_bar(x, y, current_hp, max_hp):
    #     # Background of the HP bar
    #     pygame.draw.rect(screen, RED, (x, y, 200, 18))

    #     # Calculate the green/yellow portion
    #     ratio = max(0, current_hp) / max_hp if max_hp > 0 else 0
    #     bar_color = GREEN if ratio > 0.5 else YELLOW

    #     pygame.draw.rect(
    #         screen, bar_color,
    #         (x, y, int(200 * ratio), 18)
    #     )
    #     pygame.draw.rect(screen, BLACK, (x, y, 200, 18), 2)

    # def draw_button(text, rect):
    #     pygame.draw.rect(screen, WHITE, rect, border_radius=8)
    #     pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

    #     label = font.render(text, True, BLACK)
    #     screen.blit(label, label.get_rect(center=rect.center))

    # # Four move buttons
    # move_buttons = [
    #     pygame.Rect(470, 410, 190, 55),
    #     pygame.Rect(680, 410, 190, 55),
    #     pygame.Rect(470, 475, 190, 55),
    #     pygame.Rect(680, 475, 190, 55),
    # ]

    # running = True

    # while running:
    #     # Handle user input
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1 and enemy_hp > 0 and player_hp > 0:
    #                 for i, rect in enumerate(move_buttons):
    #                     if rect.collidepoint(event.pos):
    #                         # Temporary damage placeholder
    #                         damage = 15
    #                         enemy_hp = max(0, enemy_hp - damage)

    #                         message = (
    #                             f"{player_name} used {moves[i]}!"
    #                         )

    #                         if enemy_hp == 0:
    #                             message = f"{enemy_name} fainted!"

    #                         break

    #     # Draw the screen
    #     screen.fill(WHITE)

    #     # Opponent section
    #     draw_text(enemy_name, 550, 60)
    #     draw_text(
    #         f"HP: {enemy_hp}/{enemy_max_hp}", 550, 95,
    #         text_font=small_font
    #     )
    #     draw_hp_bar(550, 125, enemy_hp, enemy_max_hp)

    #     # Temporary sprites represented by circles
    #     pygame.draw.circle(screen, RED, (680, 220), 55)

    #     # Player section
    #     draw_text(player_name, 100, 275)
    #     draw_text(
    #         f"HP: {player_hp}/{player_max_hp}", 100, 310,
    #         text_font=small_font
    #     )
    #     draw_hp_bar(100, 340, player_hp, player_max_hp)

    #     pygame.draw.circle(screen, BLUE, (240, 220), 65)

    #     # Battle message box
    #     pygame.draw.rect(screen, WHITE, (25, 395, 420, 145))
    #     pygame.draw.rect(screen, BLACK, (25, 395, 420, 145), 3)
    #     draw_text(message, 45, 420, text_font=small_font)

    #     # Move selection
    #     for i, rect in enumerate(move_buttons):
    #         draw_button(moves[i], rect)

    #     pygame.display.flip()
    #     clock.tick(60)

    # pygame.quit()
    # sys.exit()



