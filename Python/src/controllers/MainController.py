import math

from models.business.OrganismController import OrganismController
from models.value.Finder import Finder
from models.value.Labyrinth import Labyrinth


class MainController:

    def __init__(self):
        self.labyrinth = Labyrinth("config.json")
        self.labyrinth.loadLabyrinth("labyrinth.la")
        self.controllerOrganism = OrganismController(Finder, self.labyrinth.getBeginPosition())
        self.genomeDecoder = ("UP", "RIGHT", "DOWN", "LEFT")
        self.stateDecoder = {'alive': 0, 'dead': -1, 'finished': 1}

    def calculateFitness(self, organism):
        xDiference = organism.getX()
        xDiference = xDiference - self.objectiveCoordinates['x']
        yDiference = organism.getY()
        yDiference = yDiference - self.objectiveCoordinates['y']
        return math.sqrt(math.pow(xDiference, 2) + math.pow(yDiference, 2))

    def move(self, organisms):
        for index, organism in organisms:

            for key, genome in organism.getGenome():
                if organism.getState() == self.stateDecoder['alive']:
                    print(str(genome) + " - ")
                    position = organism.getPosition()
                    has_moved = self.labyrinth.move(self.genomeDecoder[genome], position)
                    if has_moved:  # Caso não tenha batido na parede
                        organism.setFitness(organism.getFitness() + 1)
                        organism.setPosition(has_moved)
                        if self.labyrinth.isAtFinal(has_moved):
                            print("Finished")
                            organism.setFitness(organism.getFitness() + 10)
                            organism.setState(self.stateDecoder['finished'])
                    else:  # Se bateu na parede
                        organism.setFitness(organism.getFitness() - 2)
                        organism.setState(self.stateDecoder['dead'])

            begin_position = self.labyrinth.getBeginPosition()
            organism.setPosition({'x': begin_position['x'], 'y': begin_position['y']})

    def execute(self):
        organisms = self.controllerOrganism.getOrganisms()
        if not organisms:
            return None
        self.move(organisms)

        mom, dad = self.controllerOrganism.selectBestOnes()
        self.controllerOrganism.crossover(mom, dad, 0.002)

        if mom.getGeneration() % 11 == 0:
            self.controllerOrganism.saveGenomes("LastsGenomes.json")
