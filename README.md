# Word Count Bot
Do you wonder how many times your friend said 'lmao' in your Discord server?
Do you think that you say "bruh" too much?

Word Count Bot is a Discord bot written in Python that can do just that!
It can count how many times you or someone else have said a word, which is user-inputted, over the last three days.

## Features

- **Count Word:** Count the amount of times a user-inputted word has been said by either you or another person within the last 3 days.
- **Channel Exclusion:** You can exclude the channel you do not want the bot to check in by pasting the channel ID in its dedicated section in the code.
- **Hybrid Commands:** This bot will work with the current Application Commands system (/), or if you are too stubborn to convert, the legacy prefix commands (!) will work too.

## Setup

### Requirements

- discord.py (Obviously)
- python-dotenv
- datetime

### Installation

1. Clone the repository to your local machine.
   
2. Install the required Python libraries:

   ```
   pip install -r requirements.txt
   ```
   
### Configuration

1. Fill in your Discord Token in the `.env.example` file.

2. Rename the file to `.env`

3. In `main.py`, make sure to replace the channel.id1 and channelid.2 into the channel ID of the channel you want to exclude. Leave blank (NOT LEAVING channel.id1 and channel.id2 AS IS) if you don't want any exclusions.

4. Run `main.py`

## Command Structure

### Application Command:
- /wordcount word @user (leave user blank if you want the bot to count your messages)

### Legacy Prefix Command
- !wordcount word @user (leave user blank if you want the bot to count your messages)

## Development

You may fork the project and customise it according to your needs. Make sure to follow the Discord guidelines for bot development and API usage.
