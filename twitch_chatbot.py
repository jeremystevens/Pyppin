#!/usr/bin/env python
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
import asyncio
from twitchio.ext import commands
from dotenv import load_dotenv
from chatbot import ChatBot  # Import the ChatBot class
import time
import pyttsx3
import pyautogui

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
TMI_TOKEN = os.getenv('TMI_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BOT_PREFIX = os.getenv('BOT_PREFIX')
CHANNEL = os.getenv('CHANNEL')

# Initialize the ChatBot and TTS engine
chatbot = ChatBot()
tts_engine = pyttsx3.init()

# Dictionary to store user stats
user_stats = {}
user_join_times = {}

# Define your bot class
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=TMI_TOKEN, prefix=BOT_PREFIX, initial_channels=[CHANNEL])
        self.loop.create_task(self.track_watch_time())

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        print(f'Received message: {message.content}')
        if message.echo:
            return

        # Check if the message is a !say command
        if message.content.startswith(f'{BOT_PREFIX}say '):
            # Extract the text after !say
            text_to_say = message.content[len(f'{BOT_PREFIX}say '):].strip()
            # Send the text as a message in chat
            await message.channel.send(f"Repeating: {text_to_say}")
            # Handle TTS and key press
            self.text_to_speech(text_to_say)
        else:
            # Process message using chatbot.py's ChatBot class
            response = chatbot.respond(message.content)
            print(f'Response: {response}')  # Debug print statement
            await message.channel.send(response)
        
        # Update user stats (e.g., increment message count)
        user = message.author.name
        if user not in user_stats:
            user_stats[user] = {'messages': 0, 'points': 0, 'watch_time': 0}
        user_stats[user]['messages'] += 1

    async def event_join(self, channel, user):
        # Greet the user when they join the chat
        if user.name.lower() != self.nick.lower():  # Avoid greeting the bot itself
            greeting_message = f"Welcome to the chat, {user.name}!"
            await channel.send(greeting_message)
        
        # Record the join time
        user_join_times[user.name] = time.time()

    async def event_part(self, channel, user):
        # Calculate watch time when a user leaves
        if user.name in user_join_times:
            join_time = user_join_times.pop(user.name)
            watch_time = time.time() - join_time
            if user.name in user_stats:
                user_stats[user.name]['watch_time'] += watch_time / 60  # Convert to minutes
            else:
                user_stats[user.name] = {'messages': 0, 'points': 0, 'watch_time': watch_time / 60}

    async def track_watch_time(self):
        while True:
            # Periodically update watch time for users still in chat
            await asyncio.sleep(60)
            current_time = time.time()
            for user, join_time in list(user_join_times.items()):
                if user in user_stats:
                    user_stats[user]['watch_time'] += (current_time - join_time) / 60  # Convert to minutes
                    user_join_times[user] = current_time

    def text_to_speech(self, text):
        # Press and hold Shift+1
        pyautogui.keyDown('shift')
        pyautogui.keyDown('1')

        # Speak the text
        tts_engine.say(text)
        tts_engine.runAndWait()

        # Release Shift+1 after speaking
        pyautogui.keyUp('1')
        pyautogui.keyUp('shift')

    @commands.command(name='hello')
    async def hello(self, ctx):
        print(f'Received hello command from {ctx.author.name}')
        # Generate a response using chatbot.py's ChatBot class
        response = chatbot.respond('hello')
        await ctx.send(response)

# Run the bot
if __name__ == '__main__':
    bot = Bot()
    bot.run()
