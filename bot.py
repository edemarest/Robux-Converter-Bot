import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
import threading

# Load bot token directly from Railway environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Define conversion rate (1000 Robux = $3.5 USD)
ROBUX_TO_USD_RATE = 3.5 / 1000

# Supported currencies and their exchange rates relative to USD
CURRENCY_EXCHANGE_RATES = {
    "USD": 1.0,  # US Dollar ($)
    "EUR": 0.85,  # Euro (€)
    "JPY": 110.0,  # Japanese Yen (¥)
    "GBP": 0.75,  # British Pound Sterling (£)
    "AUD": 1.35,  # Australian Dollar (A$)
    "CAD": 1.25,  # Canadian Dollar (C$)
    "CHF": 0.92,  # Swiss Franc (CHF)
    "CNY": 6.45,  # Chinese Yuan (¥)
    "HKD": 7.75,  # Hong Kong Dollar (HK$)
    "NZD": 1.4,  # New Zealand Dollar (NZ$)
    "SEK": 8.6,  # Swedish Krona (kr)
    "KRW": 1150.0,  # South Korean Won (₩)
    "SGD": 1.36,  # Singapore Dollar (S$)
    "NOK": 8.5,  # Norwegian Krone (kr)
    "MXN": 20.0  # Mexican Peso (MX$)
}

# Currency symbols mapping
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "CNY": "¥",
    "HKD": "HK$",
    "NZD": "NZ$",
    "SEK": "kr",
    "KRW": "₩",
    "SGD": "S$",
    "NOK": "kr",
    "MXN": "MX$",
    "R$": "R$"  # Robux symbol
}

# Keep-alive web server to prevent Railway from stopping the bot
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200  # Ensure HTTP 200 Response

def run():
    """Runs the keep-alive web server."""
    app.run(host="0.0.0.0", port=8080, debug=False)

def keep_alive():
    """Starts the keep-alive server in a separate thread."""
    server = threading.Thread(target=run, daemon=True)
    server.start()

# Initialize bot with intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready."""
    print(f"Logged in as {bot.user}")

    # Sync commands for slash commands to work
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

def format_number(value):
    """Format number with commas (e.g., 1000000 -> 1,000,000)."""
    return f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"

def convert_usd_to_currency(usd_amount, currency_code):
    """Convert USD to the specified currency."""
    rate = CURRENCY_EXCHANGE_RATES.get(currency_code.upper())
    if rate:
        return usd_amount * rate
    return None

def convert_currency_to_usd(amount, currency_code):
    """Convert the specified currency to USD."""
    rate = CURRENCY_EXCHANGE_RATES.get(currency_code.upper())
    if rate:
        return amount / rate
    return None

# /robux2money command
@bot.tree.command(name="robux2money",
                  description="Convert Robux to real-world currency.")
@app_commands.describe(robux="Amount of Robux",
                       currency="Currency code (default: USD)")
async def robux2money(interaction: discord.Interaction,
                      robux: int,
                      currency: str = "USD"):
    """Converts Robux to money value based on the given rate."""
    currency = currency.upper()

    if currency not in CURRENCY_EXCHANGE_RATES:
        recognized_currencies = ", ".join(CURRENCY_EXCHANGE_RATES.keys())
        await interaction.response.send_message(
            f"❌ This bot does not recognize `{currency}`. Defaulted to **USD**.\n✅ Recognized currencies: {recognized_currencies}."
        )
        currency = "USD"

    # Convert Robux to USD
    usd_value = robux * ROBUX_TO_USD_RATE

    # Convert USD to the specified currency
    converted_value = convert_usd_to_currency(usd_value, currency)
    currency_symbol = CURRENCY_SYMBOLS.get(currency, currency)

    if converted_value is not None:
        await interaction.response.send_message(
            f"💰 **{format_number(robux)} R$** is approximately **{currency_symbol}{format_number(converted_value)}** in DevEx rates."
        )
    else:
        await interaction.response.send_message(
            f"⚠️ Conversion for `{currency}` is not available. Please try again later."
        )

# /money2robux command
@bot.tree.command(name="money2robux",
                  description="Convert real-world currency to Robux.")
@app_commands.describe(amount="Amount of money",
                       currency="Currency code (default: USD)")
async def money2robux(interaction: discord.Interaction,
                      amount: float,
                      currency: str = "USD"):
    """Converts money to Robux value based on the given rate."""
    currency = currency.upper()

    if currency not in CURRENCY_EXCHANGE_RATES:
        recognized_currencies = ", ".join(CURRENCY_EXCHANGE_RATES.keys())
        await interaction.response.send_message(
            f"❌ This bot does not recognize `{currency}`. Defaulted to **USD**.\n✅ Recognized currencies: {recognized_currencies}."
        )
        currency = "USD"

    # Convert the specified currency to USD
    usd_value = convert_currency_to_usd(amount, currency)
    currency_symbol = CURRENCY_SYMBOLS.get(currency, currency)

    if usd_value is not None:
        # Convert USD to Robux
        robux_value = usd_value / ROBUX_TO_USD_RATE
        await interaction.response.send_message(
            f"💰 **{currency_symbol}{format_number(amount)}** is approximately **{format_number(int(robux_value))} R$** in DevEx rates."
        )
    else:
        await interaction.response.send_message(
            f"⚠️ Conversion for `{currency}` is not available. Please try again later."
        )

# Ping command for basic testing
@bot.command()
async def ping(ctx):
    """Simple ping command to check bot responsiveness."""
    await ctx.send("🏓 Pong!")

# Keep the bot alive using the Flask web server
keep_alive()

# Run the bot using the token from Railway Environment Variables
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ BOT_TOKEN not found. Make sure to add it to Railway Variables.")
