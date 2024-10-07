# run all webscraping scripts here when done
import pandas, web_scraping

def main():
    #imports devices csv file into dataframe
    devices = pandas.read_csv("URL/DEVICES.csv")

    #executes web scraping on the url
    for url in devices["URL"]:
        web_scraping.geodnet(url)


if __name__ == "__main__":
    main()