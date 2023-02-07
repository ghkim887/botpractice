import asyncio
import discord
from discord.ext import commands
import yt_dlp as youtube_dl

intents = discord.Intents().all()
intents.message_content = True
intents.voice_states = True

act = discord.Game(name='v0.1 || ;;help')
stat = discord.Status.online
bot = commands.Bot(command_prefix=';;',intents=intents,activity=act,status=stat,help_command=None)

ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    }

info = []
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

#==================================================================================================================================

#boot
@bot.event
async def on_ready():
    print("{0.user} activated.".format(bot))
        
#test
@bot.command()
async def Hello(ctx):
    await ctx.send("Hello")

#미래시
@bot.command()
async def 미래시(ctx):
    await ctx.send("https://gall.dcinside.com/mgallery/board/view?id=projectmx&no=3150575")
    
#commanderror
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("존재하지 않는 명령어입니다")

#help
@bot.command(aliases=['help'])
async def 도움말(ctx):
    embed = discord.Embed(title="귱효봇",description="명령어 접두사는 ;; 을 사용합니다",color=0x2E9AFE)
    embed.add_field(name="1.대화",value=";;우흥 | ;;미래시",inline=False)
    embed.add_field(name="2.노래",value=";;play,p,ㅔ [검색어] | 노래 재생\n;;skip,s,ㄴ | 노래 스킵",inline=False)
    embed.add_field(name="3.채널",value=";;join | 음성채널 입장\n;;leave | 음성채널 퇴장",inline=False)
    await ctx.send(embed=embed)

#not in channel
async def notinc(ctx):
    if not ctx.message.author.voice:
        embed = discord.Embed(title="",description=str(ctx.message.author)+" 님은 현재 음성채널에 참가하지 않았습니다",color=0x2E9AFE)
        await ctx.send(embed=embed)

#join
@bot.command()
async def join(ctx):
    await notinc(ctx)
    channel=ctx.message.author.voice.channel
    embed = discord.Embed(title="",description="["+str(channel)+"] 채널에 참가합니다",color=0x2E9AFE)
    try:
        await ctx.voice_client.move_to(channel)
    except:
        await channel.connect()
    await ctx.send(embed=embed)
        
#leave
@bot.command()
async def leave(ctx):
    await notinc(ctx)
    if ctx.message.author.voice.channel.id == ctx.voice_client.channel.id:
        embed = discord.Embed(title="",description="현재 채널에서 나갔습니다",color=0x2E9AFE)
        await ctx.voice_client.disconnect()
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="",description=str(ctx.message.author)+" 님은 현재 채널에 참가하지 않았습니다",color=0x2E9AFE)
        await ctx.send(embed=embed)
        return
    
#data
async def data(ctx, song):
    video_title = song['title']
    video_len = song['duration']
    video_id = song['webpage_url']
    video_min = int(video_len) / 60
    video_sec = int(video_len) % 60
    embed = discord.Embed(title="재생 중: "+str(video_title)+" ("+str(int(video_min))+":"+str(int(video_sec))+")",description=str(video_id),color=0x2E9AFE)
    embed.set_thumbnail(url=song['thumbnail'])
    await ctx.send(embed=embed)

#search
async def search(ctx,*arg):
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch5:{arg}", download=False)['entries'][0:5]
        embed = discord.Embed(title="",description="1."+info[0]['title']+"\n2."+info[1]['title']+"\n3."+info[2]['title']+"\n4."+info[3]['title']+"\n5."+info[4]['title'],color=0x2E9AFE)
        await ctx.send(embed=embed)
        return info

#playcommand
@bot.command(aliases=['p','ㅔ'])
async def play(ctx, *arg):
    await join(ctx)
    global info
    info = await search(ctx,*arg)

#run_queue
async def runQueue(ctx,song):
    queue = []
    queue.append(song)
    embed = discord.Embed(title="",description="큐에 추가됨: "+ song['title'],color=0x2E9AFE)
    await ctx.send(embed=embed)
    voice = bot.voice_clients[0]
    URL = queue[0]['url'] 
    while len(queue) > 0:
        if voice.is_playing() == True:
            await asyncio.sleep(1)
        else: 
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            await data(ctx,queue[0])
            queue.pop(0)
            return

#play 1
@bot.command(aliases=['1'])
async def a(ctx):
    if len(info) == 5:
        song = info[0]
        print(song)
        print(song['title'])
        await runQueue(ctx,song)
    else:
        embed = discord.Embed(title="",description="먼저 노래를 검색해주세요",color=0x2E9AFE)
        await ctx.send(embed=embed)
        
#play 2
@bot.command(aliases=['2'])
async def b(ctx):
    if len(info) == 5:
        song = info[1]
        print(song['title'])
        await runQueue(ctx,song)
    else:
        embed = discord.Embed(title="",description="먼저 노래를 검색해주세요",color=0x2E9AFE)
        await ctx.send(embed=embed)
    
#play 3
@bot.command(aliases=['3'])
async def c(ctx):
    if len(info) == 5:
        song = info[2]
        print(song['title'])
        await runQueue(ctx,song)
    else:
        embed = discord.Embed(title="",description="먼저 노래를 검색해주세요",color=0x2E9AFE)
        await ctx.send(embed=embed)

#play 4
@bot.command(aliases=['4'])
async def d(ctx):
    if len(info) == 5:
        song = info[3]
        print(song['title'])
        await runQueue(ctx,song)
    else:
        embed = discord.Embed(title="",description="먼저 노래를 검색해주세요",color=0x2E9AFE)
        await ctx.send(embed=embed)

#play 5
@bot.command(aliases=['5'])
async def e(ctx):
    if len(info) == 5:
        song = info[4]
        print(song['title'])
        await runQueue(ctx,song)
    else:
        embed = discord.Embed(title="",description="먼저 노래를 검색해주세요",color=0x2E9AFE)
        await ctx.send(embed=embed)
    
#skip
@bot.command(aliases=['s','ㄴ'])
async def skip(ctx):
    await notinc(ctx)
    if bot.voice_clients[0].is_playing():
        embed = discord.Embed(title="",description="현재 음악을 중단합니다",color=0x2E9AFE)
        await ctx.send(embed=embed)
        await bot.voice_clients[0].stop()
    else:
        embed = discord.Embed(title="",description="재생 중인 음악이 없습니다",color=0x2E9AFE)
        await ctx.send(embed=embed)

bot.run('TOKEN')
