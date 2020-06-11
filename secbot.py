from discord.ext import commands
import discord
import re
import credentials

client = discord.Client()

regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    isUrl = re.match(regex, message.content)
    if isUrl:
        await message.channel.send('url was sent!')

client.run(credentials.TOKEN)