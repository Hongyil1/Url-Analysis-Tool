import requests
import csv
import urllib3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test(url):

    filednames = ['url', 'status_code', 'CMS']
    url = url.rstrip()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    try:
        status_code = requests.get(url=url, headers=headers).status_code
        if status_code == 200:
            url_cms = new_cms_detct(url)
            print(url, status_code, url_cms)
            if url_cms != "Not Detect":
                with open("result.csv", 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, filednames)
                    writer.writerow({'url': url, 'status_code': status_code, 'CMS': url_cms})
            else:
                with open("noDetect.csv", 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, filednames)
                    writer.writerow({'url': url, 'status_code': status_code, 'CMS': url_cms})
        else:
            # print(status_code)
            with open("wrong.csv", 'a') as csvfile:
                writer = csv.DictWriter(csvfile, filednames)
                writer.writerow({'url': url, 'status_code': status_code})
    except:
        print("can not go to the website: ", url)
        # status_code = requests.get(url=url, headers=headers,verify=False).status_code
        with open("wrong.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, filednames)
            writer.writerow({'url': url, 'status_code': "None", 'CMS': 'Wrong'})
        pass

def new_cms_detct(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    # driver.set_window_size(1120, 550)
    driver = webdriver.Chrome("./chromedriver", chrome_options=options)
    web = "https://whatcms.org/"
    # delet the http:// or https://
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    # delet ending '/'
    if url.endswith('/'):
        url = url.strip('/')
    search_url = web + "?s=" + url + "&"
    driver.get(search_url)

    sourceCode = driver.page_source
    detect_text = "We haven't crawled"
    if detect_text in sourceCode:
        button = driver.find_element_by_class_name("btn-success")
        button.click()
        time.sleep(3)

    result = driver.find_elements_by_class_name("nowrap")
    elem_list = []

    for elem in result:
        elem_list.append(elem.text)

    # print("elem_list: ", elem_list)

    driver.close()
    driver.quit()

    if "Magento" in elem_list:
        return "Magento"
    elif "WordPress" in elem_list:
        return "WordPress"
    elif "PrestaShop" in elem_list:
        return "PrestaShop"
    elif "OpenCart" in elem_list:
        return "OpenCart"
    elif "Shopify" in elem_list:
        return "Shopify"
    elif "Squarespace" in elem_list:
        return "Squarespace"
    else:
        return "Not Detect"
