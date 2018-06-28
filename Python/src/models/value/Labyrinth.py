import json
import string


class Labyrinth:

    def __init__(self, file_name):
        self.matrix = []
        self.beginning = None
        if file_name:
            file = open(file_name, 'r')
            self.characters = json.decoder.JSONDecoder().decode(file.read())

    def loadLabyrinth(self, file):
        for line in file.readline():
            column = []
            self.matrix.append(column)
            for block in string.gmatch(line, "."):
                if not self.characters[block] and block != " ":
                    print("Error, undefined Character")
                else:
                    column.append({'class': self.characters[block], 'character': block})
                    if self.characters[block] == "begining":
                        self.beginning = {'y': len(self.matrix), 'x': len(column)}

    def getBeginPosition(self):
        return self.beginning

    def validPosition(self, x, y):
        if x and y:
            if y <= len(self.matrix):
                if x <= len(self.matrix[y]):
                    position_class = self.matrix[y][x]['class']
                    return position_class != "wall"
        return False

    def move(self, direction, current_position):
        if self.validPosition(current_position.x, current_position.y):
            newX, newY = current_position.x, current_position.y
            if direction == "UP":
                newX, newY = current_position.x, current_position.y - 1
            elif direction == "DOWN":
                newX, newY = current_position.x, current_position.y + 1
            elif direction == "RIGHT":
                newX, newY = current_position.x + 1, current_position.y
            elif direction == "LEFT":
                newX, newY = current_position.x - 1, current_position.y
            if self.validPosition(newX, newY):
                return {'x': newX, 'y': newY}
        return None

    def isAtFinal(self, position):
        if position:
            if self.validPosition(position.x, position.y):
                return self.matrix[position.y][position.x]['class'] == "ending"
