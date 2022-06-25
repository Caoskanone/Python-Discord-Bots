import discord
import time
import datetime
import random
import typing
from discord.ext import commands


client = commands.Bot(
    command_prefix="!",
    help_command=None
)
intents = discord.Intents.default()
intents.members = True


@client.event
async def on_ready():
    print("Wooahhh dein Code war ohne Error, der Bot ist on!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='!help'))


@commands.has_guild_permissions()
@client.command(
    name="help",
    description="Bannt einen User.",
    help="help",

)
async def help(ctx):
    embed = discord.Embed(title="Commands-Liste",
                          description="Hier ist eine volle Command Liste von diesem Bot!",
                          color=discord.Color.dark_blue(),
                          timestamp=datetime.datetime.utcnow())

    embed.add_field(
        name="!ban @Nutzer/ID [Grund]",
        value="Dieser Command bannt einen Nutzer.",
        inline=True
    )

    embed.add_field(
        name="!kick @Nutzer/ID [Grund]",
        value="Dieser Command kickt einen Nutzer.",
        inline=True
    )

    embed.add_field(
        name="!unban @Nutzer/ID [Grund]",
        value="Dieser Command unbanned einen Nutzer. / Coming Soon",
        inline=True
    )

    embed.add_field(
        name="!mute @Nutzer/ID [Grund]",
        value="Dieser Command muted einen Nutzer.",
        inline=True
    )

    embed.add_field(
        name="!unmute @Nutzer/ID",
        value="Dieser Command unmuted einen Nutzer!",
        inline=True
    )

    embed.add_field(
        name="!userinfo @Nutzer/ID",
        value="Dieser Command zeigt dir Infos über einen Nutzer!",
        inline=True
    )

    embed.add_field(
        name="Wichtig!",
        value="Jeder der diese Commands ausführen will muss eine Rolle haben die genug Rechte hat um den jeweiligen Command auszuführen und der Bot auch!",
        inline=False
    )

    await ctx.send(embed=embed)


@commands.has_guild_permissions(ban_members=True)
@client.command(
    name="ban",
    description="Bannt einen User.",
    help="ban",

)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member is None:

        member_embed = discord.Embed(title="User nicht angegeben!",
                                     description=f"Es wurde kein User angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=member_embed)
        return



    elif reason is None:
        reason_embed = discord.Embed(title="Grund nicht angegeben!",
                                     description=f"Es wurde kein Grund angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=reason_embed)
        return

    embed = discord.Embed(title="Erfolgreich gebannt!",
                          description=f"Der User {member.mention} wurde erfolgreich gebannt!",
                          color=discord.Color.dark_blue(),
                          timestamp=datetime.datetime.utcnow())

    await ctx.send(embed=embed)
    await member.ban(reason=reason)


@commands.has_guild_permissions(kick_members=True)
@client.command(
    name="kick",
    description="Kickt einen User.",
    help="kick",
)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member is None:
        member_embed = discord.Embed(title="User nicht angegeben!",
                                     description=f"Es wurde kein User angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow()
                                     )
        await ctx.send(embed=member_embed)
        return



    elif reason is None:
        reason_embed = discord.Embed(title="Grund nicht angegeben!",
                                     description=f"Es wurde kein Grund angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=reason_embed)
        return

    embed = discord.Embed(title="Erfolgreich gekickt!",
                          description=f"Der User {member.mention} wurde erfolgreich gekickt!",
                          color=discord.Color.dark_blue(),
                          timestamp=datetime.datetime.utcnow())

    await ctx.send(embed=embed)
    await member.ban(reason=reason)


@commands.has_guild_permissions(administrator=True)
@client.command(
    name="unban",
    description="Unbanned einen User.",
    help="unban",
)
async def unban(ctx, *, member):
    pass


@commands.has_guild_permissions(kick_members=True, ban_members=True)
@client.command(
    name="mute",
    description="Muted einen User.",
    help="mute",
)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,
                                          read_messages=False)

    if member is None:
        member_embed = discord.Embed(title="User nicht angegeben!",
                                     description=f"Es wurde kein User angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow()
                                     )
        await ctx.send(embed=member_embed)
        return



    elif reason is None:
        reason_embed = discord.Embed(title="Grund nicht angegeben!",
                                     description=f"Es wurde kein Grund angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=reason_embed)
        return

    await member.add_roles(mutedRole, reason=reason)
    embed1 = discord.Embed(title="Erfolgreich gemuted!",
                           description=f"Der User {member.mention} wurde erfolgreich gemuted!",
                           color=discord.Color.dark_blue(),
                           timestamp=datetime.datetime.utcnow())
    await ctx.send(embed=embed1)
    await member.send(f"Du wurdest auf dem Server {guild.name} für {reason} gemuted!")


@commands.has_guild_permissions(ban_members=True, kick_members=True)
@client.command(
    name="unmute",
    description="Unmuted einen User.",
    help="unmute"
)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    if member is None:
        member_embed = discord.Embed(title="User nicht angegeben!",
                                     description=f"Es wurde kein User angegeben!",
                                     color=discord.Color.dark_blue(),
                                     timestamp=datetime.datetime.utcnow()
                                     )
        await ctx.send(embed=member_embed)
        return

    await member.remove_roles(mutedRole)
    embed1 = discord.Embed(title="Erfolgreich entmuted!",
                           description=f"Der User {member.mention} wurde erfolgreich entmuted!",
                           color=discord.Color.dark_blue(),
                           timestamp=datetime.datetime.utcnow())

    await ctx.send(embed=embed1)
    await member.send(f"Du wurdest entmuted auf dem Server {ctx.guild.name}!")


@commands.has_guild_permissions(administrator=True)
@client.command(
    name="userinfo",
    description="Zeigt dir alle Infos über einen User.",
    help="userinfo"
)
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f'{member}', description=f'{member.mention}', color=discord.Color.dark_blue(),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name='**Benutzername:**', value=member.name, inline=False)
    embed.add_field(name='**Tag:**', value=member.discriminator, inline=False)
    embed.add_field(name='**ID:**', value=member.id, inline=False)
    embed.add_field(name='**Status:**', value=member.status, inline=False)
    embed.add_field(name="**Höchste Rolle:**", value=member.top_role, inline=False)
    embed.add_field(name='**Account erstellt:**', value=member.created_at.__format__('%A, %d. %B %Y | %H:%M:%S'),
                    inline=False)
    embed.add_field(name='**Server gejoint:**', value=member.joined_at.__format__('%A, %d. %B %Y | %H:%M:%S'),
                    inline=False)
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(content=None, embed=embed)


client.run("TOKEN")





