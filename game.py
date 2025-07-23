from spellsystem import SpellSystem
from wizard import Wizard
import random
import os
import json


class Game:
    def __init__(self):
        self.wizard = None
        self.listOfNames = ['Thalorin', 'Bramwick',
                            'Zepharion', 'Nymera', 'Caldrin']
        self.wizardTypes = ['Unconventional', 'Righteous', 'Rogue']

    def menu(self):
        while True:
            print("Welcome to Wizard Trainer 1000!")
            print("1) New Wizard")
            print("2) Load Wizard")
            print("3) Ingredients Book")
            print("4) Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.new_wizard()
                break
            elif choice == '2':
                clear_terminal()
                self.load_wizard()
                break
            elif choice == '3':
                clear_terminal()
                self.ingredients_book()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                input("Invalid choice, try again.")
                clear_terminal()

    def new_wizard(self):
        # Here you could ask for name/type, or random generate
        clear_terminal()
        name = random.choice(self.listOfNames)
        wizard_type = random.choice(self.wizardTypes)
        self.wizard = Wizard(name, wizard_type)
        input(f"Created new wizard: {name} the {wizard_type}!")
        # Call war mechanic after actions
        # war_result = self.wizard.progress_war()
        # print(war_result)
        self.wizard.action_menu()
        self.wizard.display_stats()
        self.save_wizard()

    def load_wizard(self):
        save_dir = "saves"
        if not os.path.exists(save_dir):
            print("No save directory found.")
            return

        save_files = [f for f in os.listdir(save_dir) if f.endswith(".json")]

        if not save_files:
            print("No save files found.")
            return

        while True:
            try:
                print("Available save files:")
                for idx, file in enumerate(save_files):
                    print(f"{idx + 1}) {file}")
                choice = int(input("Select a file number to load: "))

                if 1 <= choice <= len(save_files):
                    selected_file = os.path.join(
                        save_dir, save_files[choice - 1])
                    break
                else:
                    input("Invalid choice. Try again.")
                    clear_terminal()
            except ValueError:
                input("Please enter a valid number.")
                clear_terminal()

        try:
            with open(selected_file, "r") as f:
                data = json.load(f)
                self.wizard = Wizard.from_dict(data)
            input(f"{self.wizard.name} has been loaded. Press Enter to continue.")
            clear_terminal()
        except Exception as e:
            print(f"Failed to load wizard: {e}")
            return
        # Display the stats of the loaded wizard
        self.wizard.display_stats()
        clear_terminal()
        self.wizard_menu()
        # Ask for their actions
        # self.wizard.action_menu()
        # wizard is your Wizard instance
        # spell_system = SpellSystem(self.wizard)
        # spell_system.experiment()
        # Display the stats after doing their actions
        # self.wizard.display_stats()
        # Save the wizard after all daily actions have completed
        self.save_wizard()

    def save_wizard(self):
        if self.wizard:
            filename = f"{self.wizard.name}_the_{self.wizard.type}.json"
            save_dir = "saves"
            # Ensure the 'saves/' directory exists
            os.makedirs(save_dir, exist_ok=True)
            filepath = os.path.join(save_dir, filename)

            with open(filepath, "w") as f:
                json.dump(self.wizard.to_dict(), f, indent=2)
            print(
                f"{self.wizard.name} the {self.wizard.type} has been saved to {filepath}.")
        else:
            print("No wizard to save.")

    def ingredients_book(self):
        world_file = "world.json"
        if not os.path.exists(world_file):
            print("🧪 No ingredients have been discovered yet.")
            input("Press Enter to return to the menu.")
            clear_terminal()
            return

        with open(world_file, "r") as f:
            world_data = json.load(f)

        print("📖 INGREDIENTS BOOK\n")
        for item, methods in world_data.items():
            print(f"{item.title()}:")
            for method, entry in methods.items():
                prop = entry.get("property")
                discoverer = entry.get("discovered_by", "Unknown")
                if prop:
                    print(
                        f"  🔹 {method.title()} → {prop} (discovered by {discoverer})")
                else:
                    print(
                        f"  🔸 {method.title()} → No result (discovered by {discoverer})")
            print()

        input("Press Enter to return to the main menu.")
        clear_terminal()

    def wizard_menu(self):
        while self.wizard.ap > 0:
            clear_terminal()
            print(f"🕒 Action Points: {self.wizard.ap}")
            print("What would you like to do?")
            print("1) Perform an activity (read, scheme, question)")
            print("2) Learn spells")
            print("3) Forage for ingredients")
            print("4) Experiment")
            print("5) View known spells and properties")
            print("6) View Inventory")
            print("7) End the day")

            choice = input("Choose an option: ").strip()

            match choice:
                case '1':
                    self.wizard.perform_activity()
                case '2':
                    self.wizard.handle_spells()
                case '3':
                    self.wizard.forage()
                case '4':
                    spell_system = SpellSystem(self.wizard)
                    spell_system.experiment()
                case '5':
                    self.wizard.view_knowledge()
                    input("\nPress Enter to return.")
                case '6':
                    self.wizard.show_inventory()
                    input("\nPress Enter to return.")
                case '7':
                    print("🌙 Your wizard rests for the night...")
                    break
                case _:
                    input("Invalid choice. Press Enter to try again.")

        self.wizard.days += 1
        clear_terminal()
        input("The day ends. Time marches on...")

    def start(self):
        clear_terminal()
        # This can start the game after menu, or handle game loop
        self.menu()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
