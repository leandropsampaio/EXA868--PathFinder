from models.value.Organism import Organism


class Finder(Organism):

    def __init__(self, genome_size):
        super(Finder, self).__init__(genome_size)
        self._genome_size = genome_size
        self.state = 0  # --[==[--0-Alive (-1)-Dead 1-Finish--]==]
        self.position = {'x': 0, 'y': 0}

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def reset(self):
        self.setFitness(self._genome_size * 2)
        self.state = 0

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position
