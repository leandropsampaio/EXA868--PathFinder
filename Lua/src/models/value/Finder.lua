local Organism = require "models.value.Organism"
local Finder = {}

function Finder:new(genomeSize)

  local self = {--creating the table
    super;
    state; --[==[--0-Alive (-1)-Dead 1-Finish--]==]
    position;

    constructor = function (this, genomeSize)
      this.super = Organism:new(genomeSize)
      this.state = 0
      this.position = {x = 0, y = 0}
    end
  }

  self.constructor(self, genomeSize)

  local getState = function()
    return self.state
  end

  local setState = function(state)
    self.state = state
  end

  local reset = function()
    self.super.setFitness(genomeSize * 2)
    self.state = 0
  end

  local getPosition = function()
    return self.position
  end

  local setPosition = function(position)
    self.position = position
  end

  self.super.getState = getState
  self.super.setState = setState
  self.super.getPosition = getPosition
  self.super.setPosition = setPosition
  self.super.reset = reset

  return self.super
end

return Finder
