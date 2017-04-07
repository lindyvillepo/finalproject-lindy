## Your name: Lindy Villeponteau
## The option you've chosen: Option 2

# Put import statements you expect to need here!
import unittest
import tweepy
import requests
import twitter_info
import json
import sqlite3
import itertools
import collections

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

CACHE_NAME = "SI206_finalproj_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_NAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


# Write your test cases here.
class myTests(unittest.TestCase):
	def test_search_term(self):
		self.assertEqual(type(search_term), type([]), "testing search_term function is type list")
	def test_movie_data(self):
		self.assertEqual(type(movie_data), type({}), "testing movie_data function is type dictionary")
	def test_movie_actors(self):
		shes_the_man = {"She's the Man": ["Andy Fickman", 6.4, ["Amanda Bynes", "Channing Tatum", "Laura Ramsey", "Vinny Jones"], 1]}
		movie = Movie(shes_the_man)
		self.assertEqual(type(movie.actors), type([]), "testing movie.actors is type list")
	def test_movie_rating(self):
		shes_the_man = {"She's the Man": ["Andy Fickman", 6.4, ["Amanda Bynes", "Channing Tatum", "Laura Ramsey", "Vinny Jones"], 1]}
		movie = Movie(shes_the_man)
		self.assertEqual(movie.rating, 6.4, "testing movie.rating is 6.4")
	def test_database(self):
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result)>=3, "Testing there are at least 3 records in the Tweets database")
		conn.close()
	def test_movie_list(self):
		self.assertEqual(type(screen_names),type([]),"Testing that movie_list is a list")
	def test_movie_list2(self):
		self.assertEqual(type(movie_list[1]),type(""),"Testing that an element in movie_list is a string")
	def test_tweet_director(self):
		self.assertEqual(type(tweet_director[0]),type(("hi","bye")),"Testing that an element in the joined query tweet_director is a tuple")
	def test_tweet_movie(self):
		self.assertEqual(type(tweet_movie[0]), type({}), "Testing that an element in tweet_movie is a dictionary")
		self.assertEqual(type(tweet_movie[0][0]), type(""), "Testing that the first key in an element of tweet_movie is a string")


## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)