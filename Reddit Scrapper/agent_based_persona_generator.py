import os
import praw
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Replace with your Reddit API credentials
CLIENT_ID = "pMXakbbG5BIPBDy6tbemDQ"
CLIENT_SECRET = "ZsaqtBceBpXrGWNJBKgw_yevxBXFTg"
USER_AGENT = "Repulsive-Gap1482"

# Replace with your Google Gemini API key
GOOGLE_API_KEY = "AIzaSyCHYjTzacegc3SpOpa8zOf5bEfQH3VKilc"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Replace with the subreddit you want to analyze
SUBREDDIT_NAME = "AskIndianWomen"

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

def get_subreddit_comments(reddit, subreddit_name, limit=100):
    """
    Returns comments from a subreddit.
    """
    try:
        subreddit = reddit.subreddit(subreddit_name)
        comments = subreddit.comments(limit=limit)
        comment_list = []
        for comment in comments:
            comment_data = {
                "id": comment.id,
                "body": comment.body,
                "author": comment.author.name if comment.author else None,
                "score": comment.score,
                "created_utc": comment.created_utc,
            }
            comment_list.append(comment_data)
        return comment_list
    except Exception as e:
        print(f"Error getting comments from {subreddit_name}: {e}")
        return None

def analyze_subreddit_sentiment(comments):
    """
    Analyzes the sentiment of a subreddit based on comments.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    prompt = """You are an expert in sentiment analysis. Analyze the following comments and determine the overall sentiment of the subreddit.
    Comments:
    {comments}
    Overall Sentiment:"""
    prompt_template = ChatPromptTemplate.from_template(prompt)
    chain = prompt_template | model | StrOutputParser()
    sentiment = chain.invoke({"comments": comments})
    return sentiment

def create_persona_map(comments):
    """
    Creates a persona map based on comments from a subreddit.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    prompt = """You are an expert in creating persona maps. Analyze the following comments and create a persona map that can be created from that subreddit.
    Comments:
    {comments}
    Persona Map:"""
    prompt_template = ChatPromptTemplate.from_template(prompt)
    chain = prompt_template | model | StrOutputParser()
    persona_map = chain.invoke({"comments": comments})
    return persona_map

if __name__ == '__main__':
    reddit = get_reddit_instance(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    if reddit:
        comments = get_subreddit_comments(reddit, SUBREDDIT_NAME)
        if comments:
            # Agent 1: Analyze subreddit sentiment
            subreddit_sentiment = analyze_subreddit_sentiment(comments)
            print(f"Subreddit Sentiment: {subreddit_sentiment}")

            # Agent 2: Create persona map
            persona_map = create_persona_map(comments)
            print(f"Persona Map: {persona_map}")

            # Combined output
            print(f"Combined Output: Subreddit Sentiment: {subreddit_sentiment}, Persona Map: {persona_map}")
        else:
            print(f"Could not retrieve comments from {SUBREDDIT_NAME}")
    else:
        print("Could not connect to Reddit API")
