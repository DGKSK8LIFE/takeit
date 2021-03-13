import praw
from dotenv import dotenv_values
from datetime import date
from urllib import request # For downloading.
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
arg2 = int(sys.argv[2]) # 2 will be how many submissions needed.
arg3 = str(sys.argv[3]) # 3 will be the folder to download the images,
# gifs or videos to.

# Create the instance
takeit = praw.Reddit(
    client_id=Id,
    client_secret=token,
    user_agent="takeit by /u/abcado"
)

print(f"Created REDDIT instance at {today.strftime('%m/%d, %Y')}")

isNsfwEnabled = False # just default, because...
# Start doing the submission downloading
for i in range(arg2):
    for submission in takeit.subreddit(arg1).hot(limit=arg2):
        if submission.over_18:
            if isNsfwEnabled == True:
                request.urlretrieve(submission.url, arg3)      
            else:
                nsfwCheck = input("Do you want to enable nsfw for this session? (y/N) ")
                if nsfwCheck == 'y':
                    isNsfwEnabled = True
                else:
                    # Do NOT download the image.
                    print(f"Not downloading image {i} of {arg2}")
        else:
            # Just normally download the image...
            request.urlretrieve(submission.url, arg3)


