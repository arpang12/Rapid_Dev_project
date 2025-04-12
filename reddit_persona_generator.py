import praw
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

CLIENT_ID = "pMXakbbG5BIPBDy6tbemDQ"
CLIENT_SECRET = "ZsaqtBceBpXrGWNJBKgw_yevxBXFTg"
USER_AGENT = "Repulsive-Gap1482"
SUBREDDIT_NAME = "AskIndianWomen"

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
subreddit = reddit.subreddit(SUBREDDIT_NAME)
comments_by_user = {}

# Collect comments
for comment in subreddit.comments(limit=1000):
    user = comment.author.name if comment.author else "deleted"
    if user != "deleted":
        if user not in comments_by_user:
            comments_by_user[user] = []
        comments_by_user[user].append(comment.body)

# Preprocess comments
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return " ".join(tokens)

user_documents = {user: " ".join(preprocess_text(c) for c in comments) for user, comments in comments_by_user.items()}

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Prepare documents
users = list(user_documents.keys())
docs = list(user_documents.values())

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.95)
tfidf_matrix = vectorizer.fit_transform(docs)

# Convert to DataFrame for easier handling
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=users, columns=vectorizer.get_feature_names_out())

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Elbow method to choose k
inertias = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(tfidf_matrix)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.plot(k_range, inertias, "bx-")
plt.xlabel("k")
plt.ylabel("Inertia")
plt.title("Elbow Method for Optimal k")
plt.show()

# Assume k=5 from elbow method
kmeans = KMeans(n_clusters=5, random_state=42)
clusters = kmeans.fit_predict(tfidf_matrix)

# Map users to clusters
user_clusters = pd.Series(clusters, index=users)

from agno.agent import Agent
import numpy as np
import json

# Initialize Agno agent
persona_agent = Agent(
    name="RedditPersonaCreator",
    model="""
    # TODO: Replace with Mistral model integration
    # Example: model=MistralChat(model="mistral-medium")
    """,
    instructions="""
You are a Reddit persona creator. Given a cluster of commenters summarized by:
- Top keywords (representing interests or style)
- Average metadata (e.g., karma, comment frequency)
Create a realistic Reddit persona with:
- Username
- Bio
- Subreddits (based on keywords)
- Posting style
- Estimated karma
- Account age
Output as JSON.
"""
)

# Generate personas for each cluster
personas = []
for cluster_id in range(5):
    # Get users in this cluster
    cluster_users = user_clusters[user_clusters == cluster_id].index
    if not cluster_users.empty:
        # Get TF-IDF centroid
        cluster_indices = user_clusters[user_clusters == cluster_id].index
        cluster_tfidf = tfidf_matrix[cluster_indices].mean(axis=0)
        top_terms_idx = np.argsort(cluster_tfidf.A1)[-10:]  # Top 10 terms
        top_terms = [vectorizer.get_feature_names_out()[i] for i in top_terms_idx]
        
        # Mock metadata (replace with real data if available)
        metadata = {
            "avg_karma": 1000,  # Example
            "avg_comments_per_day": 2.5
        }
        
        # Prepare input for Agno
        cluster_summary = {
            "top_keywords": top_terms,
            "metadata": metadata
        }
        
        # Generate persona
        response = persona_agent.run(json.dumps(cluster_summary))
        try:
            persona = json.loads(response)
            persona["cluster_id"] = cluster_id
            personas.append(persona)
        except json.JSONDecodeError:
            print(f"Error parsing persona for cluster {cluster_id}")

# Print personas
for persona in personas:
    print(json.dumps(persona, indent=2))