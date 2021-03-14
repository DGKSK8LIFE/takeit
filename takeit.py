import praw
from dotenv import dotenv_values
from datetime import date
from urllib import request # For downloading.
import sys

today = date.today()

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

# Create the instance
takeit = praw.Reddit(
    client_id=Id,
    client_secret=token,
    user_agent="takeit by /u/abcado"
)

# Print out the full arguments
for k in range(len(sys.argv)):
    print(f"Argument {k}: {sys.argv[k]}")

print(f"Created REDDIT instance at {today.strftime('%m/%d, %Y')}")

# Use I for iterations, see below
i = 0

isNsfwEnabled = False # just default, because...
# Start doing the submission downloading
while True:
    for submission in takeit.subreddit(str(arg1)).hot(limit=int(arg2 + 1)):
        if submission.over_18:
            if isNsfwEnabled == True:
                request.urlretrieve(submission.url, arg3)      
                i += 1
            else:
                nsfwCheck = input("Do you want to enable nsfw for this session? (y/N) ")
                if nsfwCheck == 'y':
                    isNsfwEnabled = True
                else:
                    # Do NOT download the image.
                    print(f"Not downloading image {i} of {arg2}")
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
    if i == arg2 + 1:
        break
    else:
        continue
