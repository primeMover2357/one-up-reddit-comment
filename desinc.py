import praw

reddit = praw.Reddit(user_agent="Descending Increase",
					 client_id="d5n8CMZMGx52yQ",
					 client_secret="l54jhktdoxXFWNfOVM8FY2AnolI")

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

