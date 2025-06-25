import praw
from dotenv import load_dotenv
import os


load_dotenv()  # Load variables from .env into environment


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)


def rfunction(submission_id):

    submission = reddit.submission(id=submission_id)
    submission.comments.replace_more(limit=0)
    parent = submission.comments
    karma = comment_karma(parent[0])

    for comment in parent[0].replies:
        if comment_karma(comment) > karma:
            print(parent[0].body)
            print(40 * '-')
            print(comment.body)
            print('\nIn ratio ', karma, '-->', comment_karma(comment), '/')
    else:
        print('Nothing to see here')



def comment_karma(comment):
    return comment.ups - comment.downs

