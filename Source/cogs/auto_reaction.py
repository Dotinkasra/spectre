import discord
from discord import app_commands
from discord.ext import commands
import emoji

from Source.env.config import Config
from Source.module.sub_commands import subcommands
from Source.module.cllm import ConnectLLM

from datetime import timedelta, timezone, datetime
import base64, io
from PIL import Image

config = Config()

admin = config.admin
notification = config.notification

class AutoReaction(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.cllm = ConnectLLM()
        self.ctx_menu = app_commands.ContextMenu(name="AddReaction", callback=self.add_reaction)
        self.bot.tree.add_command(self.ctx_menu)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : AutoReaction')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        target_text_channel = config.llm_target_channel

        if message.channel.id not in target_text_channel:
            return
    
        if message.attachments is None:
            return
        
        await self.do_add_emoji(message)

    async def add_reaction(self, interaction: discord.Interaction, message: discord.Message):
        if message.attachments is None or len(message.attachments) <= 0:
            await interaction.response.send_message("画像が添付されていないメッセージです。 ", ephemeral=True)
        else:
            await interaction.response.defer(ephemeral=True)
            res = await self.do_add_emoji(message)
        
        if res:
            await interaction.followup.send("追加しました", ephemeral=True)

        await interaction.send_message("追加に失敗しました", ephemeral=True)

    async def do_add_emoji(self, message: discord.Message):
        if 'image' not in message.attachments[0].content_type:
            return

        img = await message.attachments[0].read()
        with Image.open(io.BytesIO(img)) as image:
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='PNG')
            png_bytes = output_buffer.getvalue()
            print("ollamaへレスポンス送信")
            result = self.cllm.get_reaction(base64.b64encode(png_bytes).decode('utf-8'))
            print("ollamaのレスポンスを確認：" + result)

            if result is None:
                return
            
            for s in result:
                if emoji.emoji_count(s) == 1:
                    await message.add_reaction(s)
                else:
                    continue
                
        return True
        

def setup(bot):
    return bot.add_cog(AutoReaction(bot))