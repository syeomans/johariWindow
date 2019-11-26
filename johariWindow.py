# import sys
from os import system, name
from random import randint

# Function to clear the console
def clear():
    if name == 'nt': # for windows
        _ = system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        _ = system('clear')

# Get all adjectives from adjectives.txt
with open('adjectives.txt', 'r') as f:
    adjectives = f.read().split()

# Get the number of players
print("How many players are there?")
numPlayers = int(input())

# Get the number of words to use
print("How many words do you want to use? (max " + str(len(adjectives)) + ")")
numWords = int(input())
numWords = min(numWords, len(adjectives))

# Randomly choose numWords number of adjectives to keep
newAdjectives = []
for i in range(0,numWords):
    newAdjectives.append(adjectives.pop(randint(0,len(adjectives)-1)))
adjectives = newAdjectives

clear()

# Get player names
playerNames = []
for i in range(0, numPlayers):
    print("What is player " + str(i+1) + "'s name?")
    playerNames.append(input())

clear()

# Initialize responses list as a 2D array
# read as: "player [row i] thinks player [col j] is [response]"
responses = []
for i in range(0, numPlayers):
    responses.append([])
    for j in range(0, numPlayers):
        responses[i].append([])

# Ask each player for responses
for j in range(0, numPlayers):
    for i in range(0,numPlayers):
        # Print whose turn it is
        print("Player " + str(i+1) + "'s turn")
        print(playerNames[i] + " can look at the screen")
        # Go through each word
        for word in adjectives:
            response = "easter egg"
            # Keep asking for a response until the user says y, n, yes, or no
            while response.lower() not in ['y', 'n', 'yes', 'no']:
                if i == j: # Player is being asked about himeslf
                    response = input("Do you think you are " + word + "? (y/n): ")
                else: # Player is being asked about someone else
                    response = input("Do you think " + playerNames[j] + " is " + word + "? (y/n): ")
            # Record response
            if response[0].lower() == 'y':
                responses[i][j].append(word)
        clear()

# Collect responses into two columns: self's responses and others' responses
processedData = []
for i in range(0, numPlayers):
    col1 = responses[i][i]
    col2 = []
    for j in range(0, numPlayers):
        if i != j:
            col2 += responses[i][j]
    # col2 = list(set(col2)) # remove duplicates
    processedData.append([col1, col2])

# Create a Johari window for each player
windows = []
for i in range(0, numPlayers):
    windows.append({'Name': playerNames[i], 'Arena': [], 'Blind Spot': [], "Facade": []})
    # for j in range(0, numPlayers):
    for word in adjectives:
        # Known to self and others
        if word in processedData[i][0] and word in processedData[i][1]:
            windows[i]['Arena'].append(word)
        # Known to self, but not others
        elif word in processedData[i][0] and word not in processedData[i][1]:
            windows[i]['Facade'].append(word)
        # Known to others, but not self
        elif word not in processedData[i][0] and word in processedData[i][1]:
            windows[i]['Blind Spot'].append(word)

# Create an html doc to display each player's johari window

# Open template
template = open('template.html', 'r')
htmlString = ""
for char in template:
    htmlString += char
template.close()

# Edit template
for i in windows:
    outfile = open('outputs/'+i['Name']+'JohariWindow.html', 'w')
    outString = htmlString.replace("namePlaceholder", i['Name'])
    outString = outString.replace("arenaPlaceholder", "Arena: " + ", ".join(i['Arena']))
    outString = outString.replace("facadePlaceholder", "Facade: " + ", ".join(i['Facade']))
    outString = outString.replace("blindSpotPlaceholder", "Blind Spot: " + ", ".join(i['Blind Spot']))
    outfile.write(outString)
    outfile.close()
