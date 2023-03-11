'''
    main
    
    Main script.
'''

import os
from core import fetcher, progress

url = 'https://neko-sama.fr/anime/info/9520-tensei-shitara-slime-datta-ken_vostfr'
out = './result/sdkfr_1/'

# Create dirs
if not os.path.exists(out): os.makedirs(out)

cla = '\n[ MAIN PY ]'
print(cla, 'Starting')

syn, eps = fetcher.get_anime(url)
open(out + 'syn.txt', 'w').write(syn)

print(cla, 'Wrote syn')

for episode in progress.Bar(cla, eps[7:]):
    
    while 1:
    
        try:
            name = '_'.join(episode.split('/episode/')[1].split('-')[10:])
            
            print(cla, '### Fetching', name)
            
            prov, eurl = fetcher.get_episode(episode)
            links = fetcher.get_episode_links(eurl)
            
            path = fetcher.download_episode(links, out + name + '.mp4')
            
            print(cla, f'### Fetched {name} ({path = })')
            
            break # exit retry loop
    
        except Exception as e:
        
            print(cla, '\033[91mFailed to scrappe:', e.args, '\033[0m, retrying...')    
        
        except KeyboardInterrupt:
            print(cla, 'User interruption.')


print(cla, 'Finished process')
# NOTE threads raises 429

# EOf