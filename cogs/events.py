import discord
import datetime
import sqlite3
from discord.ext import commands

class Events(commands.Cog, name='Event System Cog'):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def event(self, ctx):
        embed = discord.Embed(colour=0xffa2ce)
        embed.set_author(name="Help Module" ,icon_url=f'{self.client.user.avatar_url}')
        embed.set_footer(text="Made by brady#5078")
        embed.add_field(name="__Events__ Module", value="This module allows users to manage events in the database. \n`<>` = input optional \n`[]` = input required")
        embed.add_field(name="Available Commands", value='1. `m.event new [event date] <event description>` \n2. `m.event update [event id] [updated event date] <updated event description>` \n3. `m.event status <event id> [new event status]` \n4. `m.event delete [event id] \n5. `m.event search [query]` \n`m.event upcoming`')
        embed.add_field(name="Command Descriptions", value="""1. Adds a new event to the database. If no description is givent, it will be 'None'. 
                                                                2. Updates an event in the database. If an event id does not match or does not exist, a new event will be created with the given inputs.
                                                                3. Check and events status or update an events status
                                                                4. Delete and existing event. Note: This cannot be undone. If an event was accidentaly deleted, just make a new event with the same details.
                                                                5. Searches for events with the provided search query. Note: This searches all columns EXCEPT date added. You are able to search for the event id, status, date, description and who added the event.
                                                                6. Gets the next 3 upcoming events, if any exists.""")
        embed.add_field(name="Command Examples", value="1. `m.event new 04/23/2020 Come celebrate Brady's b-day at 3pm pst!` \n2. `m.event update 34 05/24/2021 Brady's new birthday` \n3. `m.event status 34 Event is closed` or `m.event status 34` \n4. `m.event delete 34` \n5. `m.event search 12/25/2019` \n6. `m.event upcoming`")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

#@TODO Add error handling for new and update
#@TODO Make new event func more efficient
    @event.command()
    async def new(self, ctx, event_date, *, event=None):
        date_added = datetime.datetime.now()
        status = 'upcoming'
        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        sql = ("INSERT INTO events(created_by, event_date, event, date_added, status) VALUES(?,?,?,?,?)")
        val = (str(ctx.message.author), event_date, event, date_added, status)
        cursor.execute(sql, val)
        main.commit()
        cursor.close()
        main.close()

        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        cursor.execute(f'SELECT max(id) FROM events WHERE status = "upcoming"')
        event_id = str(cursor.fetchone()).replace(',', '')
        embed = discord.Embed(colour=0xff005b, description=f"{event}")
        embed.set_author(name=f"Event id - {event_id}")
        embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name="Event added by", value=f"`{ctx.message.author}`", inline=True)
        embed.add_field(name="Date event was added", value=f"`{datetime.datetime.now().date()}`", inline=True)
        embed.add_field(name="Date of Event", value=f"`{event_date}`", inline=True)
        await ctx.send(embed=embed)
        main.commit()
        cursor.close()
        main.close()
#@TODO fix event number when result is none. It currently says the previous max id number and not the new one.
    @event.command()
    async def update(self, ctx, id, event_date, *, event=None):
        date_added = datetime.datetime.now()
        status = 'upcoming'
        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        cursor.execute(f'SELECT id FROM events WHERE id = {id}')
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO events(created_by, event_date, event, date_added, status) VALUES(?,?,?,?,?)")
            val = (str(ctx.message.author), event_date, event, date_added, status)
            cursor.execute(f'SELECT max(id) FROM events WHERE status = "upcoming"')
            event_id = str(cursor.fetchone()).replace(',', '')
            embed = discord.Embed(colour=0xff005b, description=f"{event}")
            embed.set_author(name=f"Event id - {event_id}")
            embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="Event added by", value=f"`{ctx.message.author}`", inline=True)
            embed.add_field(name="Date event was added", value=f"`{datetime.datetime.now().date()}`", inline=True)
            embed.add_field(name="Date of Event", value=f"`{event_date}`", inline=True)
            await ctx.send(embed=embed)
        elif result is not None:
            sql = ("UPDATE events SET created_by = ?, event_date = ?, event = ? WHERE id = ?")
            val = (str(ctx.message.author), event_date, event, id)
            cursor.execute(f'SELECT max(id) FROM events WHERE status = "upcoming"')
            event_id = str(cursor.fetchone()).replace(',', '')
            embed = discord.Embed(colour=0xff005b, description=f"{event}")
            embed.set_author(name=f"Event - {event_id} - Updated")
            embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="Event added by", value=f"`{ctx.message.author}`", inline=True)
            embed.add_field(name="Date event was added", value=f"`{date_added}`", inline=True)
            embed.add_field(name="Date of Event", value=f"`{event_date}`", inline=True)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        main.commit()
        cursor.close()
        main.close()

    @event.command()
    async def status(self, ctx, id=None, *, status=None):
        if id is None:
            embed = discord.Embed(colour=0xffffff, description="No event id provided")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name="Something is not right...")
            embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
            await ctx.send(embed=embed)
        else:
            main = sqlite3.connect('main.sqlite')
            cursor = main.cursor()
            try:
                cursor.execute(f'SELECT id FROM events WHERE id = {id}')
                result = cursor.fetchone()
                cursor.execute(f'SELECT status FROM events WHERE id = {id}')
                old_status = str(cursor.fetchone()).replace(',','')
            except:
                result = None
            if result is None:
                embed = discord.Embed(colour=0xffffff, description="No event exist with that id")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name="Something is not right...")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                await ctx.send(embed=embed)
            elif status is None:
                embed = discord.Embed(colour=0xff9cdd)
                embed.set_author(name=f"Event - {id} - Status")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="Status", value=f"{old_status}", inline=True)
                await ctx.send(embed=embed)
            elif result is not None:
                sql = ("UPDATE events SET status = ? WHERE id = ?")
                val = (status, id)
                embed = discord.Embed(colour=0xff9cdd)
                embed.set_author(name=f"Event - {id} - Status Updated")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="Old Status", value=f"{old_status}", inline=True)
                embed.add_field(name="New Status", value=f"('{status}')", inline=True)
                await ctx.send(embed=embed)
                cursor.execute(sql, val)
                main.commit()
            cursor.close()
            main.close()

    @event.command()
    async def delete(self, ctx, id=None):
        if id is None:
            embed = discord.Embed(colour=0xffffff, description="No event id provided")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name="Something is not right...")
            embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
            await ctx.send(embed=embed)
        else:
            main = sqlite3.connect('main.sqlite')
            cursor = main.cursor()
            cursor.execute(f'SELECT id FROM events WHERE id = {id}')
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(colour=0xffffff, description="No event exist with that id")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name="Something is not right...")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                await ctx.send(embed=embed)
            elif result is not None:
                sql = ("DELETE FROM events WHERE id = ?")
                embed = discord.Embed(colour=0xff9cdd)
                embed.set_author(name=f"Event - {id} - Deleted")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                cursor.execute(sql, (id,))
                main.commit()
            cursor.close()
            main.close()
        
    @event.command()
    async def search(self, ctx, *, query=None):
        if query is None:
            embed = discord.Embed(colour=0xffffff, description="No search query provided")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_author(name="Something is not right...")
            embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
            await ctx.send(embed=embed)   
        else:
            main = sqlite3.connect('main.sqlite')
            cursor = main.cursor()
            cursor.execute(f'''SELECT * FROM events WHERE id LIKE '%{query}%' OR event_date LIKE '%{query}%' OR event LIKE '%{query}%' 
                                OR created_by LIKE '%{query}%' OR status LIKE '%{query}%' ORDER BY event_date''')                 
            result = cursor.fetchmany(size=3)
            if not result:
                result = None
            if result is None:
                    embed = discord.Embed(colour=0xffffff, description="No event found with provided search query")
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(name="Something is not right...")
                    embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                    await ctx.send(embed=embed)
            elif result is not None:
                embed = discord.Embed(colour=0xff005b, description=f"{result[0][2]}")
                embed.set_author(name=f"Event id - {result[0][0]}")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="Event added by", value=f"`{result[0][3]}`", inline=True)
                embed.add_field(name="Date event was added", value=f"`{result[0][4]}`", inline=True)
                embed.add_field(name="Date of Event", value=f"`{result[0][1]}`", inline=True)
                embed.add_field(name="Event Status", value=f"`{result[0][5]}`", inline=True)
                await ctx.send(embed=embed)
                try:
                    embed = discord.Embed(colour=0xff005b, description=f"{result[1][2]}")
                    embed.set_author(name=f"Event id - {result[1][0]}")
                    embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.add_field(name="Event added by", value=f"`{result[1][3]}`", inline=True)
                    embed.add_field(name="Date event was added", value=f"`{result[1][4]}`", inline=True)
                    embed.add_field(name="Date of Event", value=f"`{result[1][1]}`", inline=True)
                    embed.add_field(name="Event Status", value=f"`{result[1][5]}`", inline=True)
                    await ctx.send(embed=embed)
                except:
                    pass
                try:
                    embed = discord.Embed(colour=0xff005b, description=f"{result[2][2]}")
                    embed.set_author(name=f"Event id - {result[2][0]}")
                    embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.add_field(name="Event added by", value=f"`{result[2][3]}`", inline=True)
                    embed.add_field(name="Date event was added", value=f"`{result[2][4]}`", inline=True)
                    embed.add_field(name="Date of Event", value=f"`{result[2][1]}`", inline=True)
                    embed.add_field(name="Event Status", value=f"`{result[2][5]}`", inline=True)
                    await ctx.send(embed=embed)
                except:
                    pass
            cursor.close()
            main.close()

    @event.command()
    async def upcoming(self, ctx):
        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        cursor.execute(f'''SELECT * FROM events WHERE status = 'upcoming' ORDER BY event_date ASC LIMIT 3''')                 
        result = cursor.fetchmany(size=3)
        if not result:
            result = None
        if result is None:
                embed = discord.Embed(colour=0xffffff, description="No upcoming events")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_author(name="Something is not right...")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                await ctx.send(embed=embed)
        elif result is not None:
                embed = discord.Embed(colour=0xff005b, description=f"{result[0][2]}")
                embed.set_author(name=f"Event id - {result[0][0]}")
                embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(name="Event added by", value=f"`{result[0][3]}`", inline=True)
                embed.add_field(name="Date event was added", value=f"`{result[0][4]}`", inline=True)
                embed.add_field(name="Date of Event", value=f"`{result[0][1]}`", inline=True)
                embed.add_field(name="Event Status", value=f"`{result[0][5]}`", inline=True)
                await ctx.send(embed=embed)
                try:
                    embed = discord.Embed(colour=0xff005b, description=f"{result[1][2]}")
                    embed.set_author(name=f"Event id - {result[1][0]}")
                    embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.add_field(name="Event added by", value=f"`{result[1][3]}`", inline=True)
                    embed.add_field(name="Date event was added", value=f"`{result[1][4]}`", inline=True)
                    embed.add_field(name="Date of Event", value=f"`{result[1][1]}`", inline=True)
                    embed.add_field(name="Event Status", value=f"`{result[1][5]}`", inline=True)
                    await ctx.send(embed=embed)
                except:
                    pass
                try:
                    embed = discord.Embed(colour=0xff005b, description=f"{result[2][2]}")
                    embed.set_author(name=f"Event id - {result[2][0]}")
                    embed.set_footer(text="Bot", icon_url=f'{self.client.user.avatar_url}')
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.add_field(name="Event added by", value=f"`{result[2][3]}`", inline=True)
                    embed.add_field(name="Date event was added", value=f"`{result[2][4]}`", inline=True)
                    embed.add_field(name="Date of Event", value=f"`{result[2][1]}`", inline=True)
                    embed.add_field(name="Event Status", value=f"`{result[2][5]}`", inline=True)
                    await ctx.send(embed=embed)
                except:
                    pass
        cursor.close()
        main.close()

def setup(client):
    client.add_cog(Events(client))
    print('Events Cog loaded')