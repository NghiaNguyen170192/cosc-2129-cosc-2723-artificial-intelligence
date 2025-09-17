# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
from backend import ReplayMemory

import backend
import gridworld

import random, util, math
import numpy as np
import copy


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"
        self.values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        print("self.values: " + str(self.values))
        return self.values[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legal_actions = self.getLegalActions(state)
        if not legal_actions:
            return 0.0

        max_value = float("-inf")
        for action in legal_actions:
            q_value = self.getQValue(state, action)
            if q_value > max_value:
                max_value = q_value

        return max_value

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legal_actions = self.getLegalActions(state)
        if not legal_actions:
            return None

        max_q_value = self.computeValueFromQValues(state)
        best_actions = []

        for action in legal_actions:
            if self.getQValue(state, action) == max_q_value:
                best_actions.append(action)

        return random.choice(best_actions)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        "*** YOUR CODE HERE ***"
        is_true = util.flipCoin(self.epsilon)

        if is_true:
            return random.choice(legalActions)

        return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """

        "*** YOUR CODE HERE ***"
        # Q(s,a) ← Q(s,a) + alpha * [R(s,a,s′) + discount*maxQ(s′,a′) − Q(s,a)]
        # where
        # s(state)  = current state = state
        # a(action)  = action taken = action
        # s' = next state = nextState
        # R(s, a, a') = reward received = reward
        # alpha = learning rate = self.alpha
        # discount = self.discount
        # [R(s,a,s′) + discount*maxQ(s′,a′) − Q(s,a)] = temporal difference error = temporal_difference_error

        old_q_value = self.getQValue(state, action)  # before update
        max_q_value = self.computeValueFromQValues(nextState)

        temporal_difference_error = reward + self.discount * max_q_value - old_q_value
        new_q_value = old_q_value + self.alpha * temporal_difference_error

        self.values[(state, action)] = new_q_value

        # self.debug_update(state, action, reward, old_q_value, max_q_value, temporal_difference_error, {})

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def debug_update(self, state, action, reward, old_q, max_q, td_error, features):
        # Flatten features into a string: key=value pairs joined by ";"
        features_str = ";".join([f"{k}={v:.4f}" for k, v in features.items()])

        # Build one CSV-like row with "|" as delimiter
        print(
            f"state={state} | action={action} | reward={reward:.4f} | "
            f"old_q={old_q:.4f} | max_q={max_q:.4f} | td_error={td_error:.4f} | "
            f"alpha={self.alpha} | discount={self.discount} | features={features_str}"
        )


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        sum = 0
        for feature, value in self.featExtractor.getFeatures(state, action).items():
            sum += self.weights[feature] * value

        return sum

    def update(self, state, action, nextState, reward: float):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        old_q_value = self.getQValue(state, action)  # before update
        max_q_value = self.computeValueFromQValues(nextState)
        alpha = self.alpha
        discount = self.discount

        # temporal difference error
        temporal_difference_error = reward + discount * max_q_value - old_q_value

        features = self.featExtractor.getFeatures(state, action)
        for feature, value in features.items():
            self.weights[feature] += alpha * temporal_difference_error * value

        # self.debug_update(state, action, reward, old_q_value, max_q_value, temporal_difference_error, features)

    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)
        print("Final weights:", dict(self.weights))
        print("------------------------")

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass

            # print("\nTraining complete. Learned weights:")
            # for feature, weight in self.weights.items():
            #     print(f"  {feature}: {weight:.4f}")
