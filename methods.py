"""

The methods.py contains all the functions this project needs

@ author: Hongyi Lin
@ Last Modified: 11/07/2018

"""
import requests
import csv
import urllib3
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_result(url):
    """
    The get_result method integrate the result from other method
    and write the result to the file
    :param url: input comes from Main.py, example: https://www.shore-lines.co.uk/
    :return: No return, write the result to the file
    """

    #Pre-process the url
    url = pre_process(url)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    try:
        # Get the status code
        s = requests.Session()
        r = s.get(url, headers=headers)
        status_code = r.status_code
        soup = BeautifulSoup(r.text, 'lxml')
        s.close()

        if status_code == 200:

            # Get CMS
            url_cms = cms_detct(url)

            # Get category
            url_category = get_category(url)
            advertise = ""

            if url_cms == "WordPress":

                # Advertise detection
                advertise = has_advertise(soup)

            write_target(url, status_code, url_cms, url_category, advertise)

        # Record the urls which status code is not 200
        else:
            write_problem(url, status_code)

    # Record the error url
    except:
        print("can not go to the website: ", url)
        write_problem(url, "wrong")
        pass

def cms_detct(url):
    """
    This method detect the cms of the url
    :param url: the pre-process url, a String. example: www.shore-lines.co.uk
    :return: A string, One of the following: "Magento", "WordPress", "PrestaShop"
    "OpenCart", "Shopify", "Squarespace" and "Not Detect".
    """

    web = "https://whatcms.org/"
    search_url = web + "?s=" + url + "&"

    # Use bfs
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    s = requests.Session()
    r = s.get(search_url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    s.close()

    # Get the pure text
    web_text = soup.get_text()
    # print(web_text)

    detect_text = "We haven't crawled"

    # The url has not been detected before, use selenium to click the button
    if detect_text in web_text:
        # print("No detected")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
        driver = webdriver.Chrome("./chromedriver", chrome_options=options)

        try:
            driver.get(search_url)
        except:
            driver.close()
            driver.quit()
            return False

        button = driver.find_element_by_class_name("btn-success")
        button.click()
        time.sleep(2)
        result = driver.find_elements_by_class_name("nowrap")
        elem_list = []
        for elem in result:
            elem_list.append(elem.text)
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

    # The url has been detected before
    else:
        if soup.find("div", {"class": "large text-center"}):
            target_div = soup.find("div", {"class": "large text-center"})
            result = target_div.a.get_text()
            # print("result: ", result)

            if "Magento" == result:
                return "Magento"
            elif "WordPress" == result:
                return "WordPress"
            elif "PrestaShop" == result:
                return "PrestaShop"
            elif "OpenCart" == result:
                return "OpenCart"
            elif "Shopify" == result:
                return "Shopify"
            elif "Squarespace" == result:
                return "Squarespace"
            else:
                return "Not Detect"

def get_category(url):
    """
    This method category the url. The detail category can be found here: https://fortiguard.com/webfilter/categories
    :param url: A pre-processed url, a Sting. example: www.shore-lines.co.uk
    :return: A String.
    """

    web = "https://fortiguard.com/webfilter?q="
    search_url = web + url
    r = requests.get(search_url)
    soup = BeautifulSoup(r.content, "lxml")
    result = soup.find_all(class_="info_title")

    for elem in result:
        if "Category:" in elem.text:
            category = elem.text[10:]
            return category
        else:
            return "Not Detection"

def has_advertise(soup):
    """
    This method is used to judge whether a WorldPress website can advertise.
    :param soup: The soup of this website. soup comes from BeautifulSoup(r.text, 'lxml').
    :return: A String. "True" or "False".
    """

    for script in soup(["script", "style"]):
        script.decompose()

    # Get the pure text
    web_text = soup.get_text()

    # Target words
    target_word = ["advertise", "media kit", "advertising", "promote with us", "advertise with us",
                   "press kit", "press room", "press inquiries", "advertising inquiries"]

    # break into lines and remove leading and trailing space on each, lowercase
    lines = [line.strip().lower() for line in web_text.splitlines() if 9 <= len(line.strip()) <= 21]

    if len(set(lines) & set(target_word)) > 0:
        return "True"
    else:
        return "False"

# Remove the http:// part from the url
def pre_process(url):
    """
    This method is used to remove the http and / from the url.
    :param url: The original url read from file. A String. like: https://www.shore-lines.co.uk/
    :return: The processed url. A String. Example: www.shore-lines.co.uk
    """
    # delet the http:// or https://
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    # delet ending '/'
    if url.endswith('/'):
        url = url.strip('/')
    return url

def write_target(url, status_code, url_cms, url_category, advertise):
    """
    Write the result to target.csv file.
    :param url: The processed url. A String. like: www.shore-lines.co.uk
    :param status_code: The status_code. An int. Like: 200
    :param url_cms: cms of the url. A String. Like: OpenCart
    :param url_category: A String. Like: Shopping
    :param advertise: A String. Like: ""
    :return: No return. Write result to target.csv file.
    """
    filednames = ['url', 'status_code', 'CMS', 'category', 'advertise']
    with open("target.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, filednames)
        writer.writerow({'url': url, 'status_code': status_code, 'CMS': url_cms,
                         'category': url_category, 'advertise': advertise})

def write_problem(url, status_code):
    """
    Write result to problem.csv file.
    :param url: The processed url. A String. like: www.shore-lines.co.uk
    :param status_code: The status_code. An int. Like: 404
    :return: No return. Write result to problem.csv file.
    """
    filednames = ['url', 'status_code', 'CMS', 'category', 'advertise']
    with open("wrong.csv", 'a') as csvfile:
        writer = csv.DictWriter(csvfile, filednames)
        writer.writerow({'url': url, 'status_code': status_code})
