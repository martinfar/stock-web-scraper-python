import time
import timeunit as TimeUnit
from tbselenium.tbdriver import TorBrowserDriver
import io
from PIL import Image
import json
from datetime import datetime
import os
import logging


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
    img_list = []
    for ticker in tickers_list:
        if not os.path.exists(result_path + date_str):
            os.mkdir(result_path + date_str)
        screenshot_fullpath = result_path + date_str + "/" + "guru_"+ ticker + '.png'
        try:
                firefox_driver = TorBrowserDriver(tbb_path=tbb_path,headless=True) 
                firefox_driver.get('https://gurufocus.com/stock/'+ ticker+'/summary')
                fondos = firefox_driver.find_elements_by_class_name("v-modal")
                for fondo in fondos:
                    print(fondo.text)
                    firefox_driver.execute_script("""
                        arguments[0].parentNode.removeChild(arguments[0]);
                        """, fondo)
                popups = firefox_driver.find_elements_by_class_name("el-dialog__wrapper")
                for popup in popups:
                    print(popup.text)
                    firefox_driver.execute_script("""
                        arguments[0].parentNode.removeChild(arguments[0]);
                        """, popup)

                element = firefox_driver.find_element_by_id("guru-investment-theses")
                print(element.text)
                firefox_driver.execute_script("""
                    arguments[0].scrollIntoView(true);
                    """, element)
                time.sleep(10)
                firefox_driver.set_window_size(width=1700,height=5500)
                time.sleep(120)
                
                firefox_driver.find_element_by_class_name("more-margin").click()



                try:
                    element = firefox_driver.find_element_by_xpath("//div[@id='band']/div/div/div[3]/span/button/span")
                    print(element.text)

                    if ('undervalued' in element.text.lower()) or ('fair' in element.text.lower()) :
                        pagedata=firefox_driver.page_source
                        with open(result_path + date_str + "/" + ticker + '_pagedata.txt', "w") as text_file:
                            text_file.write(pagedata)                        
                        firefox_driver.save_screenshot(screenshot_fullpath)
                        img_list.append(screenshot_fullpath)
                        valuations.append( Ticker(valuation=element.text,report_paths=img_list,ticker=ticker) )

                except Exception as e:
                    print(e)
                

                firefox_driver.close()
                firefox_driver.quit()

        except Exception as e:
            print(ticker)
            print(e)

    
  
    return valuations

#print('=======      FINAL =               ==============')
#print('======================')
#print(result)
#
#with open(result_path + "analisis.txt", "w") as text_file:
#    text_file.write(json.dumps(result))
#
#send_email(img_list)