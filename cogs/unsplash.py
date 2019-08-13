import discord
import requests
import datetime
from discord.ext import commands

class Unsplash(commands.Cog, name='Unsplash API Cog'):

    def __init__(self, client):
        self.client = client
        self.client_id = "unsplash api key goes here"
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Client-ID {self.client_id}' }

    @commands.group(invoke_without_command=True)
    async def unsplash(self, ctx):
        pass #Can put command or message detailing sub-commands for unsplash

    @unsplash.command()
    async def random(self, ctx):
        url = f'https://api.unsplash.com/photos/random'
        r = requests.get(url, headers=self.headers)
        data = r.json()
        embed = discord.Embed(colour=0xffffff)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_image(url=f"{data['urls']['regular']}")
        embed.set_author(name=f"Photo by {data['user']['name']} on Unsplash", url=f"{data['user']['links']['html']}")
        embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}')
        embed.add_field(name="Photo Downloads", value=f"`{data['downloads']}`", inline=True)
        embed.add_field(name="Photo Likes", value=f"`{data['likes']}`", inline=True)
        try:
            embed.add_field(name="Photo Location", value= f"`{data['location']['city']}, {data['location']['country']}`", inline=True)
        except:
            embed.add_field(name="Photo Location", value= f"`No Location Provided`", inline=True)

        await ctx.send(embed=embed)
        
    @unsplash.command()
    async def profile(self, ctx, username=None):
        if not username == None:
            pass



def setup(client):
    client.add_cog(Unsplash(client))
    print('Unsplash API Cog loaded')
    
