'''
    Web scrapper handler.
'''

from playwright.sync_api import sync_playwright

def scrap(url: str, debug: bool = False) -> str:
    '''
    Get the list of providing urls from a provider.
    '''
    
    x, y = 800, 600
    
    with sync_playwright() as core:
        if debug:
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
        
        if debug: print('[ SCRPPER ] Listening reqs...')
        
        # Wait for quality request (m method)
        with page.expect_request_finished(lambda req: '//fusevideo.net/m/' in req.response().url) as info:
            
            if debug: print('[ SCRPPER ] Grabbed request')
                
            res = info.value.response().text()
            
            browser.close()
            if debug: print('[ SCRPPER ] Exiting')
            return res

# EOF