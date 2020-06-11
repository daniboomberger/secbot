from discord.ext import commands
import requests
import discord
import re
import credentials


url = 'https://www.virustotal.com/vtapi/v2/url/report'
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
    targetUrl = message.content
    isUrl = re.match(regex, targetUrl)
    if isUrl:
        params = {'apikey': credentials.virusTotalToken, 'resource': targetUrl}
        resp = requests.get(url, params)
        data = resp.json()
        result = "url: {0}, timestamp: {1}, result: {2}".format(data['url'], data['scan_date'], data['scans']['Avira']['result'])
        await message.channel.send(result)

discordClient.run(credentials.discordToken)