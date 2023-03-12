'''
    Main script.
'''

import os
import string
from core import fetcher, progress

url = 'https://neko-sama.fr/anime/info/9520-tensei-shitara-slime-datta-ken_vostfr'
out = './result/sdkfr_1/'

# Create dirs
if not os.path.exists(out): os.makedirs(out)

cla = '\033[94m[\033[0m MAIN PY \033[94m]\033[0m'
print(cla, 'Starting')

syn, eps = fetcher.get_anime(url)
open(out + 'syn.txt', 'w').write(syn)

print(cla, 'Wrote syn')

chars = string.ascii_letters + string.digits + '-_'

for i, episode in progress.Bar(cla, list(enumerate(eps))):
    
    print()
    
    while 1:
    
        try:
            # Parse name
            name = episode.split('/')[-1]
            name = ''.join([c for c in name if c in chars])
            
            print(cla, f'Fetching \033[92m{name}\033[0m')
            
            prov, eurl = fetcher.get_episode(episode)
            links = fetcher.get_episode_links(eurl)
            
            path = fetcher.download_episode(links, out + name + '.mp4')
            
            print(cla, f'### Fetched {name} ({path = })')
            
            break # exit retry loop
    
        except Exception as e:
            raise e

print(cla, 'Finished process')
# EOf