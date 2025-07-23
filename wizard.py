import os
import random
import copy
from spells import SPELLBOOK_TEMPLATES, SHARED_SPELLS

yesVariations = ['yes', 'ya', 'yeah', 'ye', 'y', 'yas']
noVariations = ['no', 'nah', 'nope', 'na', 'n']
actions1 = ['read', 'scheme', 'question', 'spell']


class Wizard:
    def __init__(self, name, wtype, devotion=None, whimsy=None, iniquity=None, ap=1, war=0.0, days=0,
                 learned_spells=None, learned_properties=None, known_properties=None, inventory=None, spellbook=None):
        self.name = name
        self.type = wtype

        self.devotion = devotion or {"level": 1, "xp": 0, "required": 5}
        self.whimsy = whimsy or {"level": 1, "xp": 0, "required": 5}
        self.iniquity = iniquity or {"level": 1, "xp": 0, "required": 5}

        self.ap = ap
        self.war = war
        self.days = days

        self.learned_spells = learned_spells or []
        self.learned_properties = learned_properties or {}
        self.known_properties = set(known_properties or [])
        # self.unlocked_spells = unlocked_spells or []
        self.inventory = inventory or {}

        # Load spellbook — either from save or build it fresh based on type
        if spellbook is not None:
            self.spellbook = spellbook
        else:
            # Start with spell template based on wizard type
            base = copy.deepcopy(SPELLBOOK_TEMPLATES.get(wtype, {}))
            for stat, spells in SHARED_SPELLS.items():
                base.setdefault(stat, []).extend(copy.deepcopy(spells))
            self.spellbook = base

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "devotion": self.devotion,
            "whimsy": self.whimsy,
            "iniquity": self.iniquity,
            "war": self.war,
            "days": self.days,
            "inventory": self.inventory,
            "learned_spells": self.learned_spells,
            "spellbook": self.spellbook

        }

    @classmethod
    def from_dict(cls, data):
        wizard = cls(
            name=data["name"],
            wtype=data["type"],
            devotion=data.get("devotion"),
            whimsy=data.get("whimsy"),
            iniquity=data.get("iniquity"),
            ap=data.get("ap", 1),
            war=data.get("war", 0.0),
            days=data.get("days", 0),
            inventory=data.get("inventory", {}),
            learned_spells=data.get("learned_spells", []),
            spellbook=data.get("spellbook", {})

        )
        return wizard

    def display_stats(self):
        clear_terminal()
        print("Your stats are:")
        for stat_name in ['devotion', 'whimsy', 'iniquity']:
            stat = getattr(self, stat_name)
            print(
                f"{stat_name.capitalize()} - Level: {stat['level']}, XP: {stat['xp']}/{stat['required']}")
        input(f"\nDays Completed: {self.days}")

    @classmethod
    def load(cls, filename):
        name = ""
        wtype = ""
        devotion = whimsy = iniquity = days = 0
        war = 0.0
        with open(f"save/{filename}", "r") as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    match key:
                        case 'Name':
                            name = value
                        case 'Type':
                            wtype = value
                        case 'Devotion':
                            devotion = int(value)
                        case 'Whimsy':
                            whimsy = int(value)
                        case 'Iniquity':
                            iniquity = int(value)
                        case 'War':
                            war = float(value)
                        case 'Days':
                            days = int(value)
        wiz = cls(name, wtype)
        wiz.devotion = devotion
        wiz.whimsy = whimsy
        wiz.iniquity = iniquity
        wiz.war = war
        wiz.days = days
        return wiz

    def action_menu(self):
        while self.ap > 0:
            clear_terminal()
            print(f"🕒 Action Points: {self.ap}")
            print("What would you like to do?")
            print("1) Perform an activity (read, scheme, question)")
            print("2) Learn spells")
            print("3) Forage for ingredients")
            print("4) View inventory")
            print("5) View known spells and properties")
            print("6) End the day")

            choice = input("Choose an option: ").strip()

            match choice:
                case '1':
                    self.perform_activity()
                case '2':
                    self.handle_spells()
                case '3':
                    self.forage()
                case '4':
                    self.show_inventory()
                    input("\nPress Enter to return.")
                case '5':
                    self.view_knowledge()
                    input("\nPress Enter to return.")
                case '6':
                    print("🌙 Your wizard rests for the night...")
                    break
                case _:
                    input("Invalid choice. Press Enter to try again.")

        self.days += 1
        clear_terminal()
        input("The day ends. Time marches on...")

    def perform_activity(self):
        while True:
            clear_terminal()
            print("Choose an activity:")
            print("1) Read (devotion)")
            print("2) Question (whimsy)")
            print("3) Scheme (iniquity)")
            print("B) Go back")

            act = input("Choice: ").lower()

            match act:
                case '1':
                    self.increase_stat(
                        "devotion", 10 if random.random() < 0.1 else 3)
                    self.ap -= 1
                    return
                case '2':
                    self.increase_stat(
                        "whimsy", 10 if random.random() < 0.1 else 3)
                    self.ap -= 1
                    return
                case '3':
                    self.increase_stat(
                        "iniquity", 10 if random.random() < 0.1 else 3)
                    self.ap -= 1
                    return
                case 'b':
                    return
                case _:
                    input("Invalid choice.")

    def handle_spells(self):
        # while True:
        #     clear_terminal()
        #     print("📚 Spell Menu")
        #     print("1) Learn a new spell")
        #     print("2) View unlocked spells")
        #     print("B) Go back")
        #     choice = input("Choice: ").lower()

        #     if choice == '1':
        while True:
            clear_terminal()
            print("Character Stats")
            print("1) Devotion")
            print("2) Whimsy")
            print("3) Iniquity")
            stat_input = input(
                "Learn from which stat? (or press 'b' to go back): ").lower()

            if stat_input == 'b':
                break
            if stat_input in ['1', '2', '3']:
                outcome = self.spell_choice(int(stat_input))
                if outcome == 'gain':
                    self.ap -= 1
                    break
                continue
            # elif choice == '2':
            #     clear_terminal()
            #     print("📖 Unlocked Spells:")
            #     if not self.unlocked_spells:
            #         print("  You haven't unlocked any spells yet.")
            #     else:
            #         for spell in self.unlocked_spells:
            #             print(f"  - {spell.title()}")
            #     input("\nPress Enter to return.")
        # elif choice == 'b':
        #     return
        # else:
        #     input("Invalid choice. Press Enter to try again.")

    def forage(self):
        clear_terminal()
        print("🌿 You begin to forage in the wilds...")

        possible_items = [
            'leaf', 'moss', 'scale', 'glimmerroot', 'morinyite stone',
            'undead amethyst', 'flaerrin', 'shadecap spores', 'wyrmshard'
        ]

        found = random.choice(possible_items)
        self.inventory[found] = self.inventory.get(found, 0) + 1

        print(f"✨ You found: {found.title()}!")
        self.ap -= 1
        input("\nPress Enter to return.")

    def show_inventory(self):
        clear_terminal()
        print("🎒 Inventory:")
        if not self.inventory:
            print("  (empty)")
        else:
            for item, qty in self.inventory.items():
                print(f"  - {item.title()}: {qty}")

    def perform_action(self, action):
        if action == 'read':
            if random.random() < 0.10:
                input("Advanced arcane knowledge absorbed (10%)")
                self.increase_stat("devotion", 10)
                return 'gain'
            else:
                input("The tome was confusing and dense (90%)")
                self.increase_stat("devotion", 3)
                return 'gain'

        elif action == 'question':
            if random.random() < 0.10:
                input(
                    "What are the true motives of the Ministry for the Advancement of Global Enchantment?")
                self.increase_stat("whimsy", 10)
                return 'gain'
            else:
                input("If every wand is a stick, is every stick a wand?")
                self.increase_stat("whimsy", 3)
                return 'gain'

        elif action == 'scheme':
            if random.random() < 0.10:
                input(f"{self.name} orders the book 'How to Scheme' from Etsy!")
                self.increase_stat("iniquity", 10)
                return 'gain'
            else:
                input(f"{self.name} scribbles evil plans on a napkin at McDonald's.")
                self.increase_stat("iniquity", 3)
                return 'gain'

        elif action == 'spell':
            while True:
                clear_terminal()
                print("Available stats and levels:")
                print(f"{1}) Devotion - Level: " + str(self.devotion['level']))
                print(f"{2}) Whimsy - Level: " + str(self.whimsy['level']))
                print(f"{3}) Iniquity - Level: " + str(self.iniquity['level']))

                # try:
                user_input = input(
                    "Which stat do you want to attempt to learn a spell from? (or 'b' to go back):\n")
                if user_input.lower() == 'b':
                    clear_terminal()
                    return  # Exit and let player pick a new stat

                if not user_input.isdigit():
                    print("Please enter a valid number or 'b' to go back.")
                    continue

                if 1 <= int(user_input) <= 3:
                    outcome = self.spell_choice(int(user_input))
                    if outcome == 'gain':
                        return outcome
                else:
                    input("Invalid choice. Try again.")
                    clear_terminal()
                # except ValueError:
                #     input("Please enter a valid number.")
                #     clear_terminal()
        else:
            clear_terminal()
            input("Your wizard was unsure of your action, try again.")

    def increase_stat(self, stat, xp):
        if stat == "devotion":
            input("You gained " + str(xp) + "XP towards Devotion!")
            self.gain_xp("devotion", xp)  # Gain XP
        elif stat == "whimsy":
            input("You gained " + str(xp) + "XP towards Whimsy!")
            self.gain_xp("whimsy", xp)
        elif stat == "iniquity":
            input("You gained " + str(xp) + "XP towards Iniquity!")
            self.gain_xp("iniquity", xp)

    def gain_xp(self, stat_name, amount):
        stat = getattr(self, stat_name)
        stat['xp'] += amount
        while stat['xp'] >= stat['required']:
            stat['xp'] -= stat['required']
            stat['level'] += 1
            # Increase difficulty
            stat['required'] = int(stat['required'] * 1.5)
            input(
                f"{self.name}'s {stat_name.capitalize()} increased to level {stat['level']}!")

    def spell_choice(self, choice):
        stat_map = {
            1: 'devotion',
            2: 'whimsy',
            3: 'iniquity'
        }

        if choice not in stat_map:
            input("Invalid choice.")
            return

        stat_name = stat_map[choice]
        stat_level = self.__dict__[stat_name]['level']
        spells = self.spellbook.get(stat_name, [])

        # Find the next learnable spell
        next_spell = None
        for spell in spells:
            if spell['name'] not in self.learned_spells:
                if stat_level >= spell['level']:
                    next_spell = spell
                    break
                else:
                    # Stop here: future spells not shown
                    break

        while True:
            clear_terminal()
            print(f"📖 {stat_name.capitalize()} Tome (Level {stat_level})\n")

            if next_spell:
                print(f"1. {next_spell['name'].title()} 🔓")
                user_input = input(
                    "\nAttempt to learn this spell? (y/n or 'b' to go back): ").strip().lower()

                if user_input == 'b':
                    return  # Go back to stat selection
                elif user_input in yesVariations:
                    return self.attempt_single_spell_learn(next_spell)
                elif user_input in noVariations:
                    input("Very well. You may choose again later.")
                    return
                else:
                    input("Please type 'y', 'n', or 'b'.")
            else:
                input("No spells are currently available to learn for this stat.")
                return

    def attempt_single_spell_learn(self, spell):
        if spell['name'] in self.learned_spells:
            input(f"You already know the {spell['name']} spell.")
            return

        rand = random.random()
        print(rand)
        if rand < spell['chance']:
            self.learned_spells.append(spell['name'])
            input(f"✨ You learnt the {spell['name']} spell!")
            return 'gain'
        else:
            input(f"The spell eludes your grasp... Try again another time.")
            return 'gain'

    def add_item(self, item, amount=1):
        self.inventory[item] = self.inventory.get(item, 0) + amount
        print(f"🧺 Added {amount}x {item.title()} to inventory.")

    def remove_item(self, item, amount=1):
        if self.inventory.get(item, 0) >= amount:
            self.inventory[item] -= amount
            if self.inventory[item] == 0:
                del self.inventory[item]
            print(f"🗑 Removed {amount}x {item.title()} from inventory.")
            return True
        else:
            print(f"⚠️ Not enough {item} in inventory.")
            return False

    def show_inventory(self):
        clear_terminal()
        print("🎒 Inventory:")
        if not self.inventory:
            print("  (empty)")
        else:
            for item, count in self.inventory.items():
                print(f"  - {item.title()}: {count}")

    def unlock_spell(self, stat, spell):
        """
        Unlocks a new spell for the wizard under the given stat category (e.g., devotion).
        """
        if stat not in self.spellbook:
            self.spellbook[stat] = []

        # Prevent duplicates
        if any(s['name'] == spell['name'] for s in self.spellbook[stat]):
            print(
                f"🔮 {self.name} already has the spell '{spell['name']}' in {stat}.")
            return

        self.spellbook[stat].append(spell)
        print(
            f"✨ {self.name} has unlocked a new {stat} spell: '{spell['name']}'!")

    def view_knowledge(self):
        clear_terminal()
        print(f"📘 Arcane Knowledge of {self.name} the {self.type}:\n")

        print("🔮 Known Properties:")
        if self.known_properties:
            for prop in sorted(self.known_properties):
                print(f"  - {prop}")
        else:
            print("  (none discovered yet)")

        print("\n📖 Learned Spells:")
        if self.learned_spells:
            for spell in self.learned_spells:
                print(f"  - {spell.title()}")
        else:
            print("  (none learned yet)")

        # print("\n🧠 Unlocked Spells:")
        # if self.unlocked_spells:
        #     for spell in self.unlocked_spells:
        #         print(f"  - {spell.title()}")
        # else:
        #     print("  (none unlocked yet)")

    def progress_war(self):
        if self.war == 0:
            self.war = round(random.uniform(0.0, 0.5), 2)
            return f"War has started at {self.war}%."
        elif self.war >= 0.9:
            self.war = 0
            return "War has begun! Resetting war chance."
        else:
            self.war = round(self.war + 0.1, 2)
            return f"War chance increased to {self.war}%."


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
