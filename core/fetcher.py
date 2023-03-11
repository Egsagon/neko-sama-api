import os
import requests
import threading
from time import sleep
import core.scrapper as scrapper
import core.progress as progress
from requests_html import HTMLSession


def get_anime(url: str, session: HTMLSession = None) -> tuple[str, list[str]]:
    '''
    Get the synopsis and a list of all the anime episode urls.
    '''

    # Get
    res = (session or HTMLSession()).get(url)
    res.html.render()
    soup = res.html

    # Parse
    synopsis = soup.find('.synopsis', first = True).text
    episodes = list({e.absolute_links.pop() for e in soup.find('.js-list-episode-container *')
                if e.absolute_links})
    
    print(f'[ LAYER 1 ] Fetched syn (\033[93m{len(synopsis)}\033[0m chars) and \033[92m{len(episodes)}\033[0m urls.')
    
    # Sort by name
    episodes.sort()
    
    return synopsis, episodes

def get_episode(url: str, session: HTMLSession = None) -> tuple[str, str]:
    '''
    Return the anime episode' provider and its stream url.
    '''
    
    session = session or HTMLSession()
    
    res = session.get(url)
    res.html.render()
    soup = res.html
    
    player = soup.find('#display-player iframe', first = True).attrs
    
    aurl = player['src']
    provider = aurl.split('//')[1].split('/')[0]
    
    print(f'[ LAYER 2 ] Found provider \033[93m{provider}\033[0m')
    
    return provider, aurl

def get_episode_links(url: str) -> list[str]:
    '''
    Fetch all episode links
    '''
    
    # Catch request
    res = scrapper.scrap(url) # NOTE gen all
    
    # Parse providers
    qual = [l.split('\n')[:-1] for l in '\n'.join(res.split('\n')[1:]).split('#')[1:]]
    quals = {int(data.split('=')[-1].replace('"', '')): link for data, link in qual}
    
    keys = list(quals.keys())
    
    print(f'[ LAYER 3 ] Got \033[92m{len(keys)}\033[0m qualities: \033[93m{", or ".join(map(str, keys))}\033[0m')
    
    # Pick best quality (TODO choose)
    best = quals[max(keys)]
    
    print(f'[ LAYER 3 ] Picking \033[93m{max(keys)}\033[0m quality')
    
    # Fetch segments
    headers = {
        'Host': 'fusevideo.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    raw = requests.get(best, headers = headers).text
    
    links =  [l for l in raw.split('\n') if l.startswith('https://')]
    
    print(f'[ LAYER 3 ] Got \033[92m{len(links)}\033[0m links')
    
    return links

def download_episode(links: list[str], path: str, session: requests.Session = None,
                     thread: bool = False) -> str:
    '''
    Download an episode to a directory an return its path.
    '''
    
    session = session or requests.Session()
    sum_ = []
    
    def dl(i, li) -> None:
        # Download one segment

        name = li.split('/')[-1]
        # print(f'\r[ LAYER 4 ] Fetched segment \033[92m{name}\033[0m/{len(links)}', end = '')
        res = session.get(li)
        
        if not res.ok:
            raise TimeoutError('Segment Error:', res.status_code, res.text)
        
        sum_.append( (i, res.content) )
    
    # Download segments through threads
    for i, link in progress.Bar('[ LAYER 4 ] Fetching segments', list(enumerate(links))):
        
        if thread:
            threading.Thread(target = dl, args = [i, link]).start()
        
        else:
            dl(i, link)
    
    # Check
    sleep(1)
    print(f'\n[ LAYER 4 ] Checking segments...', end = '')
    
    keys = [el[0] for el in sum_]
    expected = list(range(min(keys), max(keys) + 1))
    
    if expected == sorted(keys):
        print(f'\n[ LAYER 4 ] No one missing.')
    
    else:
        diff = set(expected) - set(keys)
        print(f'Error\nMissing {len(diff)} elements:\n{diff}')
        
        exit()
    
    # Concat segments
    print(f'\n[ LAYER 4 ] Fetched all segments, building video...')
    merged = bytes()
    
    # Sort by index in case some threads were quickier than others
    
    for i, (_, seg) in progress.Bar('[ LAYER 4 ] Merging', list(enumerate(sum_))):
        merged += seg
        # print(f'\r[ LAYER 4 ] Concat \033[92m{i + 1}\033[0m/{len(sum_)}', end = '')
    
    # Write to file
    print(f'\n[ LAYER 4 ] Concat finished, writing to \033[92m{path}\033[0m...')
    
    with open(path, 'wb') as file: file.write(merged)
    print('[ LAYER 4 ] Done.')

# EOF