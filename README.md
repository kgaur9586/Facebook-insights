# Facebook-insights

# Facebook Insights Microservice

A Django-based service to scrape and analyze Facebook page insights, storing data in a relational database with REST API endpoints.

## Features

- **Facebook Page Scraping**
  - Profile details (name, category, followers, etc.)
  - Recent posts (up to 40 posts per page)
  - Follower/following information
  - Automatic data refresh on request

- **Database Storage**
  - PostgreSQL/MySQL support
  - Model relationships maintained:
    - Page → Posts → Comments
    - Page → Followers (SocialMediaUser)

- **REST API**
  - Filter pages by follower count range
  - Search pages by name/category
  - Pagination support
  - Get recent posts/followers for any page

- **Advanced Features**
  - Headless browser scraping with Selenium
  - Anti-detection mechanisms
  - Request throttling
  - Partial response handling

## Installation

### Prerequisites
- Python 3.10+
- MySQL/PostgreSQL database
- Chrome browser (latest stable version)
- ChromeDriver (matching browser version)

### Steps
1. Clone repository:
```bash
git clone https://github.com/yourusername/facebook-insights.git
cd facebook-insights
