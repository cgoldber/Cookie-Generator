class Ingredient:
    def __init__(self, name, amount, unit="g"):
        self.name = name
        self.amount = amount
        self.unit = unit
    
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
        if "butter" in self.name:
            return str(round(self.amount / 14.2)) + " tbsp " + self.name
        unit = " " + self.unit + " "
        return str(round(self.amount, 2)) + unit + self.name
    
    def __repr__(self):
        return str(self)