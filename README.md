# YouTube Video Restriction Fetcher 🚫🎥

This script is designed to efficiently gather data on regionally restricted YouTube videos. It randomly selects topics, fetches corresponding video IDs, and checks for regional restrictions.

## Setup 🛠️

Ensure Python 3.x is installed. Install required libraries:

```bash
pip install requests pandas coloredlogs configparser
```

### Configuration

1.  **API Key**: Obtain a YouTube Data API key. Place it in `config.ini`:

```ini
[DEFAULT]
API_KEY = Your_API_Key_Here
```

2.  Create `config.ini` in the root directory and insert your API key.

## Usage 🚀

Run the script from the command line:

```bash
python youtube_restriction_fetcher.py
```

## How It Works 🧩

-   **Random Topic Selection**: Chooses a topic like technology, politics, or science.
-   **Data Fetching**: Requests YouTube Data API to fetch video IDs related to the topic.
-   **Restriction Check**: Checks for regional restrictions on these videos.
-   **Data Aggregation**: Repeats until details of 50 restricted videos are collected.
-   **Logging**: Logs vital information and errors for debugging.
-   **Data Storage**: Saves data in a timestamped CSV file.

Enjoy using YouTube Video Restriction Fetcher! 🎉

## Appendix

To obtain a YouTube Data API key, you need to follow these general steps:

1.  **Google Developers Console**: Visit the Google Developers Console and sign in with your Google account.
2.  **Create a Project**: If you don't already have a project, create one by providing a name for your project.
3.  **Enable YouTube Data API**: Once the project is created, go to the library section and search for the YouTube Data API v3. Enable this API for your project.
4.  **Create Credentials**: After enabling the API, navigate to the credentials page. Choose 'Create credentials' and select 'API key'. This will generate a new API key for you.
5.  **Restrict and Use API Key**: It's a good practice to restrict the API key to specific APIs or web services and to secure it properly. After this, you can use this API key in your application.
    
For detailed instructions and additional information, it is best to refer to the official [Getting Started guide on the Google Developers site](https://developers.google.com/youtube/v3/getting-started).