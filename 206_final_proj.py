# Put all import statements you need here.
import unittest
import tweepy
import requests
import twitter_info
import json
import sqlite3
import itertools
import collections

##### TWEEPY SETUP CODE:
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Part 1 - Gathering Tweet and Movie data

CACHE_NAME = "SI206_finalproj_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_NAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

## Define a function called get_tweets that gets 10 Tweets from a specific Twitter user's timeline, and uses caching. The function should return a Python object representing the data that was retrieved from Twitter.
def get_tweets(user_input):
	search = "twitter_{}".format(user_input)
	if search in CACHE_DICTION:
		print('using cached data for', user_input)
		twitter_results = CACHE_DICTION[search]
	else:
		print('getting data from internet for', user_input)
		twitter_results = api.search(q=user_input, count=10, lang="en", result_type="popular")
		CACHE_DICTION[search] = twitter_results
		f = open(CACHE_NAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return twitter_results

## Define a function called get_movie_data that takes in a movie input and returns a Python object representint the data of the movie that was searched. It should use catching. 
def get_movie_data(movie):
	baseurl = "http://www.omdbapi.com/" 
	identify = "movie_{}".format(movie)
	if identify in CACHE_DICTION:
		print('using cached data for', movie)
		movie_data = CACHE_DICTION[identify]
	else:
		print('fetching data for', movie)
		response = requests.get(baseurl, params={'t': movie})
		r_text = response.text
		movie_data = json.loads(r_text)
		CACHE_DICTION[identify] = movie_data
		f = open(CACHE_NAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return movie_data

# Write a Movie class that takes in a dictionary representing a movie. The constructor should have information regarding the movie's id number, title, director, language, rating, and actors. The class should also have a method that returns a list of actors and another one that returns the number of languages the movie has. Finally, there should be a str method.
class Movies(object):
	def __init__(self, movie_diction):
		self.id = movie_diction["imdbID"]
		self.title = movie_diction["Title"]
		self.director = movie_diction["Director"]
		self.languages = self.num_languages(movie_diction)
		self.rating = movie_diction["imdbRating"]
		self.actors = self.list_of_actors(movie_diction)

	def list_of_actors(self, movie_diction):
		actor_list = movie_diction["Actors"].split(", ")
		return actor_list

	def num_languages(self, movie_diction):
		language_list = movie_diction["Language"].split(", ")
		return len(language_list)

	def movie_tuple(self):
		movie_tup = zip(self.id, self.title, self.director, self.languages, self.rating, self.actors)

	def __str__(self):
		return "{} is directed by {} with a rating of {} with main actor {}.\n".format(self.title, self.director, self.rating, self.actors[0])

# Write a Tweet class that takes in a dictionary representing a tweet. The constructor should have information regarding the tweet's id number, text, number of favorites, number of retweets, id string, and search. There should also be a str method.
class Tweet(object):
	def __init__(self, tweet_diction, actor):
		self.id = self.tweet_id(tweet_diction)
		self.text = self.tweet_text(tweet_diction)
		self.favorites = self.num_favs(tweet_diction)
		self.retweets = self.num_retweets(tweet_diction)
		self.idstr = self.tweet_idstr(tweet_diction)
		self.search = actor

	def tweet_id(self, tweet_diction):
		id_list = []
		for tweet in tweet_diction["statuses"]:
			id_list.append(tweet["id"])
		return id_list

	def tweet_text(self, tweet_diction):
		text_list = []
		for tweet in tweet_diction["statuses"]:
			text_list.append(tweet["text"])
		return text_list

	def num_favs(self, tweet_diction):
		fav_list = []
		for tweet in tweet_diction["statuses"]:
			fav_list.append(tweet["favorite_count"])
		return fav_list

	def num_retweets(self, tweet_diction):
		retweet_list = []
		for tweet in tweet_diction["statuses"]:
			retweet_list.append(tweet["retweet_count"])
		return retweet_list

	def tweet_idstr(self, tweet_diction):
		idstr_list = []
		for tweet in tweet_diction["statuses"]:
			idstr_list.append(tweet["id_str"])

	def tweet_tuple(self):
		tweet_tup = zip(self.id, self.text, self.favorites, self.retweets, self.idstr, self.search)
		return tweet_tup

	def __str__(self):
		return "Searching popular tweets about {} with tweets like {}.\n".format(self.search, self.text[0])

# Write a tweetUser class that takes in a dictionary representing a tweet. The constructor should have information regarding each of the users in the "neighborhood", which is generally defined by tweet posters, all the users mentioned, all the users who have favorited/liked a tweet. Some people also define it with e.g. everyone who has RT'd the tweet as well. For each user, the constructor should initialize the user id, screen name, number of favorites ever favorited, and user description.
class TweetUser(object):
	def __init__(self, tweet_diction):
		self.idstr = self.user(tweet_diction)
		self.screen_name = self.user_name(tweet_diction)
		self.num_favs = self.favs_ever(tweet_diction)
		self.description = self.user_description(tweet_diction)

	def user(self, tweet_diction):
		user_list = []
		for tweet in tweet_diction["statuses"]:
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["id_str"])
				user_list.append(info["id_str"])
			for user in tweet["user"]:
				user_list.append(user["id_str"])
		return user_list

	def user_name(self, tweet_diction):
		name_list = []
		for tweet in tweet_diction["statuses"]:
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["id_str"])
				name_list.append(info["screen_name"])
			for user in tweet["user"]:
				name_list.append(user["screen_name"])
		return name_list

	def favs_ever(self, tweet_diction):
		favs_list = []
		for tweet in tweet_diction["statuses"]:
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["id_str"])
				favs_list.append(info["favourites_count"])
			for user in tweet["user"]:
				favs_list.append(user["favourites_count"])
		return favs_list

	def user_description(self, tweet_diction):
		description_list = []
		for tweet in tweet_diction["statuses"]:
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["id_str"])
				description_list.append(info["description"])
			for user in tweet["user"]:
				description_list.append(user["description"])
		return description_list

	def user_tuple(self):
		user_tup = zip(self.idstr, self.screen_name, self.num_favs, self.description)
		return user_tup

# Write a list of the three movie search terms you want to use to search in OMDB and put them in a list called movie_search_list. Then, make a request to OMDB on each of those search terms and accumulate the dictionaries of each movie into a list called movie_info_list.
movie_search_list = ["the proposal", "neighbors 2", "crazy, stupid, love"]
movie_info_list = []
for movie in movie_search_list:
	search = get_movie_data(movie)
	movie_info_list.append(search)

# Make a list of movie instances of the movie instances of each movie in the list "movie_info_list"
movie_instance = []
for movie in movie_info_list:
	instance = Movies(movie)
	movie_instance.append(instance)

# Iterate through movie_instance to get the twitter diction of the second top-paid actor. Then get an instance of that tweet and append it in the list "twitter_list"
twitter_list = []
user_list = []
for movie in movie_instance:
	actor = movie.actors[1]
	print(actor)
	tweet_diction = get_tweets(actor)
	tweet = Tweet(tweet_diction, actor)
	print(tweet)
	twitter_list.append(tweet)
	user = TweetUser(tweet_diction)
	print(user_instance)
	user_list.append(user)

## Part 2 - Creating database and loading data into database

# You will be creating a database file: final_project.db
# The database file should have 3 tables, and each should have the following columns...
conn = sqlite3.connect("finalproject.db")
cur = conn.cursor() 

# Table Users, with columns:
# -user_id - containing the string id belonging to the user (Primary Key)
# -screen_name - containing the screen name of the user on Twitter
# -num_favs - containing the number of tweets that user has ever favorited
# -description - text containing the description of that user on Twitter
cur.execute('DROP TABLE IF EXISTS Users')
user_table = 'CREATE TABLE IF NOT EXISTS '
user_table += 'Users (user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER, description TEXT)'
cur.execute(user_table)

# Table Movies, with columns:
# -movie_id - containing the unique id that belongs to the movie (Primary Key)
# -title - containing the string of the movie title name
# -director - containing the string of the movie director name 
# -languages - containing the number that represents how many languages the movie has
# -imbd_rating - containing the number that represents the rating of the movie
# -actor - containing the string of the movie's top paid actor/actress
cur.execute('DROP TABLE IF EXISTS Movies')
movie_table = 'CREATE TABLE IF NOT EXISTS '
movie_table += 'Movies (movie_id INTEGER PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, imbd_rating INTEGER, actor TEXT)'
cur.execute(movie_table)

# Table Tweets, with columns:
# -tweet_id - containing the unique id that belongs to each tweet (Primary Key)
# -tweet_text - containing the text that goes with that tweet
# -favorites - containing the number that represents the number of favorites the tweet had
# -retweets - containing the number that represents how many times the tweet has been retweeted
# -user_id - containing an ID string, referencing the Users table
# -movie_search - containing a string of the movie search this tweet came from (represented by a reference to the movies table)
cur.execute('DROP TABLE IF EXISTS Tweets')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id INTEGER PRIMARY KEY, tweet_text TEXT, favorites INTEGER, retweets INTEGER, user_id TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES Users(user_id) on UPDATE SET NULL, movie_search TEXT NOT NULL, FOREIGN KEY (movie_search) REFERENCES Movies(title) on UPDATE SET NULL)'
cur.execute(statement)

# You should load into the Users table:
# The user, and all of the data about users that are mentioned in the movie search's timeline. 

# user_id = []
# screen_name = []
# num_favs = []
# description = []
# for user in user_list:
# 	user_id.append(user.idstr)
# 	screen_name.append(user.screen_name)
# 	num_favs.append(user.num_favs)
# 	description.append(user.description)

# user_info = zip(user_id, screen_name, num_favs, description)

user_info = []
for user in user_list:
	user_info.append(movie.user_tuple())

user_table = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'
for user in user_info:
	cur.execute(user_table, user)

# You should load into the Movies table:
# Info about the movie that is from the movie search's timeline.

# movie_id = []
# titles = []
# directors = []
# language = []
# rating = []
# actor = []
# for movie in movie_instance:
# 	movie_id.append(movie.id)
# 	titles.append(movie.title)
# 	directors.append(movie.director)
# 	language.append(movie.languages)
# 	rating.append(movie.rating)
# 	actor.append(movie.actors[0])

# movie_info = zip(movie_id, titles, directors, language, rating, actor)

movie_info = []
for movie in movie_instance:
	movie_info.append(movie.movie_tuple())

movie_table = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'
for movie in movie_info:
	cur.execute(movie_table, movie)

# You should load into the Tweets table: 
# Info about all the tweets that is from the movie search's timeline.

# tweet_id = []
# text = []
# num_favorite = []
# retweets = []
# user_id = []
# movie_title = []
# for tweet in twitter_list:
# 	tweet_id.append(tweet.id)
# 	tweet_text.append(tweet.text)
# 	num_favorite.append(tweet.favorites)
# 	retweets.append(tweet.retweets)
# 	user_id.append(tweet.idstr)
# 	movie_title.append(tweet.search)

# tweet_info = list(zip(tweet_id, tweet_text, num_favorite, retweets, user_id, movie_title))

tweet_info = []
for tweet in twitter_list:
	tweet_info.append(tweet.tweet_tuple())

statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_info:
	cur.execute(statement, tweet)

## Part 3 - Making queries

# Make a query to select all of the tweet texts from the database. Save a resulting list of strings in the variable tweet_texts.
query = "SELECT tweet_text FROM Tweets"
cur.execute(query1)
tuple_text = cur.fetchall()
tweet_texts = [x[0] for x in tuple_text]

## Part 4 - Manipulating data

# Use a set comprehension to get a set of all words among the texts in the tweet_texts list. Save the resulting set in a variable called tweet_words.
word_list = []
for line in tweet_texts:
 	words = line.split()
 	for word in words:
 		word_list.append(word)

tweet_words = {word for word in word_list}

# Put your tests here, with any edits you now need from when you turned them in with your project plan.
# class myTests(unittest.TestCase):
# 	def test_get_user_tweets(self):
# 		bride = get_user_tweets("bridesmaids")
# 		self.assertEqual(type(bride), type(["hey", 10]))
# 	def test_meangirl_tweets(self):
# 		self.assertEqual(type(meangirls_tweets), type([]))
# 	def test_bridesmaids_tweets(self):
# 		self.assertEqual(type(bridesmaids_tweets), type([]))
# 	def test_hangover_tweets(self):
# 		self.assertEqual(type(hangover_tweets), type([]))
# 	def test_movie_instance(self):
# 		self.assertEqual(type(movie_instance), type([]))
# 	def test_search_term(self):
# 		self.assertEqual(type(search_term), type([]), "testing search_term function is type list")
# 	def test_movie_data(self):
# 		self.assertEqual(type(movie_data), type({}), "testing movie_data function is type dictionary")
# 	def test_movie_actors(self):
# 		shes_the_man = {"She's the Man": ["Andy Fickman", 6.4, ["Amanda Bynes", "Channing Tatum", "Laura Ramsey", "Vinny Jones"], 1]}
# 		movie = Movie(shes_the_man)
# 		self.assertEqual(type(movie.actors), type([]), "testing movie.actors is type list")
# 	def test_movie_rating(self):
# 		shes_the_man = {"She's the Man": ["Andy Fickman", 6.4, ["Amanda Bynes", "Channing Tatum", "Laura Ramsey", "Vinny Jones"], 1]}
# 		movie = Movie(shes_the_man)
# 		self.assertEqual(movie.rating, 6.4, "testing movie.rating is 6.4")
# 	def test_database(self):
# 		conn = sqlite3.connect('final_project.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Movies');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)>=3, "Testing there are at least 3 records in the Tweets database")
# 		conn.close()
# 	def test_movie_list(self):
# 		self.assertEqual(type(screen_names),type([]),"Testing that movie_list is a list")
# 	def test_movie_list2(self):
# 		self.assertEqual(type(movie_list[1]),type(""),"Testing that an element in movie_list is a string")
# 	def test_tweet_director(self):
# 		self.assertEqual(type(tweet_director[0]),type(("hi","bye")),"Testing that an element in the joined query tweet_director is a tuple")
# 	def test_tweet_movie(self):
# 		self.assertEqual(type(tweet_movie[0]), type({}), "Testing that an element in tweet_movie is a dictionary")
# 		self.assertEqual(type(tweet_movie[0][0]), type(""), "Testing that the first key in an element of tweet_movie is a string")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)

