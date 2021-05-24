import time
import timeunit as TimeUnit
from tbselenium.tbdriver import TorBrowserDriver
import io
from PIL import Image
from sends.tmp import send_email
import json
from datetime import datetime


now = datetime.now()

tickers_list =  []  #df['Ticker'].to_list()
result = {}
img_list = []
tbb_path="/home/vtx/.local/share/torbrowser/tbb/x86_64/tor-browser_en-US/"
result_path="/home/vtx/stock/"
date_str = now.strftime("%m-%d-%Y")
print("date",date_str)