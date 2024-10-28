import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os

# URL to scrape
URL = 'https://www.vg247.com/roblox-dress-to-impress-codes#section-1'
TOKEN = ''  # Replace with your actual Discord bot token
CHANNEL_ID =   # Replace with the ID of the channel you want to send a message to
CODES_FILE = 'dti_codes.txt'

# Function to scrape codes
def get_dti_codes():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific section with the id "section-1"
        section = soup.find('h2', id='section-1')
        keywords = ['WORKING DRESS TO IMPRESS CODES']
        working_codes = any(keyword in section.text.upper() for keyword in keywords)

        if working_codes:
            # Get the next <ul> element after the <h2> section
            codes_list = section.find_next('ul')

            # Extract each <li> within the <ul>
            if codes_list:
                codes = [item.get_text(strip=True) for item in codes_list.find_all('li')]
                return codes
            else:
                print('No list of codes found in the section.')
                return []
        else:
            print('Section with id "section-1" not found.')
            return []

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return []

# Function to read codes from a file
def read_codes_from_file():
    if os.path.exists(CODES_FILE):
        with open(CODES_FILE, 'r') as file:
            return file.read().splitlines()
    return []

# Function to save codes to a file
def save_codes_to_file(codes):
    with open(CODES_FILE, 'w') as file:
        file.write('\n'.join(codes))

# Function to send codes to Discord
async def send_codes_to_discord(codes):
    intents = discord.Intents.default()
    intents.messages = True  # Enable message intents

    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            channel = self.get_channel(CHANNEL_ID)
            if channel:
                # Prepare the message with the codes
                message = 'New Working Dress to Impress codes:\n' + '\n'.join(codes)
                await channel.send(message)
                print(f'Successfully sent the message to channel ID {CHANNEL_ID}.')
            else:
                print(f'Channel with ID {CHANNEL_ID} not found.')
            await self.close()  # Close the bot after sending the message

    client = MyClient(intents=intents)
    await client.start(TOKEN)

# Main function
def main():
    # Get the codes from the website
    current_codes = get_dti_codes()
    
    if current_codes:
        # Read the previously saved codes
        saved_codes = read_codes_from_file()

        # Check if the current codes differ from the saved ones
        if current_codes != saved_codes:
            print('New or updated codes found. Saving and sending to Discord...')
            save_codes_to_file(current_codes)
            asyncio.run(send_codes_to_discord(current_codes))
        else:
            print('No new codes found. The codes are the same as before.')
    else:
        print('No codes to check.')

# Run the main function
if __name__ == '__main__':
    main()
