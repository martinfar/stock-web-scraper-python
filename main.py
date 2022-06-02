import logging
import os

import tor_scraper as ts
import screeners.finviz_screen as fs
import sends.mails as mails
import pydevd_pycharm
import subprocess

def main():
    # pydevd_pycharm.settrace('192.168.1.110', port=5650, stdoutToServer=True, stderrToServer=True)
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    logging.info("=======================   Hello Stock   ========================================")
    logging.info("=======================   Hello Stock   ========================================")


    json_dict = {
        "Market Cap.": "Any" 
        # ,"Dividend Yield": "Over 1%"
        ,"P/E": "Under 35" 
        #,"PEG": "Under 2"
        # ,"Quick Ratio": "Over 1"
        ,"Return on Equity": "Over +10%"
        # ,"Current Ratio": "Over 1"
        #,"Sales growth qtr over qtr": "Over 5%"
        ,"EPS growthpast 5 years": "Over 5%"
        ,"Debt/Equity": "Under 0.8"        
        ,"Return on Investment": "Positive (>0%)"
        # ,"Country":"USA"
        }  

    ticket_list = fs.custom_screener(json_dict)

    # tbb_path="/root/"
    # result_path="/home/vtx/ops/fun-projects/stock-results/"
    tbb_path="/app/"
    result_path="/opt/pystock/stock-results/"

    valuations = ts.guru_scraper(tbb_path=tbb_path,result_path=result_path,tickers_list=ticket_list)

    logging.info("===============================================================================")
    logging.info("===============================   FINAL  ======================================")




if __name__ == '__main__':
    main()





