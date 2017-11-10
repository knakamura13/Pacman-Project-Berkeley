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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        for move in legalMoves:
          if move == 'Stop':
            legalMoves.remove(move)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        "* YOUR CODE HERE *"
        shouldRunAway = False # initialize running away as false each time
        for ghostState in newGhostStates: #iterate through all the ghosts
            #get the ghosts position
            x = ghostState.configuration.getPosition()[0]
            y = ghostState.configuration.getPosition()[1]
            if abs(newPos[0]-x) ==0 and abs(newPos[1]-y) ==0: #check to see if pacman will end up on top of ghost
                print"RUN!"
                return -100
            elif abs(newPos[0]-x) <=1 and abs(newPos[1]-y) <=1: #check to see if pacman will end up on top of ghost
                print"RUN!"
                return -1
        if currentGameState.getFood()[newPos[0]][newPos[1]]==True: # checjs to see
            return 10000
        minDist = 999999
        for food in successorGameState.getFood():
            dist = manhattanDistance(newPos, food)
            if dist<minDist:
                minDist = dist
        if minDist <= 2:
            return 9000
        #we cant find the next closest pellet when it is more than 1 away
        else:
            return 1000
       # return #successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

      You do not need to make any changes here, but you can if you want to
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

    def getAction(self, gameState):
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
        """
        "* YOUR CODE HERE *"
        agentIndex = 0
        maxScore = -100000000
        bestAction = "N/A"
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action) # pacmans turn
            score = self.value(successor, 1, self.depth) #next turn
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        
        
    def value(self, successor, agentIndex, depth):
        if agentIndex == successor.getNumAgents():
            agentIndex = 0
        if successor.isWin() or successor.isLose() or depth==0:
            return self.evaluationFunction(successor)
        elif agentIndex ==0:
            depth = depth-1
            return self.maxValue(successor, agentIndex, depth)
        elif agentIndex !=0:
            return self.minValue(successor, agentIndex, depth)
            
    def maxValue(self, state, agentIndex, depth):
        v = -1000000
        for action in state.getLegalActions(0):
            successor = state.generateSuccessor(0, action)
            v = max(v, self.value(successor, 1, depth))
        agentIndex = agentIndex+1
        return v
    
    def minValue(self, state, agentIndex, depth):
        v = 1000000
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action) # needs to be ghost actions #SOMETHING TO DO WITH THIS IS GENERATING THE SUCCESSORS SUCCESSORS
            v = min(v, self.value(successor, agentIndex+1, depth))  
        agentIndex = agentIndex + 1
        return v
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "* YOUR CODE HERE *"
        agentIndex = 0
        maxScore = -100000000
        alpha = -1000000000
        Beta = 1000000000
        bestAction = "N/A"
        for action in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, action) # pacmans turn
            score = self.value(successor, 1, self.depth, alpha, Beta) #next turn
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        
        
    def value(self, successor, agentIndex, depth, alpha, Beta):
        if agentIndex == successor.getNumAgents():
            agentIndex = 0
        if successor.isWin() or successor.isLose() or depth==0:
            return self.evaluationFunction(successor)
        elif agentIndex ==0:
            depth = depth-1
            return self.maxValue(successor, agentIndex, depth, alpha, Beta)
        elif agentIndex !=0:
            return self.minValue(successor, agentIndex, depth, alpha, Beta)
            
    def maxValue(self, state, agentIndex, depth, alpha, Beta):
        v = -1000000
        for action in state.getLegalActions(0):
            successor = state.generateSuccessor(0, action)
            v = max(v, self.value(successor, 1, depth, alpha, Beta))
            if v >= Beta:
                return v
            alpha = max(alpha, v)
        agentIndex = agentIndex+1
        return v
    
    def minValue(self, state, agentIndex, depth, alpha, Beta):
        v = 1000000
        for action in state.getLegalActions(agentIndex):
            successor = state.generateSuccessor(agentIndex, action) # needs to be ghost actions #SOMETHING TO DO WITH THIS IS GENERATING THE SUCCESSORS SUCCESSORS
            v = min(v, self.value(successor, agentIndex+1, depth, alpha, Beta))
            if v<= alpha:
                return v
            Beta = min(Beta, v)
        agentIndex = agentIndex + 1
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "* YOUR CODE HERE *"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "* YOUR CODE HERE *"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction