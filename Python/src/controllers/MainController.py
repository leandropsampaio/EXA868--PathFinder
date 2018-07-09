import math

from models.business.OrganismController import OrganismController
from models.value.Finder import Finder
from models.value.Labyrinth import Labyrinth


class MainController:

    def __init__(self):
        self.__labyrinth = Labyrinth("../config.json")
        self.__labyrinth.loadLabyrinth("../labyrinth.la")
        self.__controllerOrganism = OrganismController(Finder, self.__labyrinth.getBeginPosition())
        self.__genomeDecoder = ("UP", "RIGHT", "DOWN", "LEFT")
        self.__stateDecoder = {'alive': 0, 'dead': -1, 'finished': 1}
        self.__ending = self.__labyrinth.getEndingPosition()
        self.__have_finished = False
        self.__generations_finished = 0

        self.__generations_fitness_average = []
        self.__best_fitness = []
        self.__best_organisms = []

    def finished_generations(self):
        return self.__generations_finished

    def get_generations_fitness_average(self):
        return self.__generations_fitness_average

    def get_best_fitness(self):
        return self.__best_fitness

    def get_genome_decoder(self):
        return self.__genomeDecoder

    def get_labyrinth(self):
        return self.__labyrinth

    def get_best_one(self):
        return self.__controllerOrganism.getSmallerPath(list_to_order=self.__best_organisms)[0]

    def __calculate_fitness(self, organism):
        x_diference = organism.getPosition()['x']
        x_diference = x_diference - self.__ending['x']
        y_diference = organism.getPosition()['y']
        y_diference = y_diference - self.__ending['y']
        # return math.sqrt(math.pow(x_diference, 2) + math.pow(y_diference, 2))
        return math.fabs(x_diference) + math.fabs(y_diference)

    def move(self, organisms):
        for organism in organisms:

            count = 0
            for genome in organism.getGenome():
                if organism.getState() == self.__stateDecoder['alive']:
                    position = organism.getPosition()
                    has_moved = self.__labyrinth.move(self.__genomeDecoder[genome], position)
                    if has_moved:
                        organism.updateFitness(1)
                        organism.setPosition(has_moved)
                        if self.__labyrinth.isAtFinal(has_moved):
                            organism.updateFitness(100)
                            organism.setState(self.__stateDecoder['finished'])
                            organism.setLast(count)
                            print("Generation: " + str(organism.getGeneration()), organism.getGenome())
                            self.__have_finished = True
                    else:
                        organism.updateFitness(-5)
                        # organism.setState(self.stateDecoder['dead'])
                count = count + 1

            if organism.getState() == self.__stateDecoder['dead']:
                organism.updateFitness(-10)
            organism.updateFitness(-10 * self.__calculate_fitness(organism))

            # print(organism.getPosition())
            begin_position = self.__labyrinth.getBeginPosition()
            organism.setPosition({'x': begin_position['x'], 'y': begin_position['y']})

    def execute(self):
        organisms = self.__controllerOrganism.getOrganisms()
        if not organisms:
            return None
        self.move(organisms)

        if self.__have_finished:
            self.__generations_finished = self.__generations_finished + 1
            self.__have_finished = False

        self.__generations_fitness_average.append(self.__controllerOrganism.average_fitness())

        mom, dad = self.__controllerOrganism.selectBestOnes()
        self.__best_fitness.append(mom.getFitness())
        self.__best_organisms.append(mom)

        self.__controllerOrganism.crossover(mom, dad, 0.05)

        if mom.getGeneration() % 11 == 0:
            self.__controllerOrganism.saveGenomes("../LastsGenomes.json")
