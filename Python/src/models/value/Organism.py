import random


class Organism:

    def __init__(self, genome_size):
        self.generation = 0  # --[==[--This is an array containing the genome--]==]
        self.fitness = 0
        self.genome = []
        for index in range(0, genome_size):
            self.genome.append(random.randint(0, 3))
        self.last = 99999

    def getGeneration(self):
        return self.generation

    def setGeneration(self, generation):
        self.generation = generation

    def getGenome(self):
        return self.genome

    def setGenome(self, genome):
        self.genome = genome

    def getGenomeInIndex(self, index):
        return self.genome[index]

    def setGenomeInIndex(self, index, genome_part):
        self.genome[index] = genome_part

    def getLast(self):
        return self.last

    def setLast(self, last):
        self.last = last

    def getFitness(self):
        return self.fitness

    def setFitness(self, new_fitness):
        self.fitness = new_fitness

    def updateFitness(self, update):
        self.fitness = self.fitness + update

    def compareTo(self, to_compare):
        if to_compare:
            return self.generation - to_compare.getGeneration()
