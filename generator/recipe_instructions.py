import numpy as np

class RecipeInstructions: 
    def __init__(self, temp=350, bake_time=10, rest_time=2, size=50):
        self.temp = temp
        self.bake_time = bake_time
        self.rest_time = rest_time
        self.size = size

    def adjust_temp(self):
        """ Randomly sets temperature to a multiple of 25 degrees F between 325
            and 425 inclusive
        """
        self.temp = np.random.randint(13, 18) * 25

    def adjust_bake_time(self):
        """ Randomly sets bake time to a time between 8 and 12 minutes
        """
        self.bake_time = np.random.randint(8,13) 

    def adjust_rest_time(self):
        """ Randomly sets rest time to a time between 0 and 12 hours
        """
        self.rest_time = np.random.randint(0,13) 

    def adjust_size(self):
        """ Randomly sets size to a multiple of 5 between 40 and 60 grams per 
            cookie.
        """
        self.size = np.random.randint(8, 13) * 5

    def mutate(self):
        """ Calls an above mutation
        """
        mutation = np.random.randint(0,4)
        if mutation == 0: 
            self.adjust_temp() 
        elif mutation == 1: 
            self.adjust_bake_time()
        elif mutation == 2: 
            self.adjust_rest_time()
        elif mutation == 3:
            self.adjust_size()

    def get_temp(self):
        return self.temp
    
    def get_bake_time(self):
        return self.bake_time
    
    def get_rest_time(self):
        return self.rest_time
    
    def get_size(self):
        return self.size

    def get_temp_times_size(self):
        return list(self.temp, self.bake_time, self.rest_time, self.size)