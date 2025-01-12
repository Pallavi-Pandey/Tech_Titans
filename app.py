import os
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, render_template, send_from_directory, url_for
import praw
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Flask app
app = Flask(__name__)

# Create directory for storing plots
if not os.path.exists('static/plots'):
    os.makedirs('static/plots')

# Reddit API credentials
reddit = praw.Reddit(
    client_id='a52JCncam94o0-RAYUMLWQ',
    client_secret='wVuG-LeEENNV_L8nAQ_3BKUUVgDDNg',
    user_agent='BrandSentio'
)

# Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Fetch Reddit posts and calculate sentiment
def fetch_reddit_posts(subreddit, keyword, limit=100):
    posts = []
    for post in reddit.subreddit(subreddit).search(keyword, limit=limit):
        upvotes = max(post.score, 0)
        downvotes = int((1 - post.upvote_ratio) * (upvotes + abs(post.score))) if post.score < 0 else int((1 - post.upvote_ratio) * (upvotes + abs(post.score)))
        posts.append({
            "id": post.id,
            "title": post.title,
            "selftext": post.selftext,
            "created_utc": post.created_utc,
            "score": post.score,
            "upvotes": upvotes,
            "downvotes": downvotes
        })

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Calculate total upvotes and downvotes
    total_upvotes = df['upvotes'].sum()
    total_downvotes = df['downvotes'].sum()

    # Normalize upvotes and downvotes
    df['normalized_upvotes'] = df['upvotes'] / total_upvotes if total_upvotes > 0 else 0
    df['normalized_downvotes'] = df['downvotes'] / total_downvotes if total_downvotes > 0 else 0

    # Perform sentiment analysis on titles using VADER and normalize sentiment
    df['sentiment'] = df['title'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    df['normalized_sentiment'] = (df['sentiment'] + 1) / 2  # Scale from [-1, 1] to [0, 1]

    # Calculate unique score using a weighted sum of normalized components
    weight_upvotes = 0.5   # Weight for upvotes
    weight_downvotes = -0.3 # Weight for downvotes (negative impact)
    weight_sentiment = 0.2   # Weight for sentiment

    df['unique_score'] = (
        weight_upvotes * df['normalized_upvotes'] +
        weight_downvotes * df['normalized_downvotes'] +
        weight_sentiment * df['normalized_sentiment']
    )

    return df, total_upvotes, total_downvotes

# Function to calculate brand performance score
def calculate_brand_performance(total_upvotes, total_downvotes, average_sentiment):
    if total_upvotes + total_downvotes > 0:
        engagement_ratio = (total_upvotes - total_downvotes) / (total_upvotes + total_downvotes)
    else:
        engagement_ratio = 0  # Neutral if no votes

    normalized_sentiment = (average_sentiment + 1) / 2  # Scale from [-1, 1] to [0, 1]

    brand_performance_score = engagement_ratio + normalized_sentiment

    return brand_performance_score

# Function to generate sentiment plot
def generate_sentiment_plot(df):
    plt.figure(figsize=(8, 6))
    sns.histplot(df['sentiment'], kde=True, color='blue')
    plt.title('Sentiment Distribution for Reddit Posts', fontsize=16)
    plt.xlabel('Sentiment Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig('static/plots/sentiment_distribution.png')
    plt.close()

# Function to generate pie chart for upvotes vs downvotes
def generate_upvotes_downvotes_pie_chart(df):
    total_upvotes = df['upvotes'].sum()
    total_downvotes = df['downvotes'].sum()

    labels = ['Upvotes', 'Downvotes']
    sizes = [total_upvotes, total_downvotes]
    colors = ['#66b3ff', '#ff6666']
    explode = (0.1, 0)  # Explode the first slice (Upvotes)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Upvotes vs Downvotes Distribution', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular
    plt.savefig('static/plots/upvotes_downvotes_pie_chart.png')
    plt.close()

# Route for brand input
@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze Reddit sentiment
@app.route('/analyze', methods=['POST'])
def analyze_brand():
    brand = request.form.get('brand')
    if not brand:
        return "Brand name is required", 400

    # Fetch Reddit posts and calculate sentiment
    reddit_df, total_upvotes, total_downvotes = fetch_reddit_posts('technology', brand, limit=50)

    # Calculate average sentiment and brand performance score
    average_sentiment = reddit_df['sentiment'].mean() if not reddit_df.empty else 0
    brand_performance_score = calculate_brand_performance(total_upvotes, total_downvotes, average_sentiment)

    # Generate the plots
    generate_sentiment_plot(reddit_df)
    generate_upvotes_downvotes_pie_chart(reddit_df)  # Update to generate pie chart

    # Interpretation of brand performance
    if brand_performance_score < 1:
        performance = "The brand is struggling with user engagement and/or has negative sentiment."
    elif brand_performance_score == 1:
        performance = "The brand is performing adequately but may need improvement."
    else:
        performance = "The brand is doing well with positive engagement and sentiment."

    # Render results
    sentiment_plot = url_for('static', filename='plots/sentiment_distribution.png')
    upvotes_downvotes_plot = url_for('static', filename='plots/upvotes_downvotes_pie_chart.png')

    return render_template(
        'results.html',
        brand=brand,
        total_upvotes=total_upvotes,
        total_downvotes=total_downvotes,
        average_sentiment=average_sentiment,
        brand_performance_score=brand_performance_score,
        performance=performance,
        reddit_data=reddit_df.to_dict(orient="records"),
        sentiment_plot=sentiment_plot,
        upvotes_downvotes_plot=upvotes_downvotes_plot
    )

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
