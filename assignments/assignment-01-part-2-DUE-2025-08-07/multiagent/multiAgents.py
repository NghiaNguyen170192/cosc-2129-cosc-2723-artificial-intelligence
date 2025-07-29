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
import math
from typing import Tuple, Any
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
        capsules = currentGameState.getCapsules()

        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        print(newGhostStates)
        "*** YOUR CODE HERE ***"
        if action == "Stop":
            return -math.inf
        if not newFood.asList():
            return math.inf

        foodDistances = [manhattanDistance(
            newPos, food) for food in newFood.asList()]
        foodScore = 1 / min(foodDistances)

        ghostInfos = [
            (ghostState.getPosition(), scaredTime)
            for ghostState, scaredTime in zip(newGhostStates, newScaredTimes)
        ]

        scaredGhosts = [pos for pos, timer in ghostInfos if timer > 0]
        unscaredGhosts = [pos for pos, timer in ghostInfos if timer == 0]
        ghostScore = 0

        if scaredGhosts:
            distanceToScaredGhost = min(
                [manhattanDistance(newPos, ghost)
                 for ghost in scaredGhosts]
            )
            # chase scared ghosts!
            ghostScore += 10.0 / (distanceToScaredGhost + 1)

        if unscaredGhosts:
            ghostScore = min(
                [manhattanDistance(newPos, ghost)
                 for ghost in unscaredGhosts]
            )

        capsuleScore = 0
        if capsules:
            distanceToCapsule = min(
                [manhattanDistance(newPos, capsule) for capsule in capsules]
            )
            capsuleScore = 5.0 / (distanceToCapsule + 1)

        return successorGameState.getScore() + capsuleScore + foodScore * ghostScore


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
        # minimax returns a tuple: score and action
        _, action = self.runMiniMax(gameState, 0, 0)
        return action

    def runMiniMax(self, gameState: GameState, agentIndex: int, depth: int) -> Tuple[float, Any]:
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        legalActions = gameState.getLegalActions(agentIndex)
        nextGameStates = [gameState.generateSuccessor(
            agentIndex, action) for action in legalActions]
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth + (nextAgentIndex == 0)

        branches = []
        for nextGameState, action in zip(nextGameStates, legalActions):
            score, _ = self.runMiniMax(
                nextGameState, nextAgentIndex, nextDepth)
            branches.append((score, action))

        if agentIndex == 0:
            return max(branches)

        return min(branches)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        _, action = self.runAlphaBetaPruning(
            gameState, agentIndex=0, depth=0, alpha=-math.inf, beta=math.inf
        )
        return action

    def runAlphaBetaPruning(self, gameState: GameState, agentIndex: int, depth: int, alpha: float, beta: float) -> Tuple[float, Any]:
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        if agentIndex == 0:
            return self.getMaxValue(gameState, agentIndex, depth, alpha, beta)

        return self.getMinValue(gameState, agentIndex, depth, alpha, beta)

    def getMaxValue(self, gameState: GameState, agentIndex: int, depth: int, alpha: float, beta: float) -> Tuple[float, Any]:
        bestValue = -math.inf
        bestAction = None
        legalActions = gameState.getLegalActions(agentIndex)

        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            nextDepth = depth + (nextAgentIndex == 0)

            value, _ = self.runAlphaBetaPruning(
                nextGameState, nextAgentIndex, nextDepth, alpha, beta)

            if value > bestValue:
                bestValue, bestAction = value, action

            if bestValue > beta:
                break

            alpha = max(alpha, bestValue)

        return bestValue, bestAction

    def getMinValue(self, gameState: GameState, agentIndex: int, depth: int, alpha: float, beta: float) -> Tuple[float, Any]:
        bestValue = math.inf
        bestAction = None
        legalActions = gameState.getLegalActions(agentIndex)

        for action in legalActions:
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
            nextDepth = depth + (nextAgentIndex == 0)

            value, _ = self.runAlphaBetaPruning(
                nextGameState, nextAgentIndex, nextDepth, alpha, beta)

            if value < bestValue:
                bestValue, bestAction = value, action

            if bestValue < alpha:
                break

            beta = min(beta, bestValue)

        return bestValue, bestAction


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
        _, action = self.runExpectiMax(gameState, agentIndex=0, depth=0)
        return action

    def runExpectiMax(self, gameState: GameState, agentIndex, depth) -> Tuple[float, Any]:
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None

        legalActions = gameState.getLegalActions(agentIndex)
        nextGameStates = [gameState.generateSuccessor(
            agentIndex, action) for action in legalActions]
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
        nextDepth = depth + (nextAgentIndex == 0)

        branches = []
        for nextGameState, action in zip(nextGameStates, legalActions):
            score, _ = self.runExpectiMax(
                nextGameState, nextAgentIndex, nextDepth)
            branches.append((score, action))

        if agentIndex == 0:
            return max(branches)

        numberOfBranches = len(branches)
        totalSum = 0
        for value, _ in branches:
            totalSum += value

        return (totalSum / numberOfBranches, None)


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    return 0


class LocalMiniMaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
