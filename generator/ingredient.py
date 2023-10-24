class Ingredient:
    """ A class representing an ingredient.
    ...

    Attributes
    ----------
    name : string
        Ingredient name.
    amount : float
        Amount of ingredient.
    unit : string
        Unit of measurement for this ingredient.

    Methods
    -------
    set_amount(): 
        Sets the amount of the Ingredient.
    get_amount(): 
        Returns the amount of the Ingredient.
    set_name():
        Sets the name of the Ingredient.
    get_name():
        Gets the name of the Ingredient.
    """

    def __init__(self, name, amount, unit="g"):
        """ Initializes ingredient.
            Args:
                name (string) : ingredient name
                amount (float) : ingredient quantity
                unit (str) : unit associated with ingredient
        """
        self.name = name
        self.amount = amount
        self.unit = unit
    
    def set_amount(self, amount):
        """ Sets the amount of the ingredient in oz.
            Args:
                amount (float) : quanitity of the ingredient
        """
        self.amount = amount

    def get_amount(self):
        """ Returns the amount of the ingredient in oz.
        """
        return self.amount

    def set_name(self, name):
        """ Sets the name of the ingredient.
            Args:
                name (str) : the name of the ingredient
        """
        self.name = name
    
    def get_name(self):
        """ Returns the name of the ingredient.
        """
        return self.name
    
    def __str__(self):
        """ Returns a string representation of the ingredient.
        """
        if ("butter" in self.name and "peanut" not in self.name):
            return str(round(self.amount / 14.2)) + " tbsp " + self.name
        unit = " " + self.unit + " "
        if self.unit == "g":
            return str(round(self.amount)) + unit + self.name
        return str(round(self.amount, 2)) + unit + self.name
    
    def __repr__(self):
        """ Returns a representation of the ingredient for debugging.
        """
        return str(self)