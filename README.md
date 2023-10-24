# Cookie-Generator
## Title: Emotimaker
## By Bereket Abebe, Casey Goldberg, Cairo Dasilva and Sophie Lipset
## Project Description
The Emotimaker is a recipe generator that uses a genetic algorithm to create cookie recipes based on user inputted emotions. The chosen emotions are between Happy, Sad, Tired, Angry, Stressed and Excited. Recipes are made up of both base ingredients and flavor ingredients with base ingredients including ingredients such as flour and butter and flavor ingredients being mix-ins such as chocolate, different fruits and added spices. 


The generator starts by choosing sets of 2 recipes from the inspiring set with probabilities proportional to their fitness and then crosses them over with each other choosing one of the bases and combining the flavor ingredients at random. New recipes can then be mutated. Mutations include changes to base and/or flavor ingredients. Changes in the ratios of different base ingredients such as the ratios of types of sugars changes in the ratios of types of flours or also changes in the overall ratios between flour, fats and sugars. Changes in flavor ingredients can either add, swap or delete a flavor ingredient. 


New recipes are then evaluated on their fitness where there are four key factors that make a recipe more fit than another. The first is the number of ingredients where recipes with more ingredients are encouraged. The second is the flavor pairings; using researched flavor pairings and computed scores between two different ingredients, the algorithm then ranks recipes based on the average score between all of the combinations of flavor ingredients in the recipe where recipes with more flavors that align with each other are fitter. The third score is how closely the recipe matches with the chosen emotion. Using scores for how each flavor ingredient aligns with each of the six emotions, recipes with a higher total score for the chosen emotion are more fit. The final evaluation of fitness is dissimilarity as recipes with flavor ingredients that deviate further from the inspiring set of recipes in both their amounts and ingredients are more fit. All four of these evaluations are weighted differently in an order that creates the most unique and quality recipes. These four evaluations all play a role in evaluating which recipes are more novel, taste better and align with the function of the algorithm in matching a cookie to an emotion. The Metrics folder has three example recipes which show the recipe and the ranking of which all four of the methods of evaluation are weighted. The total fitness is the sum of the four. We can see that for these three recipes the two highest scores are the alignment with the emotion and the length. This means the algorithm prioritizes having a variety of ingredients which makes it different from other recipes in that generation as well as how closely it aligns with the emotion. This benefits the system's creativity by selecting for recipes with more ingredients is like selecting for more variety in ingredients which creates more unique ingredient lists. Selecting for recipes with high emotion scores also benefits the creativity because it allows for more unique flavor and ingredient combinations and allows it to fit the users needs, whereas if the flavor pairing score was selected for we wouldn’t see much difference between emotions and some flavor pairings are significantly stronger than others where they constantly occur such as chocolate and vanilla.


After evaluating all of the new recipe’s fitness, the top half of both the new recipes and the previous generation’s recipes (the first generation uses the inspiring set as the previous generation) crosses over and mutates again, creating a new generation of recipes. The number of generations the algorithm runs over is selected by the user.
After all the generations have executed, the top recipe is placed into the fittest recipe folder; the algorithm then creates instructions for the recipe by adding in the ingredients in a set string for the recipe.


Then a spotify playlist for the user based on the emotion to cook with. The playlist is made by randomly choosing a song that aligns with the emotion and then creating a 30 song playlist around that song. 


## How to Install and Run
### Step 1:
To Run the program you should install:
pip3 install numpy 
pip3 install pandas
pip3 install random
pip3 install os
pip3 install spotipy 


### Step 2: 
Change cd(change directory) to cookie_generator (this should be what you named the file)/generator/ in the user terminal
“cd generator/”


### Step 3 
Go to file “cookie_generator” and run file


### Step 4
Input number for emotions (1-6): -> hit Enter in terminal


### Step 5 
Input name -> hit Enter in terminal 


### Step 6
Input the amount of generations you would like to run the program for: -> hit Enter in terminal 


### Step 7 
Go to fittest_recipes to view the generations based on emotions. 


### Step 8 
Copy Spotify link given in terminal and simply paste in browser to retrieve your tailored playlist 



The output of the fittest recipes are separated by these headers: Base ingredients, flavor ingredients, Instructions. 







