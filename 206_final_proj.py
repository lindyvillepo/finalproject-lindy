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
		twitter_results = api.search(q=user_input, count=10, lang="en", result_type="mixed")
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

	def list_of_tweet_tuples(self, tweet_diction, actor):
		tweet_list = []
		for tweet in tweet_diction["statuses"]:
			user_id = tweet["id"]
			text = tweet["text"]
			favs = tweet["favorite_count"]
			retweets = tweet["retweet_count"]
			post = tweet["user"]["screen_name"]
			search = actor
			tweet_list.append((user_id, text, favs, retweets, post, search))
		return tweet_list

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

	def __str__(self):
		return "Searching tweets about {} with tweets like {}.\n".format(self.search, self.text[0])

# Write a tweetUser class that takes in a dictionary representing a tweet. The constructor should have information regarding each of the users in the "neighborhood", which is generally defined by tweet posters, all the users mentioned, all the users who have favorited/liked a tweet. Some people also define it with e.g. everyone who has RT'd the tweet as well. For each user, the constructor should initialize the user id, screen name, number of favorites ever favorited, and user description.
class TweetUser(object):
	def __init__(self, tweet_diction):
		self.idstr = self.user(tweet_diction)
		self.screen_name = self.user_name(tweet_diction)
		self.num_favs = self.favs_ever(tweet_diction)
		self.description = self.user_description(tweet_diction)

	def list_of_user_tuple(self, tweet_diction):
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

	def user(self, tweet_diction):
		user_list = []
		for tweet in tweet_diction["statuses"]:
			user_list.append(tweet["user"]["id_str"])
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["screen_name"])
				user_list.append(info["id_str"])
		return user_list

	def user_name(self, tweet_diction):
		name_list = []
		for tweet in tweet_diction["statuses"]:
			name_list.append(tweet["user"]["screen_name"])
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["screen_name"])
				name_list.append(info["screen_name"])
		return name_list

	def favs_ever(self, tweet_diction):
		favs_list = []
		for tweet in tweet_diction["statuses"]:
			favs_list.append(tweet["user"]["favourites_count"])
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["screen_name"])
				favs_list.append(info["favourites_count"])
		return favs_list

	def user_description(self, tweet_diction):
		description_list = []
		for tweet in tweet_diction["statuses"]:
			description_list.append(tweet["user"]["description"])
			for user in tweet["entities"]["user_mentions"]:
				info = api.get_user(id=user["screen_name"])
				description_list.append(info["description"])
		return description_list

	def __str__(self):
		return "User {} has made {} favorites ever.\n".format(self.screen_name[0], self.num_favs[0])

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

# Iterate through movie_instance to get the twitter diction of the second top-paid actor. Then get an instance of that tweet and the users and append it in the list "twitter_list" and "user_list". 
twitter_list = []
user_list = []
for movie in movie_instance:
	actor = movie.actors[1]
	tweet_diction = get_tweets(actor)
	tweet = Tweet(tweet_diction, actor)
	twitter_list.append(tweet.list_of_tweet_tuples(tweet_diction, actor))
	user = TweetUser(tweet_diction)
	user_list.append(user.list_of_user_tuple(tweet_diction))

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
movie_table += 'Movies (movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, languages INTEGER, imbd_rating DECIMAL, actor TEXT)'
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
# The user, and all of the data about users that are mentioned in the movie search's timeline. 

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
# Info about all the tweets that is from the movie search's timeline.

lol = []
kms = []
wtf = []
fml = []
smd = []
fuck = []
for search in twitter_list:
	for tweet in search:
		lol.append(tweet[0])
		kms.append(tweet[1])
		wtf.append(tweet[2])
		fml.append(tweet[3])
		smd.append(tweet[4])
		fuck.append(tweet[5])

print(len(lol), len(kms), len(wtf), len(fml), len(smd), len(fuck))

# tweet_id = []
# text = []
# favorites = []
# retweets = []
# posts = []
# search = []
# for search in twitter_list:
# 	for tweet in search:
# 		tweet_id.append(tweet[0])
# 		text.append(tweet[1])
# 		favorites.append(tweet[2])
# 		retweets.append(tweet[3])
# 		print(type(tweet[4]))
# 		print(tweet[4])

		#posts.append(tweet[4])

tweet_info = zip(lol, kms, wtf, fml, smd, fuck)

statement = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_info:
	cur.execute(statement, tweet)

conn.commit()

## Part 3 - Making queries

# Make a query to select all of the tweet texts from the database. Save a resulting list of strings in the variable tweet_texts.
# query = "SELECT tweet_text FROM Tweets"
# cur.execute(query1)
# tuple_texts = cur.fetchall()
# tweet_texts = [x[0] for x in tuple_texts]

# Make a query using an INNER JOIN to get a list of tuples with 2 elements in each tuple: the user screenname and the text of the tweet -- for each tweet that has been retweeted more than 50 times. Save the resulting list of tuples in a variable called user_description.
# query1 = "SELECT Tweets.tweet_id, Users.description FROM Tweets INNER JOIN Users on Tweets.user_id = Users.user_id"
# cur.execute(query1)
# user_description = cur.fetchall()

# Select all of the TEXT values of the tweets that are retweets of another account (i.e. have "RT" at the beginning of the tweet text). Save the tuples in a variable called tuple_rt.
# query2 = "SELECT tweet_text FROM Tweets WHERE instr(tweet_text, 'RT')"
# cur.execute(query2)
# tuple_rt = cur.fetchall()

## Part 4 - Manipulating data

# Use a set comprehension to get a set of all words among the texts in the tweet_texts list. Save the resulting set in a variable called tweet_words.
# word_list = []
# for line in tweet_texts:
#  	words = line.split()
#  	for word in words:
#  		word_list.append(word)

# tweet_words = {word for word in word_list}

# Use a Counter in the collections library to find the most common word among all of the texts in the tweet_texts list. Save that most common word in a variable called most_common. 
#below is for common character
# word_string = " ".join(word for word in word_list)
# word_string = word_string.replace(" ", "")
# most_common_char = collections.Counter(word_string).most_common(1)[0]
# most_common_char = most_common_char[0]

# Write code to create a dictionary whose keys are Twitter tweet id's and whose associated values are lists of tweet texts that that user posted. You should save the final dictionary in a variable called twitter_info.
# twitter_default = collections.defaultdict(list)

# for key, value in user_description:
# 	twitter_default[key].append(value)

# twitter_info = dict(twitter_default)

## Make sure to close database!!!
# conn.close()

# Define a function get_twitter_hashtags that accepts a string as in put and returns a set of the hashtags of each hashtag that was mentioned in the tweet string. Then iterate through tweet_texts to find all the hashtags in the texts and append it to a list called hashtag_set.
# def get_twitter_hashtags(user_input):
# 	phrase = r"\@[A-Za-z0-9]+\_*[A-Za-z0-9_]*"
# 	hashtags = re.findall(phrase, user_input)
# 	results = []
# 	for tags in hashtags:
# 		results.append(tags[1:])
# 	return set(results)

# hashtag_set = []
# for tweet in tweet_texts:
# 	hashtag_set.append(get_twitter_hashtags(tweet))

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

