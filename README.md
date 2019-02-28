# eecs337-project2
Tasks: 
1) Accept the URL of a recipe from AllRecipes.com, and programmatically fetch the page.
2) Parse it into the recipe data representation your group designs. <br />Your parser should be able to recognize: <br />
   a. Ingredients <br />
      i.   Ingredient name<br />
      ii.  Quantity<br />
      iii. Measurement (cup, teaspoon, pinch, etc.)<br />
      iv.  (optional) Descriptor (e.g. fresh, extra-virgin)<br />
      v.   (optional) Preparation (e.g. finely chopped)<br />
   b. Tools – pans, graters, whisks, etc.<br />
   c. Methods<br />
      i.   Primary cooking method (e.g. sauté, broil, boil, poach, etc.)<br />
      ii.  (optional) Other cooking methods used (e.g. chop, grate, stir, shake, mince, crush, squeeze, etc.)<br />
   d. Steps – parse the directions into a series of steps that each consist of ingredients, tools, methods, and times<br />
3) Ask the user what kind of transformation they want to do.<br />
   a. To and from vegetarian (REQUIRED)<br />
   b. To and from healthy (REQUIRED)<br />
   c. Style of cuisine (AT LEAST ONE REQUIRED)<br />
   d. Additional Style of cuisine (OPTIONAL)<br />
   e. DIY to easy (OPTIONAL)<br />
   f. Cooking method (from bake to stir fry, for example) (OPTIONAL)<br />
