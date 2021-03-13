import praw
from dotenv import dotenv_values
from datetime import date
import sys

today = date.today()

# load config file
config = dotenv_values("./.env")
# get the client id and the token
token = config['REDDIT_SECRET']
Id    = config['REDDIT_ID']

# setup user arguments
# (reason why i have sys imported)
arg1 = str(sys.argv[1]) # 0 is the python script itself
# 1 will be the subreddit
arg2 = str(sys.argv[2]) # 2 will be how many submissions needed.
arg3 = str(sys.argv[3]) # 3 will be the folder to download the images,
# gifs or videos to.

# Create the instance
takeit = praw.Reddit(
    client_id=Id,
    client_secret=token,
    user_agent="takeit by /u/abcado"
)
print(f"Created REDDIT instance at {today.strftime('%m/%d, %Y')}")
