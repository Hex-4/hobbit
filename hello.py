import discord
import os # default module
from dotenv import load_dotenv
from tinydb import TinyDB, Query

load_dotenv() # load all the variables from the env file
bot = discord.Bot()
db = TinyDB('db.json')
lookup = Query()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("erm what the sigma")

@bot.slash_command(name="start", description="Start earning Merits!")
async def start(ctx: discord.ApplicationContext):
    if db.search(lookup.id == ctx.author.id):
        await ctx.respond("You have already joined the Merit system!")
    else:
        db.insert({'id': ctx.author.id, 'merits': 50})
        await ctx.respond(f"<:Checkmark:1313714877772337233> You have joined the Merit system! Here's 50 <:Merit:1312943394854670398> to get you started. Earn more Merits by participating  in community events! Use `/merits` to check your balance.")

@bot.slash_command(name="grant", description="Grant merits to a user. Admin only.")
async def grant(ctx: discord.ApplicationContext, user: discord.Option(discord.SlashCommandOptionType.user), amount: discord.Option(int)):
    if db.search(lookup.id == 1043961200662286347) == ctx.author:
        db.update({'merits': db.search(lookup.id == user.id)[0].get('merits') + amount}, lookup.id == user.id)
        await ctx.respond(f"<:Checkmark:1313714877772337233> You have granted {user.name} {amount} <:Merit:1312943394854670398>.")
    else:
        await ctx.respond(f"This command is admin only! Use `/merits` to check your balance.")

@bot.command(name="merits", description="Check how many Merits you have")
async def merits(ctx, user: discord.Option(discord.SlashCommandOptionType.user)):
    
    if db.search(lookup.id == user.id):
        balance = db.search(lookup.id == user.id)[0].get('merits')
        await ctx.respond(f"{user.mention} has {balance} <:Merit:1312943394854670398>!")
    else:
        await ctx.respond(f"{user.mention} has not joined the Merit system! Run `/start` to join.")

bot.run(os.getenv('TOKEN')) # run the bot with the token
