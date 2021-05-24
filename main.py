import logging
import tor_scraper as ts
import screeners.finviz_screen as fs
import sends.mails as mails
import multiprocessing
import json
import time

def main():
    logging.basicConfig(filename='tor_scraper.log', level=logging.INFO)
    logging.info('Started')   
    json_dict = {
        "Market Cap.": "Any" 
        ,"Dividend Yield": "Over 1%" 
        ,"P/E": "Under 35" 
        #,"PEG": "Under 2"
        ,"Quick Ratio": "Over 1"
        ,"Return on Equity": "Over +10%"
        ,"Current Ratio": "Over 1"
        #,"Sales growth qtr over qtr": "Over 5%"
        #,"EPS growth past 5 years": "Over 5%"
        ,"Debt/Equity": "Under 0.8"        
        ,"Return on Investment": "Positive (>0%)"
        ,"Country":"USA"
        }  

    ticket_list = fs.custom_screener(json_dict)

    tbb_path="/home/vtx/.local/share/torbrowser/tbb/x86_64/tor-browser_en-US/"
    result_path="/home/vtx/stock/"
    valuations = ts.guru_scraper(tbb_path=tbb_path,result_path=result_path,tickers_list=ticket_list)

    for valuation in valuations:
        mails.send_email(valuation,result_path)

    logging.info('Finished')

if __name__ == '__main__':
    main()





