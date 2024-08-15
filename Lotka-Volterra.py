import matplotlib.pyplot as plt
import numpy as np

class Ecological:
    """Simplification of nature. This model consists of a set of species (animal and vegetable) related to each other. 
    For this version we deal with four species (Acorn, Boar, Wolf and Human)"""
    def __init__(self, initial_values: list= [], alpha: list= []) -> None:
        self.species= initial_values if initial_values else self.__fill_dict__()
        self.alpha= alpha if alpha else self.__fill_alpha__()
        self.data= [[],[],[],[]]
        self.t = 1

    def __fill_alpha__(self)-> list:
        return [[0, -0.1, 0, -0.1], [0, 0, -1, -0.9], [0, 0, 0, 0.00039], [0, 0, 0, 0]]

    def __fill_dict__(self)-> list:
        return [{'name': 'acorn', 'r': 0.015, 'p': 31300, 'K': 122000, 'A': 0.1},
         {'name': 'boar', 'r': 0.5, 'p': 300, 'K': 6000, 'A': 0.1},
         {'name': 'wolf', 'r': 0.4, 'p': 4, 'K': 12, 'A': 0.15},
         {'name': 'human', 'r': 0.106, 'p': 1900, 'K': 2500, 'A': 0.05}]

    def step(self):
        for i in range(self.species.__len__()):
            self.species[i]['p']= self.__grow__(i)
        self.t+= 1

    def __grow__(self, index: int) -> int:
        p= self.species[index]['p']
        r= self.species[index]['r']
        K= self.species[index]['K']
        A= self.species[index]['A']
        p = p + p * r * (1 - (p / (K * (1 + A * np.sin(np.pi / 4 * self.t)))))
        p = p + self.__interactions__(index)
        return int(p) if p > 0 else 0

    def __interactions__(self, index: int)-> int:
        a=0
        for i in range(0, self.species.__len__()):
          if index != i:
            a+=  self.species[i]['p'] * self.alpha[index][i] * self.species[index]['p'] / self.species[index]['K']
        return int(a)

    def collect_Data(self):
      for i in range(0, self.species.__len__()):
        self.data[i].append(self.species[i]['p'])

if __name__ == '__main__':
  # Run the model
  titles= ['Acorn', 'Boar', 'Wolf', 'Human']
  eco= Ecological()
  x= [num for num in range(1,71)]
  for i in range(0, 70):
    eco.collect_Data()
    eco.step()
  
  # Create a figure and a 3x3 grid of subplots
  fig, axs = plt.subplots(2, 2, figsize=(10, 10))
  
  # Populate each subplot
  for i in range(0,2):
    for j in range(0,2):
      axs[i, j].plot(x, eco.data[2*i+j], label=f'P(t)')
      axs[i, j].set_title(titles[2*i+j])
      axs[i, j].legend()
      axs[i, j].axhline(y=eco.species[2*i+j]['K'], color='r', linestyle='--')
  
  # Adjust layout
  plt.tight_layout()
  plt.show()
