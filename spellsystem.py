import os
import random
import json

WORLD_FILE = "world.json"


class SpellSystem:
    ITEMS = ['morinyite stone', 'undead amethyst', 'flaerrin', 'driftstone']
    VALID_ACTIONS = [
        'crush', 'boil', 'dry', 'burn', 'cut', 'polish', 'slice', 'soak', 'infuse',
        'freeze', 'press', 'whisper', 'expose', 'mix',
        'enchant', 'scry', 'transmute', 'channel', 'runemark', 'focus',
        'corrupt', 'cleanse', 'bind', 'taste', 'sing'
    ]
    ITEM_ACTIONS = {
        'morinyite stone': ['crush', 'boil', 'dry', 'cut'],
        'undead amethyst': ['boil', 'burn'],
        'flaerrin': ['crush', 'polish'],
        'driftstone': ['crush', 'infuse', 'expose', 'runemark']

    }

    ALL_PROPERTIES = ['energizing', 'toxic',
                      'soothing', 'brittle', 'slippery', 'smoky']

    SPELL_UNLOCK_REQUIREMENTS = {
        'praengenis': {'energizing', 'brittle', 'toxic', 'smoky'},
        'cruel expulsion': {'slippery', 'brittle', 'toxic', 'soothing'}
    }

    def __init__(self, wizard):
        self.wizard = wizard
        self.world_properties = load_world_properties()

    def experiment(self):
        while True:
            clear_terminal()
            print("🧪 Available Items:")
            # start=1 for 1-based numbering
            for i, item in enumerate(self.ITEMS, 1):
                print(f"{i}. {item.title()}")
            print("B. Go back")

            item_input = input(
                "\nChoose an item to experiment with: ").strip().lower()
            if item_input == 'b':
                return

            item_keys = list(self.ITEMS)
            if item_input.isdigit() and 1 <= int(item_input) <= len(item_keys):
                item = item_keys[int(item_input) - 1]
                self.choose_method(item)
            else:
                input("Invalid selection. Press Enter to continue.")

    def choose_method(self, item):
        while True:
            clear_terminal()
            print(f"🧪 {item.title()} - What would you like to do with it?")
            print("Type your action(Or type 'b' to go back)\n")

            method = input("Action: ").strip().lower()

            if method == 'b':
                return

            if method not in self.VALID_ACTIONS:
                input(
                    f"Your wizard is unsure of what action it should do with the {item}.")
                continue

            if method not in self.ITEM_ACTIONS.get(item, []):
                input(
                    f"That action seems to do nothing notable to the  {item}.")
                continue

            # Valid and meaningful → proceed with discovery
            self.perform_experiment(item, method)
            break

    def perform_experiment(self, item, method):
        wiz = self.wizard

        if item not in wiz.learned_properties:
            wiz.learned_properties[item] = {}

        if method in wiz.learned_properties[item]:
            prop = wiz.learned_properties[item][method]
            if prop:
                input(
                    f"🧠 You've already discovered '{prop}' from {method}ing the {item}.")
            else:
                input(f"{method.title()}ing the {item} previously revealed nothing.")
            return

        # Check if already discovered globally
        world_entry = self.world_properties.get(item, {}).get(method)
        if world_entry:
            prop = world_entry["property"]
            discoverer = world_entry["discovered_by"]

            wiz.learned_properties[item][method] = prop
            if prop:
                wiz.known_properties.add(prop)
                input(f"📜 You rediscovered '{prop}' by {method}ing the {item}.\n"
                      f"🧙 First discovered by: {discoverer}")
                self.check_for_spell_unlock()
            else:
                input(
                    f"{method.title()}ing the {item} yielded no result (as first discovered by {discoverer}).")
            return

        # First-time discovery (60% chance)
        if random.random() < 0.6:
            prop = random.choice(self.ALL_PROPERTIES)
            wiz.learned_properties[item][method] = prop
            wiz.known_properties.add(prop)

            # Save to world
            self.world_properties.setdefault(item, {})[method] = {
                "property": prop,
                "discovered_by": wiz.name
            }
            save_world_properties(self.world_properties)

            input(
                f"✨ You discovered the property: '{prop}' by {method}ing the {item}!")
            self.check_for_spell_unlock()
        else:
            wiz.learned_properties[item][method] = None
            self.world_properties.setdefault(item, {})[method] = {
                "property": None,
                "discovered_by": wiz.name
            }
            save_world_properties(self.world_properties)

            input(f"{method.title()}ing the {item} yielded no useful result.")

    def check_for_spell_unlock(self):
        wiz = self.wizard
        newly_unlocked = []

        for spell, required_props in self.SPELL_UNLOCK_REQUIREMENTS.items():
            if spell not in wiz.unlocked_spells and required_props.issubset(wiz.known_properties):
                wiz.unlocked_spells.append(spell)
                newly_unlocked.append(spell)

        if newly_unlocked:
            for spell in newly_unlocked:
                input(f"🌟 You’ve unlocked a new spell: '{spell.title()}'!")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_world_properties():
    if os.path.exists(WORLD_FILE):
        with open(WORLD_FILE, "r") as f:
            return json.load(f)
    return {}


def save_world_properties(world_props):
    with open(WORLD_FILE, "w") as f:
        json.dump(world_props, f, indent=2)
