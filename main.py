import discord
from discord.ext import commands
import json
import re

# Load config
with open("config.json") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
PREFIX = config["PREFIX"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

FAKE_LTC_RATE = 85.0  # Example rate: $85 = 1 LTC

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def tip(ctx, member: discord.Member, amount_str: str, coin: str):
    # Match "10$" format
    match = re.match(r"(\d+(?:\.\d+)?)\$", amount_str)
    if not match:
        await ctx.send("Please use the format like `10$`.")
        return

    usd = float(match.group(1))
    ltc = round(usd / FAKE_LTC_RATE, 4)

    # Reply with fake tip.cc message
    response = f"{ctx.author.mention} sent {member.mention} {ltc} LTC (≈ ${usd:.2f})."
    await ctx.reply(response)

bot.run(TOKEN)
