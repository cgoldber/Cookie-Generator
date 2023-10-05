class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.tastes = {} # dictionary mapping salty, sweet, bitter, umami, sour to metrics 
    
    def set_amount(self, amount):
        """ Sets the amount of the ingredient in oz.
        """
        self.amount = amount

    def get_amount(self):
        """ Returns the amount of the ingredient in oz.
        """
        return self.amount
    
    def get_name(self):
        """ Returns the name of the ingredient.
        """
        return self.name

    def set_name(self, name):
        """ Sets the name of the ingredient.
        """
        self.name = name
    
    def __str__(self):
        """ Returns a string representation of the ingredient.
        """
        return str(round(self.amount, 2)) + " g " + self.name