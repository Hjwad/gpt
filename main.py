from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
from pyrogram.enums import ChatAction
import requests
import random
from random import choice
import os
import re
import asyncio
import time
from datetime import datetime
from pyrogram import enums
from pyrogram.errors import ChatWriteForbidden

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
MONGO_URL = os.environ.get("MONGO_URL", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
UPDATE_CHNL = os.environ.get("UPDATE_CHNL", "ABOUT_NOBI")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "NOBI7A")
SUPPORT_GRP = os.environ.get("SUPPORT_GRP", "ABOUT_NOBI")
BOT_NAME = os.environ.get("BOT_NAME", "CHATBOT")
START_IMG = os.environ.get("START_IMG", "")

STKR = os.environ.get("STKR")

StartTime = time.time()
Mukesh = Client(
    "chat-gpt",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

START = f"""
**๏ مرحبًا، أنا {BOT_NAME}**
**➻ روبوت محادثة مبني على الذكاء الاصطناعي.**
**──────────────────**
**➻ الاستخدام /chatbot [تشغيل/إيقاف]**
**๏ للحصول على المساعدة استخدم /help**
"""

SOURCE_TEXT = f"""
**๏ مرحبًا، أنا [{BOT_NAME}]
➻ روبوت محادثة مبني على الذكاء الاصطناعي.
──────────────────
انقر على الزر أدناه للحصول على الكود المصدري**
"""

SOURCE_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton('المصدر', callback_data='hurr')],
     [InlineKeyboardButton("الدعم", url=f"https://t.me/{SUPPORT_GRP}"), InlineKeyboardButton(text="عودة", callback_data="HELP_BACK")]]
)

SOURCE = 'https://te.legra.ph/file/ebc3fc421b8776e29ad98.mp4'
x = ["❤️", "🎉", "✨", "🪸", "🎉", "🎈", "🎯"]
g = choice(x)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in Mukesh.get_chat_members(
            chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]

MAIN = [
    [
        InlineKeyboardButton(text="المطور", url=f"https://t.me/{OWNER_USERNAME}"),
        InlineKeyboardButton(text="الدعم", url=f"https://t.me/{SUPPORT_GRP}"),
    ],
    [
        InlineKeyboardButton(
            text="أضفني",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="مساعدة وأوامر", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="كود المصدر", callback_data='source'),
        InlineKeyboardButton(text="التحديثات", url=f"https://t.me/{UPDATE_CHNL}"),
    ],
]

PNG_BTN = [
    [
        InlineKeyboardButton(
            text="أضفني",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="الدعم",
                             url=f"https://t.me/{SUPPORT_GRP}",
                             ),
    ],
]

HELP_READ = """
**الاستخدام ☟︎︎︎**
**➻ استخدم** `/chatbot on` **لتفعيل الروبوت.**
**➻ استخدم** `/chatbot off` **لإيقاف الروبوت.**
**๏ ملاحظة ➻ كلا الأمرين أعلاه لتشغيل/إيقاف الروبوت يعملان في المجموعات فقط!!**
**➻ استخدم** `/ping` **للتحقق من استجابة الروبوت.**
||©️ @NOBI7A||
"""

HELP_BACK = [
    [
        InlineKeyboardButton(text="عودة", callback_data="HELP_BACK"),
    ]
]

@Mukesh.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not UPDATE_CHNL:
        return
    try:
        try:
            await bot.get_chat_member(UPDATE_CHNL, msg.from_user.id)
        except UserNotParticipant:
            if UPDATE_CHNL.isalpha():
                link = "https://t.me/" + UPDATE_CHNL
        else:
            chat_info = await bot.get_chat(UPDATE_CHNL)
            link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo=START_IMG,
                    caption=f"حسب قاعدة البيانات الخاصة بي، لم تنضم بعد إلى [قناة التحديث]({link})، إذا كنت تريد استخدامي، انضم إلى [قناة التحديث]({link}) وابدأ من جديد!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("قناة التحديث", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"قم بترقيتي كمسؤول في قناة التحديث: {UPDATE_CHNL}!")

@Mukesh.on_message(filters.command(["start", f"start@{BOT_USERNAME}"]))
async def restart(client, m: Message):
    accha = await m.reply_text(text=f"{g}")
    await asyncio.sleep(1)
    await accha.edit("بدء...")
    await asyncio.sleep(0.5)
    await accha.edit("جاري البدء...")
    await asyncio.sleep(0.5)
    await accha.delete()
    if STKR:
        umm = await m.reply_sticker(sticker=STKR)
        await asyncio.sleep(1)
        await umm.delete()
    await m.reply_photo(
        photo=START_IMG,
        caption=START,
        reply_markup=InlineKeyboardMarkup(MAIN),
    )

@Mukesh.on_callback_query()
async def cb_handler(Client, query: CallbackQuery):
    if query.data == "HELP":
        await query.message.edit_text(
            text=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BACK),
        )
    elif query.data == "HELP_BACK":
        await query.message.edit(
            text=START,
            reply_markup=InlineKeyboardMarkup(MAIN),
        )
    elif query.data == 'source':
        await query.message.edit_text(SOURCE_TEXT, reply_markup=SOURCE_BUTTONS)
    elif query.data == 'hurr':
        await query.answer()
        await query.message.reply(SOURCE)

@Mukesh.on_message(filters.command(["help", f"help@{BOT_USERNAME}"], prefixes=["", "+", ".", "/", "-", "?", "$"]))
async def restart(client, message):
    await message.reply_photo(
        START_IMG,
        caption=HELP_READ,
        reply_markup=InlineKeyboardMarkup(HELP_BACK),
    )

@Mukesh.on_message(filters.command(['source', 'repo']))
async def source(bot, m):
    await m.reply_photo(START_IMG, caption=SOURCE_TEXT, reply_markup=SOURCE_BUTTONS, reply_to_message_id=m.id)

# التحقق من استجابة الروبوت
@Mukesh.on_message(filters.command(["ping", "alive"], prefixes=["/"]))
async def ping(client, message: Message):
    start = datetime.now()
    t = "__جاري التحقق...__"
    txxt = await message.reply(t)
    await asyncio.sleep(0.25)
    await txxt.edit_text("__جاري التحقق.....__")
    await asyncio.sleep(0.35)
    await txxt.delete()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.reply_photo(
        photo=START_IMG,
        caption=f"مرحبًا!\n**[{BOT_NAME}](t.me/{BOT_USERNAME})** قيد العمل بشكل جيد مع استجابة \n➥ `{ms}` ms\n\n**تم الإنشاء بواسطة ❣️ || [NOBITA](https://t.me/NOBI7A)||**",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )

@Mukesh.on_message(
    filters.command(["chatbot off", f"chatbot@{BOT_USERNAME} off"], prefixes=["/"])
    & ~filters.private
)
async def chatbotofd(client, message):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
                await is_admins(chat_id)
        ):
            return await message.reply_text(
                "أنت لست مسؤولاً"
            )
    is_vick = vick.find_one({"chat_id": message.chat.id})
    if not is_vick:
        vick.insert_one({"chat_id": message.chat.id})
        await message.reply_text("تم تعطيل الروبوت!")
    if is_vick:
        await message.reply_text("الروبوت معطل بالفعل")

@Mukesh.on_message(
    filters.command(["chatbot on", f"chatbot@{BOT_USERNAME} on"], prefixes=["/"])
    & ~filters.private
)
async def chatboton(client, message):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "أنت لست مسؤولاً"
            )
    is_vick = vick.find_one({"chat_id": message.chat.id})
    if not is_vick:
        await message.reply_text("الروبوت مفعل بالفعل!")
    if is_vick:
        vick.delete_one({"chat_id": message.chat.id})
        await message.reply_text("تم تفعيل الروبوت!")

@Mukesh.on_message(filters.text & filters.reply & ~filters.private & ~filters.bot)
async def vickai(client: Client, message: Message):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    is_vick = vick.find_one({"chat_id": message.chat.id})
    if not is_vick:
        if message.reply_to_message:
            if message.reply_to_message.from_user.id == BOT_ID:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)
                await asyncio.sleep(1)
                TEXT = message.text
                REPLY = await Chatbot(TEXT)
                try:
                    await message.reply_text(REPLY)
                except ChatWriteForbidden:
                    pass

@Mukesh.on_message(filters.text & filters.private & ~filters.bot)
async def vickprivate(client: Client, message: Message):
    await Mukesh.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(1)
    TEXT = message.text
    REPLY = await Chatbot(TEXT)
    try:
        await message.reply_text(REPLY)
    except ChatWriteForbidden:
        pass

async def Chatbot(TEXT):
    try:
        url = f"http://api.brainshop.ai/get?bid=175107&key=KhNdrEybX13w0GmN&uid=uid&msg={TEXT}"
        response = requests.get(url)
        data = response.json()
        return data['cnt']
    except Exception as e:
        print(f"Chatbot Error: {e}")
        return "الرجاء إعادة المحاولة لاحقًا!"

print("جاري البدء….")
Mukesh.run()