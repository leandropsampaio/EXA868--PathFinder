local Json = require "util.Json"

local Labyrinth = {}

function Labyrinth:new(fileName)
  local self = {
    matrix;
    characters;
    beginning;
    constructor = function(this, fileName)
      this.matrix = {}
      if fileName then
        file = io.open(fileName,'r')
        this.characters = Json.decode(file:read("*all"))
      end
    end
  }

  self.constructor(self, fileName)

  local loadLabyrinth = function(file)
    for line in io.lines(file) do
      local column = {}
      table.insert(self.matrix, column)
      for block in string.gmatch(line, ".") do
        if not self.characters[block] and block ~= " " then
          error("Error, undefined Character")
        else
          table.insert(column, {class = self.characters[block], character = block})
          if self.characters[block] == "begining" then
            self.beginning = {y = #self.matrix, x = #column};
          end
        end
      end
    end
  end

  local getBeginPosition = function()
    return self.beginning
  end

  local validPosition = function(x, y)
    if x and y then
      if y <= #self.matrix then
        if x <= #self.matrix[y] then
          local positionClass = self.matrix[y][x].class
          return positionClass ~= "wall"
        end
      end
    end
    return false
  end

  local move = function(direction, currentPosition)
    if validPosition(currentPosition.x,currentPosition.y) then
      local newX, newY = currentPosition.x, currentPosition.y
      if direction == "UP" then
        newX, newY = currentPosition.x, currentPosition.y - 1
      elseif direction == "DOWN" then
        newX, newY = currentPosition.x, currentPosition.y + 1
      elseif direction == "RIGHT" then
        newX, newY = currentPosition.x + 1, currentPosition.y
      elseif direction == "LEFT" then
        newX, newY = currentPosition.x - 1, currentPosition.y
      end
      if validPosition(newX, newY) then
        return {x = newX, y = newY}
      end
    end
    return nil
  end

  local isAtFinal = function(position)
    if position then
      if validPosition(position.x,position.y) then
        return self.matrix[position.y][position.x].class == "ending"
      end
    end
  end

  return {
    loadLabyrinth = loadLabyrinth;
    move = move;
    isAtFinal = isAtFinal;
    getBeginPosition = getBeginPosition;
  }

end

return Labyrinth
