# Put all import statements you need here.
import unittest
import tweepy
import requests
import twitter_info
import json
import re
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

## Define a function called get_tweets that gets tweets from Twitter, and uses caching. The function should return a Python object representing the data that was retrieved from Twitter.
def get_tweets(user_input):
	search = "twitter_{}".format(user_input)
	if search in CACHE_DICTION:
		print('using cached data for', user_input)
		twitter_results = CACHE_DICTION[search]
	else:
		print('getting data from internet for', user_input)
		twitter_results = api.search(q=user_input, lang="en", result_type="mixed")
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
		self.rating = float(movie_diction["imdbRating"])
		self.actors = self.list_of_actors(movie_diction)

	def list_of_actors(self, movie_diction):
		actor_list = movie_diction["Actors"].split(", ")
		return actor_list

	def num_languages(self, movie_diction):
		language_list = movie_diction["Language"].split(", ")
		return len(language_list)

	def __str__(self):
		return "{} is directed by {} with a rating of {} with main actor {}.\n".format(self.title, self.director, self.rating, self.actors[0])

# Write a function called list_of_tweet_tuples that takes in a dictionary representing tweets and an actor that the tweet is about. Make a tuple of the id, text, number of favorites, number of retweets, username who posted the tweet, and what was searched to find the tweet. Save this tuple in a list called tweet_list.
def list_of_tweet_tuples(tweet_diction, actor):
	tweet_list = []
	for tweet in tweet_diction["statuses"]:
		tweet_id = tweet["id"]
		text = tweet["text"]
		favs = tweet["favorite_count"]
		retweets = tweet["retweet_count"]
		post = tweet["user"]["screen_name"]
		search = actor
		tweet_list.append((tweet_id, text, favs, retweets, post, search))
	return tweet_list

# Write a function called list_of_user_tuples that takes in a dictionary representing a tweet. It should contain a tuple of the user who posted the tweet, and all the users mentioned in the tweet. Save these tuples in a list called user_list
def list_of_user_tuples(tweet_diction):
	user_list = []
	for tweet in tweet_diction["statuses"]:
		user_id = tweet["user"]["id_str"]
		user_name = tweet["user"]["screen_name"]
		user_favs = tweet["user"]["favourites_count"]
		user_desc = tweet["user"]["description"]
		user_list.append((user_id, user_name, user_favs, user_desc))
		for user in tweet["entities"]["user_mentions"]:
			info = api.get_user(id=user["screen_name"])
			strid = info["id_str"]
			name = info["screen_name"]
			favs = info["favourites_count"]
			desc = info["description"]
			user_list.append((strid, name, favs, desc))
	return user_list

# Write a list of the three movie search terms you want to use to search in OMDB and put them in a list called movie_search_list. Then, make a request to OMDB on each of those search terms and accumulate the dictionaries of each movie into a list called movie_info_list.
movie_search_list = ["the proposal", "high school musical", "crazy, stupid, love", "mean girls", "we're the millers", "la la land"]
movie_info_list = []
for movie in movie_search_list:
	search = get_movie_data(movie)
	movie_info_list.append(search)

# Make a list of movie instances of the movie instances of each movie in the list "movie_info_list"
movie_instance = []
for movie in movie_info_list:
	instance = Movies(movie)
	movie_instance.append(instance)

# Iterate through movie_instance to get the twitter diction of the top-paid actor. Then get an instance of that tweet and the users and append it in the list "twitter_list" and "user_list". 
twitter_list = []
user_list = []
for movie in movie_instance:
	actor = movie.actors[0]
	tweet_diction = get_tweets(actor)
	twitter_list.append(list_of_tweet_tuples(tweet_diction, actor))
	user_list.append(list_of_user_tuples(tweet_diction))

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
movie_table += 'Movies (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, imbd_rating FLOAT, actor TEXT)'
cur.execute(movie_table)

# Table Tweets, with columns:
# -tweet_id - containing the unique id that belongs to each tweet (Primary Key)
# -tweet_text - containing the text that goes with that tweet
# -favorites - containing the number that represents the number of favorites the tweet had
# -retweets - containing the number that represents how many times the tweet has been retweeted
# -user_id - containing an ID string, referencing the Users table
# -search - containing a string of the movie search this tweet came from (represented by a reference to the movies table)
cur.execute('DROP TABLE IF EXISTS Tweets')
statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id INTEGER PRIMARY KEY, tweet_text TEXT, favorites INTEGER, retweets INTEGER, user_post TEXT NOT NULL, search TEXT NOT NULL, FOREIGN KEY (user_post) REFERENCES Users(screen_name) on UPDATE SET NULL, FOREIGN KEY (search) REFERENCES Movies(actor) on UPDATE SET NULL)'
cur.execute(statement)

# You should load into the Users table:
# The user, and all of the data about users that are mentioned in the tweet's dictionary. 
user_id = []
screen_name = []
num_favs = []
description = []
for search in user_list:
	for user in search:
		user_id.append(user[0])
		screen_name.append(user[1])
		num_favs.append(user[2])
		description.append(user[3])

user_info = zip(user_id, screen_name, num_favs, description)

user_table = 'INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)'
for user in user_info:
	cur.execute(user_table, user)

# You should load into the Movies table:
# Info about the movie that is from the movie search's timeline.
movie_id = []
titles = []
directors = []
language = []
rating = []
actor = []
for movie in movie_instance:
	movie_id.append(movie.id)
	titles.append(movie.title)
	directors.append(movie.director)
	language.append(movie.languages)
	rating.append(movie.rating)
	actor.append(movie.actors[0])

movie_info = zip(movie_id, titles, directors, language, rating, actor)

movie_table = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'
for movie in movie_info:
	cur.execute(movie_table, movie)

# You should load into the Tweets table: 
# Info about all the tweets that is from the tweet's dictionary.
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
for search in twitter_list:
	for tweet in search:
		list1.append(tweet[0])
		list2.append(tweet[1])
		list3.append(tweet[2])
		list4.append(tweet[3])
		list5.append(tweet[4])
		list6.append(tweet[5])

tweet_info = zip(list1, list2, list3, list4, list5, list6)

statement = 'INSERT OR IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_info:
	cur.execute(statement, tweet)

conn.commit()

## Part 3 - Making queries

# Make a query to select all of the tweet texts where the favorites were greater than 10 from the database. Save a resulting list of strings in the variable tweet_texts.
query = "SELECT tweet_text FROM Tweets WHERE favorites > 10"
cur.execute(query)
tuple_texts = cur.fetchall()
tweet_texts = [x[0] for x in tuple_texts]

# Select all of the movies (the full rows/tuples of information) that have an IMBD score of MORE than 7.0, and fetch them into the variable more_than_7.
query1 = "SELECT * FROM Movies WHERE imbd_rating > 7.0"
cur.execute(query1)
more_than_7 = cur.fetchall()

# Make a query using an INNER JOIN to get a list of tuples with 2 elements in each tuple: the movie title and the screen name of the user who posted the tweet. Save the resulting list of tuples in a variable called movie_tweet.
query2 = "SELECT Movies.actor, Tweets.tweet_text FROM Tweets INNER JOIN Movies on Tweets.search = Movies.actor"
cur.execute(query2)
actor_tweet = cur.fetchall()

# Select all of the TEXT values of the tweets that are retweets of another account (i.e. have "RT" at the beginning of the tweet text). Save the tuples in a variable called tuple_rt.
query3 = "SELECT tweet_text FROM Tweets WHERE instr(tweet_text, 'RT')"
cur.execute(query3)
tuple_rt = cur.fetchall()

# Make a query using an INNER JOIN to get a list of tuples with 2 elements in each tuple: the screen name of the user and the number of retweets when retweets are bigger than 50.
query4 = "SELECT Users.screen_name, Tweets.retweets FROM Users INNER JOIN Tweets on Users.screen_name = Tweets.user_post WHERE Tweets.retweets > 50"
cur.execute(query4)
pop_users = cur.fetchall()


## Part 4 - Manipulating data

# Use a set comprehension to get a set of all the screen names from pop_users where their retweets were more than 50. Add an '@' sign to each user of the set and call this popular_users.
popular_users = {('@'+x[0]) for x in pop_users}

# Use a set comprehension to get a set of all words among the texts in the tweet_texts list. Save the resulting set in a variable called tweet_words.
word_list = []
for line in tweet_texts:
 	words = line.split()
 	for word in words:
 		word_list.append(word)

tweet_words = {word for word in word_list}

# Use a Counter in the collections library to find the most common words among all of the texts in the tweet_texts list. Save the 3 most common words in a list called most_common.
common_words = collections.Counter(word_list).most_common(3)
most_common = []
for word in common_words:
	most_common.append(word[0])

# Write code to create a dictionary whose keys are the top paid movie actor and whose associated values are lists of tweet texts that that was posted about them. You should save the dictionary in a variable called twitter_actor.
default = collections.defaultdict(list)

for key, value in actor_tweet:
	default[key].append(value)

twitter_actor = dict(default)

# Define a function get_twitter_hashtags that accepts a string as in put and returns a set of the hashtags of each hashtag that was mentioned in the tweet string. Then iterate through tweet_texts to find all the hashtags in the texts and append it to a list called hashtag_set.
def get_twitter_hashtags(user_input):
	phrase = r"\#\w+\_*[A-Za-z0-9_]*"
	hashtags = re.findall(phrase, user_input)
	results = []
	for tags in hashtags:
		results.append(tags)
	return set(results)

hashtag_set = []
for tweet in tweet_texts:
	if (get_twitter_hashtags(tweet)):
		hashtag_set.append(get_twitter_hashtags(tweet))
	else:
		continue

## Make sure to close database!!!
conn.close()

# Put your tests here, with any edits you now need from when you turned them in with your project plan.
class partOne(unittest.TestCase):
	def test_get_user_tweets(self):
		bride = get_tweets("bridesmaids")
		self.assertEqual(type(bride), type({}))
	def test_get_movie_data(self):
		movie = get_movie_data("love actually")
		self.assertEqual(type(movie), type({}))
	def test_movie_class(self):
		clue = get_movie_data("clueless")
		clue_movie = Movies(clue)
		self.assertEqual(clue_movie.director, "Amy Heckerling")
		self.assertEqual(clue_movie.rating, 6.8)
		self.assertEqual(type(clue_movie.rating), type(float()))
	def test_list_tuples(self):
		more_tweets = get_tweets("graduation")
		self.assertEqual(type(list_of_user_tuples(more_tweets)[0]), type(tuple()))
		self.assertEqual(type(list_of_user_tuples(more_tweets)), type([]))

class partTwo(unittest.TestCase):
	def test_tweets1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==6,"Testing that there are 5 columns in the Tweets table")
		conn.close()
	def test_users_1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==4,"Testing that there are 4 columns in the Users database")
		conn.close()
	def test_movies1(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies')
		result  = cur.fetchall()
		self.assertTrue(len(result[0])==6)
		conn.close()
	def test_users_2(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=5)
		conn.close()
	def test_movies2(self):
 		conn = sqlite3.connect('finalproject.db')
 		cur = conn.cursor()
 		cur.execute('SELECT * FROM Movies');
 		result = cur.fetchall()
 		self.assertTrue(len(result)>=3, "Testing there are at least 3 records in the Movies database")
 		conn.close()

class partThree(unittest.TestCase):
	def test_tweet_texts(self):
		self.assertEqual(type(tweet_texts[0]), type(str()))
	def test_rating(self):
		if len(more_than_7) >= 1:
			self.assertTrue(len(more_than_7[0])==6)
	def test_rating2(self):
		self.assertEqual(type(more_than_7), type([]))
	def test_innerjoin(self):
		self.assertEqual(type(actor_tweet), type([]))
		self.assertEqual(type(actor_tweet[0]), type(()))
	def test_rt(self):
		self.assertEqual(tuple_rt[0][0][:2], "RT")
	def test_pop_users(self):
		self.assertEqual(type(pop_users[0][0][0]), type(str()))

class partFour(unittest.TestCase):
	def test_popular_users(self):
		self.assertEqual(type(popular_users), type({"hi","sup"}))
	def test_tweet_words(self):
		self.assertEqual(type(tweet_words),type({"hi","Bye"}))
	def test_most_common(self):
		self.assertEqual(type(most_common), type([]))
	def test_most_common_type(self):
		self.assertEqual(type(most_common[0]), type(""))
	def test_most_common_len(self):
		self.assertEqual(len(most_common), 3)
	def test_twitter_actor(self):
		self.assertEqual(type(twitter_actor), type({"hey":"sup"}))
	def test_hashtag(self):
		self.assertEqual(type(hashtag_set[0]), type({"hey", "sup"}))
	def test_hashtag2(self):
		self.assertEqual(hashtag_set[0][0][0], "#")

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)
if __name__ == "__main__":
	unittest.main(verbosity=2)

