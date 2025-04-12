import praw

# Set up Reddit API credentials
client_id = 'cfm9tiYM9JRDoNTRVCGnCw'
client_secret = '8rD8KtPOhHxtqznBniS5dTats1-AcQ'
user_agent = 'persona_script'

# Initialize Reddit API
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Define target subreddit
subreddit_name = 'r/AskIndianWomen'
subreddit = reddit.subreddit(subreddit_name)

# Collect comments
# comments = []
# try:
#     for comment in subreddit.comments(limit=100):
#         comments.append({
#             'user': comment.author.name,
#             'text': comment.body,
#             'score': comment.score
#         })
# except Exception as e:
#     print(f"Error collecting comments: {e}")
# comments = []

comments = [
    {'user': 'user1', 'text': 'This is a great comment!', 'score': 5},
    {'user': 'user2', 'text': 'I disagree with that.', 'score': 2},
    {'user': 'user1', 'text': 'Another comment from user1.', 'score': 3},
    {'user': 'user3', 'text': 'This is a neutral comment.', 'score': 1},
    {'user': 'user2', 'text': 'I have mixed feelings about this.', 'score': 4}
]

# if not comments:
#     print("No comments collected. Skipping analysis.")
#     exit()

import spacy
from textblob import TextBlob
from collections import defaultdict, Counter
from sklearn.cluster import KMeans

print("Data collection complete.")

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Process comments
processed_comments = []
for comment in comments:
    doc = nlp(comment['text'])
    processed_comments.append(doc)

# Analyze sentiment
for comment in comments:
    sentiment = TextBlob(comment['text']).sentiment.polarity  # Ranges from -1 to 1
    comment['sentiment'] = sentiment

# Feature extraction
user_metrics = defaultdict(lambda: {'count': 0, 'sentiment_sum': 0, 'score_sum': 0})
for comment in comments:
    user = comment['user']
    user_metrics[user]['count'] += 1
    user_metrics[user]['sentiment_sum'] += comment['sentiment']
    user_metrics[user]['score_sum'] += comment['score']

for user in user_metrics:
    user_metrics[user]['avg_sentiment'] = user_metrics[user]['sentiment_sum'] / user_metrics[user]['count']

# Clustering
features = [[metrics['count'], metrics['avg_sentiment'], metrics['score_sum']]
            for metrics in user_metrics.values()]
kmeans = KMeans(n_clusters=3, n_init='auto')  # Adjust number of clusters as needed
clusters = kmeans.fit_predict(features)

# Assign cluster labels to users
for i, user in enumerate(user_metrics.keys()):
    user_metrics[user]['cluster'] = clusters[i]

# Persona generation
personas = {}
for cluster_id in set(clusters):
    cluster_users = [user for user, metrics in user_metrics.items()
                     if metrics['cluster'] == cluster_id]
    cluster_comments = [c for c in comments if c['user'] in cluster_users]

    # Calculate averages
    avg_sentiment = sum(user_metrics[u]['avg_sentiment'] for u in cluster_users) / len(cluster_users)
    avg_frequency = sum(user_metrics[u]['count'] for u in cluster_users) / len(cluster_users)

    # Extract top keywords
    words = ' '.join(c['text'] for c in cluster_comments).split()
    top_keywords = [word for word, count in Counter(words).most_common(5)]

    # Define persona
    personas[cluster_id] = (
        f"Persona {cluster_id}:\n"
        f"- Average sentiment: {avg_sentiment:.2f}\n"
        f"- Posting frequency: {avg_frequency:.1f} comments\n"
        f"- Top keywords: {', '.join(top_keywords)}"
    )

# Output personas
with open('personas.txt', 'w') as f:
    for persona in personas.values():
        f.write(persona + '\n\n')

print("Persona generation complete. Results saved to personas.txt")
