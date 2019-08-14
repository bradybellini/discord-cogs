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
        embed = discord.Embed(colour=int(data['color'].strip('#'), 16))
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_image(url=f"{data['urls']['regular']}")
        embed.set_author(name=f"Photo by {data['user']['name']} on Unsplash", url=f"{data['user']['links']['html']}")
        embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}') #add your own bot name and profile image if you prefer
        embed.add_field(name="Photo Downloads", value=f"`{data['downloads']}`", inline=True)
        embed.add_field(name="Photo Likes", value=f"`{data['likes']}`", inline=True)
        try:
            embed.add_field(name="Photo Location", value= f"`{data['location']['city']}, {data['location']['country']}`", inline=True)
        except:
            embed.add_field(name="Photo Location", value= f"`No Location Provided`", inline=True)

        await ctx.send(embed=embed)
        
    @unsplash.command()
    async def profile(self, ctx, username=None):
        if username == None:
            embed = discord.Embed(colour=0xffffff, description="No username was provided")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name="Something is not right...")
            embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}')
            await ctx.send(embed=embed)
        else:
            try:
                url = f'https://api.unsplash.com/users/{username}'
                r = requests.get(url, headers=self.headers)
                data = r.json()
                embed = discord.Embed(colour=0x845169, description=f"{data['bio']}")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=f"{data['profile_image']['small']}")
                embed.set_author(name=f"{data['name']} on Unsplash", url=f"https://unsplash.com/@{username}", icon_url=f"{data['profile_image']['large']}")
                embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}')
                embed.add_field(name="Total Downloads", value=f"`{data['downloads']}`", inline=True) #add your own bot name and profile image if you prefer
                embed.add_field(name="Total Likes", value=f"`{data['total_likes']}`", inline=True)
                embed.add_field(name="Total Photos", value=f"`{data['total_photos']}`", inline=True)
                embed.add_field(name="Total Followers", value=f"`{data['followers_count']}`", inline=True)
                embed.add_field(name="Total Following", value=f"`{data['following_count']}`", inline=True)
                embed.add_field(name=f"{data['name']}'s Location", value=f"`{data['location']}`", inline=True)
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(colour=0xffffff, description="This user does not exist")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name="Something is not right...")
                embed.set_footer(text="Marvin", icon_url=f'{self.client.user.avatar_url}')
                await ctx.send(embed=embed)


            



def setup(client):
    client.add_cog(Unsplash(client))
    print('Unsplash API Cog loaded')
    