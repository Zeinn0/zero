from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command("generate"))
async def main(_, msg):
    await msg.reply(
        "اختر الجلسة المراد استخراجها من الأسفل ",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("بايروجرام ❍", callback_data="pyrogram"),
                    InlineKeyboardButton("تليثون ❍", callback_data="telethon"),
                ]
            ]
        ),
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply(
        "تم بدء  {} استخراج الجلسة...".format(
            "Telethon" if telethon else "Pyrogram"
        )
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "أرسل الآن الخاص بك `API_ID`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "غير صالحAPI_ID(أعد المحاولة).  الخاص بك غير صالح حاول مرة أخرى.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "أرسل الآن الخاص بك `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "الآن أرسل رقم الهاتف الخاص بك`ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` قم بكتابة رقم مع رمز بلدك. \nمثال : `+96279654210`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("جاري إرسال الكود انتظر قليلًا لطفًا ♥️...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` و `API_HASH` الايبيات الخاصة بك غير صحيحة يرجى إعادة الاستخراج مرة أخرى.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` رقم الهاتف الخاص بك غير صحيح يرجى إعادة الاستخراج مرة أخرى ",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(user_id, "[ارسل الكود مثل اللي في الصورة ](https://telegra.ph/file/da1af082c6b754959ab47.jpg)»  🔍من فضلك افحص حسابك بالتليجرام وتفقد الكود من حساب إشعارات التليجرام. إذا كان\n  هناك تحقق بخطوتين( المرور ) ، أرسل كلمة المرور هنا بعد إرسال كود الدخول بالتنسيق أدناه.- إذا كانت كلمة المرور او الكود  هي\n 12345 يرجى إرسالها بالشكل التالي 1 2 3 4 5 مع وجود مسـافـات بين الارقام إذا احتجت مساعدة @devpokemon.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "لقد تجاوزت الحد الزمني 10 دقائق أعد استخراج الجلسة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            " رقم الهاتف الخاص بك غير صحيح يرجى إعادة الاستخراج مرة أخرى ",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "الكود الذي أدخلته خاطئ يرجى إعادة الإستخراج مرة أخرى",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "التحقق بخطوتين مفعل بحسابك لذا قم بإدخاله هنا لطفًا.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "لقد تجاوزت المدة الزمنية يجب عليك إعادة استخراج الجلسة مرة أخرى",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "التحقق بخطوتين الذي ادخلته خطأ يرجى إعادة الاستخراج مرة أخرى 🤍.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} كود الجلسة** \n\n`{}` \n\مستخرج من @devpokemon".format(
"تليثون" if telethon else "بايروجرام", string_session
    )
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply(
        "تم استخراج {} الجلسة. \n\nيرجى تفحص الرسائل المحفوظة! \n\nمن @devpokemon".format(
            "telethon" if telethon else "pyrogram"
        )
    )


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "تم إلغاء استخراج الجلسة!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif "/restart" in msg.text:
        await msg.reply(
            "تم ترسيت البوت!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم إلغاؤه!", quote=True)
        return True
    else:
        return False 
