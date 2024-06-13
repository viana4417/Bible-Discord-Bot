from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import re

TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)

antigo_testamento1 = {
    "gênesis": "https://vulgata.online/bible/Gn",
    "êxodo": "https://vulgata.online/bible/Ex",
    "levítico": "https://vulgata.online/bible/Lv",
    "números": "https://vulgata.online/bible/Nm",
    "deuteronômio": "https://vulgata.online/bible/Dt",
    "livro de josué": "https://vulgata.online/bible/Js",
    "livro dos juízes": "https://vulgata.online/bible/Ju",
    "livro de rute": "https://vulgata.online/bible/Rt",
    "livro primeiro de samuel": "https://vulgata.online/bible/1Sm",
    "livro segundo de samuel": "https://vulgata.online/bible/2Sm",
    "livro primeiro dos reis": "https://vulgata.online/bible/1Rs",
    "livro segundo dos reis": "https://vulgata.online/bible/2Rs",
    "livro primeiro das crônicas": "https://vulgata.online/bible/1Pa",
    "livro segundo das crônicas": "https://vulgata.online/bible/2Pa",
    "livro de esdras": "https://vulgata.online/bible/Esd",
    "livro de neemias": "https://vulgata.online/bible/Ne",
    "livro de tobias": "https://vulgata.online/bible/Tob",
    "livro de judit": "https://vulgata.online/bible/Jdi",
    "livro de ester": "https://vulgata.online/bible/Est",
    "livro de job": "https://vulgata.online/bible/Job",
    "salmos": "https://vulgata.online/bible/Ps",
    "livro dos provérbios": "https://vulgata.online/bible/Pv",
    "livro do eclesiaste": "https://vulgata.online/bible/Ees",
    "cânticos dos cânticos": "https://vulgata.online/bible/Cc",
    "livro da sabedoria": "https://vulgata.online/bible/Sa",
}
antigo_testamento2 = {
    "eclesiástico": "https://vulgata.online/bible/Eus",
    "profecia de isaías": "https://vulgata.online/bible/Is",
    "profecia de jeremias": "https://vulgata.online/bible/Je",
    "trenos ou lamentações de jeremias": "https://vulgata.online/bible/Lm",
    "profecia de baruch": "https://vulgata.online/bible/Ba",
    "profecia de ezequiel": "https://vulgata.online/bible/Ez",
    "profecia de daniel": "https://vulgata.online/bible/Dn",
    "oseias": "https://vulgata.online/bible/Os",
    "profecia de joel": "https://vulgata.online/bible/Jl",
    "profecia de amós": "https://vulgata.online/bible/Am",
    "profecia de abdias": "https://vulgata.online/bible/Ab",
    "profecia de jonas": "https://vulgata.online/bible/Jn",
    "profecia de miqueias": "https://vulgata.online/bible/Mic",
    "profecia de naum": "https://vulgata.online/bible/Na",
    "profecia de habucuc": "https://vulgata.online/bible/Hc",
    "profecia de sofonias": "https://vulgata.online/bible/So",
    "profecia de ageu": "https://vulgata.online/bible/Ag",
    "profecia de zacarias": "https://vulgata.online/bible/Zc",
    "profecia de malaquias": "https://vulgata.online/bible/Ml",
    "livro primeiro dos macabeus": "https://vulgata.online/bible/1Ma",
    "livro segundo dos macabeus": "https://vulgata.online/bible/2Ma",
}

novo_testamento1 = {
    "evangelho segundo s. mateus": "https://vulgata.online/bible/Mt",
    "evangelho segundo s. marcos": "https://vulgata.online/bible/Mc",
    "evangelho segundo s. lucas": "https://vulgata.online/bible/Lc",
    "evangelho segundo s. joão": "https://vulgata.online/bible/Jo",
    "actos dos apóstolos": "https://vulgata.online/bible/Act",
    "epístola aos romanos": "https://vulgata.online/bible/Rm",
    "primeira epístola aos coríntios": "https://vulgata.online/bible/1Co",
    "segunda epístola aos coríntios": "https://vulgata.online/bible/2Co",
    "epístola aos gálatas": "https://vulgata.online/bible/Gl",
    "epístola aos efésios": "https://vulgata.online/bible/Ef",
    "epístola aos filipenses": "https://vulgata.online/bible/Fp",
    "epístola aos colossenses": "https://vulgata.online/bible/Cl",
    "primeira epístola aos tessalonicenses": "https://vulgata.online/bible/1Ts",
    "segunda epístola aos tessalonicenses": "https://vulgata.online/bible/2Ts",
    "primeira epístola a timóteo": "https://vulgata.online/bible/1Tm",
    "segunda epístola a timóteo": "https://vulgata.online/bible/2Tm",
    "epístola a títo": "https://vulgata.online/bible/Tt",
    "epístola a filêmon": "https://vulgata.online/bible/Fm",
    "epístola aos hebreus": "https://vulgata.online/bible/Hb",
    "epístola de s. tiago": "https://vulgata.online/bible/Tg",
    "primeira epístola de s. pedro": "https://vulgata.online/bible/1Pe",
    "segunda epístola de s. pedro": "https://vulgata.online/bible/2Pe",
    "primeira epístola de s. joão": "https://vulgata.online/bible/1Jo",
    "segunda epístola de s. joão": "https://vulgata.online/bible/2Jo",
    "terceira epístola de s. joão": "https://vulgata.online/bible/3Jo",
}
novo_testamento2 = {
    "epístola de s. judas": "https://vulgata.online/bible/Jda",
    "apocalipse de s. joão": "https://vulgata.online/bible/Ap",
}


def pegar_versiculo(nome, cap, vers_inicio, vers_fim=None):
    if nome.lower() in antigo_testamento1:
        base_url = antigo_testamento1[nome.lower()]
    elif nome.lower() in novo_testamento1:
        base_url = novo_testamento1[nome.lower()]
    elif nome.lower() in antigo_testamento2:
        base_url = antigo_testamento2[nome.lower()]
    elif nome.lower() in novo_testamento2:
        base_url = novo_testamento2[nome.lower()]

    url = f'{base_url}.{cap}?ed=MS'

    resposta = requests.get(url)

    if resposta.status_code == 200:
        html = resposta.text
        soup = BeautifulSoup(html, 'html.parser')
        versiculos = []
        for vers in range(int(vers_inicio), int(vers_fim or vers_inicio) + 1):
            vers_div = soup.find('div', string=re.compile(rf'^\[{vers}\] '))
            if vers_div:
                versiculos.append(vers_div.get_text(strip=True))
        return ' '.join(versiculos)

@bot.slash_command(name="biblia1",description='25 primeiros livros do Antigo Testamento')
@discord.option(name='livro', description='Selecione um livro do Antigo Testamento', required=True, choices=antigo_testamento1)
@discord.option(name='capitulo_e_versiculo', description='Especificar o capítulo e o versículo', required=True)
async def biblia1(ctx,livro,capitulo_e_versiculo: str):
    capitulo_e_versiculo = livro + ' ' + capitulo_e_versiculo
    match = re.match(r'^(.+) (\d+),(\d+)(-(\d+))?$', capitulo_e_versiculo.strip())
    if match:
        nome, cap, vers_inicio, _, vers_fim = match.groups()
        vers_texto = pegar_versiculo(nome, cap, vers_inicio, vers_fim)
        try:
            print(capitulo_e_versiculo)
            await ctx.respond(vers_texto)
        except:
            pass

@bot.slash_command(name="biblia2",description='21 últimos livros do Antigo Testamento')
@discord.option(name='livro', description='Selecione um livro do Antigo Testamento', required=True, choices=antigo_testamento2)
@discord.option(name='capitulo_e_versiculo', description='Especificar o capítulo e o versículo', required=True)
async def biblia2(ctx,livro,capitulo_e_versiculo: str):
    capitulo_e_versiculo = livro + ' ' + capitulo_e_versiculo
    match = re.match(r'^(.+) (\d+),(\d+)(-(\d+))?$', capitulo_e_versiculo.strip())
    if match:
        nome, cap, vers_inicio, _, vers_fim = match.groups()
        vers_texto = pegar_versiculo(nome, cap, vers_inicio, vers_fim)
        try:
            print(capitulo_e_versiculo)
            await ctx.respond(vers_texto)
        except:
            pass

@bot.slash_command(name="biblia3",description='25 primeiros livros do Novo Testamento')
@discord.option(name='livro', description='Selecione um livro do Novo Testamento', required=True, choices=novo_testamento1)
@discord.option(name='capitulo_e_versiculo', description='Especificar o capítulo e o versículo', required=True)
async def biblia3(ctx,livro,capitulo_e_versiculo: str):
    capitulo_e_versiculo = livro + ' ' + capitulo_e_versiculo
    match = re.match(r'^(.+) (\d+),(\d+)(-(\d+))?$', capitulo_e_versiculo.strip())
    if match:
        nome, cap, vers_inicio, _, vers_fim = match.groups()
        vers_texto = pegar_versiculo(nome, cap, vers_inicio, vers_fim)
        try:
            print(capitulo_e_versiculo)
            await ctx.respond(vers_texto)
        except:
            pass

@bot.slash_command(name="biblia4",description='2 últimos livros do Novo Testamento')
@discord.option(name='livro', description='Selecione um livro do Novo Testamento', required=True, choices=novo_testamento2)
@discord.option(name='capitulo_e_versiculo', description='Especificar o capítulo e o versículo', required=True)
async def biblia4(ctx,livro,capitulo_e_versiculo: str):
    capitulo_e_versiculo = livro + ' ' + capitulo_e_versiculo
    match = re.match(r'^(.+) (\d+),(\d+)(-(\d+))?$', capitulo_e_versiculo.strip())
    if match:
        nome, cap, vers_inicio, _, vers_fim = match.groups()
        vers_texto = pegar_versiculo(nome, cap, vers_inicio, vers_fim)
        try:
            print(capitulo_e_versiculo)
            await ctx.respond(vers_texto)
        except:
            pass


bot.run(TOKEN)