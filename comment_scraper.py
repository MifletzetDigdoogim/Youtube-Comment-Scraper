from selenium import webdriver, common
import sys
import time

# Grab the url as the first command line argument
url = sys.argv[1]
# url = r'https://www.youtube.com/watch?v=cYLrntJhZd0'

# Create a Chrome browser
driver = webdriver.Chrome()

# Open the url from the command line
driver.get(url)

# Maximize window
driver.maximize_window()

time.sleep(7)
# Scroll to the bottom in order to load the comments
height = 0
prev_len = 0
items = []
while True:
    height += 10000
    driver.execute_script("window.scrollTo(0, "+str(height)+");") # execute scrolling
    print("Scrolling")
    time.sleep(3.5) # wait for comments to load.
    items = driver.find_elements_by_xpath(r"//div[@id='main' and @class='style-scope ytd-comment-renderer']") # Get Comments.

    # Check to see if there are no new comments - reached end of comment list.
    if prev_len == len(items) :
        break

    prev_len = len(items)


# print the comments, separated by a line
for item in items:
    header_element = item.find_element_by_xpath("div[@id='header']")

    # Pinned Comment
    if len(header_element.text.split('\n')) > 2:
        print("Pinned Comment Avoided")
        continue

    author_text, time_stamp_text = header_element.text.split('\n')

    content_element = item.find_element_by_xpath("ytd-expander[@id='expander']").find_element_by_xpath("div[@id='content']")
    content_text = content_element.text

    print("Author: ")
    print(author_text)
    print()

    print("TimeStamp: ")
    print(time_stamp_text)
    print()

    print("Content: ")
    print(content_text)

    print("-" * 80)


# close the browser
driver.close()

print("Done!")