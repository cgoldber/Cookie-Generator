# Cookie-Generator
## Title: Emotimaker
## By Bereket Abebe, Casey Goldberg, Cairo Dasilva and Sophie Lipset
## Project Description
The Emotimaker is a recipe generator that uses a genetic algorithm to create 
cookie recipes tailored to the user's current emotion. The possible emotions 
are Happy, Sad, Tired, Angry, Stressed and Excited. Recipes are made up of both
base ingredients (flour, butter, etc) and flavor ingredients (chocolate, 
fruits, spices, etc). All possible flavors that may be included in the recipes
appear is the BASE/FLAVOR_INGREDIENT_TYPES lists in the base_ingredients.py and
flavor_ingredients.py files.


The generator starts by reading a set of inspiring recipes, which are a diverse
set of recipes which were extracted from expert bakers on the internet. Then, 
it runs a genetic algorithm on the recipe set. First, the genetic algorithm 
chooses 2 recipes from the inspiring set with probabilities proportional to 
their fitness. Then, it crosses them over by choosing one of the bases and 
combining the flavor ingredients based on a random pivot index. After that, 
newly crossed recipes can then be mutated. Mutations may be applied to base 
ingredients, recipe ingredients, or the recipe baking instructions. Base 
ingredient mutations involve chaning ingredient ratios, flavor ingredient 
mutations involve adding, deleting, or swapping ingredients, and instruction 
mutations involve altering parameters such as bake time or preheat temperature.


New- and previous-generation recipes are then evaluated to determine their 
fitness, which incorporates four different components. The first component of 
the fitness function is the number of ingredients in the recipe, which helps to 
encourage more complex flavor pairings. The second component is a flavor pairing
score that indicates how similar the recipe flavors are. These values are 
extracted from previous flavor pairing research provided by Prof Harmon. The 
third component is an emotion alignment score that indicates how well the recipe
flavors correspond to the user-given emotion. We manually generated an emotion
to flavor ingredient alignment matrix based on associations we as developers
have gained through our past life experiences. The final component of the 
fitness function indicates how dissimilar the recipe flavors are from the 
flavors in the inspiring set. The recipes that contain flavor ingredients that 
deviate more from the inspiring sets based on both their ingredients and 
ingredient quantities are more fit. All four of these fitness components are 
weighted differently based on how much we felt we wanted our system to consider 
value versus novelty. We selected these coefficients with a human-in-the-loop 
manual experimentation process, where we used our previous knowledge of 
cookie-making to inform our final decisions.


After evaluating the fitness for each new recipe, the fittest half of both the
new recipes and the previous generation’s recipes (the first generation uses 
the inspiring set as the previous generation) are crossed over and mutate again, 
creating a new generation of recipes. After all the generations have executed,
the fittest recipe is written into the fittest recipe folder along with its
corresponding baking instructions. Included in the instructions is the 
direction to listen to a random song that aligns with the user's chosen 
emotion.


## More on Evaluation Metrics

The primary goal of our system was to generate yummy, well-structured, and 
novel cookie recipes that aligned well with the user's emotion. Therefore, we 
generated our previously explained metrics with these ideas in mind. 

To ensure that the cookies would taste good, we employed the flavor pairing 
component of the fitness function. However, we found that we did not need to 
weigh it heavily, as the original inspiring recipes and the emotion alignment 
aspect already resulted in tasty ingredient combinations. Weighting this 
component more heavily resulted in less varied flavor ingredients in recipes
regardless of emotions chosen, specifically selecting for chocolate and vanilla
when the coefficient is increased.

To ensure that the cookies would actually resemble traditional cookies, our
algorithm ensured that key base ingredients would never be deleted and it also
maintained conventional ratios between dry ingredients, wet ingredients, etc.
(verified these conventions on Google). In addition, we also ensured that the
baking instructions followed a conventional format and the parameter such as
oven temperature stayed between reasonable amounts.

Both the dissimilarity and length component of the fitness function contributed
to the novelty of the system. The length component encourages more complex
pairings that include a larger amount of ingredients. When the length component
is weighted less heavily, the flavor pairing component can force just a few high
scoring ingredients, such as chocolate, coffee, and vanilla. The dissimilarity 
score ensures that the recipe does not resemble too closely the flavor 
ingredients of the inspiring set.

The extent to which the recipe aligned with the user's emotion was evaluated
with the emotion alignment component described above. This component was
weighted heavily, as we very much prioritized the creation of cookies that met
the user's emotional needs. For example, a user who is happy is more likely to 
receive a recipe with fruit or citrus in it while a user who is sad is more 
likely to receive a recipe with lavender or black tea. 

Throughout the genetic algorithm process, these evaluation metrics were
employed entirely within the fitness function (except for the well-structured
metric which was incorporated throughout the process) to decide which recipes
would continue on in the genetic algorithm. Once the algorithm terminates,
these evaluation metrics are used to determine which recipe is the most fit and
should be written for the user to then bake.

The Metrics folder contains three examples of system deployment for Happy, 
Stressed, and Excited input emotions for 7 generations each. The examples contain
the top three and bottom three fitness scores for the output generation. In
addition to the total fitness score, it also includes the four components that
make up the fitness function (already multiplied by their respective 
coefficients). Finally, the examples also contain the written recipe for the 
top ranked recipe. The folder also contains the fitness componenets for the 
inspiring set recipes, which were printed when the user chose Happy.

For instance, in example 1, it is of course no surprise that the highest ranked
recipe has the highest total fitness score. Since this recipe has the highest
emotion score in comparison to the other printed metrics, that means that the 
flavors in the recipe best correspond to the user's emotion and is therefore 
valuable to them. It also has a emotion score of 4.56, which is much more than
the maximal emotion score in the inspiring set 3.6. This indicates that the
system was able to tailor the recipes towards the desired Happy emotion (the
emotion chosen was Happy for example1 and the inspiring_set_metrics).

You can also see that all of the output metrics in the last generation of example
1 have dissimilaritiy scores around 2.5. In the inspiring set metric outputs, 
you can see that most of the dissimilarity scores are around 1.3 (with the 
highest one reacing around 2.5). Therefore, it is evident that our system was 
successful in crafting recipes that are very different from the inspiring set,
even more so than the inspiring set recipes were different from each other!

However, it is important to note that the highest ranked recipe does not have 
the highest dissimilarity and flavor pairing scores. Since the goal of this 
system is finding a creative recipe (which is implemented through processes 
based on probabilities) and not necessarily the "optimal" cookie, there will 
be trade-offs with certain evaluation metrics. For instance, the highest ranked
recipe has a relatively low flavor pairing score, but it makes up for this by 
being novel in comparison to the inspiring set and well tuned to the user's 
emotions. 

Overall, the metrics of our resulting recipes indicate that our system met our 
evaluation goals: the employment of known cookie structure ratios from experts
on the internet/flavor pairing from experts indicate that our cookies are yummy 
and well-structured, the fact that the resulting generation of recipes is more 
dissimilar from the inspiring set than they are from each other indicates that 
the recipes are unique/novel, and the fact that the optimal cookies have a higher 
emotional score than the original inspiring recipes indicate the system is valuable
because it successfully tailors a cookie recipe based on one's emotion.

## How to Install and Run
### Step 1:
To Run the program you should install:
pip3 install numpy 
pip3 install pandas
pip3 install random
pip3 install os
pip3 install spotipy 


### Step 2: 
Change cd(change directory) to cookie_generator (this should be what you named 
the file)/generator/ in the user terminal
“cd generator/”


### Step 3 
Go to file “cookie_generator” and run file


### Step 4
Input number for emotions (1-6): -> hit Enter in terminal


### Step 5
Input the amount of generations you would like to run the program for: -> hit 
Enter in terminal 


### Step 6 
Go to fittest_recipes folder to view the generations based on emotion :
the file will be named "rank1.txt". 


The output of the fittest recipes are separated by these headers: Base 
ingredients, flavor ingredients, Instructions. 







