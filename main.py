import discord
import zzz
from discord.ext import commands
from discord.utils import get
from discord.ui import Button, View
from datetime import datetime
import json

with open("boosters.json") as arquivo:
    dados =json.load(arquivo)

intents = discord.Intents.all()
intents.members = True
Token = zzz.seuToken()
client = commands.Bot(command_prefix = ">", case_insensitive = True, intents=intents)

class MyView(View):
    def __init__(self):
        super().__init__()
#evento ao entrar no sv
@client.event
async def on_ready():
    print('Olá Boosters eu sou o {0.user} '.format(client))

#comando de resposta
@client.command()
async def ola(ctx):
    await ctx.send(f'Olá, booster {ctx.author}')

@client.event
async def on_member_join(member):
    embed = discord.Embed()
    embed.set_image(url='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYm9hZGltd2c3bDFsMWtvcWJiOXR5OG81NmltYmlrN2wyem9seWFjeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/sTgRVWuQMgmAS48QH7/giphy.gif')
    welcome = client.get_channel(1269370113425932298)
    mensagem = await welcome.send(f"Bem vindo a empresa, {member.mention}", embed = embed)




#lista de comandos do bot
@client.command()
async def comandos(ctx, Button): 
    embed = discord.Embed(
        title='Comandos do GoatBot',
        colour= 141212,
        description= 'basta usar o prefixo ">" antes do nome do comando desejado'
    )

    embed.add_field(name= 'Serviços', value='Lista uma tabela com nossos serviços', inline= False)
    embed.add_field(name= 'Ticket', value='Abre um Ticket para solicitar o serviço desejado', inline= False)
    embed.add_field(name= '"Nome do booster"', value='basta usar o prefixo e o nome do booster que abrirá uma descrição sobre ele', inline= False)

    await ctx.send(embed=embed)

#cards dos boosters
def create_booster_command(booster):
    async def command_template(ctx):
        embed = discord.Embed(
            title=f'Booster {booster["champion"]}',
            description=booster["description"],
            colour=141212
        )
        embed.set_image(url=booster["linkImg"])
        embed.add_field(name="Mains", value=booster["mains"])
        await ctx.send(embed=embed)

    return command_template

for booster in dados["boosters"]:
    command = create_booster_command(booster)
    client.command(name=booster["champion"].lower())(command)


@client.command()
async def dev(ctx):
    embed = discord.Embed(
        title= 'Developer Bleed',
        description= 'Dev FullStack e Estudante de Cybersec',
        colour = 15548997
    )

    embed.add_field(name='Email para contato', value='raphamf421@gmail.com', inline=False)
    await ctx.send(embed = embed)

#comando para exibir serviços por embed
@client.command()
async def serviços(ctx): 
    contas = discord.utils.get(ctx.guild.channels, name="💸│contas")
    tickets = discord.utils.get(ctx.guild.channels, name="🎫│ticket")
    embed = discord.Embed(
        title='Nossos serviços',
        colour= 141212
    )

    embed.add_field(name= 'Ticket', value=f'Para qualquer pedido, dúvida ou serviço você pode recorrer ao {tickets.mention}', inline= False)
    embed.add_field(name= 'EloBoost', value=f'Jogamos na sua conta para você adquirir o seu sonhado elo ', inline= False)
    embed.add_field(name= 'DuoBoost', value='Jogamos Duo com você durante sua jornada ao seu novo elo', inline= False)
    embed.add_field(name= 'Contas lvl 30', value='15R$', inline= False)
    embed.add_field(name= 'Contas com Elo', value=f'Abrir chat {contas.mention} para buscar uma conta ideal para você', inline=False)

    await ctx.send(embed=embed)

#comando para exibir o how to open ticket
@client.command()
async def summon_ticket(ctx): 
    embed = discord.Embed(
        title='Ticket',
        colour= 141212
    )

    embed.add_field(name= '', value='Ao clicar no botão abaixo será aberto um canal privado para solicitar o serviço desejado', inline= False)
    view = MyView()
    view.add_item(Button(style=discord.ButtonStyle.primary, label="Abrir ticket", custom_id="abrir_ticket"))

    await ctx.send(embed=embed, view=view)

#comando para exibir redes sociais
@client.command()
async def sociais(ctx):
    
    embed = discord.Embed(
        title='Nossas Redes sociais',
        colour= 141212
    )

    embed.add_field(name='Twitch', value= 'https://twitch.com/exemplo', inline=False)
    embed.add_field(name='TikTok', value= 'https://www.tiktok.com/exemplo', inline=False)
    embed.add_field(name='Twitter', value= 'https://x.com/exemplo', inline=False)
    embed.add_field(name='Discord', value= 'https://discord.gg/exemplo', inline=False)
    embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/256/3543/3543076.png')
    view= MyView()


    await ctx.send(embed=embed, view=view)

#comando para criar o ticket em call privada
@client.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "abrir_ticket":
            guild = interaction.guild
            member = interaction.user
            #insira o nome do cargo em name
            admin_role = get(guild.roles, name="CEO")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
            }
            #insira o id da categoria de tickets
            category = discord.utils.get(guild.categories, id=1269381361446420481)
            timestamp = datetime.now().strftime('%Y-%m-%d')
            channel = await guild.create_text_channel(f'ticket-{member}-{timestamp}', overwrites=overwrites, category=category)
            await channel.send(f'{member.mention}, seu atendimento será iniciado em instantes!')
            await interaction.response.send_message(f'Seu ticket foi criado: {channel.mention}', ephemeral=True)

#comando para add botao
#view.add_item(Button(style=discord.ButtonStyle.primary, label="Ver mais detalhes"))


client.run(Token)
