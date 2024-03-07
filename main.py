import os
import re
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta

message_history = {}
is_request_in_progress = False  # Flag to track whether a request is in progress

load_dotenv()
intents = discord.Intents.all()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# List of channel IDs to exclude from checking (replace channel.id1 and channel.id2 with your channel ID, leave blank if you don't want any exclusions)
excluded_channel_ids = [channel.id1, channel.id2]

# Initialize Discord bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("----------------------------------------")
    print(f'Logged in as {bot.user}')
    print("----------------------------------------")

    await bot.tree.sync()

@bot.hybrid_command(
    name='wordcount',
    description='Counts the amount of times a certain user said a specific word')
async def wordcount(ctx, word: str, user: discord.User = None):
    global is_request_in_progress

    if is_request_in_progress:
        await ctx.send(f'{ctx.author.mention} ❌ Another request is already in progress. Please wait.')
        return

    is_request_in_progress = True

    if user is None:
        user = ctx.author

    # Generate variants for the provided word
    word_variants = [word.lower(), word.upper(), word.capitalize()]

    # Add variants with spaces between each letter
    spaced_variants = [' '.join(char for char in word) for word in word_variants]
    word_variants.extend(spaced_variants)

    # Create a regular expression pattern for matching the word and its reverse variants
    word_pattern = re.compile(fr'\b({"|".join(map(re.escape, word_variants + [word[::-1] for word in word_variants]))})\b',
                              flags=re.IGNORECASE)

    print(f'Word pattern: {word_pattern.pattern}')  # Debug print

    # Send initial counting message
    counting_message = await ctx.send(
        f'Counting the amount of times {user.mention} said \'{word}\' within the last 3 days. This may take a while, so please be patient...'
    )

    # Start the counting task in the background
    await bruh_count_task(ctx, user, counting_message, word_pattern, word)

@tasks.loop(count=1)
async def bruh_count_task(ctx, user, counting_message, word_pattern, word):
    global is_request_in_progress

    word_count = 0
    total_messages_checked = 0
    update_interval = 250  # Adjust this value based on server activity

    for channel in ctx.guild.text_channels:
        # Skip channels in the excluded list
        if channel.id in excluded_channel_ids:
            print(f'Skipping excluded channel: {channel.name} (ID: {channel.id})')
            continue

        print(f'Checking channel: {channel.name}')

        try:
            # Limit the search to messages from the last 3 days
            limit_date = datetime.utcnow() - timedelta(days=3)
            async for message in channel.history(limit=None,
                                                after=limit_date,
                                                oldest_first=False):
                # Search for the provided word variants and their reverse
                if word_pattern.search(message.content.lower()):
                    if message.author.id == user.id:
                        word_count += 1
                        print(f'Found {word} in message: "{message.content}"')

                total_messages_checked += 1
                # Update progress every specified interval
                if total_messages_checked % update_interval == 0:
                    await update_counting_message(counting_message, total_messages_checked)

        except discord.HTTPException as e:
            print(f"Discord API request failed: {e}")

    # Edit the existing counting message with the result and a ping to the user
    await counting_message.edit(
        content=f'Counting is completed. The total count for {user.mention} saying \'{word}\' within the last 3 days is: {word_count}'
    )

    is_request_in_progress = False

    print("Counting process completed successfully.")

async def update_counting_message(counting_message, total_checked):
    await counting_message.edit(
        content=f'Counting in progress... {total_checked} messages checked'
    )

bot.run(DISCORD_BOT_TOKEN)
