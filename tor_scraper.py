import time
import timeunit as TimeUnit
from tbselenium.tbdriver import TorBrowserDriver
import io
from PIL import Image
import json
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



class Ticker:  
    def __init__(self, valuation, report_paths,ticker):  
        self.valuation = valuation  
        self.report_paths = report_paths 
        self.ticker = ticker 

now = datetime.now()
date_str = now.strftime("%m-%d-%Y")



def guru_scraper (tbb_path,result_path,tickers_list):


    valuations = []

    start = time.time()

    valuations = ticker_scraper(result_path, "BABA", tbb_path)

    # for ticker in tickers_list:
    #     valuations = ticker_scraper(result_path, ticker, tbb_path)
    processes = []
    #with ThreadPoolExecutor(max_workers=2) as executor:
    #    args = ((result_path, ticker, tbb_path) for ticker in tickers_list[:1])
    #    processes.append(executor.map(lambda p: ticker_scraper(*p), args))

    #for task in as_completed(processes):
    #    valuations.append(task.result())

    return valuations

def ticker_scraper(result_path, ticker, tbb_path):
    img_list = []
    if not os.path.exists(result_path + date_str):
        os.mkdir(result_path + date_str)
    screenshot_fullpath = result_path + date_str + "/" + "guru_"+ ticker + '.png'

    logging.error("===============================================================================")
    logging.error("================================    INICIO    =================================")
    logging.error("===============================================================================")
    logging.error(screenshot_fullpath)
    logging.error("===============================================================================")
    
    try:
            firefox_driver = TorBrowserDriver(tbb_path=tbb_path,headless=True, tbb_logfile_path=result_path+'tbselenium.log') 
            firefox_driver.get('https://gurufocus.com/stock/'+ ticker) #+'/summary')
            # fondos = firefox_driver.find_elements_by_class_name("v-modal")
            # logging.info("===============================================================================")
            # logging.info("================================    fondos    =================================")
            # logging.info("===============================================================================")
            # for fondo in fondos:
            #     logging.info(fondo.text)
            #     firefox_driver.execute_script("""
            #         arguments[0].parentNode.removeChild(arguments[0]);
            #         """, fondo)
            firefox_driver.set_window_size(width=1900,height=6500)
            
            # firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--test-image-before" + '.png')
            logging.info("===============================================================================")
            logging.info("================================    popups    =================================")
            logging.info("===============================================================================")   

            time.sleep(10)

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

            time.sleep(30)

            # firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--small" + '.png')

            scroll_page(element, firefox_driver)

            popup_remove(firefox_driver)
            firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_"+ ticker + "--size" + '.png')

            # time.sleep(60)



            logging.info("===============================================================================")
            logging.info("================    Get Valuation    ==========================================")
            logging.info("===============================================================================")  
            try:
                popup_remove(firefox_driver)
                time.sleep(60)
                valuation_text = firefox_driver.find_element_by_xpath('//div[@id="band"]/div/div/div/span/div/div')
                logging.info("===============================================================================")
                logging.info("============================= VALUATION  ======================================")
                logging.info("===============================================================================")
                logging.info(screenshot_fullpath)
                logging.info(valuation_text.text)




                if ('undervalued' in valuation_text.text.lower()) or ('fair' in valuation_text.text.lower()) :

                    #pagedata=firefox_driver.page_source
                    #with open(result_path + date_str + "/" + ticker + '_pagedata.txt', "w") as text_file:
                    #        text_file.write(pagedata)


                    firefox_driver.save_screenshot(screenshot_fullpath)

                    img_list.append(screenshot_fullpath)


                    # DCF screen
                    wait = WebDriverWait(firefox_driver, 10)
                    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'DCF'))).click()

                    popup_remove(firefox_driver)
                    dcf_element = firefox_driver.find_element_by_link_text('DCF')

                    logging.info(dcf_element.text)

                    scroll_page(dcf_element, firefox_driver)

                    time.sleep(40)


                    try:
                        logging.info("Try to get DCF by FCF model for Ticker: "+ticker)
                        wait = WebDriverWait(firefox_driver, 10)
                        wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@id='stock-page-container']/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[4]/div/label[2]/span/span"))).click()
                        firefox_driver.find_element_by_xpath("//section[@id='stock-page-container']/main/div[2]/div/div/div[2]/div/div/div/div[2]/div[4]/div/label[2]/span/span").click()
                    except Exception as e:
                        logging.info(e)


                    firefox_driver.save_screenshot(result_path + date_str + "/" + "guru_" + ticker + "--dcf" + '.png')



                    valuation = Ticker(valuation=valuation_text.text,report_paths=img_list,ticker=ticker)


                    try:
                        logging.info("Sending Email for Ticker: "+ticker)
                        mails.send_email(valuation,result_path)
                    except Exception as e:
                        logging.info(e)


                    return Ticker(valuation=element.text,report_paths=img_list,ticker=ticker)

            except Exception as e:
                logging.info(e)

            logging.info("===============================================================================")
            logging.info("===============================   FINAL  ======================================")
            logging.info("===============================================================================")

            firefox_driver.close()
            firefox_driver.quit()

            os.system("pkill firefox.real")

    except Exception as e:
        logging.info(ticker)
        logging.info(e)


def scroll_page(element, firefox_driver):
    firefox_driver.execute_script("""
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                window.scrollTo(0,0);
                """, element)

    firefox_driver.execute_script("""
                window.scrollTo(0, 220);
                """)

    firefox_driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

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

