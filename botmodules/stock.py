import locale, urllib2

locale.setlocale(locale.LC_ALL, 'en_US')

def get_stock_quote(stock):
    # stock quotes from Yahoo Finance
    # http://cliffngan.net/a/13
  # For the f argument in the url here are the values:
  #     code   description                
  #                                       
  #     l1     price                      
  #     c1     change                     
  #     v      volume                     
  #     a2     avg_daily_volume           
  #     x      stock_exchange             
  #     j1     market_cap                 
  #     b4     book_value                 
  #     j4     ebitda                     
  #     d      dividend_per_share         
  #     y      dividend_yield             
  #     e      earnings_per_share         
  #     k      52_week_high               
  #     j      52_week_low                
  #     m3     50day_moving_avg           
  #     m4     200day_moving_avg          
  #     r      price_earnings_ratio       
  #     r5     price_earnings_growth_ratio
  #     p5     price_sales_ratio          
  #     p6     price_book_ratio           
  #     s7     short_ratio  
  
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
    pagetmp = opener.open("http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=nl1c1va2j1" % stock)
    quote = pagetmp.read(1024)
    opener.close()
  
    name,price,change,volume,avg_volume,mkt_cap = quote.split(",")
    if price != "0.00": #assume no price = no result
       name = name.replace('"','')
    
       if change != "N/A":
           change = change + ' ({0:.2%})'.format((float(change)/(float(price) - float(change))))
       if volume != "N/A":
           volume = '{0:n}'.format(int(volume))
           avg_volume = '{0:n}'.format(int(avg_volume))
       
       return "[%s] %s    %s %s | Cap: %s | Volume (Avg): %s (%s)" % (stock,name.strip(),price,change,mkt_cap.strip(),volume,avg_volume)
get_stock_quote.command = "!stock"