# Imports

import praw
import os
import sys
from dotenv import dotenv_values
from datetime import date
from urllib import request # For downloading.

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
        if not submission.over_18:
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
            else:
                print(f"Will not, and can't (because I don't want to), download submission {i}")
                # add 1 to i
                i += 1
            print(f"Downloaded {i} of {arg2}")
        else:
            nsfwDownload()
    print("Removing abnormalities.")
    # Remove any abnormalities.
    for file in os.listdir(arg3):
        # Check against:
        # mp4, png, jpg, and gif...
        # (tested at 7:40 on 3/15/2021, it removed gifs...)
        if "mp4" in file or "png" in file or "jpg" in file or "gif" in file: # The ugliest code i have done in
            # this entire project
            continue
        else:
            print(f"Removed {file}, since it had no extension")
            # delete that file
            os.remove(f"{arg3}/{file}")
    if file > arg3:
        print("ok whatttttt")

# nsfwDownload downloads nsfw. what did you expect?
# probably broken.
# TODO: refactor this later
def nsfwDownload():
    j = 1 # :)
    for submission in takeit.subreddit(arg1).hot(limit=int(arg2)):
        if "i.imgur" in submission.url: # why is imgur so wack? why couldn't they do i.img.ur,
            # like reddit does, it just makes no sensee. anyways, 20 bytes.
            request.urlretrieve(submission.url, f"{arg3}/{submission.url[20:]}")
        else:
            print(f"{submission.url} with size of {len(submission.url)}")
# Main clause
if __name__ == "__main__":
    download()
