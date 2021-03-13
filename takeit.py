import praw
from dotenv import python-dotenv
import sys

# load config file
config = dotenv_values("./.env")
# get the client id and the token
token = config['REDDIT_SECRET']
Id    = config['REDDIT_ID']
