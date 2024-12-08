import requests
import random
import time
from bs4 import BeautifulSoup
import os

# Function to read proxies from a file
def load_proxies(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Function to read OAuth tokens (or cookies) from a file
def load_tokens(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Automatically locate files on Replit
proxies_file = os.path.join(os.getcwd(), "proxies.txt")
tokens_file = os.path.join(os.getcwd(), "tokens.txt")

if not os.path.exists(proxies_file):
    print(f"Error: Proxies file not found at {proxies_file}")
    exit(1)

if not os.path.exists(tokens_file):
    print(f"Error: Tokens file not found at {tokens_file}")
    exit(1)

PROXIES = load_proxies(proxies_file)
TOKENS = load_tokens(tokens_file)

# Function to follow a Twitch channel without using the API
def follow_channel_custom(token, proxy, channel_name):
    try:
        # Initialize session with proxy
        session = requests.Session()

        # Use ip:port format for proxies (no authentication)
        session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

        # Set headers (including authentication token as cookie)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.twitch.tv/",
            "Cookie": f"auth-token={token}"
        }

        # Get channel ID by scraping Twitch
        url = f"https://www.twitch.tv/{channel_name}"
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            channel_id = soup.find("meta", {"property": "og:url"})
            if channel_id:
                print(f"Found channel: {channel_name}")

                # Simulate following the channel (this is a placeholder; actual endpoint interaction may vary)
                follow_url = f"https://www.twitch.tv/follow/{channel_name}"
                follow_response = session.post(follow_url, headers=headers)

                if follow_response.status_code in [200, 204]:
                    print(f"Successfully followed: {channel_name}")
                else:
                    print(f"Failed to follow {channel_name}: {follow_response.status_code}")
            else:
                print(f"Channel ID for {channel_name} not found.")
        else:
            print(f"Failed to load channel page for {channel_name}: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

# Main script
if __name__ == "__main__":
    target_channel = input("Enter the Twitch channel to follow: ")

    # Ask the user how many proxies and tokens to use
    num_proxies = int(input(f"How many proxies to use (max {len(PROXIES)}): "))
    num_tokens = int(input(f"How many tokens to use (max {len(TOKENS)}): "))

    # Ensure the numbers don't exceed available proxies or tokens
    num_proxies = min(num_proxies, len(PROXIES))
    num_tokens = min(num_tokens, len(TOKENS))

    for i in range(num_tokens):
        token = TOKENS[i]
        for j in range(num_proxies):
            proxy = PROXIES[j]
            print(f"Using proxy: {proxy} with token: {token[:10]}...")  # Mask token for privacy
            follow_channel_custom(token, proxy, target_channel)
            time.sleep(1)  # Add delay to avoid triggering detection
