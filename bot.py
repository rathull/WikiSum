import os
import discord
from summary import summary
import re

PREFIX = '!'
TOKEN = os.environ.get('DISCORD_TOKEN')
client = discord.Client()
isURL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


@client.event
async def on_ready():
    print('Logged in as {0.user}\n'.format(client))
    print(f'Watching {str(len(client.guilds))} servers:')
    for g in client.guilds:
        print(g.name)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(f'{PREFIX}help'):  # !help
        await message.channel.send('Commands:')
        await message.channel.send('Get a summary: !wiki {thoroughness (1-20)} {WikiPedia url}')
        if message.content.startswith(f'{PREFIX}help wiki'):
            await message.channel.send('Usage: !wiki {thoroughness (1-20)} {WikiPedia url}')

    if message.content.startswith(f'{PREFIX}wiki'):  # !wiki
        q = message.content.split(' ')[1:]  # Query split into a number and url

        valid = True;
        # Checking for invalid argument count or invalid if message is !wiki help
        if not message.content.count(' ') == 2 or message.content.startswith(f'{PREFIX}wiki help'):
            await message.channel.send('Usage: !wiki {thoroughness (1-20)} {WikiPedia url}')
            valid = False

        # Checking if thoroughness score is a number
        try:
            q[0] = int(q[0])
        except:
            await message.channel.send('The thoroughness score must be a number')
            await message.channel.send('Usage: !wiki {thoroughness (1-20)} {WikiPedia url}')
            valid = False
        
        # Checking if the URL is valid
        if not re.match(isURL, q[1]):
            await message.channel.send("Enter a valid URL")
            valid = False

        if valid:
            try:
                await message.channel.send(
                    summary(
                        q[0], q[1]
                    )
                )
            except Exception as e:
                await message.channel.send(
                    'There was an error.'
                )
                await message.channel.send(e)


client.run(TOKEN)