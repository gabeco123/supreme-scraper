import requests
import discord
from discord.ext import commands
from colorama import Fore, Back, Style 


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", description="Supreme-Scraper")
        

    async def on_ready(self):
        await self.change_presence(activity=discord.Game("Supreme Info"), status=discord.Status.online, afk=False)
        print(Fore.GREEN + "Bot ready")

    async def on_message(self, message):
        if message.content[:1] == "!":
            try:
                response = requests.get("https://www.supremenewyork.com/mobile_stock.json")
                supreme = response.json()
                for i in supreme["products_and_categories"][message.content[1:].title()]:
                    embed = discord.Embed(title="Product - " + str(i["name"]), description="", color=2899536)
                    embed.set_author(name='Supreme-Scraper' , url="", icon_url='')
                    embed.set_thumbnail(url="https:" + (i["image_url"]))
                    embed.add_field(name='Item-name' , value=str(i["name"]))
                    embed.add_field(name='Price', value="$" + str(i["price"]//100))
                    embed.add_field(name='ID', value=i["id"])
                    embed.add_field(name='Product-Link', value="https://supremenewyork.com/shop/" + str((i["id"])))
                    embed.set_footer(text='')
                    product_response = requests.get("https://www.supremenewyork.com/shop/{}.json".format(i["id"]))
                    product_api = product_response.json()
                    for style in product_api["styles"]:
                        for size in style["sizes"]:
                            if size["stock_level"]:
                                print(Fore.GREEN + "https://supremenewyork.com/shop/" + str(i["id"]) + " Is In Stock")
                            else:
                                print(Fore.GREEN + "https://supremenewyork.com/shop/" + str(i["id"]) + " Is Out Of Stock")
                    await message.channel.send(embed=embed)
            except:
                await message.channel.send("")

bot = Bot()



bot.run("INSERT-Your-Bot-Token-Here")
