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

# إلغاء أمر المساعدة الافتراضي لمنع التعارض مع alias="help"
bot = commands.Bot(command_prefix="؟", intents=intents, help_command=None)

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


# --- نظام الأزرار التفاعلية للقوانين (Ephemerally Sent) ---
class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent View لتبقى شغالّة دائماً

    @discord.ui.button(
        label="القوانين بالعربية", 
        style=discord.ButtonStyle.primary, 
        emoji="🇸🇦", 
        custom_id="rules_ar_btn_persistent"
    )
    async def rules_ar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ar_rules_text = (
            "*** Server Rules :***\n\n"
            "<:one:1462866422664269975> : **الاحترام والتعامل الحسَن**\n"
            "**عامل الجميع باحترام؛ يُمنع تمامًا السب، الإساءة، التحرش، أو أي شكل من أشكال التمييز و العنصرية.**\n"
            "**يُمنع مناقشة المواضيع السياسية والدينية لتجنب الخلافات.**\n\n"
            "<:two:1462866481061560544> : **المحتوى والملفات الشخصية**\n"
            "**يُمنع نشر أي محتوى خادش، عنيف، أو غير لائق، أو يعارض اي من قونين السيرفر.**\n"
            "**يجب أن تكون صورتك الشخصية واسمك خاليين من أي إيحاءات أو عبارات مسيئة.**\n\n"
            "<:three:1462866517996605542> : **حظر الإعلانات والسبام**\n"
            "**يُمنع تكرار الرسائل (Spam) أو المنشن العشوائي.**\n"
            "**يُمنع نشر الروابط أو الترويج لسيرفرات وصفحات خارجية دون إذن الإدارة.**\n\n"
            "<:four:1462866555342819510> : **الخصوصية والأمان**\n"
            "**حافظ على خصوصيتك ولا تشارك معلوماتك أو صورك الشخصية (السيرفر غير مسؤول عن إفشاء معلوماتك لو كانت خارج سيرفرنا).**\n"
            "**يُمنع تصوير أو نقل المحادثات الخاصة بين الأعضاء دون موافقتهم. (ملاحظة مهمة)**\n\n"
            "<:five:1462866590105075817> : **الرتب والإدارة**\n"
            "**تُمنح الرتب بناءً على التفاعل والثقة؛ يُرجى عدم طلبها من الإدارة.**\n"
            "**قرارات الإدارة نهائية، وفي حال وجود اعتراض يُقدَم عبر [التكت <#1536119621940281404> ] بأسلوب راقٍ و حضاري و محترم.**\n\n"
            "***⚠️ ملاحظة:*** **تكرار المخالفات يعرّض حسابك للإنذار، الطرد، أو الحظر النهائي (Ban).**\n"
            "**وجودك بالسيرفر يعني موافقتك الكاملة على هذه القوانين.**"
        )
        await interaction.response.send_message(ar_rules_text, ephemeral=True)

    @discord.ui.button(
        label="English Rules", 
        style=discord.ButtonStyle.secondary, 
        emoji="🇬🇧", 
        custom_id="rules_en_btn_persistent"
    )
    async def rules_en_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        en_rules_text = (
            "*** Server Rules :***\n\n"
            "<:one:1462866422664269975> : **Mutual Respect & Conduct**\n"
            "**Treat everyone with respect. Harassment, hate speech, racism, or discrimination of any kind will not be tolerated.**\n"
            "**Political and religious discussions are strictly prohibited to maintain a friendly environment.**\n\n"
            "<:two:1462866481061560544> : **Content & Profiles**\n"
            "**Do not share NSFW, graphic, or inappropriate content.**\n"
            "**Profile pictures, usernames, and statuses must remain clean and free from offensive material, or violates any of the server rules.**\n\n"
            "<:three:1462866517996605542> : **Spam & Self-Promotion**\n"
            "**Avoid messaging spam, excessive caps, or unnecessary mass mentions (@.everyone/@.here).**\n"
            "**Unsolicited self-promotion, external server links, or advertising via chat or DMs is forbidden.**\n\n"
            "<:four:1462866555342819510> : **Privacy & Safety**\n"
            "**Protect your personal information (e.g., photos, full name, address). The server is not responsible for disclosing your information if it is outside our server.**\n"
            "**Leaking private conversations, screenshots, or personal data of other members without consent is strictly banned.**\n\n"
            "<:five:1462866590105075817> : **Staff & Roles**\n"
            "**Roles are earned through trust and community participation—please do not request them.**\n"
            "**The administration's decisions are final, and in case of an objection, it should be submitted via [Support: <#1536119621940281404> ] in a classy, civilized and respectful manner.**\n\n"
            "***⚠️️ Enforcement:*** **Violating these rules will result in warnings, temporary mutes, or a permanent ban depending on severity.**\n"
            "**Joining this server implies your agreement to all rules.**"
        )
        await interaction.response.send_message(en_rules_text, ephemeral=True)


@bot.event
async def on_ready():
    bot.add_view(RulesView())
    print(f"Logged in as {bot.user} - Bot is Ready on Railway!")


# --- أمر إرسال القوانين (؟قوانين) ---
@bot.command(name="قوانين")
@commands.has_permissions(administrator=True)
async def send_rules(ctx):
    embed = discord.Embed(
        title="✨ نبذة عن السيرفر | About Server",
        description=(
            "**• بدون تعقيد رفيقي**\n"
            "هذا السيرفر هو مكان مُخصص للترفيه فقط، والمحتوى فيه عشوائي حسب مزاج المالك والأعضاء.\n"
            "يعتبر **Safe Zone**، وكل ما يدور بداخله لا يمد للواقع والجدية بصلة.\n\n"
            "لا تصير دبشة ولا تعرف القوانين، إذا أنت عربي اضغط عربي واقرأ، وإذا أنت أجنبي وذي مستحيلة اضغط على الإنجليزي."
        ),
        color=discord.Color.from_rgb(30, 31, 34)
    )

    # رابط صورة البانر
    embed.set_image(url="https://your-image-url-here.com/banner.png")

    await ctx.send(embed=embed, view=RulesView())


# --- أمر المساعدة (؟مساعده / ؟help) ---
@bot.command(name="مساعده", aliases=["help", "الأوامر", "الاوامر"])
async def help_command(ctx):
    embed = discord.Embed(
        title="🛠️ قائمة أوامر البوت | Bot Help",
        description="إليك قائمة الأوامر المتاحة واستخداماتها داخل السيرفر:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📜 **أوامر القوانين**",
        value="`؟قوانين` - لإرسال إمبد القوانين مع أزرار العرض الخفية (للإدارة فقط).",
        inline=False
    )

    embed.add_field(
        name="⚠️ **أوامر نظام التحذيرات**",
        value=(
            "`؟تحذير @user [السبب]` أو `؟لهنت` - لإعطاء تحذير للعضو وتطبيق العقوبة التلقائية.\n"
            "`؟التحذيرات @user` أو `؟تحذيراتي` - لعرض سجل التحذيرات المسجلة على العضو.\n"
            "`؟مسح_تحذيرات @user` - لمسح وتصفير جميع تحذيرات العضو (للإدارة فقط)."
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ **نظام العقوبات التلقائي (Timeout)**",
        value=(
            "• **3 تحذيرات:** عزل مؤقت لمدة **15 دقيقة**\n"
            "• **6 تحذيرات:** عزل مؤقت لمدة **30 دقيقة**\n"
            "• **9 تحذيرات فأكثر:** عزل مؤقت لمدة **ساعة واحدة**"
        ),
        inline=False
    )

    embed.set_footer(text=f"طلب بواسطة: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)


# --- أوامر نظام التحذيرات (Warnings) ---

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
