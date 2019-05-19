import requests
import selenium.webdriver
import selenium
from until.helptool import HelpTool
driver = selenium.webdriver.Chrome()
driver.get('http://proxylist.fatezero.org/')
print(driver.page_source)

#content = requests.get('http://proxylist.fatezero.org/',headers=HelpTool().get_header())
#print(content.text)