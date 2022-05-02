import pandas as pd
import tor_scraper as ts
df = pd.read_csv ('simplidiv/dividend-stocks.csv')

tbb_path="/home/vtx/.local/share/torbrowser/tbb/x86_64/tor-browser_en-US/"
result_path="/home/vtx/pystock/"
tickers = df.Ticker.tolist()
valuations = ts.guru_scraper(tbb_path=tbb_path,result_path=result_path,tickers_list=tickers)

print("===============================================================================")
print("===============================   FINAL  ======================================")

