local Organism = {}

function Organism:new(genomeSize)

  local self = {--creating the table
    genome; --[==[--This is an array containing the genome--]==]
    generation;
    fitness;

    constructor = function (this, genomeSize)
      this.generation = 0
      this.fitness = 0
      this.genome = {}
      for index = 1, genomeSize, 1 do
        table.insert(this.genome, math.random(0, 3))
      end
    end
  }

  self.constructor(self, genomeSize)

  local getGeneration = function()
    return self.generation
  end

  local setGeneration = function (generation)
    self.generation = generation
  end

  local getGenome = function()
    return self.genome
  end

  local setGenome = function(genome)
    self.genome = genome
  end

  local getGenomeInIndex = function(index)
    return self.genome[index]
  end

  local setGenomeInIndex = function(index, genomePart)
    self.genome[index] = genomePart
  end

  local getFitness = function()
    return self.fitness
  end

  local setFitness = function(newFitness)
    self.fitness = newFitness
  end

  local compareTo = function(toCompare)
    if(toCompare) then
      return (self.generation - toCompare.getGeneration())
    end
  end

  return {
    getGeneration = getGeneration;
    setGeneration = setGeneration;
    getGenomeInIndex = getGenomeInIndex;
    setGenomeInIndex = setGenomeInIndex;
    getGenome = getGenome;
    setGenome = setGenome;
    getFitness = getFitness;
    setFitness = setFitness;
    compareTo = compareTo;
  }

end

return Organism
