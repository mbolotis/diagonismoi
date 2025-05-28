from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # Launch browser in headless mode
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "el-GR,el;q=0.9"
    })

    # Navigate to the URL
    print("Navigating to URL...")
    page.goto("https://cerpp.eprocurement.gov.gr/upgkimdis/unprotected/home.xhtml")

    # Click the "Προσκλήσεις - Προκηρύξεις - Διακηρύξεις" tab
    print("Clicking tab...")
    page.click('text=Προσκλήσεις - Προκηρύξεις - Διακηρύξεις')
    page.wait_for_timeout(1000)  # Wait for tab content to load

    page.wait_for_timeout(500)

    # Focus and fill the input (triggers the dropdown to appear)
    page.click('input[id="appForm:noticeProcedureType_input"]')
    page.fill('input#appForm\\:noticeProcedureType_input', '')
    page.type('input[id="appForm:noticeProcedureType_input"]', 'αν')

    # Wait briefly for the autocomplete suggestions to appear
    page.wait_for_timeout(500)

    #page.keyboard.press('ArrowDown')
    page.keyboard.press('Enter')

    page.screenshot(path="after_search_click_1.png", full_page=True)

    time.sleep(2)
    page.keyboard.press('Enter')

################################################################################################
################################################################################################

    page.click('input#appForm\\:finalDateFrom_input')
    page.wait_for_timeout(1000)

    page.screenshot(path="after_search_click_2.png", full_page=True)

    page.keyboard.press('Enter')
    page.wait_for_load_state('networkidle')  # wait until no network requests for 500ms

    page.wait_for_timeout(1000)
    time.sleep(5)
    page.screenshot(path="after_search_click_3.png", full_page=True)

    page.keyboard.press('Escape')
    page.wait_for_timeout(1000)

    page.screenshot(path="after_search_click_4.png", full_page=True)

    # Click the search button
    #print("Clicking search button...")
    #page.click('text=Αναζήτηση')
    #page.click('#appForm\\:notice_search_button')
    #page.locator('text=Αναζήτηση').click(force=True)

    page.wait_for_timeout(5000)
    time.sleep(5)

    #page.screenshot(path="after_search_click_3.png", full_page=True)
    browser.close()
'''
    # Wait for results to load
    print("Waiting for results...")
    try:
        page.wait_for_selector('#appForm\\:noticeRsltTbl_content', timeout=30000)
        #page.wait_for_selector('//div[@id="appForm:noticeRsltTbl_content"]', timeout=10000)
    except Exception as e:
        print(f"Error waiting for results: {e}")
        browser.close()
        exit()

    # Extract results
    print("Extracting results...")
    results_container = page.query_selector('#appForm\\:noticeRsltTbl_content')
    #results_container = page.query_selector('//div[@id="appForm:noticeRsltTbl_content"]')
    if results_container:
        results = results_container.query_selector_all('*')  # Get all child elements
        data = []
        for result in results:
            text = result.inner_text().strip()
            if text:  # Skip empty text
                data.append(text)
                print(text)
    else:
        print("Results container not found.")

    # Save results to file
    if data:
        print("Saving results to file...")
        with open("results.txt", "w", encoding="utf-8") as f:
            for item in data:
                f.write(item + "\n")
    else:
        print("No results to save.")

    # Close browser
    print("Closing browser...")'''
    #browser.close()
