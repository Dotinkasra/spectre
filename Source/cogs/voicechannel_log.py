from discord.ext import commands
from Source.env.config import Config
from Source.module.sub_commands import subcommands

from datetime import timedelta, timezone, datetime
import discord


config = Config()
japan_timezone = timezone(timedelta(hours=+9), 'Asia/Tokyo')


class VoiceChannelLog(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : VoiceChannelLog')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        def check_whether_enable_it(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> bool:
            ignore_channel = config.ignore_voice_channel_log
            if member.bot:
                return False
            if before.channel is not None:
                if before.channel.id in ignore_channel:
                    return False
            if after.channel is not None:
                if after.channel.id in ignore_channel:
                    return False 
            return True

        logging_channel = 1373103404838158377
        japan_time = datetime.now(japan_timezone)

        title = description = color = None
        display_avatar = member.display_avatar.url
        if before.channel is None and after.channel is not None:
            if check_whether_enable_it(member, before, after):
                title = "✅通話に参加！"
                description = f"{member.mention} さんが {after.channel.mention} に参加"
                color = 0xffbdd9

        if before.channel is not None and after.channel is None:
            if check_whether_enable_it(member, before, after):
                title = "❌通話から切断..."
                description = f"{member.mention} さんが {before.channel.mention} から落ちました"
                color = 0x87cefa

        if (title is None) or (description is None):
            return

        embed = discord.Embed(
            title = title,
            description = description,
            color = color,
            timestamp = japan_time,
        )
        embed.set_thumbnail(url = display_avatar)

        await self.bot.get_channel(logging_channel).send(
            embed = embed,
        )
        

async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceChannelLog(bot))