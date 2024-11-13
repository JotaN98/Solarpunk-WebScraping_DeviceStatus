import pandas, web_scraping, log_keeper
from datetime import datetime

def main():
    #imports devices csv file into dataframe
    devices = pandas.read_csv("DEVICES.csv")

    #stamps the log with current date & time
    #(only necessary to keep it readable for humans)
    log_keeper.init()

    #executes web scraping of each devices status according to their id, location, url
    for index,row in devices.iterrows():
        #webscraping with selenium on geodnet website
        #Input: Device ID, Location, URL, Wait time in seconds
        #Output: records the results of the operations in "logbook.txt" file
        web_scraping.selenium_geodnet(row["ID"],row["LOCATION"],row["URL"],40)

        # a consider hromdeiver installer a cada iteração
        # tme.sleep nao boa pratica, esperar por eventos

    #Sends a report of today as a telegram msg
    log_keeper.report(datetime.now().date())


if __name__ == "__main__":
    main()