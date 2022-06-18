import nextcord
from nextcord.ext import commands, tasks
import robloxpy
import json
from nextcord.ui import Button, View, button
import random

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix="k!", case_insensitive=True, intents=intents)
client.remove_command('help')

#get_enable_data function
async def get_enable_data():
    with open("enable.json", "r") as f:
        enable = json.load(f)

    return enable

#open_enable function
async def open_enable(mode):
    enable = await get_enable_data()
    enable["enable"] = str(mode)

    with open("enable.json", "w") as f:
        json.dump(enable, f, indent=4)

#get_id_data function
async def get_id_data():
    with open("id.json", "r") as f:
        id = json.load(f)

    return id

#add_id function
async def add_id(increment):
    id = await get_id_data()
    id["id"] += increment

    with open("id.json", "w") as f:
        json.dump(id, f, indent=4)

#get_qotd_data function
async def get_qotd_data():
    with open("qotd.json", "r") as f:
        qotd = json.load(f)

    return qotd

#add_qotd function
async def add_qotd(qotd):
    qot = await get_qotd_data()
    i = await get_id_data()
    id = int(i["id"])
    qot["list"][int(id)] = str(qotd)

    with open("qotd.json", "w") as f:
        json.dump(qot, f, indent=4)

    await add_id(1)

#remove_qotd function
async def remove_qotd(id):
    qot = await get_qotd_data()
    del qot["list"][str(id)]

    with open("qotd.json", "w") as f:
        json.dump(qot, f, indent=4)

#send_qotd loop
@tasks.loop(seconds = 86400)
async def send_qotd():
    qot = await get_qotd_data()
    mode = await get_enable_data()

    if mode["enable"] == "enabled":
        qotds = []

        for i in qot["list"]:
            qotds.append(qot["list"][i])

        if qotds != []:
            qotd = random.choice(qotds)

            with open("cookie.json", "r") as f:
                cookie = json.load(f)

            robloxpy.User.Internal.SetCookie(cookie["ROBLOX_COOKIE"])
            robloxpy.User.Groups.Internal.SendGroupShout(4662546, qotd)

#start event
@client.event
async def on_ready():
    send_qotd.start()
    print("Logged into the bot!")

#both enabled
class oui1(View):
    def __init__(self):
        super().__init__(timeout=20)
        self.value = None
        self.code = None

    @button(label="Next", style=nextcord.ButtonStyle.green)
    async def Next(self, button: Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @button(label="Back", style=nextcord.ButtonStyle.red)
    async def Back(self, button: Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def on_timeout(self):
        pass

#next disabled
class oui2(View):
    def __init__(self):
        super().__init__(timeout=20)
        self.value = None
        self.code = None

    @button(label="Next", style=nextcord.ButtonStyle.green, disabled=True)
    async def Next(self, button: Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @button(label="Back", style=nextcord.ButtonStyle.red)
    async def Back(self, button: Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def on_timeout(self):
        pass

#back disabled
class oui3(View):
    def __init__(self):
        super().__init__(timeout=20)
        self.value = None
        self.code = None

    @button(label="Next", style=nextcord.ButtonStyle.green)
    async def Next(self, button: Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @button(label="Back", style=nextcord.ButtonStyle.red, disabled=True)
    async def Back(self, button: Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def on_timeout(self):
        pass

#both disabled
class oui4(View):
    def __init__(self):
        super().__init__(timeout=20)
        self.value = None
        self.code = None

    @button(label="Next", style=nextcord.ButtonStyle.green, disabled=True)
    async def Next(self, button: Button, interaction: nextcord.Interaction):
        self.value = True
        self.stop()

    @button(label="Back", style=nextcord.ButtonStyle.red, disabled=True)
    async def Back(self, button: Button, interaction: nextcord.Interaction):
        self.value = False
        self.stop()

    async def on_timeout(self):
        pass

#list command
@client.command()
async def list(ctx):
    qot = await get_qotd_data()
    qotds = []

    for i in qot["list"]:
        qotd = qot["list"][i]
        qotds.append(qotd)

    if qotds == []:
        em = nextcord.Embed(title="The qotd list is empty! Add some qotd to the list!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    pages = len(qotds) // 7

    if len(qotds) % 7 != 0:
        pages += 1

    check = True
    current_page = 1
    label = "None"
    m = None
    m = await ctx.send("Showing the list..")

    while check:
        if current_page == 1:
            description = ""

            if int(current_page) == int(pages):
                if current_page == 1:
                    for i in range(0, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

                else:
                    for i in range((current_page-1)*7, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

            else:
                if current_page == 1:
                    for i in range(0, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"  

                else:
                    for i in range((current_page-1)*7, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"  

            em = nextcord.Embed(title="QOTD List", description=description, color=nextcord.Color.random())
            em.set_footer(text=f"Page {current_page}/{pages}")
            
            if pages == 1:
                view = oui4()

            elif current_page == 1:
                view = oui3()

            await m.edit(embed=em, view=view)
            await view.wait()

            if view.value == None:
                return

            elif view.value == True:
                label = "Next"

            elif view.value == False:
                label = "Back"
    
        if label == "Next":
            current_page += 1
            description = ""

            if int(current_page) == int(pages):
                if current_page == 1:
                    for i in range(0, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

                else:
                    for i in range((current_page-1)*7, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

            else:
                if current_page == 1:
                    for i in range(0, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"  

                else:
                    for i in range((current_page-1)*7, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"  

            em = nextcord.Embed(title="QOTD List", description=description, color=nextcord.Color.random())
            em.set_footer(text=f"Page {current_page}/{pages}")
            
            if pages == 1:
                view = oui4()

            elif current_page == 1:
                view = oui3()

            elif current_page == pages:
                view = oui2()

            else:
                view = oui1()

            await m.edit(embed=em, view=view)
            await view.wait()

            if view.value == None:
                return

            elif view.value == True:
                label = "Next"

            elif view.value == False:
                label = "Back"            

        elif label == "Back":
            current_page -= 1
            description = ""

            if int(current_page) == int(pages):
                if current_page == 1:
                    for i in range(0, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

                else:
                    for i in range((current_page-1)*7, len(qotds)):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"

            else:
                if current_page == 1:
                    for i in range(0, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n"  

                else:
                    for i in range((current_page-1)*7, current_page*7):
                        for x in qot["list"]:
                            if qot["list"][x] == qotds[i]:
                                description += f"ID {x}: {qotds[i]}\n" 

            em = nextcord.Embed(title="QOTD List", description=description, color=nextcord.Color.random())
            em.set_footer(text=f"Page {current_page}/{pages}")
            
            if pages == 1:
                view = oui4()

            elif current_page == 1:
                view = oui3()

            elif current_page == pages:
                view = oui2()

            else:
                view = oui1()

            await m.edit(embed=em, view=view)
            await view.wait()

            if view.value == None:
                return

            elif view.value == True:
                label = "Next"

            elif view.value == False:
                label = "Back"            

#add command
@client.command()
async def add(ctx, *, qotd: str = None):
    qot = await get_qotd_data()

    if qotd == None:
        em = nextcord.Embed(title="The qotd arguement is required!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    for i in qot["list"]:
        if qot["list"][i] == qotd:
            em = nextcord.Embed(title="The qotd provided is already there!", color=nextcord.Color.red())
            await ctx.send(embed=em)
            return  

    await add_qotd(qotd)
    em = nextcord.Embed(title="Successfully added the qotd to the list!", color=nextcord.Color.blurple())
    await ctx.send(embed=em)

#remove command
@client.command()
async def remove(ctx, id: int = None):
    qot = await get_qotd_data()

    if id == None:
        em = nextcord.Embed(title="The id arguement is required!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    if str(id) not in qot["list"]:
        em = nextcord.Embed(title="That's not a valid quote id!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    await remove_qotd(str(id))
    em = nextcord.Embed(title="Successfully removed the qotd to the list!", color=nextcord.Color.blurple())
    await ctx.send(embed=em)

#enableqotd command
@client.command()
async def enableqotd(ctx):
    enable = await get_enable_data()

    if enable["enable"] == "enabled":
        em = nextcord.Embed(title="The qotd system is already enabled!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    await open_enable("enabled")
    em = nextcord.Embed(title="Successfully enabled the qotd system!", color=nextcord.Color.blurple())
    await ctx.send(embed=em)

#disableqotd command
@client.command()
async def disableqotd(ctx):
    enable = await get_enable_data()

    if enable["enable"] == "disabled":
        em = nextcord.Embed(title="The qotd system is already disabled!", color=nextcord.Color.red())
        await ctx.send(embed=em)
        return

    await open_enable("disabled")
    em = nextcord.Embed(title="Successfully disabled the qotd system!", color=nextcord.Color.blurple())
    await ctx.send(embed=em)

#run event
client.run("YOUR_TOKEN_HERE") 
