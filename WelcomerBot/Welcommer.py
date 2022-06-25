import discord

welcome_channel_id = "Channel ID"


class Client(discord.Client):


    #Einloggen
    async def on_ready(self):
        print("Der Bot wurde erfolgreich gestartet!")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='CodeDew'))
        welcome_channel = client.get_channel(welcome_channel_id)
        await welcome_channel.send("Um das Regelwerk zu akzeptieren reagiere bitte mit ✅!")




    #Reaction-Role
    async def on_reaction_add(self, reaction, user):
        verifiziert = discord.utils.get(user.guild.roles, name="↣︱✅・VERIFIZIERUNG - ERFOLGREICH")

        if str(reaction.emoji) == "✅":
            await user.add_roles(verifiziert)




client = Client()
client.run("TOKEN")