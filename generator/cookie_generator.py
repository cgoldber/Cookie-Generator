import numpy as np
import os
from recipe import Recipe
from spotify import Spotify


class RecipeManager():
    """ Runs genetic algorithms to generate cookie recipes while considering 
        evaluation metrics.

    ...

    Attributes
    ----------
    Recipes : list
        Current recipes in genetic algorithm.
    Emotion : string
        Emotion that recipes will be based on.
    
    Methods
    -------
    parse_files():
        Reads inspiring recipe files and populates recipe list with Recipes.
    emotion_prompt():
        Asks user for their current emotion.
    set_emotion():
        Ensures emotion is valid and then sets emotion instance variable.
    get_emotion():
        Returns the current user's emotion.
    fittest_half():
        Returns the fittest 50% of the recipe set.
    crossover():
        Combines two recipes by based on probability selection processes.
    genetic_algo():
        Runs the high-level genetic algorithm.
    run_genetic_algo():
        Runs the genetic algorithm however many times the user chose.
    write_fittest_recipe():
        Writes the fittest recipe to a file.
    """

    def __init__(self):
        """ Initializes the object by creating an empty recipe list and emotion
            string to be populated later.
        """
        self.recipes = []
        self.emotion = ""
    
    def parse_files(self):
        """ Read file of recipes and populates recipe list with recipe object,
            passing in a list representation of recipe.
        """
        print("Reading Initial Recipe Files")
        dir = "../inspiring_set"
        for file in os.listdir(dir):
            with open(dir + "/" + file, "r") as f:
                recipe_str = f.readlines()
                new_recipe = Recipe(recipe_str, self.emotion)
                self.recipes.append(new_recipe)
    
    def emotion_prompt(self):
        """ Asks the user what emotion they are feeling and returns the
            associated key.
        """
        emotion_key = input("How are you feeling? \n (1) : Happy \n " + 
            "(2) : Sad \n (3) : Angry \n (4) : Excited \n (5) : Tired \n " + 
            "(6) : Stressed \n Input Number 1-6: ")
        return emotion_key
    
    def set_emotion(self):
        """ Sets the emotion instance variable for the current system's state
            based on the user input.
        """
        emotion_dic ={"1" : "Happy", "2" : "Sad", "3": "Angry",
                     "4" : "Excited", "5" : "Tired", "6" : "Stressed"}
        emotion_key = self.emotion_prompt()
        while emotion_key not in emotion_dic.keys():
            print("\nUnknown Emotion Key: Try Again!\n")
            emotion_key = self.emotion_prompt()
        self.emotion = emotion_dic[emotion_key]
        print(f"\nYou are feeling {self.emotion.lower()}!\n")
    
    def get_emotion(self):
        """ Returns the system's current emotion.
        """
        return self.emotion
    
    def fittest_half(self, recipes):
        """ Returns the fittest 50% of a given population.
            Args:
                recipes (list) : list of recipes
        """
        sorted_recipes = sorted(recipes, key = lambda x : x.get_fitness())
        return sorted_recipes[int(len(recipes)/2):]
    
    def crossover(self, recipe1, recipe2):
        """ Chooses the base ingredients from one recipe with equal 
            probability. Chooses a random pivot index to concatenate the flavor
            ingredients. Creates a new recipe object with these ingredients. 
            Args:
                recipe1 (Recipe) : first recipe to be crossed
                recipe2 (Recipe) : second recipe to be crossed
        """
        # choose base ingredients of one recipe with equal probability 
        new_base = np.random.choice([recipe1, recipe2]).get_base_ing_strings()

        # randomly select pivot to split flavor ingredients
        recipe1_flavor_strs = recipe1.get_flavor_ing_strings()
        recipe2_flavor_strs = recipe2.get_flavor_ing_strings()
        pivot = np.random.randint(0, min(len(recipe1_flavor_strs), 
                                         len(recipe1_flavor_strs)))
        new_flavors = recipe1_flavor_strs[:pivot] + recipe2_flavor_strs[pivot:]

        # choose instructions of one recipe with equal probability 
        new_instrs = np.random.choice([recipe1, recipe2]).get_instructions()
        new_recipe = Recipe(new_base + new_flavors, self.emotion, new_instrs)
        return new_recipe

    def genetic_algo(self):
        """ Iterate len(self.recipes) times. Choose recipe1 and recipe2 based 
            on fitness probabilites and cross them over (making new recipe 
            object). Then it's going to call the mutate function on it and 
            stores all of the new recipes in new_recipes. At the end, it is 
            going to taking the top 50% of the new and old recipes and store 
            it in self.recipes. 
        """
        new_recipes = []
        for _ in range(len(self.recipes)):
            #choose two recipes based on probs corresponding to their fitnesses
            fitnesses = [recipe.get_fitness() for recipe in self.recipes]
            sum_fit = sum(fitnesses)
            p = [fit / sum_fit for fit in fitnesses]
            recipe1, recipe2 = np.random.choice(self.recipes, p = p, size = 2, 
                                                replace = False)

            #cross the recipes together
            new_recipe = self.crossover(recipe1, recipe2)
            # call recipe to be potentially mutated
            new_recipe.mutate()
            new_recipes.append(new_recipe)

        #keep top 50% of old and newly generated recipes for next generation
        self.recipes = (self.fittest_half(self.recipes) + 
                        self.fittest_half(new_recipes))   

    def run_genetic_algo(self, generations):
        """ Run genetic algorithm for the # of generations that the user 
            inputs.
            Args:
                generations (int) : number of times the genetic algo will run
        """
        for i in range(generations):
            print(f"Running genetic algorithm for generation {i + 1}")
            self.genetic_algo()  
    
    def write_fittest_recipe(self):
        """ Writes the top fittest recipe to files in the fittest recipes 
            folder.
        """
        sorted_recipes = sorted(self.recipes, key = lambda x : x.get_fitness())
        recipe = sorted_recipes[-1]
        recipe.get_fitness()
        with open("fittest_recipes/rank_" + str(1), "w") as f:
            f.writelines(str(recipe))

    def print_metrics(self):
        """ Prints metric components of the top 3 and lowest 3 fittest recipes.
        """
        sorted_recipes = sorted(self.recipes, key = lambda x : x.get_fitness(),
                                reverse=True)
        for i in range(3):
            print(f"Rank {i+1}-")
            tot = sorted_recipes[i].get_fitness(do_print=True)
            print("total fitness: ", tot, "\n")
        print("...\n")
        for i in range(len(sorted_recipes) - 3, len(sorted_recipes)):
            print(f"Rank {i+1}-")
            tot = sorted_recipes[i].get_fitness(do_print=True)
            print("total fitness: ", tot, "\n")
        


def main():
    manager = RecipeManager()
    manager.set_emotion()
    emotion = manager.get_emotion()

    user_name = input("Enter your name:  ")
    generations = int(input(
    "\nHow many generations would you like to run this algorithm for? "))

    manager.parse_files()
    manager.run_genetic_algo(generations)
    manager.write_fittest_recipe() 

    spot = Spotify(emotion) 
    playlist = spot.make_playlist(user_name)
    manager.print_metrics()
    print("All done :)")


if __name__ == "__main__":
    main()