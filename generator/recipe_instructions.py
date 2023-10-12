import numpy as np

class RecipeInstructions: 
    def __init__(self, temp=350, time=10, size=50):
        self.temp = temp
        self.time = time
        self.size = size

    def adjust_temp(self):
        """ Randomly sets temperature to a multiple of 25 degrees F between 325 and 425 inclusive
        """
        self.temp = np.random.randint(13, 18) * 25

    def adjust_time(self):
        """ Randomly sets time to a time between 8 and 12 minutes
        """
        self.time = np.random.randint(8,13) 

    def adjust_size(self):
        """ Randomly sets size to a multiple of 5 between 40 and 60 grams per cookie
        """
        self.size = np.random.randint(8, 13) * 5

    def mutate(self):
        """ Calls an above mutation
        """
        mutation = np.random.randint(0,3)
        if mutation == 0: 
            self.adjust_temp() 
        elif mutation == 1: 
            self.adjust_time()
        elif mutation == 2: 
            self.adjust_size()

    def get_temp(self):
        return self.temp
    
    def get_time(self):
        return self.time
    
    def get_size(self):
        return self.size

    def get_temp_time_size(self):
        return list(self.temp, self.time, self.size)