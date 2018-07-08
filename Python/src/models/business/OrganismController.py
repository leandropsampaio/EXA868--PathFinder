import json
import random


class OrganismController:
    def __init__(self, organism_constructor, initial_position):
        self.numberOfOrganisms = 50
        self.organisms = []
        self.genomeSize = 30
        self._organismConstructor = organism_constructor
        self._initialPosition = initial_position

        for index in range(1, self.numberOfOrganisms):
            organism = organism_constructor(self.genomeSize)
            organism.setPosition({'x': initial_position['x'], 'y': initial_position['y']})
            self.organisms.append(organism)

    def average_fitness(self):
        average = 0
        count = 0
        for organism in self.organisms:
            average = average + organism.getFitness()
            count = count + 1
        return average / count

    def crossover(self, mom_organism, dad_organism, mutation_probability):
        if not (mom_organism and dad_organism and mutation_probability):
            return False

        if len(mom_organism.getGenome()) > len(dad_organism.getGenome()):
            mom_organism, dad_organism = dad_organism, mom_organism

        children = []
        for indexOfChildren in range(self.numberOfOrganisms):
            new_children_1 = self._organismConstructor(self.genomeSize)
            new_children_1.setPosition({'x': self._initialPosition['x'], 'y': self._initialPosition['y']})
            new_children_2 = self._organismConstructor(self.genomeSize)
            new_children_2.setPosition({'x': self._initialPosition['x'], 'y': self._initialPosition['y']})

            cut_point = random.randint(1, self.genomeSize - 1)
            for index in range(1, cut_point):
                new_children_1.setGenomeInIndex(index, mom_organism.getGenomeInIndex(index))
                new_children_2.setGenomeInIndex(index, dad_organism.getGenomeInIndex(index))

            for index in range(cut_point + 1, self.genomeSize):
                new_children_1.setGenomeInIndex(index, dad_organism.getGenomeInIndex(index))
                new_children_2.setGenomeInIndex(index, mom_organism.getGenomeInIndex(index))

            for genomeIndex in range(1, self.genomeSize):
                if random.uniform(0, 1) <= mutation_probability:  # --mutations (mutation_probability)
                    new_children_1.setGenomeInIndex(genomeIndex, random.randint(0, 3))
                if random.uniform(0, 1) <= mutation_probability:  # --mutations (mutation_probability)
                    new_children_2.setGenomeInIndex(genomeIndex, random.randint(0, 3))

            new_children_1.setGeneration(mom_organism.getGeneration() + 1)
            new_children_2.setGeneration(mom_organism.getGeneration() + 1)
            children.append(new_children_1)
            children.append(new_children_2)

        self.organisms = children
        return children

    def getSmallerPath(self, compare_to=None, amount=30):
        if not compare_to:
            compare_to = self.organisms[0].compareTo
        self.organisms.sort(key=compare_to, reverse=True)
        if self.organisms[1].getLast() < 99999:
            return self.organisms[:amount]
        return self.organisms

    def selectBestOnes(self):
        max_scores = [0, 0]
        best_organisms = [self.organisms[1], self.organisms[2]]

        for value in self.getSmallerPath():
            if value.getFitness() > max_scores[0]:
                best_organisms[1] = best_organisms[0]
                max_scores[1] = max_scores[0]
                best_organisms[0] = value
                max_scores[0] = value.getFitness()
            elif value.getFitness() > max_scores[1]:
                best_organisms[1] = value
                max_scores[1] = value.getFitness()
        return best_organisms[0], best_organisms[1]

    def saveGenomes(self, filePath):
        """outFile = assert(io.open(filePath, "w"))
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
        assert(outFile:close())"""

    def loadGenomes(self, file_path):
        file = open(file_path, 'r')
        self.organisms = json.JSONDecoder().decode(file.read())

    def getOrganisms(self):
        return self.organisms
