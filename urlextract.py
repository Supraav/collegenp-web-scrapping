from playwright.sync_api import sync_playwright
import json
output_file = 'schoollinks.json'
def extract_links(page):

    container_div = page.query_selector('#all-content-container')

    college_detail_contents = container_div.query_selector_all('.college-detail-content')

    # Extract the texts from each college detail content div
    urls=[]
    for content in college_detail_contents:
        text_element = content.query_selector('.college-name a')
        link_element=text_element.get_attribute('href')
        urls.append(link_element)
    print(len(urls))
    print('****************************************************************************')
    print(urls)
    return urls

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://www.collegenp.com/schools')


    container_div = page.query_selector('#all-content-container')

    college_detail_contents = container_div.query_selector_all('.college-detail-content')

    # Wait for the content to load
    page.wait_for_selector('#all-content-container .college-detail-content')

    urls = []
    last_height = page.evaluate("document.documentElement.scrollHeight")

    while True:
        # Extract URLs from the current page
        urls += extract_links(page)

        with open(output_file, 'w') as file:
            json.dump(urls, file,indent=3)

        
        # Scroll to the bottom of the page
        page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight-1000);")

        # Wait for a brief moment after scrolling
        page.wait_for_timeout(1000*5)

        new_height = page.evaluate("document.documentElement.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height

    # Print the extracted texts
    # for t in texts:
    #     print(t)

    # Close the browser
    context.close()