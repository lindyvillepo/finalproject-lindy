And, finally, write that data to a text file -- a sort of "summary stats" page with a clear title, e.g. <List your 3 movie titles> + Twitter summary, <current date>  or something, and have each result of your data processing clearly written to the file neatly below that, on several different lines.

1 full sentence or less, what does each do (a sub bullet point or in parens after the file name)
Each function
name
input
required
optional
return value
behavior if applicable (if you need to explain that the function does something that is not evident from its return value, e.g. that it caches data)
Each class
name
what does one instance represent 
required constructor input
each method
name
any input besides self 
behavior (does it change/add a new instance var? for example)
return value if any, or specify None if None
Database creation
What tables does the database have
For each table
What does each row represent
What attributes in each row
Data manipulation code
What else does the code do?
How is it useful?
What will it show you?
What should a user expect?
Note that each of these things should be 1-2 sentences at most. Just a clear idea: what’s going on here?
Why did you choose to do this project?
Because this is a class and we want to know so we have context for your work.
If you chose option 3
Make sure you explain your end result particularly clearly
Specific things to note for SI 206 -- ok to put this in a section -- copy this right into a .txt file and fill in the correct line numbers
Line(s) on which each of your data gathering functions begin(s):
Line(s) on which your class definition(s) begin(s):
Line(s) where your database is created in the program:
Line(s) of code that load data into your database:
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?
Line(s) of code that generate the output.
OK to be approximate here — ok if it ends up off by 1 or 2. Make it easy for us to find!
Anything else brief and clear we need to know?
Show us a screenshot / image of your project running. This can be included in a PDF file or included as a separate file 
Remember that you must also submit proof of at least 5 git commits for work on the final project, in a screenshot (worth 300 git commits points)


With (any input?), what does it output when run
Does it create a database? 
How do you run it?
1 line description / example of how to run the correct file.
What are its dependencies? You should list these with bulletpoints.
Any modules to install with pip ?
Any particular files you have to have? (e.g. your own twitter_info.py file with certain specifications?
What files are included? Another bulletpoint list.
What are their names


-For my final project, I decided to do option 2. 
-It grabs data from OMBD about three rom coms: the proposal, crazy, stupid, love, and neighbors 2. Then it sorts the data into movie instances, where it then takes the second highest paying actor and searches twitter for popular tweets about the actor and all the users that are mentioned in these tweets.
-I created this project because you can search your favorite movies and see what people on Twitter are saying about the actors in the movies. You just need to input three movies that you would like to get data for.
-The program outputs data about the movie with an example tweet for each movie.



