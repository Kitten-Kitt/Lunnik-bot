"""
🌙 LUNNIK BOT — v1.0
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from datetime import date
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

OWNER_ID = 1024616230012858379
DATA_FILE = "data.json"

# ─────────────────────────────────────────
# ДАННЫЕ
# ─────────────────────────────────────────

def load_data() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────
# ЛУННЫЙ ЦИКЛ
# ─────────────────────────────────────────

def get_moon_phase() -> tuple[str, str, str]:
    base = date(2000, 1, 6)
    today = date.today()
    days = (today - base).days % 29

    if days < 3:
        return "🌑", "Новолуние", "Тишина и новые начала. Время загадывать желания."
    elif days < 8:
        return "🌒", "Растущий серп", "Энергия нарастает. Твои планы обретают форму."
    elif days < 11:
        return "🌓", "Первая четверть", "Момент решений. Луна смотрит на тебя в упор."
    elif days < 15:
        return "🌔", "Прибывающая луна", "Сила достигает пика. Всё возможно."
    elif days < 18:
        return "🌕", "Полнолуние", "Пик. Тайны раскрываются. Будь осторожен с мыслями."
    elif days < 22:
        return "🌖", "Убывающая луна", "Время отпустить лишнее. Очищение."
    elif days < 26:
        return "🌗", "Последняя четверть", "Подведение итогов. Луна подсчитывает твои поступки."
    else:
        return "🌘", "Старый серп", "Последний шёпот перед тьмой. Слушай внимательно."

# ─────────────────────────────────────────
# ОРАКУЛ
# ─────────────────────────────────────────

ORACLE_ANSWERS = [
    ("🌑 Тьма перед рассветом.", "Луна прячет ответ — он придёт сам, когда ты перестанешь искать."),
    ("🌕 Да, но цена скрыта в тени.", "Полнолуние говорит: путь открыт, но смотри под ноги."),
    ("⭐ Звёзды молчат об этом.", "Вопрос слишком мал для неба. Ответ внутри тебя."),
    ("🔮 Туман не рассеется скоро.", "Терпение — единственный ключ к этой двери."),
    ("🌊 Прилив меняет берега.", "То, что ты ищешь, уже движется к тебе."),
    ("🕯️ Огонь указывает на север.", "Следуй за тем, что пугает больше всего."),
    ("🌙 Луна говорит: нет.", "Не сейчас. Момент ещё не созрел."),
    ("✨ Три знака подтвердят это.", "Жди. Вселенная уже выслала гонца."),
    ("🦉 Сова видит то, что скрыто.", "Ответ есть, но ты задаёшь не тот вопрос."),
    ("🌿 Корни глубже, чем кажется.", "Начало этой истории — не там, где ты думаешь."),
]

# ─────────────────────────────────────────
# МАСКИ
# ─────────────────────────────────────────

MASKS = {
    "мудрец": {
        "emoji": "🧙", "name": "Мудрец",
        "greeting": "Я видел тысячу лун. Спрашивай, смертный.",
        "style": "Говорит медленно, весомо. Использует метафоры.",
    },
    "шут": {
        "emoji": "🃏", "name": "Шут",
        "greeting": "О, новая жертва! То есть... друг. Привет, друг!",
        "style": "Саркастичный, остроумный.",
    },
    "детектив": {
        "emoji": "🔍", "name": "Детектив",
        "greeting": "Итак. У нас есть подозреваемый. Это ты. Рассказывай.",
        "style": "Задаёт вопросы, анализирует, подозревает всех.",
    },
}

# ─────────────────────────────────────────
# БОТ
# ─────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"🌙 Lunnik запущен как {bot.user}")
    print(f"   Серверов: {len(bot.guilds)}")

# ─────────────────────────────────────────
# /луна
# ─────────────────────────────────────────

@tree.command(name="луна", description="Узнать текущую фазу луны и её послание")
async def moon_cmd(interaction: discord.Interaction):
    emoji, name, message = get_moon_phase()
    embed = discord.Embed(
        title=f"{emoji} {name}",
        description=f"*{message}*",
        color=0x7c3aed,
    )
    embed.set_footer(text=f"🌙 Lunnik • {date.today().strftime('%d.%m.%Y')}")
    await interaction.response.send_message(embed=embed)

# ─────────────────────────────────────────
# /оракул
# ─────────────────────────────────────────

@tree.command(name="оракул", description="Задай вопрос — Луна ответит")
@app_commands.describe(вопрос="Твой вопрос к оракулу")
async def oracle_cmd(interaction: discord.Interaction, вопрос: str):
    answer, interpretation = random.choice(ORACLE_ANSWERS)
    moon_emoji, moon_name, _ = get_moon_phase()
    embed = discord.Embed(title="🔮 Оракул слышит тебя", color=0x4c1d95)
    embed.add_field(name="Твой вопрос", value=f"*{вопрос}*", inline=False)
    embed.add_field(name="Ответ Луны", value=f"**{answer}**", inline=False)
    embed.add_field(name="Знамение", value=interpretation, inline=False)
    embed.set_footer(text=f"{moon_emoji} Фаза: {moon_name} • Lunnik")
    await interaction.response.send_message(embed=embed)

# ─────────────────────────────────────────
# /маска
# ─────────────────────────────────────────

@tree.command(name="маска", description="Надеть маску — сменить личность бота")
@app_commands.describe(имя="мудрец / шут / детектив")
async def mask_cmd(interaction: discord.Interaction, имя: str):
    имя = имя.lower().strip()
    if имя not in MASKS:
        names = ", ".join(f"`{k}`" for k in MASKS.keys())
        await interaction.response.send_message(
            f"❌ Такой маски нет. Доступные: {names}", ephemeral=True
        )
        return

    mask = MASKS[имя]
    embed = discord.Embed(
        title=f"{mask['emoji']} Маска надета: {mask['name']}",
        description=f"*«{mask['greeting']}»*",
        color=0x7c3aed,
    )
    embed.set_footer(text=f"Стиль: {mask['style']}")
    await interaction.response.send_message(embed=embed)

# ─────────────────────────────────────────
# /летопись
# ─────────────────────────────────────────

@tree.command(name="летопись", description="Посмотреть летопись этого сервера")
async def chronicle_cmd(interaction: discord.Interaction):
    guild = interaction.guild
    created = guild.created_at.strftime("%d.%m.%Y")
    members = guild.member_count
    moon_emoji, moon_name, _ = get_moon_phase()

    embed = discord.Embed(
        title=f"📜 Летопись сервера «{guild.name}»",
        color=0x4c1d95,
    )
    embed.add_field(name="Основание", value=f"Сервер создан **{created}**", inline=False)
    embed.add_field(
        name="Сегодня",
        value=f"Жителей: **{members}**\nФаза луны: {moon_emoji} {moon_name}",
        inline=False,
    )
    embed.add_field(
        name="Запись хрониста",
        value=f"*«Этот сервер хранит истории {members} душ. Каждое слово здесь — часть летописи.»*",
        inline=False,
    )
    embed.set_footer(text="🌙 Lunnik • Летопись v1.0")
    await interaction.response.send_message(embed=embed)

# ─────────────────────────────────────────
# /помощь
# ─────────────────────────────────────────

@tree.command(name="помощь", description="Список всех команд Lunnik")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Lunnik — Команды v1.0",
        description="Бот, живущий по законам луны.",
        color=0x7c3aed,
    )
    embed.add_field(
        name="Команды",
        value=(
            "`/луна` — текущая фаза луны\n"
            "`/оракул [вопрос]` — мистический ответ\n"
            "`/маска [имя]` — сменить личность бота\n"
            "`/летопись` — история сервера\n"
            "`/помощь` — это сообщение"
        ),
        inline=False,
    )
    embed.set_footer(text="Lunnik v1.0 🌙")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ─────────────────────────────────────────
# ЗАПУСК
# ─────────────────────────────────────────

bot.run(TOKEN)
