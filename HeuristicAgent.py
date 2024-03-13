import random

class HeuristicAgent:
    def __init__(self,playerNumber,color):
        self.playerNumber = playerNumber
        self.color = color
        self.finishPriority = 100
        self.removeImpedence = 80 #always fairly high priority. Between one in the way and one out of the way, the one in the way is done first.
        self.initialAggression = random.randint(0,99) #incredibly passive to want to ruin your day over moving forward when the opportunity arises.
        self.currentAggression = self.initialAggression
        self.digger = random.randint(10,79) #How high priority is it to stick around to move pucks?
        self.moveNonLeadingPiece = random.randint(20,80)
    def __str__(self):
        return f"{self.color}, Priorities:\nFinish:{self.finishPriority}\nRemove Impeding Obstacles:{self.removeImpedence}\nInitial Aggression:{self.initialAggression}\nCurrent Aggression:{self.currentAggression}\nDigging Obsession Level:{self.digger}\nPriority on diversity:{self.moveNonLeadingPiece}"
    def decideNextAction(self):
        return
    def increaseAggression(self):
        '''Aggression is made to similate playing against a player who was slighted. Aka, if you stepped on their piece.'''
        angerAmount = (99-self.currentAggression)/random.randint(1,4) #on a 1, the agent has 'snapped'. Will seek vengeance for sure.
        self.currentAggression += angerAmount
    def decreaseAggression(self):
        '''Whenever a heuristic agent gets revenge, it will decrease aggression back towards their initial state. This won't stop the ones who want to see the game burn.'''
        decreaseAmount = (self.currentAggression-self.initialAggression)/2
        self.currentAggression -= decreaseAmount