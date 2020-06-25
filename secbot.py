from discord.ext import commands
import requests
import discord
import re
import credentials


checking_URL = 'https://www.virustotal.com/vtapi/v2/url/report'
discordClient = discord.Client()

dictionary = dict()
regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ip
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordClient))

@discordClient.event
async def on_message(message):
    splitted_message = message.content.split(' ')
    for i in range(len(splitted_message)):    
        result = handleMessage(splitted_message[i])
        if result != None:
            await message.channel.send(f"detected: {result}")

def handleMessage(message_content):
    isUrl = re.match(regex, message_content)
    if isUrl:
        params = {'apikey': credentials.virusTotalToken, 'resource': message_content}
        result = getVirusTotalData(checking_URL, params)
        return result  

def getVirusTotalData(url, params):
    try:
        data = requests.get(url, params).json()
        return data['positives']
    except: 
        print('couldnt reach virustotal')


discordClient.run(credentials.discordToken)