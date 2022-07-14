import re
import os
import wget

if not os.path.exists('config.ini'):
	open('config.ini', 'a').close()

if os.stat('config.ini').st_size==0:
	config = open('config.ini', 'w+')
	showName = input('Please insert the omny.fm show name you want to download: ')
	config.write(f'#---===--- Omny.fm Podcast Downloader By OREEE ---===---#\nShowName = {showName}')
else:
	config = open('config.ini', 'r+')
	try:
		showName = config.readlines()[1].rstrip()[11:]
	except:
		config = open('config.ini', 'w+')
		showName = input('Please insert the omny.fm show name you want to download: ')
		config.write(f'#---===--- Omny.fm Podcast Downloader By OREEE ---===---#\nShowName = {showName}')

RSS_URL = f'https://omny.fm/shows/{showName}/playlists/podcast.rss'
URL_REGEX = r"""((?:(?:https|ftp|http)?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|org|uk)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|uk|ac)\b/?(?!@)))"""

if os.path.exists('podcast.rss'):
	os.remove('podcast.rss')
try:
	wget.download(RSS_URL, out='podcast.rss')
except:
	try:
		RSS_URL = f'https://omny.fm/shows/{showName}/playlists/{showName}.rss'
    	wget.download(RSS_URL, out='podcast.rss')
	except:
		print(f'ERROR: Show does not exist!\nIn order to fix that you need to open "config.ini" and change the show name.')
		exit()

with open("podcast.rss",encoding ="utf8") as f:
   rss = f.read()

urls = re.findall(URL_REGEX, rss)
VALID_DOMAIN = 'https://traffic.omny.fm/d/clips/'
valid_urls = []
for url in urls:
	if VALID_DOMAIN in url:
		if not url in valid_urls:
			valid_urls.append(url)

titles = []
with open("podcast.rss", "r", encoding="utf8") as rss:
	for line in rss:
		title = re.search(r'<title>(\S+).*<\/title>', line)
		if title:
			title = title.group(0)
			title = title[7:-8]
			title = title.replace('|', '-')
			titles.append(title)
titles = titles[2:]

os.makedirs(showName, exist_ok=True)

if os.path.exists(f'{showName}\log.txt'):
	with open(f'{showName}\log.txt', 'r+') as f:
		content = f.readlines()
		f.write('\n')
		for i in range(max(len(valid_urls), len(titles))):
			titles_i = titles[i] if i< len(titles) else ''
			valid_urls_i= valid_urls[i] if i< len(valid_urls) else ''
			line = f'Title: {titles_i} URL: {valid_urls_i}\n'
			if line not in content:
				f.write(" ".join(['Title:', titles_i, 'URL:', valid_urls_i]))
				f.write("\n")
				print(f'\nDownloading {titles_i}')
				wget.download(valid_urls_i, out=f'{showName}\{titles_i}.mp3')
else:
	with open(f'{showName}\log.txt', 'w+') as f:
		content = f.readlines()
		f.write('\n')
		for i in range(max(len(valid_urls), len(titles))):
			titles_i = titles[i] if i< len(titles) else ''
			valid_urls_i= valid_urls[i] if i< len(valid_urls) else ''
			line = f'Title: {titles_i} URL: {valid_urls_i}\n'
			if line not in content:
				f.write(" ".join(['Title:', titles_i, 'URL:', valid_urls_i]))
				f.write("\n")
				print(f'\nDownloading {titles_i}')
				wget.download(valid_urls_i, out=f'{showName}\{titles_i}.mp3')