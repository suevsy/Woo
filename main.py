import os
import json
import discord
from discord.ext import commands
from datetime import timedelta

# جلب البيانات الحساسة من متغيرات البيئة في Railway
TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))  # ID روم اللوج

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# تعيين البريفكس لـ ؟ ليعمل أمر ؟قوانين
bot = commands.Bot(command_prefix="؟", intents=intents)

DATA_FILE = "warnings.json"

# --- التعامل مع ملف التحذيرات ---
def load_warnings():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_warnings(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

warnings_data = load_warnings()


# --- الأزرار التفاعلية الخاصة بالقوانين (بدون زر التكت) ---
class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # تبقى شغالة بشكل دائم (Persistent)

    @discord.ui.button(
        label="القوانين | Rules", 
        style=discord.ButtonStyle.primary, 
        emoji="📜", 
        custom_id="rules_btn_persistent"
    )
    async def rules_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "✅ **نشكرك على قراءة القوانين والالتزام بها لضمان بيئة ممتعة للجميع!**", 
            ephemeral=True
        )

    @discord.ui.button(
        label="الخريطة | Map", 
        style=discord.ButtonStyle.secondary, 
        emoji="🗺️", 
        custom_id="map_btn_persistent"
    )
    async def map_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🗺️ **تفقد روم الشاتات والقنوات للتنقل بسهولة داخل السيرفر.**", 
            ephemeral=True
        )


@bot.event
async def on_ready():
    # تسجيل الأزرار لتظل تعمل حتى لو أعيد تشغيل البوت على Railway
    bot.add_view(RulesView())
    print(f"Logged in as {bot.user} - Bot is Ready on Railway!")


# --- أمر إرسال القوانين (؟قوانين) ---
@bot.command(name="قوانين")
@commands.has_permissions(administrator=True)
async def send_rules(ctx):
    content = "@everyone"

    embed = discord.Embed(
        title="✨ نبذة عن السيرفر | About Server",
        description=(
            "**• بدون تعقيد رفيقي**\n"
            "هذا السيرفر هو مكان مُخصص للترفيه فقط، والمحتوى فيه عشوائي حسب مزاج المالك والأعضاء.\n"
            "يعتبر **Safe Zone**، وكل ما يدور بداخله لا يمد للواقع والجدية بصلة.\n\n"
            "🔹 **راجع القوانين أدناه**\n"
            "🔹 **اطّلع على الخريطة لمعرفة الشاتات وفكرتها**\n\n"
            "🔻 ──── **القوانين بالعربية** ──── 🔻\n\n"
            "<:one:1462866422664269975> : **الاحترام والتعامل الحسَن**\n"
            "• عامل الجميع باحترام؛ يُمنع تمامًا السب، الإساءة، التحرش، أو أي شكل من أشكال التمييز والعنصرية.\n"
            "• يُمنع مناقشة المواضيع السياسية والدينية لتجنب الخلافات.\n\n"
            "<:two:1462866481061560544> : **المحتوى والملفات الشخصية**\n"
            "• يُمنع نشر أي محتوى خادش، عنيف، أو غير لائق، أو يعارض أي من قوانين السيرفر.\n"
            "• يجب أن تكون صورتك الشخصية واسمك خاليين من أي إيحاءات أو عبارات مسيئة.\n\n"
            "<:three:1462866517996605542> : **حظر الإعلانات والسبام**\n"
            "• يُمنع تكرار الرسائل (Spam) أو المنشن العشوائي.\n"
            "• يُمنع نشر الروابط أو الترويج لسيرفرات وصفحات خارجية دون إذن الإدارة.\n\n"
            "<:four:1462866555342819510> : **الخصوصية والأمان**\n"
            "• حافظ على خصوصيتك ولا تشارك معلوماتك أو صورك الشخصية (السيرفر غير مسؤول عن إفشاء معلوماتك خارج السيرفر).\n"
            "• يُمنع تصوير أو نقل المحادثات الخاصة بين الأعضاء دون موافقتهم.\n\n"
            "<:five:1462866590105075817> : **الرتب والإدارة**\n"
            "• تُمنح الرتب بناءً على التفاعل والثقة؛ يُرجى عدم طلبها من الإدارة.\n"
            "• قرارات الإدارة نهائية، وفي حال وجود اعتراض يُقدَم بأسلوب راقٍ وحضاري.\n\n"
            "⚠️ **ملاحظة:** تكرار المخالفات يعرّض حسابك للإنذار، الطرد، أو الحظر النهائي (Ban).\n"
            "📌 **وجودك بالسيرفر يعني موافقتك الكاملة على هذه القوانين.**\n\n"
            "🔻 ──── **English Rules** ──── 🔻\n\n"
            "<:one:1462866422664269975> : **Mutual Respect & Conduct**\n"
            "• Treat everyone with respect. Harassment, hate speech, racism, or discrimination will not be tolerated.\n"
            "• Political and religious discussions are strictly prohibited.\n\n"
            "<:two:1462866481061560544> : **Content & Profiles**\n"
            "• Do not share NSFW, graphic, or inappropriate content.\n"
            "• Profile pictures and usernames must remain clean and appropriate.\n\n"
            "<:three:1462866517996605542> : **Spam & Self-Promotion**\n"
            "• Avoid spamming, excessive caps, or unnecessary mass mentions.\n"
            "• Unsolicited self-promotion or external server links are forbidden.\n\n"
            "<:four:1462866555342819510> : **Privacy & Safety**\n"
            "• Protect your personal information. The server is not responsible for info shared outside.\n"
            "• Leaking private conversations or personal data without consent is strictly banned.\n\n"
            "<:five:1462866590105075817> : **Staff & Roles**\n"
            "• Roles are earned through trust and activity—please do not ask for them.\n"
            "• Staff decisions are final. Objections should be submitted in a classy and civilized manner.\n\n"
            "⚠️ **Enforcement:** Violating rules will result in warnings, mutes, or a permanent ban.\n"
            "📌 **Joining this server implies your agreement to all rules.**"
        ),
        color=discord.Color.from_rgb(30, 31, 34)
    )

    # استبدل هذا الرابط برابط صورة البانر الخاصة بك
    embed.set_image(url="https://your-image-url-here.com/banner.png")

    await ctx.send(content=content, embed=embed, view=RulesView())


# --- أوامر نظام التحذيرات (Warnings) ---

# أمر إعطاء تحذير (؟تحذير أو ؟لهنت)
@bot.command(name="تحذير", aliases=["لهنت", "warn"])
@commands.has_permissions(manage_messages=True)
async def warn_user(ctx, member: discord.Member = None, *, reason: str = "بدون سبب مذكور"):
    if not member:
        await ctx.send("❌ يرجى تحديد العضو. مثال: `؟تحذير @user السبب`")
        return

    if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
        await ctx.send("❌ لا يمكنك إعطاء تحذير لعضو رتبته أعلى منك أو مساوية لك.")
        return

    user_id = str(member.id)
    
    if user_id not in warnings_data:
        warnings_data[user_id] = []

    warn_entry = {
        "reason": reason,
        "moderator": str(ctx.author),
        "time": ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    warnings_data[user_id].append(warn_entry)
    save_warnings(warnings_data)

    total_warns = len(warnings_data[user_id])
    timeout_duration = None
    timeout_str = ""

    # تطبيق نظام التايم أوت التلقائي
    if total_warns == 3:
        timeout_duration = timedelta(minutes=15)
        timeout_str = "15 دقيقة"
    elif total_warns == 6:
        timeout_duration = timedelta(minutes=30)
        timeout_str = "30 دقيقة"
    elif total_warns >= 9:
        timeout_duration = timedelta(hours=1)
        timeout_str = "ساعة واحدة"

    if timeout_duration:
        try:
            await member.timeout(timeout_duration, reason=f"تجاوز عدد التحذيرات ({total_warns} تحذيرات)")
        except Exception as e:
            print(f"Failed to timeout member: {e}")

    embed = discord.Embed(title="⚠️ تم تسجيل تحذير", color=discord.Color.gold())
    embed.add_field(name="العضو", value=member.mention, inline=True)
    embed.add_field(name="المشرف", value=ctx.author.mention, inline=True)
    embed.add_field(name="مجموع التحذيرات", value=f"**{total_warns}**", inline=True)
    embed.add_field(name="السبب", value=reason, inline=False)
    
    if timeout_str:
        embed.add_field(name="العقوبة التلقائية", value=f"عزل مؤقت (Timeout) لمدة **{timeout_str}**", inline=False)

    await ctx.send(embed=embed)

    # إرسال للوج
    if LOG_CHANNEL_ID:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            log_embed = discord.Embed(
                title="📋 سجل التحذيرات (Log)",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            log_embed.add_field(name="المخالف", value=f"{member} ({member.id})", inline=False)
            log_embed.add_field(name="الإداري", value=f"{ctx.author} ({ctx.author.id})", inline=False)
            log_embed.add_field(name="السبب", value=reason, inline=False)
            log_embed.add_field(name="إجمالي التحذيرات", value=str(total_warns), inline=True)
            if timeout_str:
                log_embed.add_field(name="العقوبة", value=f"Timeout: {timeout_str}", inline=True)
            await log_channel.send(embed=log_embed)

# أمر عرض التحذيرات (؟التحذيرات)
@bot.command(name="التحذيرات", aliases=["warns", "تحذيراتي"])
async def check_warns(ctx, member: discord.Member = None):
    target = member or ctx.author
    user_id = str(target.id)

    user_warns = warnings_data.get(user_id, [])

    if not user_warns:
        await ctx.send(f"✅ {target.mention} لا يملك أي تحذيرات مسجلة.")
        return

    embed = discord.Embed(
        title=f"📜 سجل تحذيرات {target.display_name}",
        description=f"إجمالي التحذيرات: **{len(user_warns)}**",
        color=discord.Color.orange()
    )

    for idx, warn in enumerate(user_warns, 1):
        embed.add_field(
            name=f"تحذير #{idx}",
            value=f"**السبب:** {warn['reason']}\n**بواسطة:** {warn['moderator']}\n**التاريخ:** {warn['time']}",
            inline=False
        )

    await ctx.send(embed=embed)

# أمر مسح تحذيرات عضو (؟مسح_تحذيرات)
@bot.command(name="مسح_تحذيرات", aliases=["clearwarns"])
@commands.has_permissions(administrator=True)
async def clear_warns(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("❌ يرجى تحديد العضو لمسح تحذيراته.")
        return

    user_id = str(member.id)
    if user_id in warnings_data:
        del warnings_data[user_id]
        save_warnings(warnings_data)
        await ctx.send(f"✅ تم مسح جميع تحذيرات {member.mention} بنجاح.")
    else:
        await ctx.send(f"ℹ️ {member.mention} ليس لديه أي تحذيرات لمسحها.")

if __name__ == "__main__":
    bot.run(TOKEN)
