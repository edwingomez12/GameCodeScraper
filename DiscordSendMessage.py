import discord

# Replace with your bot token
TOKEN = ''
# Replace with the ID of the channel you want to send a message to
CHANNEL_ID =   # Use the actual user ID

intents = discord.Intents.default()
intents.messages = True  

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents) 

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send('Hello! This is a message from my Discord bot!')
        else:
            print(f'Channel with ID {CHANNEL_ID} not found.')
        await self.close()  # Close the bot after sending the message

client = MyClient()
client.run(TOKEN)
