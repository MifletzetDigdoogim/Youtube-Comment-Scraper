from selenium import webdriver, common
import sys
import time
import csv

print("Starting...")
# Check for correct usage:
if len(sys.argv) is not 3:
    print("Correct usage is <URL> <OUTPUT_PATH>")
    # exit()
else:
    # Grab the url as the first command line argument
    url = sys.argv[1]
    url = url.replace("\\", "\\\\")
     # Grab the Output file's path as the second argument.
    output_path = sys.argv[2]
    output_path = output_path.replace("\\", "\\\\")

# Create a FireFox browser
driver = webdriver.Firefox()
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

output_file = open(output_path + "\\Comments.csv", "wt", encoding="utf-8")
writer = csv.writer(output_file, delimiter=',')
writer.writerow(("Author", "TimeStamp", "Content"))
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
    writer.writerow((str(author_text), str(time_stamp_text), str(content_text)))

# Close csv output file
output_file.close()
# close the browser
driver.close()

print("Done!")