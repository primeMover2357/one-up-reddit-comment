import praw
import clipboard
import webbrowser
import os

def comment_karma(comment):
    return comment.ups - comment.downs

reddit = praw.Reddit(user_agent="Descending Increase",
                     client_id="d5n8CMZMGx52yQ",
                     client_secret="l54jhktdoxXFWNfOVM8FY2AnolI")


filename = "reddit_comments.html"

page_url = clipboard.paste()
print(f"Pasted URL: '{page_url}'")  # with quotes to see whitespace


try:
    submission = reddit.submission(url=page_url)
    print("Submission found:", submission.title)
except Exception as e:
    print("Failed to load submission:", e)


submission.comments.replace_more(limit=0)


all_comments = submission.comments.list()


filename = "reddit_comments.html"


with open(filename, "w", encoding="utf-8") as f:
    f.write("<html><body style='font-family: sans-serif;'>")
    for comment in all_comments:
        if comment.is_root == False:
            parent = comment.parent()
            if (comment_karma(comment) > comment_karma(parent)) and (comment_karma(parent) > 0):
                ratio = comment_karma(comment) / comment_karma(parent)           
            # print(comment_karma(parent), '----->', comment_karma(comment), '||||||||',  parent.fullname, '----->' , comment.fullname, 'RATIO: ', ratio)
            # print(parent.body)
            # print("Permalink: https://www.reddit.com" + parent.permalink)
                link = "https://www.reddit.com" + parent.permalink
                f.write(f"<p><b>Comment:</b><br>{parent.body}<br>")
                f.write(f'<a href="{link}">Permalink</a><br>')
                f.write(f'<p><b>(r = {ratio:.2f}, comment = {comment_karma(parent)}, reply = {comment_karma(comment)})</b></p>')
                f.write(f"<p><b>Reply:</b><br>{comment.body}</p><hr>")
    f.write("<hr><p>Finished searching</p></body></html>")

webbrowser.open('file://' + os.path.abspath(filename))
