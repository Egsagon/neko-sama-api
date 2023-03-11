'''
    core.scrapper
    
    Web scrapper handler.
'''

from time import sleep
from playwright.sync_api import sync_playwright

def valid_request(req) -> bool:
    
    print('trying', req.response().url)
    
    if req.response().url.endswith('.ts'): return False
    
    try:
        req.response().text()
        return True

    except: return False

def scrap(url: str, debug: bool = False) -> str:
    '''
    Get the list of providing urls from a provider.
    '''
    
    x, y = 800, 600
    
    with sync_playwright() as core:
        print('[ SCRPPER ] Starting...')
        
        # Setup
        browser = core.firefox.launch_persistent_context(
            headless = not debug,
            args = [
                '--mute-audio',
                '--allow-legacy-extension-manifests '
            ],
            
            ignore_default_args = [
                '--disable-extensions',
            ],
            
            user_data_dir = './chrome/',
            
            has_touch = True,
            is_mobile = True,
            devtools = True
        )
        
        page = browser.new_page()
        page.set_viewport_size({'width': x, 'height': y})
        
        page.goto(url)
        page.wait_for_load_state()
        
        # Play media
        page.tap('html', position = {'x': x / 2, 'y': y / 2})
        
        print('[ SCRPPER ] Listening reqs...')
        
        # Wait for quality request (m method)
        with page.expect_request_finished(lambda req: '//fusevideo.net/m/' in req.response().url) as info:
            
            print('[ SCRPPER ] Grabbed request')
            res = info.value.response().text()
            
            browser.close()
            print('[ SCRPPER ] Exiting')
            return res

if __name__ == '__main__':

    print(scrap('https://fusevideo.net/e/5E9KrVj7gVN66E5'))

# EOF