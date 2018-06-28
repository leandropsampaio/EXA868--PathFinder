local Finder = require "models.value.Finder"
local OrganismController = require "models.business.OrganismController"
local Labyrinth = require "models.value.Labyrinth"

local MainController = {}

function MainController:new()
  local self = {
    controllerOrganism;
    genomeDecoder;
    stateDecoder;
    labyrinth;

    constructor = function (this)
      this.labyrinth = Labyrinth:new("config.json")
      this.labyrinth.loadLabyrinth("labyrinth.la")
      this.controllerOrganism = OrganismController:new(Finder, this.labyrinth.getBeginPosition())
      this.genomeDecoder = {[0] = "UP", [1] = "RIGHT", [2] = "DOWN", [3] = "LEFT"}
      this.stateDecoder = {alive = 0, dead = -1, finished = 1}
    end
  }

  self.constructor(self)

  local calculateFitness = function (organism)
    local xDiference = organism.getX()
    xDiference = xDiference - self.objectiveCoordinates.x

    local yDiference = organism.getY()
    yDiference = yDiference - self.objectiveCoordinates.y

    return (math.sqrt(math.pow(xDiference, 2) + math.pow(yDiference, 2)))

  end

  local move = function(organisms)
    for index, organism in ipairs(organisms) do

      for key, genome in ipairs(organism.getGenome()) do
        if organism.getState() == self.stateDecoder.alive then
          io.write(genome .. " - ")
          local position = organism.getPosition()
          local hasMoved = self.labyrinth.move(self.genomeDecoder[genome], position)
          if hasMoved then
            organism.setFitness(organism.getFitness() + 1)
            organism.setPosition(hasMoved)
            if self.labyrinth.isAtFinal(hasMoved) then
              print("Finished")
              organism.setFitness(organism.getFitness() + 10)
              organism.setState(self.stateDecoder.finished)
            end
          else
            organism.setFitness(organism.getFitness() - 2)
            organism.setState(self.stateDecoder.dead)
          end
        end
      end

      local beginPosition = self.labyrinth.getBeginPosition()
      organism.setPosition({x = beginPosition.x, y = beginPosition.y})
      io.write("\n")
    end
  end

  local execute = function ()
    local organisms = self.controllerOrganism.getOrganisms()
    if not organisms then
      return nil
    end

    move(organisms)

    local mom, dad = self.controllerOrganism.selectBestOnes()
    self.controllerOrganism.crossover(mom, dad, 0.002)

    if(mom.getGeneration() % 11 == 0) then
      self.controllerOrganism.saveGenomes("LastsGenomes.json")
    end

  end

  return {
    execute = execute;
  }

end

return MainController
