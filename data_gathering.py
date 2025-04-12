import praw
import uuid

def get_reddit_instance(client_id, client_secret, user_agent):
    """
    Returns a Reddit instance.
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return reddit

def get_user_data(reddit, username):
    """
    Returns user data from Reddit.
    """
    try:
        user = reddit.redditor(username)
        user.id
    except Exception as e:
        print(f"Error getting user data for {username}: {e}")
        return None

    user_data = {
        "username": user.name,
        "id": user.id,
        "comment_karma": user.comment_karma,
        "link_karma": user.link_karma,
        "created_utc": user.created_utc,
        "is_gold": user.is_gold,
        "is_mod": user.is_mod,
        "has_verified_email": user.has_verified_email,
    }
    return user_data

def get_user_comments(reddit, username, limit=100):
    """
    Returns user comments from Reddit.
    """
    try:
        user = reddit.redditor(username)
        comments = user.comments.new(limit=limit)
        comment_list = []
        for comment in comments:
            comment_data = {
                "id": comment.id,
                "body": comment.body,
                "subreddit": comment.subreddit.display_name,
                "score": comment.score,
                "created_utc": comment.created_utc,
            }
            comment_list.append(comment_data)
        return comment_list
    except Exception as e:
        print(f"Error getting user comments for {username}: {e}")
        return None

def get_user_submissions(reddit, username, limit=100):
    """
    Returns user submissions from Reddit.
    """
    try:
        user = reddit.redditor(username)
        submissions = user.submissions.new(limit=limit)
        submission_list = []
        for submission in submissions:
            submission_data = {
                "id": submission.id,
                "title": submission.title,
                "subreddit": submission.subreddit.display_name,
                "score": submission.score,
                "created_utc": submission.created_utc,
            }
            submission_list.append(submission_data)
        return submission_list
    except Exception as e:
        print(f"Error getting user submissions for {username}: {e}")
        return None

if __name__ == '__main__':
    # Replace with your Reddit API credentials
    CLIENT_ID = "pMXakbbG5BIPBDy6tbemDQ"
    CLIENT_SECRET = "ZsaqtBceBpXrGWNJBKgw_yevxBXFTg"
    USER_AGENT = "Repulsive-Gap1482"

    # Replace with the username you want to get data for
    USERNAME = "spez"

    reddit = get_reddit_instance(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    if reddit:
        user_data = get_user_data(reddit, USERNAME)
        if user_data:
            print(f"User data for {USERNAME}: {user_data}")
        else:
            print(f"Could not retrieve user data for {USERNAME}")

        user_comments = get_user_comments(reddit, USERNAME)
        if user_comments:
            print(f"User comments for {USERNAME}: {user_comments}")
        else:
            print(f"Could not retrieve user comments for {USERNAME}")

        user_submissions = get_user_submissions(reddit, USERNAME)
        if user_submissions:
            print(f"User submissions for {USERNAME}: {user_submissions}")
        else:
            print(f"Could not retrieve user submissions for {USERNAME}")
