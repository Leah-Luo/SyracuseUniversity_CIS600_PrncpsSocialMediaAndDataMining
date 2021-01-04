#!/usr/bin/env python
# coding: utf-8
"""
Course: CIS 600 
Student: Leah Luo
Date: 10/2/2020
"""
import twitter
import json
import sys
import networkx
import matplotlib.pyplot as plot
import time
from functools import partial
from sys import maxsize as maxint

CONSUMER_KEY = 'Your Consumer Key'
CONSUMER_SECRET = 'Your Consumer Secret'
OAUTH_TOKEN = 'Your Oauth Token'
OAUTH_TOKEN_SECRET = 'Your Oauth Token Secret'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# Staring Point
screen_name = 'SyracuseCrunch'

# Use function examples from twitter cookbook Ch9
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
	def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
	
		if wait_period > 3600: # Seconds
			print('Too many retries. Quitting.', file=sys.stderr)
			raise e
		if e.e.code == 401:
			print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
			return None
		elif e.e.code == 404:
			print('Encountered 404 Error (Not Found)', file=sys.stderr)
			return None
		elif e.e.code == 429: 
			print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
			if sleep_when_rate_limited:
				print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
				sys.stderr.flush()
				time.sleep(60*15 + 5)
				print('...ZzZ...Awake now and trying again.', file=sys.stderr)
				return 2
			else:
				raise e # Caller must handle the rate limiting issue
		elif e.e.code in (500, 502, 503, 504):
			print('Encountered {0} Error. Retrying in {1} seconds'\
				  .format(e.e.code, wait_period), file=sys.stderr)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		else:
			raise e
	wait_period = 2 
	error_count = 0 
	while True:
		try:
			return twitter_api_func(*args, **kw)
		except twitter.api.TwitterHTTPError as e:
			error_count = 0 
			wait_period = handle_twitter_http_error(e, wait_period)
			if wait_period is None:
				return
		except URLError as e:
			error_count += 1
			time.sleep(wait_period)
			wait_period *= 1.5
			print("URLError encountered. Continuing.", file=sys.stderr)
			if error_count > max_errors:
				print("Too many consecutive errors...bailing out.", file=sys.stderr)
				raise
		except BadStatusLine as e:
			error_count += 1
			time.sleep(wait_period)
			wait_period *= 1.5
			print("BadStatusLine encountered. Continuing.", file=sys.stderr)
			if error_count > max_errors:
				print("Too many consecutive errors...bailing out.", file=sys.stderr)
				raise


def get_user_profile(twitter_api, screen_names=None, user_ids=None):
	# Must have either screen_name or user_id (logical xor)
	assert (screen_names != None) != (user_ids != None), \
	"Must have screen_names or user_ids, but not both"
	
	items_to_info = {}

	items = screen_names or user_ids
	
	while len(items) > 0:
		items_str = ','.join([str(item) for item in items[:100]])
		items = items[100:]
		if screen_names:
			response = make_twitter_request(twitter_api.users.lookup, 
											screen_name=items_str)
		else: # user_ids
			response = make_twitter_request(twitter_api.users.lookup, 
											user_id=items_str)
		for user_info in response:
			if screen_names:
				items_to_info[user_info['screen_name']] = user_info
			else: # user_ids
				items_to_info[user_info['id']] = user_info
	return items_to_info;


def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
															friends_limit=maxint, followers_limit=maxint):
		
		# Must have either screen_name or user_id (logical xor)
		assert (screen_name != None) != (user_id != None),"Must have screen_name or user_id, but not both"
		
		# See http://bit.ly/2GcjKJP and http://bit.ly/2rFz90N for details
		# on API parameters
		get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, 
															count=5000)
		get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, 
																count=5000)

		friends_ids, followers_ids = [], []
		
		for twitter_api_func, limit, ids, label in [
										[get_friends_ids, friends_limit, friends_ids, "friends"], 
										[get_followers_ids, followers_limit, followers_ids, "followers"]
								]:
				
				if limit == 0: continue
				
				cursor = -1
				while cursor != 0:
						# Use make_twitter_request via the partially bound callable...
						if screen_name: 
								response = twitter_api_func(screen_name=screen_name, cursor=cursor)
						else: # user_id
								response = twitter_api_func(user_id=user_id, cursor=cursor)

						if response is not None:
								ids += response['ids']
								cursor = response['next_cursor']
				
						print('Fetched {0} total {1} ids for {2}'.format(len(ids), label, (user_id or screen_name)),file=sys.stderr)
						# XXX: You may want to store data during each iteration to provide an 
						# an additional layer of protection from exceptional circumstances
						if len(ids) >= limit or response is None:
								break

		# Do something useful with the IDs, like store them to disk...
		return friends_ids[:friends_limit], followers_ids[:followers_limit]
		
		
# My own code 
friends_ids, followers_ids = get_friends_followers_ids(twitter_api, screen_name=screen_name, friends_limit=5000, followers_limit=5000)
# print(friends_ids)
# print(followers_ids)

# Reciprocal friends 
reciprocal_friends = list(set(friends_ids) & set(followers_ids))
# Profiles of reciprocal friends 
response = get_user_profile(twitter_api,user_ids=list(reciprocal_friends))

my_dictionary = {}
for i in reciprocal_friends:
	# Number of followers for each user_id
	follower_count = response[i]["followers_count"]
	my_dictionary[i] = follower_count

# Sort reciprocal friends by follower count 
my_sort_dict = sorted(my_dictionary,key=my_dictionary.get,reverse=True)
# 5 most popular reciprocal friends 
ids = next_queue = list(my_sort_dict[:5])


# Draw the social network graph
G = networkx.Graph()
G.add_node(screen_name)
for i in ids:
	G.add_node(i)
	G.add_edge(screen_name,i)

# Use crawler to get distance-n friends 
while G.number_of_nodes() < 100:
	(queue, next_queue) = (next_queue, []) 
	
	for id in queue: 
		friends_ids, followers_ids = get_friends_followers_ids(twitter_api, user_id=id, friends_limit=5000, followers_limit=5000)
		reciprocal_friends = set(friends_ids) & set(followers_ids)
		response = get_user_profile(twitter_api,user_ids=list(reciprocal_friends))
		
		my_dictionary = {}
		for i in reciprocal_friends:
			if(i not in next_queue and i not in ids):
				# Number of followers for each user_id
				follower_count = response[i]["followers_count"]
				my_dictionary[i] = follower_count
			# User already exist
			else: 
				G.add_edge(id,i)
				continue
				
		# Sort reciprocal friends by follower count 
		my_sort_dict = sorted(my_dictionary,key=my_dictionary.get,reverse=True)
		# 5 most popular reciprocal friends 
		most_popular= list(my_sort_dict[:5])
		
		# Add to social network graph
		for i in most_popular:
			G.add_node(i)
			G.add_edge(id,i)
			
		next_queue += most_popular
		
	ids += next_queue
	
	
	
# Print out results
# Number of nodes 
print("Number of nodes: "+str(G.number_of_nodes()))
# Number of edges 
print("Number of edges: "+str(G.number_of_edges()))
# Diameter of graph 
my_diameter = networkx.diameter(G)
print("Diameter of this graph: " + str(my_diameter))
# Average distance of graph 
my_average = networkx.average_shortest_path_length(G)
print("Average distance of this graph: " + str(my_average))
networkx.draw(G)
plot.show()

# Save result to txt file 
text_file = open("Your_Own_Path", "w")
text_file.write("Number of nodes: " + str(G.number_of_nodes()) + "\n")
text_file.write("Number of edges: " + str(G.number_of_edges()) + "\n")
text_file.write("Diameter of this graph: " + str(my_diameter) + "\n")
text_file.write("Average distance of this graph: " + str(my_average) + "\n")
text_file.close()