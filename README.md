# BrandSentio - Reddit Sentiment Analysis

## Overview
BrandSentio is a Flask-based web application designed to analyze the sentiment of Reddit posts for specific brands or keywords. It leverages the Reddit API and VADER Sentiment Analyzer to provide actionable insights into user sentiment and engagement, making it a valuable tool for brands to monitor their online reputation.

This project was built as part of a hackathon, showcasing a quick yet effective solution for sentiment analysis and brand performance evaluation.

---

## Features
- **Real-time Reddit Data**: Fetch posts from Reddit using the PRAW API.
- **Sentiment Analysis**: Analyze user sentiment with the VADER SentimentIntensityAnalyzer.
- **Visualizations**:
  - Sentiment distribution histogram.
  - Upvotes vs. downvotes pie chart.
- **Brand Performance Score**: A unique metric combining sentiment, upvotes, and downvotes to assess brand reputation.
- **Detailed Post Analysis**: View individual Reddit posts with sentiment scores.

---

## Tech Stack
- **Backend**: Python, Flask
- **Data Processing**: Pandas, Matplotlib, Seaborn
- **API Integration**: PRAW (Python Reddit API Wrapper)
- **Visualization**: Matplotlib, Seaborn

---

## Live Demo
The application is deployed and accessible here:  
👉 [BrandSentio Live Demo](https://tech-titans-vodr.onrender.com/)

---

## Requirements

### Prerequisites
- Python 3.7 or above
- Reddit API credentials:
  - Client ID
  - Client Secret
  - User Agent

### Install Dependencies
Run the following command to install the necessary Python libraries:
```bash
pip install -r requirements.txt
```

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/brand-sentio.git
   cd brand-sentio
   ```

2. Configure your Reddit API credentials:
   Edit the `reddit` configuration in `app.py`:
   ```python
   reddit = praw.Reddit(
       client_id='your_client_id',
       client_secret='your_client_secret',
       user_agent='your_user_agent'
   )
   ```

3. Create the directory for storing plots:
   ```bash
   mkdir -p static/plots
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## Usage
1. Enter a brand name or keyword in the input form on the homepage.
2. Click "Analyze" to fetch and analyze related Reddit posts.
3. View:
   - Sentiment distribution plot.
   - Upvotes vs. downvotes pie chart.
   - Brand performance score and interpretation.
   - Detailed analysis of individual posts.

---

## Example Output
- **Sentiment Distribution Plot**: Visualizes sentiment scores across analyzed posts.
- **Upvotes vs. Downvotes Pie Chart**: Displays the ratio of upvotes to downvotes.
- **Brand Performance Score**: A concise metric reflecting brand sentiment and engagement.

---

## Hackathon Notes
- **Goal**: Build a tool that provides quick insights into brand perception using publicly available data.
- **Timeframe**: Developed within the limited timeframe of the hackathon.
- **Team Contribution**: Collaboratively built with a focus on sentiment analysis and data visualization.

---

## Future Work
- Expand support to other social media platforms.
- Add time-series analysis for tracking sentiment trends.
- Integrate machine learning for advanced sentiment analysis.

---

## License
This project is open-source and available under the MIT License.

---

We hope you enjoy using BrandSentio! Feedback and contributions are welcome.
