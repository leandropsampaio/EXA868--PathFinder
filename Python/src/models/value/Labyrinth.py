import json


class Labyrinth:

    def __init__(self, file_name):
        self.matrix = []
        self.beginning = None
        self.ending = None
        if file_name:
            file = open(file_name, 'r')
            self.characters = json.decoder.JSONDecoder().decode(file.read())

    def loadLabyrinth(self, file_name):
        file = open(file_name, 'r')
        for line in file.readlines():
            column = []
            self.matrix.append(column)
            line = line.replace("\n", "")
            for block in line:
                if (block not in self.characters.keys()) and block != " ":
                    raise ValueError("Error, undefined Labyrinth Character " + block)
                else:
                    column.append({'class': self.characters[block], 'character': block})
                    if self.characters[block] == "beginning":
                        self.beginning = {'y': len(self.matrix) - 1, 'x': len(column) - 1}
                    if self.characters[block] == "ending":
                        self.ending = {'y': len(self.matrix) - 1, 'x': len(column) - 1}

    def getBeginPosition(self):
        return self.beginning

    def getEndingPosition(self):
        return self.ending

    def validPosition(self, x, y):
        if x and y:
            if y <= len(self.matrix):
                if x <= len(self.matrix[y]):
                    position_class = self.matrix[y][x]['class']
                    return position_class != "wall"
        return False

    def move(self, direction, current_position):
        if self.validPosition(current_position['x'], current_position['y']):
            newX, newY = current_position['x'], current_position['y']
            if direction == "UP":
                newX, newY = current_position['x'], current_position['y'] - 1
            elif direction == "DOWN":
                newX, newY = current_position['x'], current_position['y'] + 1
            elif direction == "RIGHT":
                newX, newY = current_position['x'] + 1, current_position['y']
            elif direction == "LEFT":
                newX, newY = current_position['x'] - 1, current_position['y']
            if self.validPosition(newX, newY):
                return {'x': newX, 'y': newY}
        return None

    def isAtFinal(self, position):
        if position:
            if self.validPosition(position['x'], position['y']):
                return self.matrix[position['y']][position['x']]['class'] == "ending"

    def get_robot_in_labyrinth(self, robot_genome, genome_decoder):
        allPath = []
        currentPosition = {'x': 1, 'y': 1}
        labyrinthString = ""
        for genome in robot_genome:
            # Here will create labyrinth string
            for line in range(len(self.matrix)):
                for column in range(len(self.matrix[line])):
                    if line == currentPosition['y'] and column == currentPosition['x']:
                        labyrinthString = labyrinthString + "R"
                    else:
                        labyrinthString = labyrinthString + self.matrix[line][column]['character']
                labyrinthString = labyrinthString + "\n"
            allPath.append(labyrinthString)
            newPosition = self.move(genome_decoder[genome], currentPosition)
            if newPosition:
                currentPosition = newPosition
            labyrinthString = ""
        return allPath
