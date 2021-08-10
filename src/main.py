from exophase import Exophase
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
exo = Exophase()

@bot.command(aliases=["Hello"])
async def hello(ctx):
    await ctx.send("Hello world!")

@bot.command(aliases=["command", "cmd", "Commands", "Command", "Cmd"])
async def commands(ctx):
    await ctx.send("List of commands:```\n!hello\n!help\n!search gamename (aliases: !find gamename)\n!set gamename (aliases: !setgame gamename !set_game gamename)\n!stalk player alt1 alt2 ...```Source code:<https://github.com/mateusfavarin/PlaytimeStalkerBot/blob/main/README.md>")

@bot.command(aliases=["find", "Search", "Find"])
async def search(ctx, *args):
    await ctx.send("Games found:\n\n"+exo.find_game(args))

@bot.command(aliases=["set", "setgame", "Set_game", "Setgame", "Set"])
async def set_game(ctx, *args):
    await ctx.send(exo.set_game(args))

@bot.command(aliases="Stalk")
async def stalk(ctx, *args):
    await ctx.send(exo.stalk(args[0], args))

f = open(".TOKEN", "r")
token = f.readline()
f.close()

bot.run(token)