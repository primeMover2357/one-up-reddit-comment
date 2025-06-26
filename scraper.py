import praw
from desinc import comment_karma
import clipboard


reddit = praw.Reddit(user_agent="Descending Increase",
                     client_id="d5n8CMZMGx52yQ",
                     client_secret="l54jhktdoxXFWNfOVM8FY2AnolI")

page_url = clipboard.paste()
print(f"Pasted URL: '{page_url}'")  # with quotes to see whitespace


try:
    submission = reddit.submission(url=page_url)
    print("Submission found:", submission.title)
except Exception as e:
    print("Failed to load submission:", e)


submission.comments.replace_more(limit=0)


all_comments = submission.comments.list()


for comment in all_comments:
    if comment.is_root == False:
        parent = comment.parent()
        if comment_karma(comment) > comment_karma(parent):
          percent_change = (comment_karma(comment) - comment_karma(parent)) / comment_karma(parent)           
          print(comment_karma(parent), '----->', comment_karma(comment), '||||||||',  parent.fullname, '----->' , comment.fullname, 'RATIO: ', percent_change)
          print(parent.body)
          print("Permalink: https://www.reddit.com" + parent.permalink)
          print(90 * '-')
          print(comment.body)
          print(90 * '*')
          print(90 * '*')

print('Finished searching')

