from controllers.MainController import MainController
import matplotlib.pyplot as plt

mainController = MainController()

maxGenerations = 10

while mainController.finished_generations() <= maxGenerations:
    mainController.execute()

plt.plot(mainController.get_best_fitness(),
         label='Melhores Fitness')  # LISTA DE FITNESS DO MELHOR INDIVIDUO DE CADA GERAÇÃO
plt.plot(mainController.get_generations_fitness_average(),
         label='Fitness médio da população')  # LISTA DE FITNESS MÉDIO DA POPULAÇÃO DE CADA GERAÇÃO

plt.xlabel('Gerações')
plt.ylabel('Fitness')
plt.title("Solução 1")
plt.figlegend(('Melhores Fitness', 'Fitness médio da população'))
plt.show()

path = mainController.get_labyrinth().get_robot_in_labyrinth(mainController.get_best_one().getGenome(),
                                                             mainController.get_genome_decoder())
for currentPosition in path:
    print(currentPosition)
