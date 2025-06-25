# Test Url
# https://www.reddit.com/r/AskReddit/comments/1lk71pn/people_born_before_2000_what_trivial_skill_you/

import praw
from desinc import comment_karma
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env into environment

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


page_url = input('URL ')

submission = reddit.submission(url = page_url)
submission.comments.replace_more(limit=0)

#top_level_comments = list(submission.comments)
all_comments = submission.comments.list()

for comment in all_comments:
    if comment.is_root == False:
        parent = comment.parent()
        if comment_karma(comment) > comment_karma(parent):
          percent_change = (comment_karma(comment) - comment_karma(parent)) / comment_karma(parent)           
          print(comment_karma(parent), '----->', comment_karma(comment), '||||||||',  parent.fullname, '----->' , comment.fullname, 'RATIO: ', percent_change)
          print(parent.body)
          print(90 * '-')
          print(comment.body)
          print(90 * '*')
          print(90 * '*')

print('Finished searching')

