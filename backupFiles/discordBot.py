#!/usr/bin/env python3

"""
Main for the Discord Bot
Author: Justin Hammel
Description: Main calls the Script for connecting and handling the interaction
                of the bot with the server. I do not think this portion is
                needed. I primarily added it to showcase calling another Script
                from within the main.
"""

# Import function to connect the bot to discord server
from backupFiles import connectDiscord


def main():
    """Called at runtime"""
    connectDiscord()  # This script is what does everything


if __name__ == "__main__":
    main()
