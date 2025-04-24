# Instagram User Behavior Analysis

## Project Overview

This project aims to analyze Instagram user behaviors, focusing specifically on content posting patterns, hashtag usage, and user interactions. The analysis is performed using a comprehensive EDA (Exploratory Data Analysis) tool that provides detailed insights into engagement patterns, content performance, and audience interaction.

## Research Questions

The primary objectives of this analysis include:

* Which types of posts (photos, videos, reels, or stories) receive the most user engagement?
* Which hashtags are most effective in driving user engagement?
* How does the timing of posts influence the level of engagement?
* Is there a significant correlation between follower count and engagement levels?
* Does caption length affect likes and comments received?

## Data Collection Sources

Data is collected through web scraping using Python (Selenium, BeautifulSoup) and stored in CSV format. The EDA tool processes this data to generate comprehensive insights.

## Dataset Description

The dataset includes the following variables:

| Attribute      | Description                                  | Type            |
| -------------- | -------------------------------------------- | --------------- |
| Post ID        | Unique identifier for each post              | Numeric         |
| User ID        | Unique user identifier                       | Numeric         |
| Username       | Instagram username                           | String          |
| Followers      | Number of followers of the user              | Numeric         |
| Following      | Number of accounts the user is following     | Numeric         |
| Post Type      | Type of the post (photo, video, reel, story) | Categorical     |
| Post Timestamp | Date and time when the post was published    | Timestamp       |
| Likes          | Number of likes the post received            | Numeric         |
| Comments       | Number of comments on the post               | Numeric         |
| Caption        | Text description of the post                 | String          |
| Hashtags       | List of hashtags used in the post            | List of strings |

## Analysis Components

The EDA tool performs the following analyses:

1. **Exploratory Data Analysis (EDA)**
   * Data distribution analysis
   * Missing value identification
   * Outlier detection
   * Visualizations (histograms, box plots, scatter plots)

2. **User Engagement Analysis**
   * Comparison of engagement by content type
   * Time series analysis for peak engagement times
   * Engagement rate calculations
   * Content type performance metrics

3. **Textual Analysis (Caption Analysis)**
   * Sentiment analysis using TextBlob
   * Relationship between caption length and user interaction
   * Word count analysis
   * Hashtag effectiveness

## Usage

1. **Installation**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Data Preparation**
   - Place your Instagram data files in the `data` directory
   - Data files should follow the naming convention: `username_YYYYMMDD_HHMMSS.csv`

3. **Running the Analysis**
   ```bash
   python instagram_eda.py
   ```

## Output Structure

The analysis generates the following outputs:

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

## Expected Results and Visualizations

The analysis produces:

* Lists and visual representations of most effective hashtags
* Charts illustrating engagement levels by content type
* Heatmaps depicting optimal posting times
* Regression and scatter plots showing relationships between various metrics
* Sentiment analysis of captions
* Time-based engagement patterns

## Applications of Results

* Enhanced social media marketing strategies
* Content optimization for brands and influencers
* Improved user interaction predictions
* Data-driven posting schedule optimization
* Hashtag strategy refinement

## Requirements

- Python 3.6+
- Required packages:
  ```
  pandas
  matplotlib
  seaborn
  textblob
  ```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the Sabancı University License - see the LICENSE file for details. 
