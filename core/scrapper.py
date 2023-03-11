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
        
        # Setup to page
        browser = core.firefox.launch(headless = not debug, args = ['--mute-audio'])
        page = browser.new_page(viewport = {'width': x, 'height': y})
        page.goto(url)
        page.wait_for_load_state()
        
        # page.on('request', on_request)
        # page.on('requestfinished', on_request)
        
        page.click('html', position = {'x': x / 2, 'y': y / 2})
        
        # Bypass ads
        for i in range(5):
            
            print(f'\r[ SCRPPER ] Passing {i}...', end  = '')
            page.click('html', position = {'x': x / 2, 'y': y / 2})
            
            # Close opened popup
            with page.expect_popup() as info:
                sleep(.5)
                info.value.close()
        
        print('\n[ SCRPPER ] Waiting for url list...')
        page.click('html', position = {'x': x / 2, 'y': y / 2})
        
        # Wait for quality request (m method)
        with page.expect_request_finished(lambda req: '//fusevideo.net/m/' in req.response().url) as info:
            
            print('[ SCRPPER ] Got response.')
            
            res = info.value.response().text()
            browser.close()
            
            print('[ SCRPPER ] Finished.')
            return res

# EOF