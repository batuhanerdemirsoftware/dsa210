# Instagram EDA (Exploratory Data Analysis) Tool

A comprehensive tool for analyzing Instagram account data, providing insights into engagement patterns, content performance, and audience interaction.

## Features

- **Account Analysis**
  - Follower and following statistics
  - Post engagement metrics
  - Content type analysis
  - Hashtag usage patterns

- **Engagement Analysis**
  - Likes and comments distribution
  - Engagement rate calculations
  - Peak engagement times
  - Content type performance

- **Temporal Analysis**
  - Posting patterns by day of week
  - Posting patterns by hour
  - Daily engagement trends

- **Textual Analysis**
  - Caption length analysis
  - Sentiment analysis
  - Word count analysis
  - Relationship between caption characteristics and engagement

## Requirements

- Python 3.6+
- Required packages:
  ```
  pandas
  matplotlib
  seaborn
  textblob
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Your Data**
   - Place your Instagram data files in the `data` directory
   - Data files should be in CSV format with the following naming convention:
     ```
     username_YYYYMMDD_HHMMSS.csv
     ```
   - Required columns in the CSV:
     - post_id
     - user_id
     - username
     - followers
     - following
     - post_type
     - post_timestamp
     - likes
     - comments
     - caption
     - hashtags

2. **Run the Analysis**
   ```bash
   python instagram_eda.py
   ```
   This will analyze all accounts found in the data directory.

3. **View Results**
   - Results are saved in the `analysis_results` directory
   - Each account has its own subdirectory with:
     - Visualizations (PNG files)
     - Text summaries (TXT files)
   - A comparison directory contains cross-account analysis

## Output Structure

```
analysis_results/
├── comparison/
│   ├── account_comparison.csv
│   ├── comparison_summary.txt
│   └── metrics_comparison.png
├── account1/
│   ├── engagement_analysis.txt
│   ├── hashtag_analysis.txt
│   ├── missing_values_analysis.txt
│   ├── numerical_summary.txt
│   ├── temporal_analysis.txt
│   ├── textual_analysis_summary.txt
│   └── visualizations/
│       ├── caption_length_distribution.png
│       ├── engagement_by_type.png
│       ├── hourly_engagement_pattern.png
│       └── ...
└── account2/
    └── ... (same structure as account1)
```

## Analysis Components

### 1. Basic Statistics
- Follower and following counts
- Average likes and comments
- Engagement rate calculations

### 2. Content Analysis
- Post type distribution
- Hashtag usage patterns
- Caption characteristics

### 3. Temporal Analysis
- Best posting times
- Day-of-week patterns
- Hourly engagement patterns

### 4. Engagement Analysis
- Like and comment distributions
- Engagement rate by content type
- Peak engagement periods

### 5. Textual Analysis
- Caption length impact
- Sentiment analysis
- Word count analysis

## Customization

To analyze specific accounts, modify the `usernames` list in the `main()` function:
```python
def main():
    eda = InstagramEDA()
    usernames = ["account1", "account2"]  # Add your account usernames here
    eda.run_full_analysis(usernames)
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 