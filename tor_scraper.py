import time

import requests
import timeunit as TimeUnit
from tbselenium.tbdriver import TorBrowserDriver
import io
from PIL import Image
import json
import subprocess
from datetime import datetime
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sends.mails as mails
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (ElementNotVisibleException,
                                        ElementNotSelectableException,
                                        NoSuchElementException,
                                        TimeoutException,
                                        StaleElementReferenceException
                                        )


class Ticker:
    def __init__(self, valuation, margin_value, growth_rank, report_paths, ticker):
        self.valuation = valuation
        self.report_paths = report_paths
        self.ticker = ticker
        self.growth_rank = growth_rank
        self.margin_value = margin_value


now = datetime.now()
date_str = now.strftime("%m-%d-%Y")

ignore_list = [ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException,
               StaleElementReferenceException, TimeoutException, BaseException]


def guru_scraper(tbb_path, result_path, tickers_list):
    valuations = []

    # valuations = retry (ticker_scraper(result_path, "AMED", tbb_path),10)
    # valuations = ticker_scraper(result_path, "ACU", tbb_path)
    for ticker in tickers_list:
        try:
            ticker_scraper(result_path, ticker, tbb_path)
        except:
            logging.info("Error en Ticker "+ticker)

    return valuations


def tor_init():
    subprocess.Popen("pkill firefox.real".split())
    time.sleep(2)
    subprocess.Popen("pkill tor".split())
    time.sleep(2)
    subprocess.Popen("tor -f /etc/tor/torrc".split())

    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050',
    }
    url = 'https://check.torproject.org/'
    # Check if tor is active
    isInTor = -1
    while isInTor == -1:
        time.sleep(1)
        response = requests.get(url, proxies=proxies, verify=False)

        logging.info(response.text.find("This browser is configured to use Tor"))
        isInTor = response.text.find("This browser is configured to use Tor")
    return


def tor_stop(firefox_driver):
    subprocess.Popen("pkill tor".split())
    firefox_driver.close()
    firefox_driver.quit()
    os.system("pkill firefox.real")

    return


def ticker_scraper(result_path, ticker, tbb_path):
    img_list = []
    if not os.path.exists(result_path + date_str):
        os.mkdir(result_path + date_str)
    screenshot_fullpath = result_path + date_str + "/" + "guru_" + ticker + '.png'
    # init new tor conection
    tor_init()

    logging.error("===============================================================================")
    logging.error("================================    INICIO    =================================")
    logging.error("===============================================================================")
    logging.error(screenshot_fullpath)
    logging.error("===============================================================================")


    firefox_driver = TorBrowserDriver(tbb_path=tbb_path, headless=True,
                                      tbb_logfile_path=result_path + 'tbselenium.log')
    firefox_driver.get('https://gurufocus.com/stock/' + ticker)  # +'/summary')
    # ACLS
    total_height = 11000
    firefox_driver.set_window_size(width=1900, height=1000)
    wait_value = WebDriverWait(firefox_driver, timeout=120, poll_frequency=4,
                               ignored_exceptions=ignore_list)

    # firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--test-image-before" + '.png')
    logging.info("===============================================================================")
    logging.info("================================    popups    =================================")
    logging.info("===============================================================================")

    # time.sleep(10)

    popup_remove(firefox_driver)

    # firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--test-image-popups" + '.png')
    logging.info("===============================================================================")
    logging.info("================    guru-investment-theses    =================================")
    logging.info("===============================================================================")
    element = firefox_driver.find_element_by_id("guru-investment-theses")
    logging.info(element.text)

    firefox_driver.execute_script("""
            arguments[0].scrollIntoView(true);
            """, element)

    popup_remove(firefox_driver)

    scroll_page(element, firefox_driver)

    # time.sleep(80)

    # firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--small" + '.png')

    popup_remove(firefox_driver)

    scroll_user(firefox_driver)

    # class ="membership-limit-section capture-area"
    # content_stats = firefox_driver.find_element_by (By,"membership-limit-section capture-area")
    firefox_driver.set_window_size(1920, total_height)  # the trick
    time.sleep(60)
    firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_" + ticker + "--size" + '.png')
    firefox_driver.set_window_size(width=1900, height=1000)
    # time.sleep(60)

    logging.info("===============================================================================")
    logging.info("================    Get Valuation    ==========================================")
    logging.info("===============================================================================")
    try:
        scroll_user(firefox_driver)
        popup_remove(firefox_driver)

        scroll_user(firefox_driver)

        try:
            valuation_text = wait_value.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@id="band"]/div/div/div/span/div/div')))
        except Exception as e:
            logging.info(e)
            logging.info("Error Getting value element")

        try:
            growth_text = wait_value.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='growth']/div/div/div/span/span")))

            logging.info("Growth rank: " + growth_text.text)
            growth_rank = growth_text.text
        except Exception as e:
            growth_rank = "unknown"
            logging.info(e)
            logging.info("Error Getting growth element")

        logging.info("===============================================================================")
        logging.info("============================= VALUATION  ======================================")
        logging.info("===============================================================================")
        logging.info(screenshot_fullpath)
        logging.info(valuation_text.text)

        ticker_valuation = valuation_text.text

        if ('undervalued' in ticker_valuation.lower()) or ('fair' in ticker_valuation.lower()):

            # pagedata=firefox_driver.page_source
            # with open(result_path + date_str + "/" + ticker + '_pagedata.txt', "w") as text_file:
            #        text_file.write(pagedata)
            scroll_to_top(firefox_driver)
            firefox_driver.set_window_size(1920, total_height)  # the trick
            time.sleep(40)
            firefox_driver.save_screenshot(screenshot_fullpath)
            firefox_driver.set_window_size(width=1900, height=1000)

            img_list.append(screenshot_fullpath)

            margin_value = dcf_extraction(firefox_driver, img_list, result_path, ticker, total_height, wait_value)

            img_list.append(result_path + date_str + "/" + "guru_" + ticker + "--size" + '.png')

            valuation = Ticker(valuation=ticker_valuation, margin_value=margin_value, growth_rank=growth_rank,
                               report_paths=img_list, ticker=ticker)

            try:
                logging.info("Sending Email for Ticker: " + ticker)
                mails.send_email(valuation, result_path)
            except Exception as e:
                logging.info(e)
                logging.info("Sending Email Error for Ticker: " + ticker)
            tor_stop(firefox_driver)
            logging.info("===============================================================================")
            logging.info("===============================   FINAL  ======================================")
            logging.info("===============================================================================")

            return Ticker(valuation=ticker_valuation, margin_value=margin_value, growth_rank=growth_rank,
                          report_paths=img_list, ticker=ticker)

    except Exception as e:
        logging.info(e)





def dcf_extraction(firefox_driver, img_list, result_path, ticker, total_height, wait_value):
    popup_remove(firefox_driver)
    popup_remove(firefox_driver)
    wait_value.until(EC.element_to_be_clickable((By.LINK_TEXT, 'DCF'))).click()
    popup_remove(firefox_driver)
    dcf_element = firefox_driver.find_element_by_link_text('DCF')
    logging.info(dcf_element.text)
    scroll_user(firefox_driver)
    scroll_page(dcf_element, firefox_driver)

    logging.info("Try to get DCF by FCF model for Ticker: " + ticker)

    try:
        # firefox_driver.find_element_by_xpath(
        #     "//section[@id='stock-page-container']/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[4]/div/label[2]/span/span").click()
        scroll_to_top(firefox_driver)
        firefox_driver.set_window_size(1920, total_height)  # the trick
        time.sleep(40)
        popup_remove(firefox_driver)
        fcf_button = wait_value.until(EC.element_to_be_clickable((By.XPATH,
                                                                  "//section[@id='stock-page-container']/main/div[3]/div/div/div[2]/div/div/div/div[2]/div[4]/div/label[2]/span[2]")))
        fcf_button.click()
        # time.sleep(20)
        logging.info("FCF model for Ticker clicked")
        firefox_driver.set_window_size(width=1900, height=1000)

        # wait_value.until(
        #     EC.visibility_of_element_located((By.XPATH,
        #                                       "//section[@id='stock-page-container']/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/span/span")))
        # wait_value.until(
        #     EC.visibility_of_element_located((By.XPATH,
        #                                       "//section[@id='stock-page-container']/main/div[2]/div/div/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr/td[2]")))
        logging.info("DCF page loaded ")

    except Exception as e:
        logging.info(e)
        logging.info("Error getting DCF ")
    scroll_to_top(firefox_driver)
    firefox_driver.set_window_size(1920, total_height)  # the trick
    time.sleep(40)
    firefox_driver.save_screenshot(
        result_path + date_str + "/" + "guru_" + ticker + "--dcf" + '.png')

    try:
        margin_value_text = wait_value.until(EC.presence_of_element_located(
            (By.XPATH,
             "//section[@id='stock-page-container']/main/div[3]/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/span/span")))

        logging.info("Margin_value: " + margin_value_text.text)
        margin_value = margin_value_text.text
    except Exception as e:
        margin_value = "unknown"
        logging.info(e)
        logging.info("Error Getting margin_value element")

    #

    # //section[@id='stock-page-container']/main/div[3]/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/span/span

    firefox_driver.set_window_size(width=1900, height=1000)
    img_list.append(result_path + date_str + "/" + "guru_" + ticker + "--dcf" + '.png')

    return margin_value


def scroll_to_top(firefox_driver):
    firefox_driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
    time.sleep(3)
    firefox_driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
    time.sleep(1)
    firefox_driver.find_element_by_tag_name('html').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(2)
    firefox_driver.execute_script("window.scrollTo({ top: 0, behavior: 'smooth' });")


def scroll_page(element, firefox_driver):
    firefox_driver.execute_script("""
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                """, element)
    scroll_to_top(firefox_driver)


def popup_remove(firefox_driver):
    try:
        popups = firefox_driver.find_elements_by_class_name("el-dialog__wrapper")
        for popup in popups:
            logging.info(popup.text)
            firefox_driver.execute_script("""
                        arguments[0].parentNode.removeChild(arguments[0]);
                        """, popup)

        v_modals = firefox_driver.find_elements_by_class_name("v-modal")
        for v_modal in v_modals:
            firefox_driver.execute_script("""
                        arguments[0].parentNode.removeChild(arguments[0]);
                        """, v_modal)
    except Exception as e:
        logging.info(e)


def scroll_user(firefox_driver):
    y = 10
    for timer in range(0, 6):
        firefox_driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 10
        time.sleep(10)

    scroll_to_top(firefox_driver)
