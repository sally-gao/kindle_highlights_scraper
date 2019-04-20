from selenium import webdriver
import time
import json
import datetime
import os

def scrape_highlights(browser):

    nb_library_elem = browser.find_element_by_xpath('//div[@id="kp-notebook-library"]')
    book_elems = [b for b in nb_library_elem.find_elements_by_xpath("//div[contains(@class, 'a-row kp-notebook-library-each-book')]")]

    book_highlights = [get_book_highlights(b) for b in book_elems]

    return book_highlights

def get_book_highlights(book_elem):
    book_elem.click()

    book_id = book_elem.get_attribute("id")
    book_name = book_elem.text

    for _ in range(3):
        time.sleep(1)

        hl_elems = [h for h in browser.find_elements_by_xpath("//span[@id='highlight']")]

        if len(hl_elems) > 0:
            break

    highlights = [get_highlight(h) for h in hl_elems]

    return {'book_id': book_id, 'book_name': book_name, 'highlights': highlights}

def get_highlight(hl_elem):
    parent_elem = hl_elem.find_element_by_xpath('./..')
    grandparent_elem = parent_elem.find_element_by_xpath('./..')

    truncated = len(parent_elem.find_elements_by_xpath(".//div[contains(@class, 'highlight-truncated')]")) > 0
    highlight_id = parent_elem.get_attribute('id')
    text = hl_elem.text
    notes = [n.text for n in grandparent_elem.find_elements_by_xpath(".//span[@id='note']")]

    return {'highlight_id': highlight_id, 'truncated': truncated, 'text': text, 'notes': notes}

def save_highlights(highlights_dict):
    datetime_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(datetime_str+"_highlights.json", "w") as outfile:
        json.dump(highlights_dict, outfile)

def main():
    path_to_chromedriver = os.environ.get('PATH_TO_CHROMEDRIVER')
    username = os.environ.get('AMAZON_USERNAME')
    password = os.environ.get('AMAZON_PW')

    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

    url = 'https://read.amazon.com/notebook'
    browser.get(url)

    browser.find_element_by_xpath("//input[@id='ap_email']").send_keys(username)
    time.sleep(3)
    browser.find_element_by_xpath("//input[@id='ap_password']").send_keys(password)
    time.sleep(3)
    browser.find_element_by_xpath("//input[@id='signInSubmit']").click()
    time.sleep(15)

    highlights = scrape_highlights(browser)
    save_highlights(highlights)

    browser.quit()

if __name__ == "__main__":
    main()
