import os
import discord
from summary import summary, summaryWithoutFirst, summaryWikipedia
import re
# from regex import isURL, isWikipedia

PREFIX = '!'
# TOKEN = os.environ.get('DISCORD_TOKEN')
TOKEN = 'ODIzNjM1OTg5MTQ1NzE0NzI4.YFjsyg.0Wbsr8MCegRQlilVCnXxRj5y7eY'

client = discord.Client()
isURL = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
isWikipedia = re.compile(
    r'(?s).*wikipedia(?s).*', re.IGNORECASE)


@client.event
async def on_ready():
    print('Logged in as {0.user}\n'.format(client))
    print(f'Watching {str(len(client.guilds))} servers:')
    for g in client.guilds:
        print(g.name)


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
        if message.content.startswith(f'{PREFIX}help') or message.content.startswith(f'{PREFIX}commands'):  # !help
            if (message.content == '!help' and len(message.content)==5)or ('!commands' and len(message.content)==9):
                await message.channel.send('Commands:\n' + 
                    'Article summary: !wiki {thoroughness (1-10)} {WikiPedia url}\n' + 
                    'Text summary: !text {thoroughness (1-10)} {Your text here}'
                )
            if 'wiki' in message.content:
                await message.channel.send('Usage: !wiki {thoroughness (1-10)} {WikiPedia url}')
            if 'text' in message.content:
                await message.channel.send('Usage: !text {thoroughness (1-10)} {Your text here}')

        if message.content.startswith(f'{PREFIX}wiki'):  # !wiki
            q = message.content.split(' ')[1:]  # Query split into a number and url
            for i in range(len(q)):
                print(i, q[i])
            valid = True;
            # Checking for invalid argument count or invalid if message is !wiki help
            if not message.content.count(' ') == 2 or message.content.startswith(f'{PREFIX}wiki help'):
                await message.channel.send('Usage: !wiki {thoroughness (1-10)} {WikiPedia url}')
                valid = False

            # Checking if thoroughness score is a number
            try:
                q[0] = int(q[0])
            except:
                await message.channel.send('The thoroughness score must be a number\n' + 
                    'Usage: !wiki {thoroughness (1-10)} {WikiPedia url}'
                )
                valid = False
            
            # Checking if the URL is valid
            if not re.match(isURL, q[1]):
                await message.channel.send("Enter a valid URL")
                valid = False

            if valid:
                try:
                    if re.match(isWikipedia, q[1]):
                        await message.channel.send(
                            summaryWikipedia(
                                q[0], q[1]
                            )
                        )
                    else:
                        await message.channel.send(
                            summaryWithoutFirst(
                                q[0], q[1]
                            )
                        )
                except Exception as e:
                    await message.channel.send(
                        'There was an error.'
                    )
                    await message.channel.send(e)

        if message.content.startswith(f"{PREFIX}text"):
            try:
                q = message.content.split(' ')[1:]
                valid = True
                if message.content.startswith(f'{PREFIX}wiki help'): 
                    await message.channel.send('Usage: !text {thoroughness (1-10)} {Your text here}')
                elif not len(q) < 3:
                    await message.channel.send('Usage: !text {thoroughness (1-10)} {Wikipedia article}. This command works best with large texts.\n' + 
                        'Enter all 3 paratmeters.'
                    )
                    valid = False
                try:
                    q[0] = int(q[0])
                except Exception as e:
                    await message.channel.send('Usage: !text {thoroughness (1-10)} {Wikipedia article}. This command works best with large texts.\n' +
                        'Enter a number for thoroughness. A default of 3 was chosen.'
                    )
                    q[0] = 3
                    
                print(q)

                if valid:
                    print('Running Algorithm')
                    await message.channel.send(
                        summary(
                            q[0], " ".join(q[1:])
                        )                    
                    )
            except Exception as e:
                print(e)
            

        if message.content.startswith(f"{PREFIX}spamgyan"):
            for i in range(30):
                await message.channel.send("hi gyan")

        if message.content.startswith(f"{PREFIX}spamrathul"):
            await message.channel.send("no")
    except Exception as e:
        print(e)


client.run(TOKEN)