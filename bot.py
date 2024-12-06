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


class Shop(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "select something!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Sigma Cake",
                description="Sourced locally from Ohio."
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction):  
        choice = select.values[0]
        select.disabled = True # set the status of the select as disabled 

        await interaction.response.edit_message(view=self) # edit the message to show the changes
        await interaction.followup.send("Are you sure?", view=Confirmation())  # Send a new message
    

class Confirmation(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Yeah!", style=discord.ButtonStyle.green, emoji="<:checkmark:1313714877772337233>")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("All done!") # Send a message when the button is clicked

@bot.command(name="market", description="Buy something with your Merits!")
async def flavor(ctx: discord.ApplicationContext):
    if db.search(lookup.id == ctx.author.id):
        embed = discord.Embed(
            title="🛒 The Market",
            description="buy yourself something nice, eh?",
            color=discord.Colour.orange(),
        )
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        embed.add_field(name="<:Merit:1312943394854670398> 500", value="**Sigma Cake**\nSourced locally from Ohio.", inline=True)
        await ctx.respond(view=Shop(), embed=embed)
    else:
        await ctx.respond(f"{ctx.author.mention} has not joined the Merit system! Run `/start` to join.")
    

bot.run(os.getenv('TOKEN')) # run the bot with the token
