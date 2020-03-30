import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!')

DataPlayers = {}

#При запуске проводим инициализацию и если в logs будут значени добовляем их в DataPlayers
@bot.event
async def on_ready():
    print('Ready!')
    i = 0
    while i < len(bot.users):
        DataPlayers.update({"<" + "@" + "!" + str(bot.users[i].id) + ">": 0})
        i = i + 1
    await load()

#При подключении нового пользователя добовяем его в DataPlayers
@bot.event
async def on_member_join(member):
    DataPlayers.update({"<" + "@" + "!" + str(member.id) + ">": 0})
    await save(DataPlayers)

#При отключении шлем пользователя нахой и удаляем его счёт
@bot.event
async def on_member_remove(member):
    del DataPlayers["<" + "@" + "!" + str(member.id) + ">"]
    await save(DataPlayers)

#Инициализация-Присваиваем каждому пользователю счёт(defolt=0)
@bot.command()
@commands.has_permissions(administrator=True)
async def initialization(ctx):
    i = 0
    while i < len(bot.users):
        DataPlayers.update({"<" + "@" + "!" + str(bot.users[i].id) + ">": 0})
        i = i + 1
    await save(DataPlayers)

#Показать счёт каждого участника
@bot.command()
@commands.has_permissions(administrator=True)
async def show_all(ctx):
    for mem in DataPlayers:
        await ctx.send("На счету " + mem + " находится " + str(DataPlayers[mem]) + " Galocoin")

#Пополнить счёт участника
@bot.command()
@commands.has_permissions(administrator=True)
async def plus(ctx, n: str, a: int):
    DataPlayers[n] += a
    await ctx.send(str(n) + " вас счёт был пополнен на: " + str(a))
    await ctx.send(str(n) + " на вашем счету: " + str(DataPlayers[n]) + " Galocoin")
    await save(DataPlayers)

#Уменьшить счёт участника
@bot.command()
@commands.has_permissions(administrator=True)
async def minus(ctx, n: str, a: int):
    DataPlayers[n] -= a
    await ctx.send(str(n) + " с вашего счёта было снято " + str(a) + " Galocoin")
    await ctx.send(str(n) + " на вашем счету: " + str(DataPlayers[n]) + " Galocoin")
    await save(DataPlayers)

#@commands.has_any_role("gnida") Просто для себя

#Показать количество денег на своём счету
@bot.command()
async def money(ctx):
    await ctx.send("На ващем счету: " + str(DataPlayers["<" + "@" + "!" + str(ctx.message.author.id) + ">"]) + " Galocoin")

#Передать деньги с одного счётна на другой
@bot.command()
async def trans(ctx, n: str, a: int):
    DataPlayers["<" + "@" + "!" + str(ctx.message.author.id) + ">"] -= a
    DataPlayers[n] += a
    await ctx.send("Со счёта " + str(ctx.message.author.name) + " переведено " + str(a) + " Galocoin " + " на счёт" + n)
    await save(DataPlayers)

#Посмотреть на количество денег у другого человека
@bot.command()
async def friend(ctx, n: str):
    await ctx.send("На счету " + str(n) + " находится: " + str(DataPlayers[n]) + " Galocoin")

#!!ВНУТРЕННЯЯ КОМАНДА!! сохранение данных путём передачи в специальный текстовый канал logs
async def save(b):
    channel = bot.get_channel(681435028982726748)
    await channel.send(str(b))

#!!ВНУТРЕННЯЯ КОМАНДА!! Загрузка данных из спец канала logs
async def load():
    channel = bot.get_channel(681435028982726748)
    async for message in channel.history(limit=1):
        mem = message.content
        memsplit = mem.split(',')
        buffer = ''.join(memsplit)
        buffersplit = buffer.split()
        cout = 0
        while cout < len(buffersplit):
            del buffersplit[cout]
            cout = cout + 1
        buffert = buffersplit[-1]
        del buffersplit[-1]
        bufferth = ''.join(buffert)
        bufferf = bufferth.split('}')
        del bufferf[1]
        peredel = ''.join(bufferf)
        buffersplit.append(peredel)
        dic = list(DataPlayers.keys())
        cnt = 0
        while cnt < len(dic):
            DataPlayers[dic[cnt]] = int(buffersplit[cnt])
            cnt = cnt + 1

        await save(DataPlayers)


bot.run(config.TOKEN)
