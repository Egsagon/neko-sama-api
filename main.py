import os
from time import sleep
from core import fetcher, progress

url = 'https://neko-sama.fr/anime/info/9520-tensei-shitara-slime-datta-ken_vostfr'
out = './result/sdkfr_1/'

# Create dirs
if not os.path.exists(out): os.makedirs(out)

cla = '[ CTHREAD ]'
print(cla, 'Starting')

syn, eps = fetcher.get_anime(url)
open(out + 'syn.txt', 'w').write(syn)

print(cla, 'Wrote syn')

for episode in progress.Bar(cla, eps):
    
    name = '_'.join(episode.split('/episode/')[1].split('-')[1:])
    
    print(cla, '### Fething', name)
    
    prov, eurl = fetcher.get_episode(episode)
    links = fetcher.get_episode_links(eurl)
    
    path = fetcher.download_episode(links, out + name + '.mp4')
    
    print(cla, f'### Fetched {name} ({path = })')

print(cla, 'Finished process')

# NOTE threads raises 429