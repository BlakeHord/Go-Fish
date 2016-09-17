from random import randint
from math import floor
import pygame

"""
PROBLEMS
-Procedures with a tie
-Better UI
"""

class Card(object): # Creates card object
    suitStr = "" # String for printing suit
    numStr = "" # String for printing number
    def __init__(self, num, suit): #initializes card when created, takes number for card num and suit
        self.num = num
        self.suit = suit
        if suit == 1:
            self.suitStr = "Spades" #Declares suit
        elif suit == 2:
            self.suitStr = "Clubs"
        elif suit == 3:
            self.suitStr = "Hearts"
        elif suit == 4:
            self.suitStr = "Diamonds"

        if self.num < 11:
            self.numStr = str(self.num) # if the number is less than 11, it means its number is the same as its name
        elif self.num == 11:
            self.numStr = "Jack"
        elif self.num == 12:
            self.numStr = "Queen"
        elif self.num == 13:
            self.numStr = "King"
        elif self.num == 14:
            self.numStr = "Ace" #14 is ace (high card)

    def printCard(self):
        print self.numStr, "of", self.suitStr #prints card (eg. ace of spaces), just like it says

    def upperNum(self):
        return self.numStr.upper()

class Deck(object): #Deck object
    unShuffCards = [] #array for cards unshuffled
    cards = [] #array for shuffled cards
    def __init__(self, num):
        self.num = num #declares number of cards
        for i in range(0, self.num): #cycles through number of cards in deck
            dude = Card((i % 13) + 2, floor(i / 13) + 1) #declares cards, assigning 2-14 and 1-4 for num and suit
            self.unShuffCards.append(dude) #adds it to list

        while len(self.cards) < self.num: #while the length of shuffled cards is less than the specified number of cards in the deck
            llama = randint(0, len(self.unShuffCards) - 1) #randon num from 0 to 1 less than the length of the OG cards
            if self.unShuffCards[llama] not in self.cards: #if the random index specified is not in the new deck
                self.cards.append(self.unShuffCards[llama]) #add from unshuffled cards the new card
                self.unShuffCards.pop(llama) #deletes card in unshuffled deck, makes things faster

class Player(object): #Player class (including their hand)
    def __init__(self):
        self.matches = 0 #sets number of matches (points) = 0, cards = 0, array of cards empty
        self.numCards = 0
        self.cards = []

    def printHand(self): #does what it says - iterates throught hand array & prints number of points you have
        print "Your Cards: \t\tYour Points:", self.matches
        for dude in self.cards:
            dude.printCard()

    def isCard(self, card): #how to tell if a card is in the hand or not, so they can go fishing
        for dude in self.cards:
            if dude.numStr.upper() == card.upper():
                return True
        else:
            return False

def dealOne(deck, player): #deals one from the deck to a player - to be compounded to start the game and go-fish
    player.cards.append(deck.cards[0])
    player.numCards += 1
    deck.cards.pop(0)
    deck.num -= 1

def dealFive(deck, player): #deals five cards from the deck to a player - starting the game
    for x in range(5):
        dealOne(deck, player)

def cardTransfer(player1, player2, num): #finds all cards matching a card's number and gives them all to the first player
    i = 0
    cache = []
    for index in range(player2.numCards):
        if player2.cards[index].numStr.upper() == num.upper():  #When they match
            player1.cards.append(player2.cards[index]) #add it to player 1
            player1.numCards += 1
            i += 1
            cache.append(index) #add the location in player 2's hand to an array

    for j in range(len(cache)):
        player2.cards.pop(cache[j] - j) #pop the card at the location held in the cache minus the index in
        player2.numCards -= 1           #the cache, to account for previous popping
    return i

def bookDelete(player, card): #Pops a set of 4 same number cards (book) out of the player's hand
    i = 0
    for dude in player.cards:
        if dude.numStr.upper() == card.upper():
            player.cards.pop(dude)
            i += 1
        if i == 4:
            player.numCards -= 4
            break

def hasFour(player, num): #checks if a player has all four of a given card - to be done after receiving a card
    count = 0 #sets number of received card to 0
    for dude in player.cards: #iterates through player's hand looking for card
        if dude.upperNum() == num.upper(): #if it sees one, increment the count
            count += 1

    cache = []
    if count == 4: #if you have four of a kind
        for thing in range(player.numCards): #iterate through hand, adding the locations of the cards
            if player.cards[thing].numStr.upper() == num.upper():
                cache.append(thing)
        for j in range(len(cache)): #Pops the designated cards
            player.cards.pop(cache[j] - j)
            player.numCards -= 1
        player.matches += 1 #increment the number of point the player has
        return True
    return False

def checkAndDelete(player, num, playnum): #uses hasFour() to check if player has a book, deletes extra cards and gives player a point
    if hasFour(player, num) == True:
        bookDelete(player, num)
        player.matches += 1
        print "Player", playnum, "has all four", card + "'s. They made a \"book\""

def checkPlayerCards(player, deck, playnum): #Checks to see if the player needs more cards when they are out
    if player.numCards == 0: #if they are out of cards
        if deck.num >= 5:
            dealFive(deck, player) #deal five cards if there are five cards
            print "Player", playnum, "ran out of cards, so they get to draw five more"
        elif deck.num > 0: #if there are less than 5 but more than 0 cards in the deck
            decknum = deck.num
            for card in range(decknum):
                dealOne(deck, player) #deal the rest to the player
            print "Player", playnum, "got the last", decknum, "cards left in the deck"
        else: #if there are no more cards left in the deck
            print "There are no cards left in the deck and Player", playnum, "has no cards left in their hand. Wait for the other players to finish"

def checkGameOver(playerList, deck): #Checks to see if the game is over, when no one has any cards left
    if deck.num == 0:
        for player in playerList:
            if player.numCards == 0:
                continue
            else:
                return 1 #returns 1 if there are cards still in play
    else:
        return 1
    return 0

def determineWinner(playerlist): #Reveals who won the game
    playnum = 0
    maxplaynum = 0
    maxmatches = 0
    for player in playerList: #cycle through the players
        playnum += 1
        if player.matches > maxmatches: #if a player has more than the current maximum books, they become the new maximum
            maxmatches = player.matches
            maxplaynum = playnum

    #NEED TO FIGURE OUT WAY TO INCORPORATE TIES
    print "Player", playnum, "won with", maxmatches, "books!"

#Initializes play--------------------------------------------------------------
playerList = [] #empty list of players
master = Deck(52) #creation of deck

print "\nYou are now playing Go Fish! \n\nThe object of the game is to collect as many \"books\", or groups of 4 of the same numbered card, by the end of the game.\n" \
      "You start with 5 cards. When prompted, ask a computer player for a card to match a card that you have in your hand.\n" \
      "If they have it, they must give it to you, but if they don't, go fish and draw a card from the deck.\n\nOnce you collect four of a kind, it is removed from your hand.\n\n" \
      "Press enter to continue playing the game"

jackdiddly = raw_input("")
numplayers = 0

while numplayers < 1 or numplayers > 4: #prompt for how many players to play against
    numplayers = int(raw_input("How many players do you want to play against? (1-4) "))
print

for ctr in range(numplayers + 1): #creates the players, including the human player, and deals five cards to each
    x = Player()
    playerList.append(x)
    dealFive(master, playerList[ctr])

#Gameplay----------------------------------------------------------------------
while True: #Infinite Loop
    playnum = 0
    for turn in playerList: #Goes through each player's turn
        playnum += 1
        if checkGameOver(playerList, master) == 0: #Check for the end of game at the start of each person's turn
            determineWinner(playerList)

        if turn == playerList[0]: #If it is the human player's turn

            checkPlayerCards(turn, master, playnum)
            turn.printHand() #prints your cards
            print
            choice = 0
            card = "" #sets blank values for player choice and what card they want
            while 1: #Who ask for card
                print "Who would you like to ask for a card?"
                for ctr in range(2, len(playerList) + 1): #Print out player numbers from 2 to last num in player list
                    print "Player", str(ctr), "\t",
                choice = int(raw_input("\n")) - 1
                if choice > 0 and choice < len(playerList): #if the choice they entered is within the ranges of the playerlist
                    break
            while 1: #Which card
                card = raw_input("What card would you like to ask for? ")
                print
                if turn.isCard(card) == True: #if the card they ask for is in their hand, keep it
                    break

            if playerList[choice].isCard(card) == True: #if the player they chose has the card that they chose
                take = cardTransfer(turn, playerList[choice], card) #transfer the cards that the chosen player has to the human
                if take > 1:
                    print "You took", str(take), card + "s from Player", str(choice + 1) #gotta make sure it's plural
                else:
                    print "You took a", card, "from Player", str(choice + 1)
                print
                checkAndDelete(turn, card, playnum)
                turn.printHand()
            else:
                print "Go Fish!\n"
                if master.num > 0: #if there are still cards left in the deck
                    dealOne(master, turn) #deal a card to the player
                    checkAndDelete(turn, turn.cards[turn.numCards - 1].numStr, playnum)
                    turn.printHand()
                else:
                    print "No more cards in the deck! Continue the game until every player runs out of cards"
        else: #If it is not the human's turn
            while True:
                choice = randint(0, len(playerList) - 1) #generate random number
                if playerList[choice] != turn: #so long as the random number is not the index of the current player
                    break

            checkPlayerCards(turn, master, playnum)

            card = turn.cards[randint(0,len(turn.cards) - 1)].numStr #card they're looking for is a random card of theirs

            if choice == 0:
                print "Player", playnum, "asks you if you have any", card, "\'s"
            else:
                print "Player", playnum, "asks Player", choice + 1, "if they have any", card, "\'s" #THE ASK

            if playerList[choice].isCard(card) == True: #if the player they chose has the card that they chose
                take = cardTransfer(turn, playerList[choice], card) #transfer the cards that the chosen player has to the human
                if choice == 0:
                    buffstr = "you"
                else:
                    buffstr = "Player", str(choice + 1)

                if take > 1:
                    print "Player", playnum, "took", str(take), card + "'s from", buffstr #gotta make sure it's plural
                else:
                    print "Player", playnum, "took a", card, "from", buffstr #singular, yo
                checkAndDelete(turn, card, playnum)
            else:
                print "Go Fish!"
                if master.num > 0: #if there are still cards left in the deck
                    dealOne(master, turn) #deal a card to the player
                    checkAndDelete(turn, turn.cards[turn.numCards - 1].numStr, playnum)
                else:
                    print "No more cards in the deck!"

        buff = raw_input("")
