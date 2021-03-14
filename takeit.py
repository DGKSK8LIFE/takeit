# Imports

import praw
from dotenv import dotenv_values
from datetime import date
from urllib import request # For downloading.
import sys

# Variables

# load config file
config = dotenv_values("./.env")
# get the client id and the token
token: str = str(config['REDDIT_SECRET'])
Id: str    = str(config['REDDIT_ID'])

# setup user arguments
# (reason why i have sys imported)
arg1 = str(sys.argv[1]) # 0 is the python script itself
# 1 will be the subreddit
arg2 = int(sys.argv[2]) # 2 will be how many submissions needed.
arg3 = str(sys.argv[3]) # 3 will be the folder to download the images,
# gifs or videos to.


takeit = praw.Reddit(
    client_id=Id,
    client_secret=token,
    user_agent="takeit by /u/abcado"
)

print(f"Created REDDIT instance at {date.today().strftime('%m/%d, %Y')}")

# Functions

# download is a function that does not take any arguments, and downloads
# images from the user's arguments supplied when executied.
# this is usually for NON nsfw things...if you want NSFW check nsfwDownload.
def download():
    i = 1
    for submission in takeit.subreddit(arg1).hot(limit=int(arg2)):
        if  submission.over_18:
            # Check if it has the following:
            # imgur, v.redd.it, and i.redd.it, and if does,
            # then we download it to arg3, which is the folder
            if "i.imgur" in submission.url: # 20 bytes in is where the file is
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[20:]}")
                i += 1
            elif "i.redd" in submission.url: # 18 bytes
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")
                i += 1
            elif "v.redd" in submission.url: # 18 bytes (still, reddit is not wacky)
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")
                i += 1
            print(f"Downloaded {i} of {arg2}")
        else:
            nsfwDownload()

# nsfwDownload downloads nsfw. what did you expect?
def nsfwDownload():
    j = 1 # :)
    for submission in takeit.subreddit(arg1).hhot(limit=int(arg2)):
        # basically the same thing as above but less code
        if "i.imgur" in submission.url:
            request.urlretrieve(submission.url, f"{arg3}/{submission.url[20:]}")
            j += 1
        elif "i.redd" in submission.url and "v.redd" in submission.url:
            request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")
            j += 1
        print(f"Downloaded {i} of {arg2}")

# Main clause
if __name__ == "__main__":
    download()
