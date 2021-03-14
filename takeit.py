#
# Imports
#

import praw
from dotenv import dotenv_values
from datetime import date
from urllib import request # For downloading.
import sys

#
# Variables
#

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

#
# Functions
#

# Some variables that are used in the download() function
i = 0 # essentially iterator (used to track how many files are downloaded)
isNsfwEnabled = False # whether NSFW imagery is allowed to be downloaded or not 
# for the current session.

# download is a function that does not take any arguments, and downloads
# images from the user's arguments supplied when executied.
def download():
    isNsfwEnabled = False
    i = 0
    for submission in takeit.subreddit(str(arg1)).hot(limit=int(arg2 + 1)):
        if submission.over_18:
            if isNsfwEnabled == True:
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")      
                i += 1
            else:
                nsfwCheck = input("Do you want to enable nsfw for this session? (y/N) ")
                if nsfwCheck == 'y':
                    isNsfwEnabled = True
                else:
                    # Do NOT download the image.
                    print(f"Not downloading image {i} of {arg2}")
                    i += 1 # so it doesn't say 0 of 100 after you say N 100 times.
        else:
            # Just normally download the image...
            # but we check for if it's a gif or
            # an image
            if "i.redd.it" in submission.url:
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")
                # Check if it has a gif, and print something:
                if "gif" in submission.url:
                    print(f"Downloaded gif. {i} of {arg2}")
                    i += 1
                else:
                    print(f"Downloaded image. {i} of {arg2}")
                    # Check if it's NOT a gif (e.g. jpg or png or webp) and print something.
                    i += 1
            elif "v.redd.it" in submission.url:
                # Also download it. I just have this in a different clause
                # because i feel that I should be able to print out different
                # messages for different things (gifs, videos, images)
                request.urlretrieve(submission.url, f"{arg3}/{submission.url[18:]}")
                print(f"Downloaded video {i} of {arg2}")
                i += 1
            else:
                # Not download it at all, because it may be a gallery or a text post
                print(f"Not downloading {i}/{arg2}")
                i += 1
    # Tell the user that we've finished downloading.
    print(f"Finished downloading {i - 1} submissions into directory {arg3}")

#
# Main "function"
#
if __name__ == "__main__":
    download()
