from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import os

download_folder = "./temp"

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

##################   ANOIXTI DIADIKASIA OK     ########################################
################################################################################################
    # Focus and fill the input (triggers the dropdown to appear)
    page.click('input[id="appForm:noticeProcedureType_input"]')
    page.fill('input#appForm\\:noticeProcedureType_input', '')
    page.type('input[id="appForm:noticeProcedureType_input"]', 'ανοι')

    # Wait briefly for the autocomplete suggestions to appear
    page.wait_for_timeout(500)

    #page.keyboard.press('ArrowDown')
    page.keyboard.press('Enter')

    time.sleep(2)
    page.keyboard.press('Enter')
    time.sleep(2)

    page.screenshot(path="xxxafter_search_click_1.png", full_page=True)

##########################################################

################    HMEROMHNIA START OK      #############################################

    page.click('input#appForm\\:finalDateFrom_input')
    page.wait_for_timeout(1000)
    #ddate = "2025-05-29"
    #page.fill("ui-datepicker-div",ddate)

    time.sleep(2)
    page.keyboard.press('Enter')
    time.sleep(2)

    page.screenshot(path="xxxafter_search_click_2.png", full_page=True)

    page.wait_for_timeout(1000)
    time.sleep(2)
    page.screenshot(path="xxxafter_search_click_3.png", full_page=True)

    page.keyboard.press('Escape')
    page.wait_for_timeout(1000)


    page.wait_for_timeout(5000)
    time.sleep(2)

#############################################################

##########  CPV OK   ##################################

    page.click('input[id="appForm:noticecpvCodeMain_input"]')
    page.fill('input#appForm\\:noticecpvCodeMain_input', '')
    page.type('input[id="appForm:noticecpvCodeMain_input"]', '15810000-9')

    # Wait briefly for the autocomplete suggestions to appear
    page.wait_for_timeout(500)

    time.sleep(2)
    page.keyboard.press('Enter')
    time.sleep(2)
    #page.keyboard.press('Enter')

    page.screenshot(path="xxxafter_search_click_4.png", full_page=True)

    page.fill('input#appForm\\:noticecpvCodeMain_input', '')
    page.type('input[id="appForm:noticecpvCodeMain_input"]', '15612120-8')

    # Wait briefly for the autocomplete suggestions to appear
    page.wait_for_timeout(500)

    time.sleep(2)
    page.keyboard.press('Enter')
    time.sleep(2)

    page.screenshot(path="xxxafter_search_click_5.png", full_page=True)

#############################################################

##########START SEARCHING###############################
    #Click the search button
    print("Clicking search button...")
    #page.click('text=Αναζήτηση')
    page.click('#appForm\\:notice_search_button')
    #page.locator('text=Αναζήτηση').click(force=True)

    time.sleep(5)

    page.screenshot(path="after_search_click_6.png", full_page=True)

    html_content = page.content()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Find all result entries
    results = []
    result_items = soup.select('ul.ui-dataview-list-container > li.ui-dataview-row')

    #for item in result_items:
    for index, item in enumerate(result_items):

        div = item.select_one('div.customPaddingLi')
        if div:
            # Extract the reference number from the <label class="tableRefNo"><span>...</span></label>
            ref_label = div.select_one('label.tableRefNo span')
            reference_number = ref_label.get_text(strip=True) if ref_label else None

            title_label = div.select_one('label.tableTitle')
            title = title_label.get_text(strip=True) if title_label else None

            # Deadline label (ID ends in :j_idt702)
            deadline_label = div.select_one('label[id$=":j_idt702"]')
            deadline = deadline_label.get_text(strip=True) if deadline_label else None

            # Contracting authority (ID ends in :j_idt705)
            authority_label = div.select_one('label[id$=":j_idt705"]')
            authority = authority_label.get_text(strip=True) if authority_label else None

            # Budget (amount)
            budget_label = div.select_one('label[id$=":j_idt708"]')
            budget = budget_label.get_text(strip=True) if budget_label else None

            print(f"Processing row {index}: {reference_number}, {title}")

            # Compose the button selector dynamically based on index
            # ID pattern: appForm:noticeRsltTbl:<index>:j_idt710 (j_idt710 might be consistent or may vary)
            # To be safe, find button inside this div by text "Λήψη Αρχείου"
            button_selector = f'button#appForm\\:noticeRsltTbl\\:{index}\\:j_idt710'
            download_button = page.query_selector(button_selector)

            if download_button:
                print(f"  Clicking download button for row {index}...")
                try:
                    with page.expect_download() as download_info:
                        download_button.click()
                    download = download_info.value
                    # Suggest filename from reference number or fallback
                    filename = f"{reference_number or 'file'}_{index}.pdf"
                    filepath = os.path.join(download_folder, filename)
                    download.save_as(filepath)
                    print(f"  Downloaded file saved to: {filepath}")
                except Exception as e:
                    print(f"  Error downloading file for row {index}: {e}")
            else:
                print(f"  No download button found for row {index}")

            # (Optional) Add other field extraction here (e.g. CPV, title, date) as needed

            result = {
                'title': title,
                'reference_number': reference_number,
                'deadline': deadline,
                'contracting_authority': authority,
                'budget': budget
                # Add other fields like 'title', 'cpv', 'date' if available
            }

            results.append(result)

    # Step 4: Display the results
    for r in results:
        print(r)

    browser.close()
