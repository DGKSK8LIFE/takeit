import praw
from dotenv import python-dotenv
import sys

# load config file
config = dotenv_values("./.env")
# get the client id and the token
token = config['REDDIT_SECRET']
Id    = config['REDDIT_ID']

# setup user arguments
# (reason why i have sys imported)
arg1 = sys.argv[1] # 0 is the python script itself
# 1 will be the subreddit
arg2 = sys.argv[2] # 2 will be how many submissions needed.
arg3 = sys.argv[3] # 3 will be the folder to download the images,
# gifs or videos to.

