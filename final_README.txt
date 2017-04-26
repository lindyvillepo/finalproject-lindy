And, finally, write that data to a text file -- a sort of "summary stats" page with a clear title, e.g. <List your 3 movie titles> + Twitter summary, <current date>  or something, and have each result of your data processing clearly written to the file neatly below that, on several different lines.


Name: Lindy Villeponteau
Date: April 25, 2017
Movies: High School Musical, Crazy, Stupid, Love, Mean Girls, We're the Millers, La La Land.

Movie output:
Crazy, Stupid, Love. is directed by Glenn Ficarra, John Requa with a rating of 7.4 with main actor Steve Carell.

Mean Girls is directed by Mark Waters with a rating of 7.0 with main actor Lindsay Lohan.

We're the Millers is directed by Rawson Marshall Thurber with a rating of 7.0 with main actor Jennifer Aniston.

La La Land is directed by Damien Chazelle with a rating of 8.3 with main actor Ryan Gosling.


Line(s) on which each of your data gathering functions begin(s):
	-queries: Line 253
	-popular_users: Line 282
	-tweet_words: Line 285
	-most_common: Line 294
	-twitter_actor: Line 306
	-hashtag_set: Line 308
Line(s) on which your class definition(s) begin(s):
	-Movies: Line 70
Line(s) where your database is created in the program:
	-Users: Line 151
	-Movies: Line 161
	-Tweets: Line 173
Line(s) of code that load data into your database:
	-Users: Line 185
	-Movies: Line 204
	-Tweets: Lind 226
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?
	-Lines 282 to 325
Line(s) of code that generate the output.
	-Lines 282 to 325 (within each code)

-For my final project, I decided to do option 2.

-It grabs data from OMBD about four movies: high school musical, crazy, stupid, love, mean girls, we're the millers, and la la land. Then it sorts the data into movie instances, where it then takes the highest paying actor and searches twitter for popular tweets about the actor and all the users that are mentioned in these tweets.

-I created this project because you can search your favorite movies and see what people on Twitter are saying about the actors in the movies. You just need to input movies into a list that you would like to get data for.

-The program outputs data about the movie with an example tweet for each movie.

-It creates a database, finalproject.db

-You can run the file "206_final_proj.py" on a PC or terminal on a Mac

-It's dependencies include:
	-tweepy
	-sqlite3
	-requests
	-collections

-You have to have your own twitter_info.py to access the twitter API that contains your consumer key and access token.

-The only files you need to run this code is 206_final_proj.py and a twitter_info.py file.

-Functions
	-get_tweets(user_input): this function takes a string (user_input), and searches if it's already in the cache file. If it's not, it will search for data on Twitter and put it in the cache file. It will return a dictionary of twitter data found from either the cache file or Twitter.

	-get_movie_data(movie): this function takes a movie name (movie), and searches if it's already in the cache file. If it's not, it will search the OMDB website for information about the movie that was inputted. It will return a dictionary of movie data found from either the cache file or OMDB. 

	-list_of_tweet_tuples(tweet_diction, actor): this function takes in a tweetdictionary (found from the get_tweets function), and a search word (actor). It will iterate through the dictionary and find information about each tweet in the dictionary. It will then put all the information, including the search word, into a tuple about a specific tweet. Finally, it will put all the tweet tuples into a list of tuples and return it.

	-list_of_user_tuples(tweet_diction): this function takes in a tweet dictionary (found from the get_tweets function). It will iterate through the dictionary and find information about the user that posted each tweet, as well as information about users that were mentioned in the tweet. It will then put all the information about a user into a tuple. Finally, it will add all the tuples of user info into a list called user_list and return it.

	-get_twitter_hashtags(user_input): this function takes in a string (user_input), and searches if it has any hashtags in the string. If it does, it will return a set of them with the hashtag included.

-Classes
	-Movie class: The constructor of this class takes in a movie dictionary. It has 6 instances: id, title, director, languages, rating, and actors. It will find these instances in the movie dictionary. 

		-Method "list_of_actors": this method takes the movie dictionary and extracts the string of actors found and adds them to a list called actor_list. It will return this list and is used to find the instance "actors".

		-Method "num_languages": this method takes in the movie dictionary and extracts the string of languages found and adds it to the list language_list. It then finds the number of languages in the list and returns the number. This is used to find the "languages" instance.

		-The string method returns a string with the title, director, rating, and top paid actor.

-Databases
	-Users: the Users database has tables with the user id (primary key), screen name, number of favorites, and user description. Each row represents a user, and the tables show information about the user. 

	-Movies: the Movies database has tables with the movie id (primary key), movie title, director, number of languages, imbd rating, and top paid actor. Each row represents a movie, and the tables show information about the specific movie. 

	-Tweets: the Tweets database has tables with the tweet id (primary key), text of the tweet, number of favorites the tweet has, number of retweets, the screen name of the user who posted the tweet (referenced from the Users table), and the actor that was searched (referenced from the Movies table). Each row represents a tweet, and the tables show information about that specific tweet. 

-Data Manipulation
	-popular_users: this code outputs the twitter screenname (with the @ sign) of the most popular users (with retweets over 50) found from the Tweets database. It's useful because you can see who is well liked on Twitter and can possibly follow them. 

	-tweet_words: this code gives you all the words in popular tweets (ones with more than 25 favorites). This is useful because you can see what words people who get a lot of favorites use.

	-most_common: this code outputs the 3 most common words from the tweets that have more than 25 favorites. This is just cool to see what words mose people use.

	-twitter_actor: this code outputs the actor and the tweet associated with the actor. This is useful to see what people say about specific actors.

	-hashtag_set: this code outputs all the hashtags found in the popular tweets from before. This is useful to see what people who get a lot of favorites hashtag.

-I did this option because I thought it was the most interesting and applicable to people our age. It's cool to see what different tweets are about different actors from my favorite movies. 

Output:

-popular_users: 
Most popular users: @people
Most popular users: @BuzzFeed
Most popular users: @elvirathyberg
Most popular users: @manuconh4
Most popular users: @thisisangelica_
Most popular users: @tritonandres
Most popular users: @flwrstohoran
Most popular users: @bollywood_life
Most popular users: @Gauwdd
Most popular users: @sasha_velour
Most popular users: @damueller22
Most popular users: @MTV
Most popular users: @allstardead
Most popular users: @emmablackery
Most popular users: @oh_hadz

-most_common:
Three most popular words used: a , to , and Efron

-twitter_actor:
 Ryan Gosling :
- See 11 gorgeous never-before-seen #LaLaLand photos: https://t.co/IhTv0MZq98 https://t.co/adVcvmdVS8
- We need to talk about Ryan Gosling at a parking meter 
https://t.co/EjKWAGh1xk https://t.co/z3akR4z6mk
- Which Best Kiss contenders could give Ryan Gosling and Rachel McAdams a run for their money at the #MTVAwards? 😘 Fi… https://t.co/wj6WGBRp99
- ryan gosling saving jazz from being gentrified by john legend is possibly the most incredible part of la la land
- 🐪 ♫ City of Stars by Ryan Gosling &amp; Emma Stone — https://t.co/HVIY8Qn32u
- RT @MIASWlLDER: me wishing for a new film where emma stone &amp; ryan gosling play two people who fall in love and are super cute together http…
- @AntBejarano The Ryan Gosling clone. Idk how he's doing that like I'm convinced this guy is actually Ryan
- #LaLaLandDay City Of Stars by Ryan Gosling ♫ https://t.co/g84Bz62RZK
- Love Emma Stone and Ryan Gosling but LaLa Land is a complete goober movie!
- Check out "City Of Stars" on #Smule: https://t.co/wjn9DiYm0K #SingKaraoke

 Zac Efron :
- 5 instances that prove Varun Dhawan is Bollywood's Zac Efron https://t.co/haOjr7Bos7
- Zac Efron looks phenomenal without a shirt, but he has to work hard on set to get (and keep) those abs:… https://t.co/d1jLG3PPNW
- What Time Is It? Time to Watch Zac Efron Search for Love on MTV's Room Raiders https://t.co/IenulaNvYL
- #Entertainment #Buzz Zac Efron Poster 24"x36" https://t.co/xBPvheg8uR #eBay #Auction https://t.co/JmYiSVL4by
- #nude pic egyptian girl naked zac efron pictures https://t.co/5dD3DgVZGN
- #naked zac efron pictures hinata blowjob https://t.co/JSY6p8bpjR
- RT @enews: What Time Is It? Time to Watch Zac Efron Search for Love on MTV's Room Raiders https://t.co/IenulaNvYL
- RT @EstefniaZila: Sim, Zac Efron e a Vanessa Hudgens😩😭 https://t.co/ByH3z7NEGG
- picture of zac efron nude #love of ray j cocktail nude https://t.co/zT8vhLUdd2
- RT @shirklesxp: Chatted w/ @ZacEfron abt #Baywatch—he called @TheRock "a flower that never stops blooming" &amp; I'm still not over it! https:/…

 Lindsay Lohan :
- Would you want to see Lindsay Lohan in a “Life-Size” Sequel?
- Retweet if you are a Cossack warrior princess but also deep down inside you are also Lindsay Lohan https://t.co/KDpkjQy9Dv
- Honestly pop music peaked after Lindsay Lohan released Speak and I won't hear any arguments about it
- RT @drugproblem: Lindsay Lohan for L'Officiel Magazine, May 2017 🌟🌹❤️ https://t.co/OibrQkUAmz
- RT @YasminAllen_: dunno why I act like I'm Gandhi when I'm more of a mess than Lindsay Lohan was
- #halfcast babe fucked lindsay lohan nude vanity fair https://t.co/g1M8eer3rd
- RT @thanx: life imitates art
-the ecstasy of st. teresa by gian lorenzo bernini (1647-1652) // lindsay lohan passed out after night of part…
- RT @xnaraarts: Lindsay Lohan for L’Officiel Hommes, 2012 https://t.co/SRKdQOxE10
- #lindsay lohan nude nude pictures of doa girls naked https://t.co/XL9biJFWmx
- #lindsay lohan naked pic amateur free movie https://t.co/VjvtKGe0tO
- RT @emmablackery: Honestly pop music peaked after Lindsay Lohan released Speak and I won't hear any arguments about it
- #NowPlaying Confessions Of A Broken Heart (Daughter To Father) - Radio de Lindsay Lohan ♫ https://t.co/kNyxKp0Kp2
- #lindsay lohan nude photo spornette italian collection https://t.co/lllo8F2SUo

 Steve Carell :
- One of a kind auction item-66 jersey signed by actors Bryan Cranston, Steve Carell, Laurence Fishburne &amp; Mario!… https://t.co/c4wFzuqxDT
- Steve Carell reveals what he thought about playing twins in '@DespicableMe 3': https://t.co/9OBApwf3Ef… https://t.co/yGrcfEZXef
- RT @TheOffice___: Steve Carell's presentation at the 2007 Emmy Awards is everything (crying laughing emoji) https://t.co/KY3UhkxGvj
- RT @rainnwilson: The world of TV should be ashamed of itself that Steve Carell never won an Emmy for Michael Gary Scott. Goodnight.
- steve carell is my eternal spirit
- RT @TheOffice___: Steve Carell's presentation at the 2007 Emmy Awards is everything (crying laughing emoji) https://t.co/KY3UhkxGvj
- I literally laugh at everything Michael Scott says/does. Truly cannot get over the brilliance of Steve Carell!!!!
- All i see when i look at this is steve carell shouting no that is not a cup of tea that is milk ☕️☕️ https://t.co/uy14m1PMxm
- #Famous #Actress THE OFFICE SIGNED SCRIPT STEVE CARELL JENNA FISCHER JOHN KRASINSKI BJ NOVACK https://t.co/ULOd1lrLy9 #JennaFischer #Deals
- RT @StarLordSwanson: Steve Carell - The Penguin https://t.co/1kOf8O1avo
- RT @Collider: See Emma Stone &amp; Steve Carell transform into tennis stars in first #BattleOfTheSexes image: https://t.co/shdexPC7WE https://t…
- I liked a @YouTube video https://t.co/7UEL9zOARP Despicable Me 3 "Villains" Trailer (2017) Steve Carell Animated Movie HD
- RT @TheOffice___: Steve Carell's presentation at the 2007 Emmy Awards is everything (crying laughing emoji) https://t.co/KY3UhkxGvj
- Just watched #dinnerforschmucks on @BBCiPlayer Haven't laughed like that at a film in a while. Love Steve Carell.
- RT @TheOffice___: Steve Carell's presentation at the 2007 Emmy Awards is everything (crying laughing emoji) https://t.co/KY3UhkxGvj

 Jennifer Aniston :
- Jennifer Aniston, Courteney Cox, Katy Perry Celebrate Jennifer Meyer's 40th Birthday (PHOTO GALLERY) https://t.co/zshr6YFfQf
- The World’s #MostBeautiful Couples of 2017 😍 https://t.co/BhPx0DfpxZ https://t.co/t9Bb0BqIPz
- Is Curvy Model @HunterMcGrady the New Jennifer Aniston? https://t.co/t2vudKCX7Z https://t.co/UAIkRfSwjq
- What Jennifer Aniston Eats In A Day Is Shocking! https://t.co/3AT5iKGzBV
- RT @countrygiral: art: sunflowers and jennifer aniston https://t.co/mc0gu58vla
- #ukraine milf jennifer aniston fully nude https://t.co/QtKh2VZe2j
- RT @alphabetsuccess: There are no regrets in life. Just lessons. - Jennifer Aniston #quote #TuesdayMotivation https://t.co/r8XAnPAFEQ
- What Jennifer Aniston Eats In A Day Is Shocking! https://t.co/EMUwnEkC1M
- RT @alphabetsuccess: There are no regrets in life. Just lessons. - Jennifer Aniston #quote #TuesdayMotivation https://t.co/r8XAnPAFEQ
- #megaupload porn mp4 jennifer aniston completely nude https://t.co/HsgfV6ASJe
- RT @alphabetsuccess: There are no regrets in life. Just lessons. - Jennifer Aniston #quote #TuesdayMotivation https://t.co/r8XAnPAFEQ
- #best place to watch porn jennifer aniston porn fake https://t.co/U9JSC0rLIc
- Marley &amp; Me Owen Wilson Jennifer Aniston Widescreen #DVD https://t.co/bnhHFd8y6I #eBay #Auction https://t.co/0KtLpVB6Kx
- RT @people: The World’s #MostBeautiful Couples of 2017 😍 https://t.co/BhPx0DfpxZ https://t.co/t9Bb0BqIPz
- RT @iLikeTitsDaily: Retweet if you would wife up Jennifer Aniston https://t.co/VeiKkOySvz

-hashtag_set:
Hashtags used from popular tweets:
- #LaLaLand
- #MostBeautiful
- #MTVAwards
