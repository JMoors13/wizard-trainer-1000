
# You select a wizard and you level them up to create a powerful wizard. At a certain point in the game you can retire your current wizard and
# start a new character where you can pass down one ability to your apprentice.
import os
import random

wizardTypes = ['Unconventional', 'Righteous', 'Rogue']
yesVariations = ['yes', 'ya', 'yeah', 'ye', 'y', 'yas']
noVariations = ['no', 'nah', 'nope', 'na', 'n']
listOfNames = ['Thalorin', 'Bramwick', 'Zepharion', 'Nymera', 'Caldrin']
# actions = ['read', 'prod', 'ponder', 'stare', 'scheme', 'devour',
#            'sit', 'inscribe', 'question', 'discover', 'carve', 'venture']
actions1 = ['read', 'scheme', 'question']
actions2 = ['read', 'scheme', 'question']
actions3 = ['read', 'scheme', 'question']
wizardType = ''
wizardName = ''
devotion = 0
whimsy = 0
iniquity = 0
ap = 1
war = 0
days = 0


def menu():
    print("Welcome to Wizard Trainer 1000!")
    print("1) New Wizard\n2) Load Wizard\n3) Settings")
    return input()


def wizardSelection():
    clearTerminal()

    while True:
        print("The current available wizard types are:")
        print("1) " + wizardTypes[0])
        print("2) " + wizardTypes[1])
        print("3) " + wizardTypes[2])
        print("Or press '4' to return to the menu")
        userSelection = input()

        if userSelection in ['1', '2', '3']:
            clearTerminal()
            print("Your selection has been confirmed!")
            return wizardTypes[int(userSelection)-1]
        elif userSelection == '4':
            return 'b'
        else:
            clearTerminal()
            print("I couldn't understand which type you selected, please try again.")
            # If the user selects the wrong number 13 times, print "Are you stupid?" (secret achievement)


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def confirmation(wizardType):
    while True:
        characterConfirm = input(
            "Would you like to continue with the " + wizardType + " wizard?\n")
        if characterConfirm.lower() in noVariations:
            return 'n'
        elif characterConfirm.lower() in yesVariations:
            return 'y'
        else:
            clearTerminal()
            print('That response was unintelligible')


def gainedLevel(action):
    match action:
        case 'read':
            global devotion
            devotion += 1
            input("You gained a devotion level!")
        case 'scheme':
            global iniquity
            iniquity += 1
            input("You gained a iniquity level!")
        case 'question':
            global whimsy
            whimsy += 1
            input("You gained a whimsy level!")


def actionResponse(action):
    match action:
        case 'read':
            if devotion < 2:
                if random.random() < 0.50:  # 10% chance
                    input(wizardName +
                          " discovers the ancient art of cauldron aestetics!")
                    return '1'
                else:
                    input(wizardName + " reads a book. Honk-shooooo")
                    return '2'
            else:
                if random.random() < 0.10:  # 10% chance
                    input(
                        "This is only allowed for people with devotion greater than 2 10%")
                    return '1'
                else:
                    input(
                        "This is only allowed for people with devotion greater than 2 90%")
                    return '2'
        case 'scheme':
            if random.random() < 0.10:  # 10% chance
                input(wizardName + " orders the book 'how to scheme' from etsy!")
            else:
                input(wizardName +
                      " scribbles on a napkin in McDonalds your evil plans.")
        case 'question':
            if random.random() < 0.10:  # 10% chance
                input("What are the true motives of the Ministry for the Advancement of Global Enchantment if not to hinder arcane exploration")
            else:
                input("If every wand is a stick, is every stick a wand?")


def displayStats():
    input("Your stats are:"
          "\nDevotion:" + str(devotion) +
          "\nWhimsy:" + str(whimsy) +
          "\nIniquity:" + str(iniquity) +
          "\n\nDays Completed:" + str(days))


def saveWizard():
    # saveName = input("Enter a filename for your wizard: ")

    with open("save/" + wizardName + " the " + wizardType + ".txt", "w") as file:
        file.write("[Wizard Info]\n")
        file.write("Name:" + wizardName + "\n")
        file.write("Type:" + wizardType + "\n\n")

        file.write("[Stats]\n")
        file.write("Devotion:" + str(devotion) + "\n")
        file.write("Whimsy:" + str(whimsy) + "\n")
        file.write("Iniquity:" + str(iniquity) + "\n\n")

        file.write("[Progress]\n")
        # formats War to 2 decimal places
        file.write("War:" + f"{war:.2f}" + "\n")
        file.write("Days:" + str(days) + "\n")

    input(wizardName + " the " + wizardType + " has been saved!")


def loadWizard(filename):
    with open("save/"+filename, "r") as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                skill, value = line.split(':')
                match skill:
                    case 'Wizard Name':
                        global wizardName
                        wizardName = value
                    case 'Wizard Type':
                        global wizardType
                        wizardType = value
                    case 'Devotion':
                        global devotion
                        devotion = int(value)
                    case 'Whimsy':
                        global whimsy
                        whimsy = int(value)
                    case 'Iniquity':
                        global iniquity
                        iniquity = int(value)
                    case 'War':
                        global war
                        war = float(value)
                    case 'Days':
                        global days
                        days = int(value)


def listSaveFiles():
    files = [f for f in os.listdir("save")]
    return files


def willYouWarWigs():
    global war
    if war == 0:
        # If no value for 'war', set it below 50%
        temp = random.uniform(0.0, 0.5)
        war = f"{temp:.2f}"
        input("War has been set to " + str(war) + "%")
    elif war > 0.89:
        input("War, has begun!")
        war = 0
    else:
        # Increase chance of war by 10% daily
        war += 0.1
        input("War has increased to " + str(war) + "%")


def dailyActions():
    global ap
    while ap > 0:
        clearTerminal()
        # Display the action points left for the user
        if ap == 1:
            action = input("You have " + str(ap) +
                           " action points today to use.\nWhat action would you like to do?: ")
        else:
            action = input("You have " +
                           str(ap) + " remaining actions\nWhat would you like to do? ")
        # Determine if the user action is valid
        if action.lower() in actions1:
            clearTerminal()
            outcome = actionResponse(action)
            if outcome == '1':
                gainedLevel(action)
            else:
                input(wizardName + " learnt nothing :(")
            # input("The outcome is :" + outcome)
            # gainedLevel(action)
            # displayStats()
            action = ''
            ap -= 1
        elif action == '?':
            print("Here is a list of actions your wizard can perform:")
            for action in actions1:
                print(action)
            input("Press enter to continue")
        elif action == 'stats':
            clearTerminal()
            displayStats()
        else:
            clearTerminal()
            input("Your wizard was unsure of your action, try again.")


menuResponse = menu()
while menuResponse in ['1', '2', '3']:
    match menuResponse:
        case '1':  # New Wizard
            while True:
                wizardType = wizardSelection()              # Select wizard type
                if wizardType == 'b':                       # Return to menu detected
                    clearTerminal()
                    menuResponse = menu()                   # Get updated menuResponse value
                    break                                   # Exit case using new menuResponse

                # Confirm the users wizard type and only continue if they agree
                userResponse = confirmation(wizardType)

                clearTerminal()
                if userResponse == 'y':
                    wizardName = random.choice(listOfNames)
                    input("You have selected the " +
                          wizardType + " wizard " + wizardName + "!")
                    menuResponse = '4'
                    break

        case '2':  # Load wizard
            while True:
                clearTerminal()
                files = listSaveFiles()
                if files == []:
                    input("No files to load")
                    clearTerminal()
                    menuResponse = menu()
                    break
                else:
                    print("Enter the number of the wizard you would like to load:")
                i = 1
                for file in files:
                    print(str(i) + ") " + os.path.splitext(file)[0])
                    i += 1
                loadNumber = input()
                # Filter user response to be a number and in the range of save files
                try:
                    if 0 < int(loadNumber) < i:
                        input("Loaded Successfully!")
                        clearTerminal()
                        loadWizard(files[int(loadNumber)-1])
                        input("You've loaded the " +
                              wizardType + " wizard " + wizardName + "!")
                        menuResponse = '4'
                        break
                    else:
                        input("Please enter a number between 1 and " + str(i) + ".")
                except ValueError:
                    input("Please only use numbers.")

        case '3':  # Settings
            clearTerminal()
            print("Settings should be found here\nPress enter to go back")
            input()


displayStats()
clearTerminal()

dailyActions()
clearTerminal()

days += 1
input("Your wizard is tired for today. Day " + str(days) + " completed.")
clearTerminal()

willYouWarWigs()

saveWizard()
