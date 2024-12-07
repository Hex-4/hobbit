import discord
import os # default module
from dotenv import load_dotenv
from tinydb import TinyDB, Query
from datetime import datetime, time, timedelta, timezone
from discord.ext import tasks
import json

load_dotenv() # load all the variables from the env file
bot = discord.Bot(intents=discord.Intents.all())
db = TinyDB('db.json')
lookup = Query()

with open("market.json", mode="r", encoding="utf-8") as read_file:
     market_data = json.load(read_file)["items"]

unconfirmed_scheduled_message = None
scheduled_messages = []
shop_options = []



@bot.event
async def on_ready():
    global market_data
    print(f"{bot.user} is ready and online!")
    print(market_data)
    send_scheduled_messages.start()
    generate_shop_options(market_data)

def generate_shop_options(data):
    global shop_options
    
    for i in data:
        print(f"Name: {i["name"]}\nDesc: {i["description"]}\nValue:{i["id"]}")
        option = discord.SelectOption(label=i["name"], description=i["description"], value=i["id"])
        shop_options.append(option)
        print(f"{len(shop_options)}")
    

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
    def __init__(self, options):
        super().__init__()
        self.options = options

        # Dynamically add the select menu with the options
        self.select_menu = discord.ui.Select(
            placeholder="Choose something to buy!",
            min_values=1,
            max_values=1,
            options=self.options,
            custom_id="shop_select"  # Unique identifier for the select menu
        )
        self.select_menu.callback = self.select_callback
        self.add_item(self.select_menu)
    async def select_callback(self, interaction):  
        choice = self.select_menu.values[0]
        self.select_menu.disabled = True # set the status of the select as disabled 
        user_merits = db.search(lookup.id == interaction.user.id)[0].get('merits')



        await interaction.response.edit_message(view=self) # edit the message to show the changes
        
        if user_merits < market_data[choice]["price"]:
            await interaction.followup.send(f"You don't have enough <:Merit:1312943394854670398> Merits to buy {market_data[choice]['name']}!")
        else:
            await interaction.followup.send(f"Are you sure? This will cost you <:Merit:1312943394854670398> {market_data[choice]["price"]}, leaving you with <:Merit:1312943394854670398> {user_merits - market_data[choice]["price"]}", view=Confirmation())  # Send a new message
    

class Confirmation(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Yeah!", style=discord.ButtonStyle.green, emoji="<:checkmark:1313714877772337233>")
    async def button_callback(self, button, interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("All done!") # Send a message when the button is clicked

@bot.command(name="market", description="Buy something with your Merits!")
async def flavor(ctx: discord.ApplicationContext):
    global market_data
    global shop_options
    print(len(shop_options))
    if db.search(lookup.id == ctx.author.id):
        embed = discord.Embed(
            title="🛒 The Market",
            description="buy yourself something nice, eh?",
            color=discord.Colour.orange(),
        )
        for i in market_data:
            embed.add_field(name=f"<:Merit:1312943394854670398> {i["price"]}", value=f"**{i["name"]}**\n{i["description"]}", inline=True)
        await ctx.respond(view=Shop(shop_options), embed=embed)
    else:
        await ctx.respond(f"{ctx.author.mention} has not joined the Merit system! Run `/start` to join.")

@bot.event
async def on_reaction_add(reaction, user):
    global unconfirmed_scheduled_message
    print("reaction!")
    if user.id == 1043961200662286347 or user.id == 846855157681881118:
        if reaction.emoji == "🔜":
            print(reaction.message)
            unconfirmed_scheduled_message = reaction.message
            await reaction.message.channel.send("Confirm message schedule? It'll send at the next 8:00 AM mountain time.",view=Schedule_Confirm())

class Schedule_Confirm(discord.ui.View):
    @discord.ui.button(label="Yeah!", style=discord.ButtonStyle.green, emoji="<:checkmark:1313714877772337233>")
    async def button_callback(self, button, interaction):
        button.disabled = True
        print(unconfirmed_scheduled_message)
        scheduled_messages.append(unconfirmed_scheduled_message)
        print(scheduled_messages)
        await interaction.response.edit_message(view=self) # edit the message to show the changes
        await interaction.followup.send("<:Checkmark:1313714877772337233> All done!")




@tasks.loop(time=time(hour=15))
async def send_scheduled_messages():
    print("sending scheduled messages!")
    events = bot.get_channel(1313658666918084678)
    for m in scheduled_messages:
        if m.attachments:
            file = await m.attachments[0].to_file()
            await events.send(f"{m.content}", file=file)
        else:
            await events.send(f"{m.content}")
        scheduled_messages.remove(m)
    

bot.run(os.getenv('TOKEN')) # run the bot with the token
