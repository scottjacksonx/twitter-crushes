#!/usr/bin/env python
"""
twitter-crushes.py
Author: Scott Jackson

Goes through your favourite twitters on Twitter and sorts them by who twittered the twitter.

Isn't it great having a word that means the name of the company, the medium, _and_ the content? Not confusing at _all_.
"""


import twitter
import json
import sys
from operator import itemgetter

def printHelp():
	"""
	Prints how the script is meant to be used
	"""
	print "usage: twitter-crushes.py [username] [pages]"
	print "arguments:"
	print "username: the username of the twitter user whose favorites you want to get"
	print "pages: the number of pages of favorites you want to count (20 per page)"
	print ""
	
def graphify(list):
	"""
	Takes a list of tuples and prints them as a pretty graph.
	
	Tuples are of the form (username, numberOfTwitters).
	"""
	names = []
	for item in list:
		names.append(item[0])
	longestName = max(names, key=len)
	maxLength = len(longestName)
	
	# Pad out all names to be the length of longestName
	formattedTuples = []
	for item in list:
		name = item[0]
		numberOfTwitters = item[1]
		
		while len(name) != maxLength:
			name += " "
		
		bar = ""
		for i in range(0, numberOfTwitters):
			bar += "="
		bar += " (" + str(numberOfTwitters) + ")"
		tuple = (name,bar)
		formattedTuples.append(tuple)
		
	for tuple in formattedTuples:
		print tuple[0] + " |" + tuple[1]
	

def main(argv=None):
	"""
	what happens when the script runs.
	
	Parses cmd-line args, gets favorites, graphs them.
	"""
	# Cmd-line args

	numPages = 2
	user = ""

	if len(argv) == 1:
		printHelp()
		exit()
	elif len(argv) == 2:
		user = argv[1]
	elif len(argv) == 3:
		user = argv[1]
		numPages = int(argv[2]) + 1

	# Get favorites
	
	api = twitter.Api()
	favorites = []
	url = "http://twitter.com/favorites/" + user + ".json?page="
	for i in range(1,numPages):
		newURL = url + str(i)
		data = json.loads(api._FetchUrl(newURL))
		for t in data:
			favorites.append(t)

	crushes = {}

	for f in favorites:
		name = f['user']['screen_name']
		try:
			crushes[name] += 1
		except KeyError:
			crushes[name] = 1

	crushes = sorted(crushes.iteritems(), key=itemgetter(1), reverse=True)

	# Graph the favorites by user.
	print "twitter favorites for: " + user
	graphify(crushes)



if __name__ == "__main__":
    main(sys.argv)	
