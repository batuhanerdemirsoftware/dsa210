import instaloader
import pandas as pd
from tqdm import tqdm
import os
from datetime import datetime
import json
import re
import time

class InstagramScraper:
    def __init__(self):
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            request_timeout=30  # Increased timeout
        )
        
    def extract_hashtags(self, text):
        """Extract hashtags from text"""
        if not text:
            return []
        return re.findall(r'#(\w+)', text)
        
    def scrape_profile(self, username, max_posts=None):
        """
        Scrape data from a public Instagram profile
        
        Args:
            username (str): Instagram username to scrape
            max_posts (int, optional): Maximum number of posts to scrape. If None, scrape all posts.
        
        Returns:
            dict: Dictionary containing profile data and posts
        """
        try:
            profile = instaloader.Profile.from_username(self.L.context, username)
            
            # Create profile data dictionary
            profile_data = {
                'user_id': profile.userid,
                'username': profile.username,
                'followers': profile.followers,
                'following': profile.followees,
                'posts_count': profile.mediacount,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Scrape posts
            posts_data = []
            post_count = 0
            
            try:
                posts_iterator = profile.get_posts()
                total_posts = min(max_posts or profile.mediacount, profile.mediacount)
                
                print(f"\nStarting to scrape {total_posts} posts from {username}...")
                print("Waiting 5 seconds between posts to avoid rate limiting...")
                
                for post in tqdm(posts_iterator, total=total_posts, desc=f"Scraping posts for {username}"):
                    if max_posts and post_count >= max_posts:
                        break
                        
                    try:
                        # Add 5-second delay to avoid rate limiting
                        time.sleep(5)
                        
                        # Extract hashtags from caption
                        hashtags = self.extract_hashtags(post.caption)
                        
                        post_data = {
                            'post_id': post.shortcode,
                            'user_id': profile.userid,
                            'username': profile.username,
                            'followers': profile.followers,
                            'following': profile.followees,
                            'post_type': 'video' if post.is_video else 'image',
                            'post_timestamp': post.date.isoformat(),
                            'likes': getattr(post, 'likes', 0),
                            'comments': getattr(post, 'comments', 0),
                            'caption': post.caption if post.caption else '',
                            'hashtags': ', '.join(hashtags) if hashtags else ''
                        }
                        
                        posts_data.append(post_data)
                        post_count += 1
                        
                    except Exception as e:
                        print(f"\nError processing post {post.shortcode}: {str(e)}")
                        print("Continuing with next post...")
                        continue
                    
            except Exception as e:
                print(f"\nError fetching posts: {str(e)}")
                if posts_data:  # Return partial data if we have any
                    print(f"Successfully scraped {len(posts_data)} posts before error")
                    return {
                        'profile': profile_data,
                        'posts': posts_data
                    }
                return None
            
            return {
                'profile': profile_data,
                'posts': posts_data
            }
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {username} does not exist")
            return None
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            print(f"Profile {username} is private")
            return None
        except Exception as e:
            print(f"Error scraping profile {username}: {str(e)}")
            return None
    
    def save_to_json(self, data, username):
        """Save scraped data to a JSON file"""
        if not os.path.exists('data'):
            os.makedirs('data')
            
        filename = f'data/{username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nData saved to {filename}")
    
    def save_to_csv(self, data, username):
        """Save posts data to a CSV file with specific columns"""
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Convert posts to DataFrame
        posts_df = pd.DataFrame(data['posts'])
        
        # Reorder columns according to specified format
        columns = [
            'post_id',
            'user_id',
            'username',
            'followers',
            'following',
            'post_type',
            'post_timestamp',
            'likes',
            'comments',
            'caption',
            'hashtags'
        ]
        
        # Select and reorder columns
        posts_df = posts_df[columns]
            
        filename = f'data/{username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        posts_df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")

def main():
    scraper = InstagramScraper()
    
    # List of official/public accounts to scrape
    usernames = [
        "instagram", "natgeo", "nasa", "nike", "nba", "9gag", "google", "apple", "cristiano", "fcbarcelona", "realmadrid", "championsleague"
    ]
    max_posts = 100  # Set to 100 posts per account
    
    for username in usernames:
        print(f"\nScraping data for {username}...")
        data = scraper.scrape_profile(username, max_posts)
        if data:
            # Save data in both JSON and CSV formats
            scraper.save_to_json(data, username)
            scraper.save_to_csv(data, username)
            print(f"\nScraping completed successfully for {username}!")
        else:
            print(f"\nScraping failed for {username}!")

if __name__ == "__main__":
    main() 