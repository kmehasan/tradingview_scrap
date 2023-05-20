from BrowserChromium import Browser
import argparse
import datetime
def getDateFromString(date_string):
    if date_string is None:
        return None
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d-%H:%M:%S')
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD-HH:MM:SS")
        exit()
    return date
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--url', help='url to scrape')
    parser.add_argument('-t', '--to_date', help='Start date of the scrape Format YYYY-MM-DD-HH:MM:SS')
    parser.add_argument('-f','--from_date', help='End date of the scrape Format YYYY-MM-DD-HH:MM:SS')
    args = parser.parse_args()
    url = args.url
    from_date_string = args.from_date
    to_date_string = args.to_date
    req_missing = False
    if not url:
        print("-u or --url is required")
        req_missing = True
    
    if not from_date_string:
        print("-f or --from_date is required")
        print("Format YYYY-MM-DD-HH:MM:SS")
        req_missing = True
    if req_missing:
        exit()
    from_date = getDateFromString(from_date_string)
    to_date = getDateFromString(to_date_string)
    # print(url, from_date, to_date)
    browser = Browser(url, from_date, to_date)
    browser.getAlldataFromUrl(url)
    browser.quit()
