import requests
import random
import pandas as pd
from datetime import datetime
import logging
import coloredlogs
import configparser
import json
import os

# Configure logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

def read_api_key(config_file='config.ini'):
    """
    Reads the API key from a configuration file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        str: API key
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['DEFAULT']['API_KEY']

def get_random_video_ids(api_key, seen_ids, max_results=50):
    """
    Fetches a list of random YouTube video IDs based on a randomly chosen query topic.

    Args:
        api_key (str): API key for YouTube Data API.
        seen_ids (set): Set of video IDs that have already been fetched.
        max_results (int): Maximum number of results to fetch.

    Returns:
        list: A list of YouTube video IDs.
    """
    # Reduced redundancy in queries
    queries = ['technology', 'politics', 'ideology', 'science', 'philosophy', 
               'religion', 'culture', 'economics', 'business', 'finance', 'history',
               'geography', 'mathematics', 'statistics', 'physics', 'chemistry', 
               'biology', 'medicine', 'psychology', 'sociology', 'anthropology', 
               'linguistics', 'literature', 'art', 'music', 'film', 'theatre', 
               'television', 'sports', 'games', 'fashion', 'food', 'travel', 
               'transportation', 'architecture', 'engineering', 'education', 
               'law', 'military', 'health', 'environment', 'weather', 'animals', 
               'plants']
    query = random.choice(queries)

    logger.info(f"Fetching video data for query: {query}")
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&maxResults={max_results}&key={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch video data: HTTP {response.status_code}")

    search_results = response.json()

    # Filter out already seen IDs
    new_video_ids = [item['id']['videoId'] for item in search_results['items'] if item['id']['videoId'] not in seen_ids]
    logger.info(f"Fetched {len(new_video_ids)} new video IDs")

    return new_video_ids

def check_video_restrictions(api_key, video_ids):
    """
    Checks for regional restrictions on a list of YouTube video IDs.

    Args:
        api_key (str): API key for YouTube Data API.
        video_ids (list): List of YouTube video IDs.

    Returns:
        list: List of dictionaries containing video IDs and their restrictions.
    """
    video_list = ','.join(video_ids)
    url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_list}&key={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch video data: HTTP {response.status_code}")

    video_data = response.json()

    restricted_videos = []
    for item in video_data.get('items', []):
        content_details = item['contentDetails']
        restrictions = content_details.get('regionRestriction', {})
        if 'blocked' in restrictions:
            restricted_videos.append({'Video ID': item['id'], 'Restrictions': restrictions['blocked']})

    return restricted_videos

def load_json_history(filename='video_history.json'):
    """
    Loads the video history from a JSON file.

    Args:
        filename (str): Path to the JSON file.

    Returns:
        dict: Video history data.
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_json_history(data, filename='video_history.json'):
    """
    Saves the video history to a JSON file.

    Args:
        data (dict): Video history data.
        filename (str): Path to the JSON file.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    logger.info(f"JSON history saved to {filename}")

# 
# Main
#
if __name__ == '__main__':
    api_key = read_api_key()

    video_history = load_json_history()  # Load the history from the JSON file
    seen_ids = set(video_history.keys())  # Initialize seen_ids with history
    restricted_videos = []

    try:
        while len(restricted_videos) < 50:
            video_ids = get_random_video_ids(api_key, seen_ids)
            restricted_data = check_video_restrictions(api_key, video_ids)
            restricted_videos.extend(restricted_data)
            seen_ids.update(video_ids)  # Update the seen IDs

            # Update video history
            for video in restricted_data:
                video_history[video['Video ID']] = video['Restrictions']

            logger.info(f"Collected {len(restricted_videos)} restricted videos so far.")

    except Exception as e:
        logger.error(f"Error: {e}")

    if restricted_videos:
        # Convert to DataFrame
        df = pd.DataFrame(restricted_videos)

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save to CSV with timestamp in filename
        filename = f'youtube_video_restrictions_{timestamp}.csv'
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")

        # Save the history to a JSON file
        save_json_history(video_history)