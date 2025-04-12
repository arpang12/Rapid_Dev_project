import uuid
import data_gathering

def generate_persona(user_data, user_comments, user_submissions):
    """
    Generates a persona based on user data, comments, and submissions.
    """
    persona = {
        "username": user_data["username"],
        "id": user_data["id"],
        "comment_karma": user_data["comment_karma"],
        "link_karma": user_data["link_karma"],
        "created_utc": user_data["created_utc"],
        "is_gold": user_data["is_gold"],
        "is_mod": user_data["is_mod"],
        "has_verified_email": user_data["has_verified_email"],
        "comments": user_comments,
        "submissions": user_submissions,
    }
    return persona

def format_persona(persona):
    """
    Formats the persona for output.
    """
    formatted_persona = f"""
Username: {persona["username"]}
ID: {persona["id"]}
Comment Karma: {persona["comment_karma"]}
Link Karma: {persona["link_karma"]}
Created UTC: {persona["created_utc"]}
Is Gold: {persona["is_gold"]}
Is Mod: {persona["is_mod"]}
Has Verified Email: {persona["has_verified_email"]}

Comments:
{chr(10).join([f'{comment["subreddit"]}: {comment["body"]}' for comment in persona["comments"]])}

Submissions:
{chr(10).join([f'{submission["subreddit"]}: {submission["title"]}' for submission in persona["submissions"]])}
"""
    return formatted_persona

    if __name__ == '__main__':
        # Replace with your Reddit API credentials
        CLIENT_ID = "pMXakbbG5BIPBDy6tbemDQ"
        CLIENT_SECRET = "ZsaqtBceBpXrGWNJBKgw_yevxBXFTg"
        USER_AGENT = "Repulsive-Gap1482"

    # Replace with the username you want to get data for
    USERNAME = "spez"

    reddit = data_gathering.get_reddit_instance(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    if reddit:
        user_data = data_gathering.get_user_data(reddit, USERNAME)
        if user_data:
            user_comments = data_gathering.get_user_comments(reddit, USERNAME)
            user_submissions = data_gathering.get_user_submissions(reddit, USERNAME)
            persona = generate_persona(user_data, user_comments, user_submissions)
            formatted_persona = format_persona(persona)
            print(formatted_persona)

            # Output to file
            with open(f"{USERNAME}_persona.txt", "w") as f:
                f.write(formatted_persona)

        else:
            print(f"Could not retrieve user data for {USERNAME}")
    else:
        print("Could not connect to Reddit API")
