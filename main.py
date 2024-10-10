# run all webscraping scripts here when done
import pandas, web_scraping

def main():
    #imports devices csv file into dataframe
    devices = pandas.read_csv("DEVICES.csv")

    #executes web scraping and sends telegram msgs about the state of each device id, location
    for index,row in devices.iterrows():
        #webscraping with selenium on geodnet website
        # Input: Device ID, Location, URL, Wait time in seconds
        web_scraping.selenium_geodnet(row["ID"],row["LOCATION"],row["URL"],60)


if __name__ == "__main__":
    main()