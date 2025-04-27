import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from game_logic import handle_dash, handle_chase
import supabase
from supabase_access import get_user_data

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

@bot.tree.command(name="dash", description="逃走にチャレンジ！")
async def dash(interaction: discord.Interaction):
    user = interaction.user
    success, coins, reason = handle_dash(user.id)
    if success == 1:
        await interaction.response.send_message(f"🏃‍♂️ {user.display_name} は逃げ切った！ +5コイン（現在: {coins}）")
    else:
        await interaction.response.send_message(
            f"{reason} << {user.display_name} は捕まった… -5コイン（現在: {coins}）",
            )


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

@bot.tree.command(name="ranking", description="コインランキングを表示")
async def ranking(interaction: discord.Interaction):
    # Supabaseからランキングデータを取得
    user_data = supabase.table("users").select("*").order("coins", desc=True).limit(10).execute()

    # Embedの作成
    embed = discord.Embed(
        title="🏆 コインランキング 🏆",
        description="トップ10のプレイヤーを表示します！",
        color=discord.Color.gold()
    )

    # ランキングデータを埋め込みに追加
    for i, user in enumerate(user_data.data):
        embed.add_field(
            name=f"{i + 1}. {user['discord_id']}",
            value=f"{user['coins']} コイン",
            inline=False
        )

    # メッセージを送信
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="status", description="自分のステータスを表示")
async def status(interaction: discord.Interaction):
    user = interaction.user
    user_data = get_user_data(user.id)

    embed = discord.Embed(
        title=f"{user.display_name} のステータス",
        color=discord.Color.blue()
    )
    embed.add_field(name="コイン", value=user_data["coins"], inline=True)
    embed.add_field(name="逃走回数", value=user_data["dash_count"], inline=True)
    embed.add_field(name="逃走成功", value=user_data["dash_success"], inline=True)
    embed.add_field(name="追跡回数", value=user_data["chase_count"], inline=True)
    embed.add_field(name="追跡成功", value=user_data["chase_success"], inline=True)

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)