import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import numpy as np
from textblob import TextBlob  # For sentiment analysis
import re

class InstagramEDA:
    def __init__(self, data_dir='data', output_dir='analysis_results'):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.dfs = {}  # Dictionary to store DataFrames for each account
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        
    def get_account_dir(self, username):
        """Create and return the output directory for an account"""
        account_dir = os.path.join(self.output_dir, username)
        os.makedirs(account_dir, exist_ok=True)
        return account_dir
        
    def load_latest_data(self, username):
        """Load the most recent CSV file for the given username"""
        # Find the most recent file
        files = [f for f in os.listdir(self.data_dir) if f.startswith(username) and f.endswith('.csv')]
        if not files:
            raise FileNotFoundError(f"No data files found for {username}")
        
        # Parse the timestamp from filename (format: username_YYYYMMDD_HHMMSS.csv)
        latest_file = max(files, key=lambda x: datetime.strptime('_'.join(x.split('_')[1:2]), '%Y%m%d'))
        file_path = os.path.join(self.data_dir, latest_file)
        
        # Load the data
        df = pd.read_csv(file_path)
        
        # Convert timestamp to datetime
        df['post_timestamp'] = pd.to_datetime(df['post_timestamp'])
        
        # Extract date features
        df['post_date'] = df['post_timestamp'].dt.date
        df['post_hour'] = df['post_timestamp'].dt.hour
        df['post_day_of_week'] = df['post_timestamp'].dt.day_name()
        
        self.dfs[username] = df
        return df
    
    def analyze_missing_values(self, username):
        """Analyze and visualize missing values in the dataset"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        missing_data = df.isnull().sum()
        missing_percentage = (missing_data / len(df)) * 100
        
        # Save missing values analysis to text file
        with open(os.path.join(account_dir, 'missing_values_analysis.txt'), 'w') as f:
            f.write(f"Missing Values Analysis for {username}:\n")
            f.write("-" * (28 + len(username)) + "\n")
            for col, count, percentage in zip(missing_data.index, missing_data, missing_percentage):
                f.write(f"{col}: {count} missing values ({percentage:.2f}%)\n")
        
        # Print to console as well
        print(f"\nMissing Values Analysis for {username}:")
        print("-" * (28 + len(username)))
        for col, count, percentage in zip(missing_data.index, missing_data, missing_percentage):
            print(f"{col}: {count} missing values ({percentage:.2f}%)")
        
        # Visualize missing values
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
        plt.title(f'Missing Values Heatmap - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'missing_values_heatmap.png'))
        plt.close()
    
    def analyze_numerical_distributions(self, username):
        """Analyze and visualize distributions of numerical features"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        numerical_cols = ['likes', 'comments', 'followers', 'following']
        
        # Save summary statistics to text file
        with open(os.path.join(account_dir, 'numerical_summary.txt'), 'w') as f:
            f.write(f"Numerical Features Summary for {username}:\n")
            f.write("-" * (31 + len(username)) + "\n")
            f.write(df[numerical_cols].describe().to_string())
        
        # Print to console as well
        print(f"\nNumerical Features Summary for {username}:")
        print("-" * (31 + len(username)))
        print(df[numerical_cols].describe())
        
        # Create subplots for distributions
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, col in enumerate(numerical_cols):
            sns.histplot(data=df, x=col, ax=axes[i], kde=True)
            axes[i].set_title(f'Distribution of {col} - {username}')
        
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'numerical_distributions.png'))
        plt.close()
        
        # Box plots for outlier detection
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df[numerical_cols])
        plt.title(f'Box Plots of Numerical Features - {username}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'numerical_boxplots.png'))
        plt.close()
    
    def analyze_temporal_patterns(self, username):
        """Analyze posting patterns over time"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        # Posts per day of week
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='post_day_of_week', 
                     order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        plt.title(f'Posts Distribution by Day of Week - {username}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'posts_by_day.png'))
        plt.close()
        
        # Posts per hour
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x='post_hour')
        plt.title(f'Posts Distribution by Hour - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'posts_by_hour.png'))
        plt.close()
        
        # Save temporal analysis to text file
        with open(os.path.join(account_dir, 'temporal_analysis.txt'), 'w') as f:
            f.write(f"Temporal Analysis for {username}:\n")
            f.write("-" * (23 + len(username)) + "\n")
            f.write("\nPosts by Day of Week:\n")
            f.write(df['post_day_of_week'].value_counts().to_string())
            f.write("\n\nPosts by Hour:\n")
            f.write(df['post_hour'].value_counts().to_string())
    
    def analyze_engagement(self, username):
        """Analyze engagement metrics"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        # Calculate engagement rate
        df['engagement_rate'] = (df['likes'] + df['comments']) / df['followers'] * 100
        
        # Engagement rate by post type
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='post_type', y='engagement_rate')
        plt.title(f'Engagement Rate by Post Type - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'engagement_by_type.png'))
        plt.close()
        
        # Scatter plot of likes vs comments
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='likes', y='comments', hue='post_type')
        plt.title(f'Likes vs Comments - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'likes_vs_comments.png'))
        plt.close()
        
        # Save engagement analysis to text file
        with open(os.path.join(account_dir, 'engagement_analysis.txt'), 'w') as f:
            f.write(f"Engagement Analysis for {username}:\n")
            f.write("-" * (24 + len(username)) + "\n")
            f.write("\nEngagement Rate Summary:\n")
            f.write(df['engagement_rate'].describe().to_string())
            f.write("\n\nEngagement Rate by Post Type:\n")
            f.write(df.groupby('post_type')['engagement_rate'].describe().to_string())
    
    def analyze_hashtags(self, username):
        """Analyze hashtag usage"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        # Count hashtags per post
        df['hashtag_count'] = df['hashtags'].fillna('').apply(lambda x: len(x.split(', ')) if x else 0)
        
        # Distribution of hashtag counts
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='hashtag_count')
        plt.title(f'Distribution of Hashtag Counts per Post - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'hashtag_distribution.png'))
        plt.close()
        
        # Most common hashtags
        all_hashtags = [tag for tags in df['hashtags'].dropna() for tag in tags.split(', ') if tags]
        
        # Save hashtag analysis to text file
        with open(os.path.join(account_dir, 'hashtag_analysis.txt'), 'w') as f:
            f.write(f"Hashtag Analysis for {username}:\n")
            f.write("-" * (22 + len(username)) + "\n")
            f.write("\nHashtag Count Summary:\n")
            f.write(df['hashtag_count'].describe().to_string())
            
            if all_hashtags:
                hashtag_counts = pd.Series(all_hashtags).value_counts()
                f.write("\n\nTop Hashtags:\n")
                f.write(hashtag_counts.head(10).to_string())
                
                plt.figure(figsize=(12, 6))
                sns.barplot(x=hashtag_counts.head(10).values, y=hashtag_counts.head(10).index)
                plt.title(f'Top 10 Most Used Hashtags - {username}')
                plt.tight_layout()
                plt.savefig(os.path.join(account_dir, 'top_hashtags.png'))
                plt.close()
            else:
                f.write("\nNo hashtags found in the dataset")
                print(f"No hashtags found in the dataset for {username}")

    def analyze_engagement_patterns(self, username):
        """Analyze detailed engagement patterns"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        # 1. Engagement by Content Type Analysis
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='post_type', y='likes', showfliers=False)
        plt.title(f'Likes Distribution by Content Type - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'likes_by_content_type.png'))
        plt.close()
        
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='post_type', y='comments', showfliers=False)
        plt.title(f'Comments Distribution by Content Type - {username}')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'comments_by_content_type.png'))
        plt.close()
        
        # Calculate engagement metrics by content type
        engagement_by_type = df.groupby('post_type').agg({
            'likes': ['mean', 'median', 'std'],
            'comments': ['mean', 'median', 'std'],
            'engagement_rate': ['mean', 'median', 'std']
        }).round(2)
        
        # Save engagement by type analysis
        with open(os.path.join(account_dir, 'engagement_by_type_analysis.txt'), 'w') as f:
            f.write(f"Engagement Analysis by Content Type - {username}\n")
            f.write("-" * (40 + len(username)) + "\n\n")
            f.write(engagement_by_type.to_string())
        
        # 2. Time Series Analysis
        # Create a time series of engagement
        df['date'] = df['post_timestamp'].dt.date
        daily_engagement = df.groupby('date').agg({
            'likes': 'mean',
            'comments': 'mean',
            'engagement_rate': 'mean'
        }).reset_index()
        
        # Plot daily engagement trends
        plt.figure(figsize=(15, 8))
        plt.plot(daily_engagement['date'], daily_engagement['engagement_rate'], marker='o')
        plt.title(f'Daily Engagement Rate Trend - {username}')
        plt.xlabel('Date')
        plt.ylabel('Engagement Rate (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'daily_engagement_trend.png'))
        plt.close()
        
        # 3. Peak Engagement Times Analysis
        # Engagement by hour
        hourly_engagement = df.groupby('post_hour').agg({
            'likes': 'mean',
            'comments': 'mean',
            'engagement_rate': 'mean'
        }).reset_index()
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=hourly_engagement, x='post_hour', y='engagement_rate', marker='o')
        plt.title(f'Hourly Engagement Rate Pattern - {username}')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Engagement Rate (%)')
        plt.xticks(range(24))
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'hourly_engagement_pattern.png'))
        plt.close()
        
        # Engagement by day of week
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_engagement = df.groupby('post_day_of_week').agg({
            'likes': 'mean',
            'comments': 'mean',
            'engagement_rate': 'mean'
        }).reindex(weekday_order)
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=daily_engagement, x=daily_engagement.index, y='engagement_rate', marker='o')
        plt.title(f'Weekly Engagement Pattern - {username}')
        plt.xlabel('Day of Week')
        plt.ylabel('Average Engagement Rate (%)')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'weekly_engagement_pattern.png'))
        plt.close()
        
        # Save time-based analysis
        with open(os.path.join(account_dir, 'time_based_analysis.txt'), 'w') as f:
            f.write(f"Time-Based Engagement Analysis - {username}\n")
            f.write("-" * (30 + len(username)) + "\n\n")
            
            f.write("Hourly Engagement Summary:\n")
            f.write(hourly_engagement.to_string())
            f.write("\n\nWeekly Engagement Summary:\n")
            f.write(daily_engagement.to_string())
            
            # Find peak engagement times
            peak_hour = hourly_engagement.loc[hourly_engagement['engagement_rate'].idxmax()]
            peak_day = daily_engagement.loc[daily_engagement['engagement_rate'].idxmax()]
            
            f.write("\n\nPeak Engagement Times:\n")
            f.write(f"Best Hour: {int(peak_hour['post_hour'])}:00 ({peak_hour['engagement_rate']:.2f}% engagement)\n")
            f.write(f"Best Day: {peak_day.name} ({peak_day['engagement_rate']:.2f}% engagement)\n")

    def analyze_captions(self, username):
        """Analyze caption content and its relationship with engagement"""
        df = self.dfs[username]
        account_dir = self.get_account_dir(username)
        
        # 1. Caption Length Analysis
        df['caption_length'] = df['caption'].fillna('').apply(len)
        
        # Plot caption length distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='caption_length', bins=20)
        plt.title(f'Caption Length Distribution - {username}')
        plt.xlabel('Caption Length (characters)')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'caption_length_distribution.png'))
        plt.close()
        
        # 2. Relationship between caption length and engagement
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='caption_length', y='likes', alpha=0.6)
        plt.title(f'Caption Length vs Likes - {username}')
        plt.xlabel('Caption Length (characters)')
        plt.ylabel('Likes')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'caption_length_vs_likes.png'))
        plt.close()
        
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='caption_length', y='comments', alpha=0.6)
        plt.title(f'Caption Length vs Comments - {username}')
        plt.xlabel('Caption Length (characters)')
        plt.ylabel('Comments')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'caption_length_vs_comments.png'))
        plt.close()
        
        # 3. Sentiment Analysis
        def get_sentiment(text):
            if pd.isna(text) or not text.strip():
                return 0
            return TextBlob(text).sentiment.polarity
        
        df['sentiment'] = df['caption'].fillna('').apply(get_sentiment)
        
        # Plot sentiment distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='sentiment', bins=20)
        plt.title(f'Caption Sentiment Distribution - {username}')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'sentiment_distribution.png'))
        plt.close()
        
        # Relationship between sentiment and engagement
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='sentiment', y='likes', alpha=0.6)
        plt.title(f'Sentiment vs Likes - {username}')
        plt.xlabel('Sentiment Polarity')
        plt.ylabel('Likes')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'sentiment_vs_likes.png'))
        plt.close()
        
        # 4. Word Analysis
        def get_word_count(text):
            if pd.isna(text) or not text.strip():
                return 0
            return len(re.findall(r'\w+', text))
        
        df['word_count'] = df['caption'].fillna('').apply(get_word_count)
        
        # Plot word count distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='word_count', bins=20)
        plt.title(f'Word Count Distribution - {username}')
        plt.xlabel('Number of Words')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(account_dir, 'word_count_distribution.png'))
        plt.close()
        
        # 5. Save textual analysis summary
        with open(os.path.join(account_dir, 'textual_analysis_summary.txt'), 'w') as f:
            f.write(f"Textual Analysis Summary - {username}\n")
            f.write("-" * (25 + len(username)) + "\n\n")
            
            # Caption length statistics
            f.write("Caption Length Statistics:\n")
            f.write(df['caption_length'].describe().to_string())
            f.write("\n\n")
            
            # Word count statistics
            f.write("Word Count Statistics:\n")
            f.write(df['word_count'].describe().to_string())
            f.write("\n\n")
            
            # Sentiment statistics
            f.write("Sentiment Analysis Statistics:\n")
            f.write(df['sentiment'].describe().to_string())
            f.write("\n\n")
            
            # Correlation analysis
            correlations = df[['caption_length', 'word_count', 'sentiment', 'likes', 'comments']].corr()
            f.write("Correlation Analysis:\n")
            f.write(correlations.to_string())
            f.write("\n\n")
            
            # Most engaging captions
            f.write("Top 5 Most Engaging Captions (by likes):\n")
            top_captions = df.nlargest(5, 'likes')[['caption', 'likes', 'comments', 'sentiment']]
            f.write(top_captions.to_string())
            f.write("\n\n")
            
            # Most commented captions
            f.write("Top 5 Most Commented Captions:\n")
            top_commented = df.nlargest(5, 'comments')[['caption', 'likes', 'comments', 'sentiment']]
            f.write(top_commented.to_string())

    def compare_accounts(self, usernames):
        """Compare metrics between accounts"""
        comparison_dir = os.path.join(self.output_dir, 'comparison')
        os.makedirs(comparison_dir, exist_ok=True)
        
        comparison_data = []
        for username in usernames:
            df = self.dfs[username]
            avg_likes = df['likes'].mean()
            avg_comments = df['comments'].mean()
            followers = df['followers'].iloc[0]
            following = df['following'].iloc[0]
            engagement_rate = ((df['likes'] + df['comments']) / df['followers'] * 100).mean()
            
            comparison_data.append({
                'username': username,
                'avg_likes': avg_likes,
                'avg_comments': avg_comments,
                'followers': followers,
                'following': following,
                'engagement_rate': engagement_rate
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Save comparison data to CSV
        comparison_df.to_csv(os.path.join(comparison_dir, 'account_comparison.csv'), index=False)
        
        # Create comparative visualizations
        metrics = ['avg_likes', 'avg_comments', 'followers', 'following', 'engagement_rate']
        fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 4*len(metrics)))
        
        for i, metric in enumerate(metrics):
            sns.barplot(data=comparison_df, x='username', y=metric, ax=axes[i])
            axes[i].set_title(f'Comparison of {metric.replace("_", " ").title()}')
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(comparison_dir, 'metrics_comparison.png'))
        plt.close()
        
        # Save comparison summary to text file
        with open(os.path.join(comparison_dir, 'comparison_summary.txt'), 'w') as f:
            f.write("Account Comparison Summary:\n")
            f.write("-" * 24 + "\n\n")
            f.write(comparison_df.to_string(index=False))
        
        # Print to console as well
        print("\nAccount Comparison:")
        print("-" * 20)
        print(comparison_df.to_string(index=False))
    
    def run_full_analysis(self, usernames):
        """Run complete EDA analysis for multiple accounts"""
        for username in usernames:
            print(f"\nStarting EDA for {username}...")
            self.load_latest_data(username)
            self.analyze_missing_values(username)
            self.analyze_numerical_distributions(username)
            self.analyze_temporal_patterns(username)
            self.analyze_engagement(username)
            self.analyze_hashtags(username)
            self.analyze_engagement_patterns(username)
            self.analyze_captions(username)
        
        # Compare accounts
        self.compare_accounts(usernames)
        print(f"\nEDA completed! Results are saved in the '{self.output_dir}' directory.")

def main():
    eda = InstagramEDA()
    usernames = ["elasonggur", "nasa"]
    eda.run_full_analysis(usernames)

if __name__ == "__main__":
    main() 