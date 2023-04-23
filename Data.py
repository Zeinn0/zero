from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [
        InlineKeyboardButton("❒ بدء استخراج الجلسة  ❒", callback_data="generate")
    ]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="父 العودة إلى الصفحة الرئيسية", callback_data="home")],
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [
            InlineKeyboardButton(
                "𝗦𝗼𝘂𝗿𝗰𝗲 𝗰𝗿𝗶𝘀𝘁𝗲𝗻", url="https://t.me/pp_g3"
            )
        ],
        [
            InlineKeyboardButton("كيفية استخدام البوت ?", callback_data="help"),
            InlineKeyboardButton("حـول  ❍", callback_data="about"),
        ],
        [InlineKeyboardButton("𝗗𝗘𝗩", url="https://t.me/devpokemon")],
    ]

    START = """
أهلًا {} ♦
ومرحبًا بك عزيزي في {}
هذا البوت مخصص لاستخراج الجلسات
مثل: - البايروجرام ، التيرمكس
من خلال إرسال الأيبي ايدي والأيبي هاش ورقم هاتفك والكود والتحقق بخطوتين إذا كنت مفعله
𝗗𝗘𝗩 :- @devpokemon
    """

    HELP = """
 **الأوامر المتاحة**

/about - لحول البوت
/help - لمساعدتك
/start - لبدء البوت 
/repo - لإعطاء ريبو البوت
/generate - لاستخراج الجلسات 
/cancel - لإلغاء الاستخراج 
/restart - لترسيت اليوت
"""

    # About Message
    ABOUT = """
**حول البوت** 

هذا هو بوت استخراج كود تيرمكس وبايروجرام مقدم من @pp_g3

قناة السورس : [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/pp_g3)
لغة البرمجة : [ᴘʏʀᴏɢʀᴀᴍ](docs.pyrogram.org)
اللغة : [ᴘʏᴛʜᴏɴ](www.python.org)
𝗗𝗘𝗩 : @devpokemon
    """

    # Repo Message
    REPO = """
━━━━━━━━━━━━━━━━━━━━━━━━
💥 أنا مشغل لكي أقوم باستخراج الجلسات 
┏━━━━━━━━━━━━━━━━━┓
┣★ ᯓ𓆩˹𝖕𝖔𝖐𝖊𝖒𝖔𝖓⚝➣⃟𝙎⟜⃜᷼•ᥴℛ ˼𓆪𓆃 : [اضغط هنا](https://t.me/devpokemon)
┣★ السورس [𝗦𝗼𝘂𝗿𝗰𝗲 𝗰𝗿𝗶𝘀𝘁𝗲𝗻](https://t.me/pp_g3)
┗━━━━━━━━━━━━━━━━━┛
💞 
إذا كان لديك أي سؤال ، فراسل » المطور » [𝗗𝗘𝗩] @devpokemon
   """
