import re
from datetime import timedelta, timezone, datetime

import discord
from discord.ext import commands
from discord import Embed

from Source.data.banlist import BanListDataBase
from Source.env.config import Config

japan_timezone = timezone(timedelta(hours=+9), 'Asia/Tokyo')
config = Config()


class AutoBAN(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.db = BanListDataBase()
        self.admin_id = config.admin
        self.logging = config.notice_channel('auto_ban')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : AutoBAN')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if self.db.is_included_banlist(member.id): 
            await self.wrap_kick(member)
            return
        
        invite_list = await member.guild.invites()
        embeds = await self.delete_invites(invite_list)

        if embeds is not None:
            for embed in embeds:
                await self.bot.get_channel(self.logging).send(embed = embed)

    async def delete_invites(self, invites: list[discord.Invite]) -> None|list[discord.Embed]:
        embeds = []
        used_invites = [
            invite for invite in invites
            if invite.uses >= 1 and invite.inviter.id not in self.admin_id
        ]

        target_inviter_ids = {invite.inviter.id for invite in used_invites}
        
        invites_to_delete = [
            invite for invite in invites if invite.inviter.id in target_inviter_ids
        ]

        invites_to_delete = list(set(invites_to_delete))
        
        for invite in invites_to_delete:
            embeds.append(
                Embed(
                    title = "招待リンクを削除しました",
                    description = f"{invite.inviter.name}({invite.inviter.mention}) さんの招待リンクを削除しました",
                    color = 0xFF0000,
                    timestamp = datetime.now(japan_timezone),
                ).set_thumbnail(
                    url = invite.inviter.display_avatar.url
                ).add_field(
                    name="招待リンク",
                    value=invite.url
                )
            )
            await invite.delete()

        if len(embeds) > 0:
            return embeds

        return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id in self.admin_id:
            return
        embeds = await self.delete_spam(message)

        if embeds is not None:
            for embed in embeds:
                await self.bot.get_channel(self.logging).send(embed = embed)

    async def wrap_kick(self, member: discord.Member):
        embed = Embed(
            title = "🧙🏿‍♂️破アアアアアアアア！！",
            description = f"{member.mention} を除霊しました。",
            color = 0xFF0000,
            timestamp = datetime.now(japan_timezone),
        ).set_thumbnail(
            url = member.display_avatar.url
        )

        await self.bot.get_channel(self.logging).send(embed = embed)
        await member.send(embed = embed)
        await member.ban()


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoBAN(bot))