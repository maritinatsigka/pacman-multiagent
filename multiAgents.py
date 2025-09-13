# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        nearestFood = []
        x, y = newPos

        newFood = newFood.asList()
        # for food in newFood:
        for food in currentGameState.getFood().asList():
            foodX, foodY = food
            nearestFood.append(manhattanDistance((foodX, foodY), (x,y)))
        for ghostState in newGhostStates:
            ghostX, ghostY = ghostState.getPosition()
            if manhattanDistance((ghostX, ghostY), (x, y)) == 0:
                return float("-inf")
            

        if nearestFood:
            minFood = min(nearestFood)
            #the lower the minFood, the better
            return successorGameState.getScore() + 1/(1 + minFood)
        else: 
            return float("-inf")
        
def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ret = self.value(-1, gameState, -1)
        
        return ret[1]
    
    def value(self, index, gameState, depth):
        index = (index + 1) % (gameState.getNumAgents())

        if index == 0: 
            depth += 1

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), "Stop")
        elif index == 0:  # when index = 0, then the maxValue is returned because maximizing player begins game
            return self.maxValue(index, gameState, depth)
        else:
            return self.minValue(index, gameState, depth)
        
    def maxValue(self, index, gameState, depth):
        maximum = float("-inf")
        maxAction = "Stop"

        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)
            newValue = self.value(index, successorGameState, depth)[0]
            if newValue > maximum:
                maximum = newValue
                maxAction = action
        return (maximum, maxAction)
    
    def minValue(self, index, gameState, depth):
        minimum = float("inf")
        minAction = "Stop"

        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)
            newValue = self.value(index, successorGameState, depth)[0]
            if newValue < minimum:
                minimum = newValue
                minAction = action
        return (minimum, minAction)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ret = self.value(-1, gameState, -1, float("-inf"), float("inf"))

        return ret[1]
    
    def value(self, index, gameState, depth, alpha, beta):
        index = (index + 1) % (gameState.getNumAgents())

        if index == 0:
            depth += 1

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), "Stop")
        elif index == 0:  # when index = 0, then the maxValue is returned because maximizing player begins game
            return self.maxValue(index, gameState, depth, alpha, beta)
        else:
            return self.minValue(index, gameState, depth, alpha, beta)
        

    def maxValue(self, index, gameState, depth, alpha, beta):
        maximum = float("-inf")
        maxAction = "Stop"
        # pacman base case

        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)
            newValue = self.value(index, successorGameState, depth, alpha, beta)[0]
            if newValue > maximum:
                maximum = newValue
                maxAction = action
            if maximum > beta:
                return (maximum, maxAction)
            if alpha < maximum:
                alpha = maximum
        return (maximum, maxAction)

    def minValue(self, index, gameState, depth, alpha, beta):
        minimum = float("inf")
        minAction = "Stop"

        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)
            newValue = self.value(index, successorGameState, depth, alpha, beta)[0]
            if newValue < minimum:
                minimum = newValue
                minAction = action
            if minimum < alpha:
                return (minimum, minAction)
            if beta > minimum:
                beta = minimum
        return (minimum, minAction)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        res = self.value(-1, gameState, -1)

        return res[1]
    
    def value(self, index, gameState, depth):
        index = (index + 1) % (gameState.getNumAgents())

        if index == 0:
            depth += 1

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), "Stop")
        elif index == 0:  # when index = 0, then the maxValue is returned because maximizing player begins game
            return self.maxValue(index, gameState, depth)
        else:
            return self.minValue(index, gameState, depth)
        
    def maxValue(self, index, gameState, depth):
        maximum = float("-inf")
        maxAction = "Stop"
        # pacman base case

        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)
            newValue = self.value(index, successorGameState, depth)[0]
            if newValue > maximum:
                maximum = newValue
                maxAction = action
        return (maximum, maxAction)

    def minValue(self, index, gameState, depth):
        minimum = float("inf")
        minAction = "Stop"
        p = 1.0/len(gameState.getLegalActions(index))
        newValue = 0
        for action in gameState.getLegalActions(index):
            successorGameState = gameState.generateSuccessor(index, action)

            newValue += p*self.value(index, successorGameState, depth)[0]

            minAction = action
        return (newValue, minAction)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    score = currentGameState.getScore()

    foodList = Food.asList()
    foodDistance = [manhattanDistance(Pos, food) for food in foodList]
    nearestGhostDistance = min([manhattanDistance(Pos, ghost.getPosition()) for ghost in GhostStates])
    weight_food = 1
    weight_reduced_food = 0.7

    if len(foodDistance) > 0:
        nearestFoodDistance = min(foodDistance)
        if ScaredTimes[0] > nearestGhostDistance:
            score += weight_reduced_food / (0.1 + nearestFoodDistance)
        else:
            score += weight_food / (0.1 + nearestFoodDistance)

    weight_ghost = 1
    if ScaredTimes[0] > nearestGhostDistance:
        score += weight_ghost / (0.1 + nearestGhostDistance)
    else:
        score -= weight_ghost / (0.1 + nearestGhostDistance)
    return score

# Abbreviation
better = betterEvaluationFunction
