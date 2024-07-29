#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2023 - Jeremy Stevens

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__version__ = '0.0.1-beta'
import os
import time
import aiohttp
from datetime import datetime, timezone
from twitchio.ext import commands
from dotenv import load_dotenv
from chatbot import ChatBot  # Import the ChatBot class
from functools import wraps

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
TMI_TOKEN = os.getenv('TMI_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BOT_PREFIX = os.getenv('BOT_PREFIX')
CHANNEL = os.getenv('CHANNEL')

# Initialize the ChatBot
chatbot = ChatBot()

# List of administrators
administrators = ["admin1", "admin2", "admin3"]

# Define a decorator for admin-only commands
def admin_only(func):
    @wraps(func)
    async def wrapper(ctx: commands.Context, *args, **kwargs):
        if ctx.author.name.lower() not in administrators:
            await ctx.send(f"Sorry, {ctx.author.name}, you don't have permission to use this command.")
            return
        return await func(ctx, *args, **kwargs)
    return wrapper

# Function to fetch stream information
async def get_stream_info(session):
    url = f'https://api.twitch.tv/helix/streams?user_login={CHANNEL}'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {TMI_TOKEN}'
    }
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            print("API Response:", data)  # Debugging: Print the API response
            if data['data']:
                stream = data['data'][0]
                return {
                    "game": stream['game_name'],
                    "start_time": stream['started_at']
                }
            else:
                print("No stream data found.")
        else:
            print("Failed to fetch stream info:", response.status)
        return None

# Define your bot class
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TMI_TOKEN, prefix=BOT_PREFIX, initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        print(f'Received message: {message.content}')
        if message.echo:
            return

        # Handle commands first
        await self.handle_commands(message)

        # If not a command, process the message using the chatbot
        if not message.content.startswith(BOT_PREFIX):
            response = chatbot.respond(message.content)
            print(f'Response: {response}')  # Debug print statement
            await message.channel.send(response)

    async def event_join(self, channel, user):
        if user.name.lower() != self.nick.lower():
            await channel.send(f"Welcome to the chat, {user.name}!")
        user_join_times = {}
        user_join_times[user.name] = time.time()

    @commands.command(name='hello')
    async def hello(self, ctx):
        print(f'Received hello command from {ctx.author.name}')
        # Generate a response using chatbot.py's ChatBot class
        response = chatbot.respond('hello')
        await ctx.send(response)

    @commands.command(name='currentgame')
    async def current_game(self, ctx):
        async with aiohttp.ClientSession() as session:
            info = await get_stream_info(session)
            if info:
                await ctx.send(f"The current game being played is: {info['game']}")
            else:
                await ctx.send("The stream is currently offline or no data is available.")

    @commands.command(name='streamduration')
    async def stream_duration(self, ctx):
        async with aiohttp.ClientSession() as session:
            info = await get_stream_info(session)
            if info:
                start_time = datetime.fromisoformat(info['start_time'][:-1]).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                duration = now - start_time
                await ctx.send(f"The stream has been live for: {duration}")
            else:
                await ctx.send("The stream is currently offline or no data is available.")

    @commands.command(name='setgame')
    @admin_only
    async def set_game(self, ctx, *, game_name: str):
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {TMI_TOKEN}',
            'Content-Type': 'application/json'
        }
        data = {
            'game_id': game_name
        }
        url = f'https://api.twitch.tv/helix/channels?broadcaster_id={ctx.author.id}'
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=headers, json=data) as response:
                if response.status == 204:
                    await ctx.send(f"Game updated to {game_name}")
                else:
                    await ctx.send("Failed to update the game. Please try again.")

# Run the bot
if __name__ == '__main__':
    bot = Bot()
    bot.run()
