# Test Url https://www.reddit.com/r/aww/comments/5vj9ut/these_cows_look_like_theyre_about_to_drop_the/
# https://www.reddit.com/r/AskReddit/comments/1lk71pn/people_born_before_2000_what_trivial_skill_you/
import praw
from desinc import comment_karma


reddit = praw.Reddit(user_agent="Descending Increase",
                     client_id="d5n8CMZMGx52yQ",
                     client_secret="l54jhktdoxXFWNfOVM8FY2AnolI")

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

