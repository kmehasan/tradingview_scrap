from BrowserFirefox import Browser

if __name__ == '__main__':
    with open('input.txt','r', encoding='utf-8') as f:
        urls = f.read().split('\n')
        for url in urls:
            browser = Browser()
            if url == '':
                continue
            browser.getAlldataFromUrl(url)
            browser.quit()