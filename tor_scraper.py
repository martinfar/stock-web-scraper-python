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

class Ticker:  
    def __init__(self, valuation, report_paths,ticker):  
        self.valuation = valuation  
        self.report_paths = report_paths 
        self.ticker = ticker 

now = datetime.now()
date_str = now.strftime("%m-%d-%Y")
print("date",date_str)

def guru_scraper (tbb_path,result_path,tickers_list):
    valuations = []

    start = time.time()
    for ticker in tickers_list:
        valuations = ticker_scraper(result_path, ticker, tbb_path)
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

    print("===============================================================================")
    print("================================    INICIO    =================================")
    print("===============================================================================")
    print(screenshot_fullpath)
    print("===============================================================================")
    
    try:
            firefox_driver = TorBrowserDriver(tbb_path=tbb_path,headless=True) 
            firefox_driver.get('https://gurufocus.com/stock/'+ ticker+'/summary')
            fondos = firefox_driver.find_elements_by_class_name("v-modal")
            print("===============================================================================")
            print("================================    fondos    =================================")
            print("===============================================================================")           
            for fondo in fondos:
                print(fondo.text)
                firefox_driver.execute_script("""
                    arguments[0].parentNode.removeChild(arguments[0]);
                    """, fondo)
            print("===============================================================================")
            print("================================    popups    =================================")
            print("===============================================================================")                      
            popups = firefox_driver.find_elements_by_class_name("el-dialog__wrapper")
            for popup in popups:
                print(popup.text)
                firefox_driver.execute_script("""
                    arguments[0].parentNode.removeChild(arguments[0]);
                    """, popup)
            print("===============================================================================")
            print("================    guru-investment-theses    =================================")
            print("===============================================================================")  
            element = firefox_driver.find_element_by_id("guru-investment-theses")
            print(element.text)
            firefox_driver.execute_script("""
                arguments[0].scrollIntoView(true);
                """, element)
            time.sleep(10)
            firefox_driver.set_window_size(width=1700,height=5500)
            time.sleep(120)

            firefox_driver.find_element_by_class_name("more-margin").click()


            print("===============================================================================")
            print("================    Get Valuation    ==========================================")
            print("===============================================================================")  
            try:
                                           
                element = firefox_driver.find_element_by_xpath("//div[@id='band']/div/div/div[3]/span/button/span")
                print("===============================================================================")
                print("============================= VALUATION  ======================================")
                print("===============================================================================")
                print(screenshot_fullpath)
                print(element.text)

                     

                if ('undervalued' in element.text.lower()) or ('fair' in element.text.lower()) :
                    #pagedata=firefox_driver.page_source
                    #with open(result_path + date_str + "/" + ticker + '_pagedata.txt', "w") as text_file:
                    #        text_file.write(pagedata)                        
                    firefox_driver.save_screenshot(screenshot_fullpath)
                    
                    img_list.append(screenshot_fullpath)
                    valuation = Ticker(valuation=element.text,report_paths=img_list,ticker=ticker)
                    try:
                        mails.send_email(valuation,result_path)
                    except Exception as e:
                        print(e)
                    return Ticker(valuation=element.text,report_paths=img_list,ticker=ticker)
            except Exception as e:
                print(e)

            print("===============================================================================")
            print("===============================   FINAL  ======================================")
            print("===============================================================================")

            firefox_driver.close()
            firefox_driver.quit()

    except Exception as e:
        print(ticker)
        print(e)


