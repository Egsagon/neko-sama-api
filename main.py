from core import fetcher

url = 'https://neko-sama.fr/anime/info/6604-shingeki-no-kyojin_vostfr'
out = './result/'

syn, eps = fetcher.get_anime(url)

episode = eps[0]
name = '_'.join(episode.split('/episode/')[1].split('-')[1:])

print(f'{name = }')

prov, eurl = fetcher.get_episode(episode)

links = fetcher.get_episode_links(eurl)

# path = fetcher.download_episode(links, out + name + '.mp4', thread = False)

path = fetcher.download_ffmpeg(links, out + name + '.mp4',
                               thread = False)

# BUG thread provide corrupted file