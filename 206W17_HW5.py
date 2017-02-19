import unittest
import tweepy
import requests
import json
import twitter_info
import codecs

## SI 206 - W17 - HW5
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment: Jon Bain

######## 500 points total ########

## Write code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function), and prints out the Tweet text and the created_at value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm an awesome Python programmer.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017

## .. plus one more.

## You should cache all of the data from this exercise in a file, and submit the cache file along with your assignment. 

## So, for example, if you submit your assignment files, and you have already searched for tweets about "rock climbing", when we run your code, the code should use CACHED data, and should not need to make any new request to the Twitter API. 
## But if, for instance, you have never searched for "bicycles" before you submitted your final files, then if we enter "bicycles" when we run your code, it _should_ make a request to the Twitter API.

## The lecture notes and exercises from this week will be very helpful for this. 
## Because it is dependent on user input, there are no unit tests for this -- we will run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

## **** For 50 points of extra credit, create another file called twitter_info.py that contains your consumer_key, consumer_secret, access_token, and access_token_secret, import that file here, and use the process we discuss in class to make that information secure! Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information for an 'extra' Twitter account you make just for this class, and not your personal account, because it's not ideal to share your authentication information for a real account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these with variables rather than filling in the empty strings if you choose to do the secure way for 50 EC points

## CODE WRITTEN BELOW

# Info neccessary to access twitter
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) 

# Name of cache file to ease searching, attempt to open it if it exists
CACHE_FNAME = "cached_data_hw5.txt"
try:
	cache_file = open(CACHE_FNAME,'r', encoding = 'utf-8')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

# Function to search twitter for tweets with a given search term
def get_tweets_keyword(search_term):
	unique_identifier = "twitter_{}".format(search_term)
	# Checks if the search term already exists in the cache
	if unique_identifier in CACHE_DICTION:
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		twitter_results = api.search(search_term)
		twitter_results = twitter_results["statuses"]
		twitter_results = twitter_results
		CACHE_DICTION[unique_identifier] = twitter_results 
		# Since keyword did not exist, need to write results to cache
		f = open(CACHE_FNAME,'w', encoding = 'utf-8') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	# Now takes results from if-else statement, stores tweets in tweet_texts to return for printing
	tweet_texts = []
	for tweet in twitter_results:
		tweet_texts.append(tweet)
	return tweet_texts[:3]

# Collects user input
user_input_term = input("Input phrase: ")
three_tweets = {}
three_tweets = get_tweets_keyword(user_input_term)
# Loops through tweets
for t in three_tweets:
	print('\n')
	string_to_print = t["text"].encode('utf-8')
	# If possible, decodes string to print, else just prints with utf-8 encoding
	print("Text: ", end = '')
	try:
		print(string_to_print.decode('utf-8'))
	except:
		print(string_to_print)
	print("CREATED AT: ", t["created_at"])