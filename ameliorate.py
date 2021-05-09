# DISCORD MODULES
import discord
from discord.ext import commands
from discord import User

# OTHER REQUIRED MODULES
import json
from PIL import Image, ImageDraw, ImageFont
import io

# client = discord.Client()
client = commands.Bot(command_prefix='_')

# EVENTS


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if not message.author.bot:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        if message.content == "_ideas" or message.content == "_projects" or message.content == "_quotes":
            await add_experience(users, message.author, 5)

        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
             json.dump(users, f)

    await client.process_commands(message)


async def update_data(users, user):

    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


# COMMANDS
@client.command()
async def ideas(ctx):

    channel = ctx.channel
    await channel.send("Recording Ideas")

    def check(m):
        return m.channel == channel and m.author == ctx.author

    def record_ideas(idea, user):
        with open('Ideas.txt', 'a') as ideas:
            print(f"{idea}-{user}", file=ideas)

    msg = await client.wait_for("message", check=check)  # take this data and store in text file.
    print(f'{msg.content}')  # try using .content
    record_ideas(msg.content, msg.author)
    await channel.send(f"Successfully recorded {msg.author.mention}", mention_author=True)


@client.command()
async def projects(ctx):
    channel = ctx.channel
    await channel.send("Recording Project Ideas")

    def check(m):
        return m.channel == channel and m.author == ctx.author

    def record_ideas(project_idea, user):
        with open('ProjectIdeas.txt', 'a') as project_ideas:
            print(f"{project_idea}-{user}", file=project_ideas)

    msg = await client.wait_for("message", check=check)  # take this data and store in text file.
    print(f'{msg.content}')  # try using .content
    record_ideas(msg.content, msg.author)
    await channel.send(f"Successfully recorded {msg.author.mention}", mention_author=True)


@client.command()
async def quotes(ctx):
    channel = ctx.channel
    await channel.send("Recording Quotes")

    def check(m):
        return m.channel == channel and m.author == ctx.author

    def record_ideas(quote, user):
        with open('Quotes.txt', 'a') as quotes:
            print(f"{quote}-{user}", file=quotes)

    msg = await client.wait_for("message", check=check)  # take this data and store in text file.
    print(f'{msg.content}')  # try using .content
    record_ideas(msg.content, msg.author)
    await channel.send(f"Successfully recorded {msg.author.mention}", mention_author=True)


@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        embed = discord.Embed(description=f"{ctx.message.author.mention}You are at level {lvl} ")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        embed = discord.Embed(description=f"{ctx.message.author.mention}You are at level {lvl} ")
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


@client.command()
async def rank(ctx, member: discord.Member = None):
    try:
        id = member.id
    except:
        id = ctx.message.author.id

    with open('users.json', 'r') as f:
        users = json.load(f)
    lvl = users[str(id)]['level']
    xp = users[str(id)]["experience"]                  # add if else statement to show message if user has 0xp.
    boxes = int((xp/(200*((1/2)*lvl)))*20)             # ("YOU HAVENT GIVEN ANY IDEAS,QUOTES,PROJECTS
    # give the respective to earn points")
    # rank = int(users[str(id)]['experience'].sort())
    embed = discord.Embed(description=f"{ctx.message. author.mention}'s Stats")
    embed.add_field(name="NAME", value=ctx.message.author.mention, inline=True)
    embed.add_field(name="LEVEL", value=lvl, inline=True)
    embed.add_field(name="XP", value=xp, inline=True)
    # embed.add_field(name="RANK",value=,inline=True)
    embed.add_field(name="PROGRESS", value=boxes*":blue_square:"+(20-boxes)*":white_large_square:", inline=False)

    embed.set_thumbnail(url=ctx.message.author.avatar_url)

    await ctx.send(embed=embed)


client.run('ODM3NjkzMjIyMjg5NTM5MDgy.YIwQmw.ZP4bwr1k4aKFDTKonr_MeF2xoyQ')
