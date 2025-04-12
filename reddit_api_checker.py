import praw
from textblob import TextBlob

SUBREDDIT_NAME = "AskIndianWomen"
CLIENT_ID = "pMXakbbG5BIPBDy6tbemDQ"
CLIENT_SECRET = "ZsaqtBceBpXrGWNJBKgw_yevxBXFTg"
USER_AGENT = "Repulsive-Gap1482"

def check_reddit_api():
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
        )

        subreddit = reddit.subreddit(SUBREDDIT_NAME)

        print(f"Subreddit name: {subreddit.display_name}")

        for submission in subreddit.hot(limit=5):
            analysis = TextBlob(submission.title)
            print(f"Title: {submission.title}")
            print(f"Sentiment: {analysis.sentiment.polarity}")

        print("Reddit API is working.")
    except Exception as e:
        print(f"Reddit API is not working. Error: {e}")

if __name__ == "__main__":
    check_reddit_api()
