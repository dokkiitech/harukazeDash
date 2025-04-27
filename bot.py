import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from game_logic import handle_dash, handle_chase

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix="/", 
    intents=intents,
    activity=discord.Game("Dash and Chase!!")
)

@bot.event
async def on_ready():
    await bot.tree.sync()  # 自動生成された tree を使う
    print(f"Logged in as {bot.user.name}")
    # print(f"Bot ID: {bot.user.id}") #debug

@bot.tree.command(name="dash", description="逃走にチャレンジ！")
async def dash(interaction: discord.Interaction):
    user = interaction.user
    success, coins = handle_dash(user.id)
    if success == 1:
        await interaction.response.send_message(f"🏃‍♂️ {user.display_name} は逃げ切った！ +10コイン（現在: {coins}）")
    else:
        await interaction.response.send_message(f"😵 {user.display_name} は捕まった… -5コイン（現在: {coins}）")

@bot.tree.command(name="chase", description="誰かを追跡する！")
@app_commands.describe(target="追いかけたい相手")
async def chase(interaction: discord.Interaction, target: discord.User):
    user = interaction.user
    target = await bot.fetch_user(target.id)

    if target.bot == True:
        await interaction.response.send_message("🤖 ボットを追跡することはできません！")
        return

    success, chaser_coins, target_coins = handle_chase(user.id, target.id)
    if success:
        await interaction.response.send_message(
            f"🚨 {user.display_name} が {target.display_name} を捕まえた！！+10コイン（現在: {chaser_coins}）"
            f"{target.display_name} は -10コイン（現在: {target_coins}）"
        )
    else:
        await interaction.response.send_message(
            f"😅 {user.display_name} は {target.display_name}の追跡に失敗した… -15コイン（現在:{chaser_coins}）"
            f"{target.display_name} は +15コイン（現在:{target_coins}）"
        )

bot.run(TOKEN)