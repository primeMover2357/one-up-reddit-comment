import praw
import webbrowser
import os
import sqlite3
import argparse

def comment_karma(comment):
    return comment.ups - comment.downs

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Analyze Reddit comment chains with high reply-to-parent karma ratio.")
parser.add_argument('--url', required=True, help='Reddit post URL')
parser.add_argument('--db', default='reddit_comments.db', help='SQLite database filename')
parser.add_argument('--out', default='reddit_comments.html', help='HTML output filename')
args = parser.parse_args()

page_url = args.url.strip()
db_filename = args.db
filename = args.out

# Initialize Reddit API
reddit = praw.Reddit(user_agent="Descending Increase",
                     client_id="d5n8CMZMGx52yQ",
                     client_secret="l54jhktdoxXFWNfOVM8FY2AnolI")

# Load submission
try:
    submission = reddit.submission(url=page_url)
    print("Submission found:", submission.title)
except Exception as e:
    print("Failed to load submission:", e)
    exit()

submission.comments.replace_more(limit=0)
all_comments = submission.comments.list()

# Set up SQLite
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS high_ratio_comments (
    submission_id TEXT,
    parent_id TEXT,
    reply_id TEXT PRIMARY KEY,
    parent_body TEXT,
    reply_body TEXT,
    parent_karma INTEGER,
    reply_karma INTEGER,
    ratio REAL,
    permalink TEXT
)
''')

# HTML output
with open(filename, "w", encoding="utf-8") as f:
    f.write("<html><body style='font-family: sans-serif;'>")

    for comment in all_comments:
        if not comment.is_root:
            try:
                parent = comment.parent()
                pk = comment_karma(parent)
                ck = comment_karma(comment)

                if ck > pk and pk > 0:
                    ratio = ck / pk
                    link = "https://www.reddit.com" + parent.permalink

                    # Save to DB
                    cursor.execute('''
                        INSERT INTO high_ratio_comments (
                            submission_id, parent_id, reply_id,
                            parent_body, reply_body,
                            parent_karma, reply_karma,
                            ratio, permalink
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        submission.id, parent.id, comment.id,
                        parent.body, comment.body,
                        pk, ck, ratio, link
                    ))

                    # Write to HTML
                    f.write(f"<p><b>Comment:</b><br>{parent.body}<br>")
                    f.write(f'<a href="{link}">Permalink</a><br>')
                    f.write(f'<p><b>(r = {ratio:.2f}, comment = {pk}, reply = {ck})</b></p>')
                    f.write(f"<p><b>Reply:</b><br>{comment.body}</p><hr>")
            except Exception as e:
                print("Error processing a comment pair:", e)

    f.write("<hr><p>Finished searching</p></body></html>")

# Finalize DB
conn.commit()
conn.close()

# Open the HTML in a browser
webbrowser.open('file://' + os.path.abspath(filename))
