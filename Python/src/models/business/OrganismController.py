import json
import random


class OrganismController:
    def __init__(self, organism_constructor, initial_position):
        self.numberOfGenomes = 50
        self.organisms = []
        self.genomeSize = 16
        self._organismConstructor = organism_constructor
        self._initialPosition = initial_position

        for index in range(1, self.numberOfGenomes):
            organism = organism_constructor(self.genomeSize)
            organism.setPosition({'x': initial_position['x'], 'y': initial_position['y']})
            self.organisms.append(organism)

    def crossover(self, mom_organism, dad_organism, mutation_probability):
        if not (mom_organism and dad_organism and mutation_probability):
            return False

        cutPoint, mutationRandom = 0, 0
        children = []
        for indexOfChildren in range(1, self.genomeSize):
            newChildren = self._organismConstructor(self.genomeSize)
            newChildren.setPosition({'x': self._initialPosition['x'], 'y': self._initialPosition['y']})

            cutPoint = random.randint(1, self.genomeSize - 1)
            for index in range(1, cutPoint):
                newChildren.setGenomeInIndex(index, mom_organism.getGenomeInIndex(index))

            for index in range(cutPoint + 1, self.genomeSize):
                newChildren.setGenomeInIndex(index, dad_organism.getGenomeInIndex(index))

            for genomeIndex in range(1, self.genomeSize):
                if random.randint() <= mutation_probability:  # --mutations (mutation_probability)
                    newChildren.setGenomeInIndex(genomeIndex, random.randint(0, 3))

            newChildren.setGeneration(mom_organism.getGeneration() + 1)
            children.append(newChildren)

        self.organisms = children
        return children

    def selectBestOnes(self):
        maxScores = [0, 0]
        bestOrganisms = [self.organisms[1], self.organisms[2]]

        for index, value in self.organisms:
            if value.getFitness() > maxScores[0]:
                bestOrganisms[1] = bestOrganisms[0]
                maxScores[1] = maxScores[0]
                bestOrganisms[0] = value
                maxScores[0] = value.getFitness()
            elif value.getFitness() > maxScores[1]:
                bestOrganisms[1] = value
                maxScores[1] = value.getFitness()
        return bestOrganisms[0], bestOrganisms[1]

    def saveGenomes(self, filePath):
        '''outFile = assert(io.open(filePath, "w"))
        outFile:write("{ \"Organisms\":[")
        for index, value in ipairs(self.organisms) do
            outFile:write("{\"Generation", "\": [", value.getGeneration(), "],")
            outFile:write("\"Genome", "\": [")

            genomeSize = #value.getGenome()
            for genomeIndex, genomeValue in ipairs(value.getGenome()) do
                if(genomeIndex < genomeSize):
                    outFile:write(genomeValue, ",")
                else
                    outFile:write(genomeValue, "]")
                end
            end
            if(index < #self.organisms):
                outFile:write("},")
            else
                outFile:write("}")
            end
        end
        outFile:write("]}")
        assert(outFile:close())'''

    def loadGenomes(self, filePath):
        file = open(filePath, 'r')
        self.organisms = json.JSONDecoder().decode(file.read())

    def getOrganisms(self):
        return self.organisms
