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

__version__ = '0.0.2'

import irc.bot
from chatbot import ChatBot  # Import the ChatBot class

class MyBot(irc.bot.SingleServerIRCBot):
    def __init__(self, nickname, server, channel):
        server_list = [(server, 6667)]
        irc.bot.SingleServerIRCBot.__init__(self, server_list, nickname, nickname)
        self.channel = channel
        self.bot = ChatBot()  # Create an instance of ChatBot

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        response = self.bot.respond(message)  # Use ChatBot to get the response

        # Split the response into separate lines
        response_lines = response.split('\n')

        # Send each line of the response as a separate PRIVMSG command
        for line in response_lines:
            # Send the response to the IRC channel
            connection.privmsg(self.channel, line)

if __name__ == "__main__":
    nickname = "pyppin"
    server = "irc.libera.chat"
    channel = "#linux"

    bot = MyBot(nickname, server, channel)
    bot.start()
