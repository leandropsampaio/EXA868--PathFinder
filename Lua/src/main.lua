local Labyrinth = require "models.value.Labyrinth"
local MainController = require "controllers.MainController"

math.randomseed(os.time())
math.random(); math.random(); math.random()

local mainController = MainController:new()

while true do
  mainController.execute()
end
