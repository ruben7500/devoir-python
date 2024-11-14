import copy
import json
import random
import os

class Game:
    def __init__(self):
        self.player_name = ""
        self.player_hp = 100
        self.player_attack = 5
        self.player_defense = 2
        self.player_level = 1
        self.player_xp = 0
        self.inventory = []
        self.game_active = False
        self.player_position = [0, 0]
        self.map = []
        self.enemies = []
        self.items = []
        self.biomes = {}
        self.last_biome = None
        self.load_map("map.txt")
        self.load_enemies("enemies.json")
        self.load_items("items.json")
        self.load_biomes("biomes.json")

    def load_map(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                self.map.append(line.strip().split())

    def load_enemies(self, filename):
        with open(filename, 'r') as file:
            self.enemies = json.load(file)

    def load_items(self, filename):
        with open(filename, 'r') as file:
            self.items = json.load(file)

    def load_biomes(self, filename):
        with open(filename, 'r') as file:
            self.biomes = json.load(file)

    def save_game(self):
        save_data = {
            "player_name": self.player_name,
            "player_hp": self.player_hp,
            "player_attack": self.player_attack,
            "player_defense": self.player_defense,
            "player_level": self.player_level,
            "player_xp": self.player_xp,
            "inventory": self.inventory,
            "player_position": self.player_position
        }
        with open("save_game.json", "w") as file:
            json.dump(save_data, file)
        print("Game saved successfully.")

    def load_game(self):
        if os.path.exists("save_game.json"):
            with open("save_game.json", "r") as file:
                save_data = json.load(file)
                self.player_name = save_data["player_name"]
                self.player_hp = save_data["player_hp"]
                self.player_attack = save_data["player_attack"]
                self.player_defense = save_data["player_defense"]
                self.player_level = save_data["player_level"]
                self.player_xp = save_data["player_xp"]
                self.inventory = save_data["inventory"]
                self.player_position = save_data["player_position"]
                self.game_active = True
            print("Game loaded successfully.")
            self.game_loop()
        else:
            print("No saved game found.")

    def main_menu(self):
        print("""
▀█████████▄   ▄██████▄  ▀█████████▄     ▄████████         ▄████████ ████████▄   ▄█    █▄     ▄████████ ███▄▄▄▄       ███     ███    █▄     ▄████████    ▄████████    ▄████████ 
  ███    ███ ███    ███   ███    ███   ███    ███        ███    ███ ███   ▀███ ███    ███   ███    ███ ███▀▀▀██▄ ▀█████████▄ ███    ███   ███    ███   ███    ███   ███    ███ 
  ███    ███ ███    ███   ███    ███   ███    █▀         ███    ███ ███    ███ ███    ███   ███    █▀  ███   ███    ▀███▀▀██ ███    ███   ███    ███   ███    █▀    ███    █▀  
 ▄███▄▄▄██▀  ███    ███  ▄███▄▄▄██▀    ███               ███    ███ ███    ███ ███    ███  ▄███▄▄▄     ███   ███     ███   ▀ ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄       ███        
▀▀███▀▀▀██▄  ███    ███ ▀▀███▀▀▀██▄  ▀███████████      ▀███████████ ███    ███ ███    ███ ▀▀███▀▀▀     ███   ███     ███     ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████ 
  ███    ██▄ ███    ███   ███    ██▄          ███        ███    ███ ███    ███ ███    ███   ███    █▄  ███   ███     ███     ███    ███ ▀███████████   ███    █▄           ███ 
  ███    ███ ███    ███   ███    ███    ▄█    ███        ███    ███ ███   ▄███ ███    ███   ███    ███ ███   ███     ███     ███    ███   ███    ███   ███    ███    ▄█    ███ 
▄█████████▀   ▀██████▀  ▄█████████▀   ▄████████▀         ███    █▀  ████████▀   ▀██████▀    ██████████  ▀█   █▀     ▄████▀   ████████▀    ███    ███   ██████████  ▄████████▀  
                                                                                                                                          ███    ███                           
""")
        print("MAIN MENU:")
        print("1. Create New Game")
        print("2. Load Saved Game")
        print("3. About")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            self.start_new_game()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            self.about()
        elif choice == "4":
            print("Exiting game...")
            exit()
        else:
            print("Invalid option. Please try again.")
            self.main_menu()

    def start_new_game(self):
        self.player_name = input("Please enter your name: ")
        print(f"Welcome, {self.player_name}. You find yourself in a dark forest with only a knife.")
        self.game_active = True
        self.game_loop()

    def about(self):
        print("Welcome to this RPG game. Created in Python as a retro-style text RPG.")
        self.main_menu()
    def gain_xp(self, amount):
        self.player_xp += amount
        xp_to_level_up = self.player_level * 10
        if self.player_xp >= xp_to_level_up:
            self.player_level += 1
            self.player_xp -= xp_to_level_up
            self.player_hp += 10
            self.player_attack += 2
            self.player_defense += 1
            print(f"Congratulations! You leveled up to level {self.player_level}!")

    def encounter_enemy(self, enemy_type="random"):

        if enemy_type == "boss":
            enemy = {"name": "Boss", "hp": 100, "attack": 15, "defense": 5, "xp": 50}
        else:

            enemy = copy.deepcopy(random.choice(self.enemies))

        enemy["hp"] = max(enemy.get("hp", 10), 1)
        enemy["attack"] = max(enemy.get("attack", 1), 0)
        enemy["defense"] = max(enemy.get("defense", 0), 0)
        enemy_xp = enemy.get("xp", 10)

        self.temporary_attack_buff = 0

        print("\n" + "=" * 30)
        print(f"A wild {enemy['name']} appears!")
        print(f"HP: {enemy['hp']}, Attack: {enemy['attack']}, Defense: {enemy['defense']}")
        print("=" * 30)

        while enemy["hp"] > 0 and self.player_hp > 0:
            print("\n--- Combat Menu ---")
            print(f"Your HP: {self.player_hp}, Enemy HP: {enemy['hp']}")
            print("Choose your action:")

            print("1. Attack with fists (Damage: 5)")

            attack_options = [item for item in self.inventory if item['effect']['type'] == "attack"]
            if attack_options:
                for i, item in enumerate(attack_options, start=2):
                    print(f"{i}. Attack with {item['name']} (Damage: {item['effect']['value']})")
                option_offset = len(attack_options) + 1
            else:
                option_offset = 1

            print(f"{option_offset + 1}. Use an item from inventory")
            print(f"{option_offset + 2}. Run")

            action = input("> ")
            try:
                action = int(action)
                if action == 1:

                    self.attack_enemy(enemy, {"name": "fists", "effect": {"value": 5}})
                elif 2 <= action <= option_offset:

                    selected_weapon = attack_options[action - 2]
                    self.attack_enemy(enemy, selected_weapon)
                elif action == option_offset + 1:
                    self.use_item()
                elif action == option_offset + 2:
                    print("You ran away!")

                    self.player_attack -= self.temporary_attack_buff
                    return
                else:
                    print("Invalid action. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if self.player_hp <= 0:
            print("\nYou have been defeated.")
            self.game_active = False
        elif enemy["hp"] <= 0:
            print(f"\nYou defeated the {enemy['name']}!")
            print(f"You gained {enemy_xp} XP.")
            self.gain_xp(enemy_xp)

        self.player_attack -= self.temporary_attack_buff

    def attack_enemy(self, enemy, weapon):

        damage = weapon['effect']['value']
        crit_chance = random.random()
        if crit_chance < 0.1:
            damage *= 2
            print("Critical hit!")

        effective_damage = max(damage - enemy["defense"], 0)
        enemy["hp"] -= effective_damage
        print(
            f"You hit the {enemy['name']} with {weapon['name']} for {effective_damage} damage. (Enemy HP: {enemy['hp']})")

        if enemy["hp"] > 0:
            self.enemy_attack(enemy)

    def enemy_attack(self, enemy):
        enemy_damage = max(enemy["attack"] - self.player_defense, 0)
        self.player_hp -= enemy_damage
        print(f"The {enemy['name']} hits you for {enemy_damage} damage. (Your HP: {self.player_hp})")

    def use_item(self):
        if not self.inventory:
            print("Your inventory is empty!")
            return

        print("Inventory:")
        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item['name']} - Effect: {item['effect']['type']}")

        choice = input("Choose an item to use: ")
        try:
            item_index = int(choice) - 1
            item = self.inventory.pop(item_index)

            if item['effect']['type'] == "heal":

                self.player_hp = min(100, self.player_hp + item['effect']['value'])
                print(f"You used {item['name']} and healed {item['effect']['value']} HP. Current HP: {self.player_hp}.")

            elif item['effect']['type'] == "attack":

                self.player_attack += item['effect']['value']
                print(
                    f"You used {item['name']} and increased your attack by {item['effect']['value']} for this battle.")

            elif item['effect']['type'] == "defense":

                self.player_defense += item['effect']['value']
                print(
                    f"You used {item['name']} and increased your defense by {item['effect']['value']} for this battle.")

            elif item['effect']['type'] == "buff":

                self.temporary_attack_buff = item['effect']['value']
                self.player_attack += self.temporary_attack_buff
                print(
                    f"You used {item['name']} and gained an attack buff of {item['effect']['value']} for this battle.")

        except (ValueError, IndexError):
            print("Invalid choice.")

    def find_item(self):
        item = random.choice(self.items)
        print(f"You found a {item['name']}!")
        self.inventory.append(item)

    def game_loop(self):
        while self.game_active:
            command = input("Enter command (go north, go south, go east, go west or save): ").lower()
            if command in ["go north", "go south", "go east", "go west"]:
                self.move_player(command)
            elif command == "save":
                self.save_game()
            else:
                print("Invalid command. Try 'go north', 'go south', 'go east', 'go west', or 'save'.")

    def move_player(self, direction):
        if direction == "go north" and self.player_position[1] > 0:
            self.player_position[1] -= 1
        elif direction == "go south" and self.player_position[1] < len(self.map) - 1:
            self.player_position[1] += 1
        elif direction == "go east" and self.player_position[0] < len(self.map[0]) - 1:
            self.player_position[0] += 1
        elif direction == "go west" and self.player_position[0] > 0:
            self.player_position[0] -= 1
        else:
            print("You can't go that way.")
            return

        print(f"You move to position {self.player_position}.")
        self.check_location()

    def check_location(self):
        x, y = self.player_position
        location = self.map[y][x]

        if location in self.biomes:
            if self.last_biome == location:
                phrase = random.choice(self.biomes[location]["stationary"])
            else:
                phrase = random.choice(self.biomes[location]["entry"])
                self.last_biome = location
            print(phrase)

        if location == "B":
            print("You encountered the boss! Prepare for battle!")
            self.encounter_enemy("boss")
        else:
            event = random.choice(["monster", "item", "nothing"])
            if event == "monster":
                self.encounter_enemy()
            elif event == "item":
                self.find_item()
            else:
                print("It's quiet here...")

if __name__ == "__main__":
    game = Game()
    game.main_menu()