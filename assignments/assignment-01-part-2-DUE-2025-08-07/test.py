def aStarFoodSearch(gameState: GameState) -> List[str]:
    from game import Directions, Actions
    import util

    startPos = gameState.getPacmanPosition()
    foodGrid = gameState.getFood()
    foodList = foodGrid.asList()
    capsules = gameState.getCapsules()
    walls = gameState.getWalls()
    ghostStates = gameState.getGhostStates()

    frontier = util.PriorityQueue()
    frontier.push((startPos, [], 0), 0)
    visited = set()

    def ghostPenalty(pos):
        penalty = 0
        for ghost in ghostStates:
            ghostPos = ghost.getPosition()
            dist = manhattanDistance(pos, ghostPos)
            if dist <= 3:
                timer = ghost.scaredTimer
                if timer > 0:
                    penalty -= 500 / (dist + 1)
                else:
                    penalty += 1000 / (dist + 1)
        return penalty

    while not frontier.isEmpty():
        currentPos, path, costSoFar = frontier.pop()
        if currentPos in visited:
            continue
        visited.add(currentPos)

        # 🎯 GOAL CONDITION: Food OR Capsule
        if currentPos in foodList or currentPos in capsules:
            return path

        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(currentPos[0] + dx), int(currentPos[1] + dy)
            nextPos = (nextx, nexty)

            if walls[nextx][nexty]:
                continue

            stepCost = 1 + ghostPenalty(nextPos)
            newCost = costSoFar + stepCost

            # Heuristic to nearest food or capsule
            heuristicTargets = foodList + capsules
            heuristic = min(
                manhattanDistance(nextPos, target) for target in heuristicTargets) if heuristicTargets else 0
            totalCost = newCost + heuristic

            frontier.push((nextPos, path + [direction], newCost), totalCost)

    return []
