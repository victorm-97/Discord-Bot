import logging.handlers
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


based_role = "Femboy"

@bot.event
async def on_ready():
    print(f"We're ready to go in {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")   

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} don't use that word!")
    
    await bot.process_commands(message)

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = await discord.utils.get_role(ctx.guild.roles, name="Femboy")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {based_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Femboy")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {based_role} removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message= await ctx.send(embed=embed)
    await poll_message.add_reaction("😭")
    await poll_message.add_reaction("👍")

@bot.command
@commands.has_role(based_role)
async def cool(ctx):
    await ctx.send("Welcome to the club!")

@bot.event
async def cool_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permession to do that!")

bot.run(token)