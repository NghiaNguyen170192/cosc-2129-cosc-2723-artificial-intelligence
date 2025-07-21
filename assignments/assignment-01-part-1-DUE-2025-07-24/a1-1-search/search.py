# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))
    visited = set([problem.getStartState()])
    expanded_states = []

    while not frontier.isEmpty():
        state, path = frontier.pop()
        expanded_states.append(state)

        if problem.isGoalState(state):
            print("Expanded states:", expanded_states)
            return path

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [action]
                frontier.push((successor, new_path))

    return []


def breadthFirstSearch(problem):
    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))
    visited = set()
    expanded_states = []

    while not frontier.isEmpty():
        state, path = frontier.pop()

        if state in visited:
            continue

        visited.add(state)
        expanded_states.append(state)

        if problem.isGoalState(state):
            print("Expanded states:", expanded_states)
            return path

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                new_path = path + [action]
                frontier.push((successor, new_path))

    return []


def uniformCostSearch(problem):
    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), [], 0), 0)
    visited = dict()
    expanded_states = []

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()

        if state in visited and visited[state] <= cost:
            continue

        visited[state] = cost
        expanded_states.append(state)

        if problem.isGoalState(state):
            print("Expanded states:", expanded_states)
            return path

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost
            new_path = path + [action]
            if successor not in visited or visited[successor] > new_cost:
                frontier.push((successor, new_path, new_cost), new_cost)

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start_state, [], 0), heuristic(start_state, problem))
    explored = set()

    while not frontier.isEmpty():
        current_state, path, cost_so_far = frontier.pop()

        if problem.isGoalState(current_state):
            return path

        if current_state not in explored:
            explored.add(current_state)

            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = cost_so_far + step_cost
                new_path = path + [action]
                priority = new_cost + heuristic(successor, problem)
                frontier.push((successor, new_path, new_cost), priority)

    return []

#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e


def iterativeDeepeningSearch(problem):
    """Search the deepest node in an iterative manner."""
    "*** YOUR CODE HERE ***"

    depth = 0
    while True:
        result = depthLimitedSearch(problem, depth)
        if result != 'cutoff':
            return result
        depth += 1


def depthLimitedSearch(problem, limit):
    start_state = problem.getStartState()
    visited = set()

    # Queue stores (state, path, depth)
    stack = util.Stack()
    stack.push((start_state, [], 0))

    while not stack.isEmpty():
        state, path, current_depth = stack.pop()

        if problem.isGoalState(state):
            return path

        if current_depth < limit and state not in visited:
            visited.add(state)
            for successor, action, _ in problem.getSuccessors(state):
                stack.push((successor, path + [action], current_depth + 1))

    return 'cutoff'


#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
