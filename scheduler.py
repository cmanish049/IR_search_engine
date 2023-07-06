from crawler import crawl, get_last_page
import datetime, time

days = 0
interval = 15
while days <= 1:
    mx = get_last_page()
    crawl(mx)
    print(f"Crawled at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f'Next crawl scheduled after {interval} days')
    time.sleep(interval)
    days = days + 1


    