import pandas, web_scraping, log_keeper, reporter
from datetime import datetime

#def report():

def main():
    #imports devices csv file into dataframe
    devices = pandas.read_csv("DEVICES.csv")

    #stamps the log with current date & time (only necessary to keep it readable for humans)
    log_keeper.init()

    #executes web scraping and sends telegram msgs about the state of each device id, location
    for index,row in devices.iterrows():
        #webscraping with selenium on geodnet website
        #Input: Device ID, Location, URL, Wait time in seconds
        #Output: records the results of the operations in "logbook.txt" file
        web_scraping.selenium_geodnet(row["ID"],row["LOCATION"],row["URL"],60)

    reporter.report(datetime.now().date())


if __name__ == "__main__":
    main()