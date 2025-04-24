# Instagram Data Scraper

A Python-based Instagram data scraper for public profiles. This tool allows you to collect data from public Instagram profiles for data science projects.

## Features

- Scrape public Instagram profiles
- Collect profile information (username, full name, biography, followers count, etc.)
- Collect post data (captions, likes, comments, timestamps, etc.)
- Save data in both JSON and CSV formats
- Progress bar for tracking scraping progress
- Error handling for private profiles and non-existent accounts

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Open `instagram_scraper.py` and modify the `username` and `max_posts` variables in the `main()` function:
```python
username = "nasa"  # Change this to any public profile
max_posts = 10    # Set to None to scrape all posts
```

2. Run the script:
```bash
python instagram_scraper.py
```

3. The scraped data will be saved in the `data` directory in both JSON and CSV formats.

## Data Structure

### JSON Output
The JSON file contains two main sections:
- `profile`: Contains profile information
- `posts`: Contains an array of post data

### CSV Output
The CSV file contains all post data with profile information added as columns.

## Important Notes

- This scraper only works with public profiles
- Be mindful of Instagram's rate limits and terms of service
- The scraper does not download media files (images/videos)
- Consider adding delays between requests if scraping multiple profiles

## Example Usage

```python
from instagram_scraper import InstagramScraper

scraper = InstagramScraper()
data = scraper.scrape_profile("nasa", max_posts=5)

if data:
    scraper.save_to_json(data, "nasa")
    scraper.save_to_csv(data, "nasa")
``` 