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
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def scoreDistancesHelper(self, array, pos):
        currentBest = 999
        for item in array:
            tempDistance = abs(pos[0] - item[0]) + abs(pos[1] - item[1])
            if currentBest > tempDistance:
                currentBest = tempDistance
        return currentBest

    def ghostDistancesHelper(self, array, pos):
        currentBest = 999
        for item in array:
            itemPos = item.configuration.pos
            tempDistance = abs(pos[0] - itemPos[0]) + abs(pos[1] - itemPos[1])
            if currentBest > tempDistance:
                currentBest = tempDistance
        return currentBest

    def ghostNextHelper(self, array, pos):
        for item in array:
            if item.configuration.pos == pos:
                return True
        return False

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minimax(self, agent, depth, gameState: GameState):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), 0

        legalMoves = gameState.getLegalActions(agent)
        maxScore = float("-inf")
        worstScore = float("inf")
        bestDirection = "Stop"

        if agent == 0:
            legalMoves = gameState.getLegalActions(agent)

            for move in legalMoves:
                successor = gameState.generateSuccessor(agent, move)
                successorScore = self.minimax(agent + 1, depth, successor)[0]
                if successorScore > maxScore:
                    maxScore = successorScore
                    bestDirection = move
            return maxScore, bestDirection

        nextAgent = agent + 1
        countAgents = gameState.getNumAgents()
        if agent == countAgents - 1:
            nextAgent = 0
            depth += 1

        for move in legalMoves:
            successor = gameState.generateSuccessor(agent, move)
            successorScore = self.minimax(nextAgent, depth, successor)[0]
            if worstScore > successorScore:
                worstScore = successorScore
                bestDirection = move
        return worstScore, bestDirection

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
        return self.minimax(0, 0, gameState)[1]

        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    def alphaBeta(self, agent, depth, gameState: GameState, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), 0

        legalMoves = gameState.getLegalActions(agent)
        maxScore = float("-inf")
        worstScore = float("inf")
        bestDirection = "Stop"

        if agent == 0:
            legalMoves = gameState.getLegalActions(agent)
            for move in legalMoves:
                successor = gameState.generateSuccessor(agent, move)
                successorScore = self.alphaBeta(
                    agent + 1, depth, successor, alpha, beta)[0]
                if successorScore > maxScore:
                    maxScore = successorScore
                    bestDirection = move
                if alpha < maxScore:
                    alpha = maxScore
                if alpha > beta:
                    break
            return maxScore, bestDirection

        nextAgent = agent + 1
        numOfAgents = gameState.getNumAgents()
        if agent == numOfAgents - 1:
            nextAgent = 0
            depth += 1

        for move in legalMoves:
            successor = gameState.generateSuccessor(agent, move)
            successorScore = self.alphaBeta(
                nextAgent, depth, successor, alpha, beta)[0]
            if worstScore > successorScore:
                worstScore = successorScore
                bestDirection = move
            if beta > worstScore:
                beta = worstScore
            if alpha > beta:
                break
        return worstScore, bestDirection

    def getAction(self, gameState: GameState):
        return self.alphaBeta(0, 0, gameState, float("-inf"), float("inf"))[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    def expectiMax(self, agent, depth, gameState: GameState):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), 0

        bestCase = float("-inf")
        bestDirection = "Stop"
        legalMoves = gameState.getLegalActions(agent)
        sumOfMinScores = 0
        numOfChildren = len(legalMoves)
        numOfAgents = gameState.getNumAgents()

        if agent == 0:
            legalMoves = gameState.getLegalActions(agent)

            for move in legalMoves:
                successor = gameState.generateSuccessor(agent, move)
                successorScore = self.expectiMax(
                    agent + 1, depth, successor)[0]
                if successorScore > bestCase:
                    bestCase = successorScore
                    bestDirection = move
            return bestCase, bestDirection

        nextAgent = agent + 1
        if agent == numOfAgents - 1:
            nextAgent = 0
            depth += 1

        for move in legalMoves:
            successor = gameState.generateSuccessor(agent, move)
            eachMinScore = self.expectiMax(nextAgent, depth, successor)[0]
            sumOfMinScores += eachMinScore
        expectedMin = sumOfMinScores / numOfChildren
        return expectedMin, 0

    def getAction(self, gameState: GameState):
        return self.expectiMax(0, 0, gameState)[1]


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
