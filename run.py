'''
    Simple downloading script with gum.
'''

import os
import platform
import subprocess
import core.fetcher as fc

ps1 = '\033[96m*\033[0m'

def gum(*args) -> str:
    '''
    Start a gum command.
    '''
    
    if platform.system() == 'Windows':
    
        # On windows
        proc = subprocess.Popen(['gum/gum.exe'] + list(args),
                                stdout = subprocess.PIPE)
    
        return proc.communicate()[0].decode('utf-8')\
            .split('Descripteur non valide')[1].strip()
    
    else:
        # On Linux
        return subprocess.run(['gum'] + list(args),
                              stdout = subprocess.PIPE,
                              text = True).stdout.strip()

# Ask for URL
url = gum('input', '--placeholder', 'Enter URL...', '--width', '200')
print(ps1, 'Fetching data...')

# Query syn
syn, eps = fc.get_anime(url, debug = 0)
print(ps1, f'Synopsis:\n\033[93m{syn}\033[0m\n')

# Query episodes
print(ps1, 'Select episodes to download...')
root = 'https://neko-sama.fr/anime/episode/'

rep_eps = [e.replace(root, '') for e in eps]

eps = gum('choose', '--no-limit', *rep_eps).split('\n')

# Get output path
path = gum('input', '--placeholder', 'Enter output dir path...', '--width', '200')

if not path[-1] in '/\\': path += '/' # NOTE on win, add './' before path
if not os.path.exists(path): os.makedirs(path)

# Write syn
with open(path + 'info.txt', 'w') as f:
    f.write(url + '\n\nSynopsis:\n' +syn)

# Download
for ep, rep in [(root + e, e) for e in eps]:
    
    # Fetch links
    print(ps1, f'Fetching links for \033[92m{rep}\033[0m')
    _, link = fc.get_episode(ep, debug = False)
    links = fc.get_episode_links(link, debug = False)
    
    # Download
    ani_path = path + rep + '.mp4'
    print(ps1, f'Downloading to \033[92m{ani_path}\033[0m...')
    fc.download_episode(links, ani_path, debug = False)

print(f'Downloaded to \033[92m{path}\033[0m!')

# EOF