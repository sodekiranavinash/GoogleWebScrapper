import pandas as pd
import os
import time
from browser_manager import BrowserManager
from scraper import Scraper
from dotenv import load_dotenv
from data_cleaning import DataCleaning
from playwright.sync_api import sync_playwright


if __name__ == "__main__": # you should be able to integrate this app into your web apps.
    try:
        load_dotenv()
        base_url : str    = os.getenv("BASE_URL")
        input_file_name : str =  os.getenv("INPUT_FILE")
        input_file_path : str = os.getenv('INPUT_FILE_PATH')
        input_file : str = f"{input_file_path}{input_file_name}"        
        output_file : str = os.getenv("OUTPUT_FILE")
        
        with sync_playwright() as p: # using context manager 
            try:
                browser_manager : BrowserManager = BrowserManager(p,base_url)
                browser_manager.initialize_browser()
                start   = time.time()
                original_data : pd.DataFrame = pd.read_csv(input_file)

                # making common string from available data so that google can understand what we want .
                original_data['namecitystate'] = original_data[['COMPANY_NAME','CITY','STATE']].agg(' '.join, axis=1)      
                          
                # extracts uncleaned data into all_data list from page object
                scraper : Scraper = Scraper(
                    page = browser_manager.page,
                    input_file_name= input_file,
                    company_data_list= original_data['namecitystate']
                    )
                scraper.scrape_data()
                
                uncleaned_data : pd.DataFrame = pd.concat(scraper.all_data,ignore_index=True) # concating uncleaned data
                data_cleaning : DataCleaning = DataCleaning(uncleaned_data,original_data)
                final_data : pd.DataFrame  = data_cleaning.clean_data() # cleaning data with regex functions
                final_data.to_csv(f"{input_file_path}{output_file}",index=False)

                end = time.time()
                print(f"-----file : {input_file_name} took {end - start} to process data and records id numbers with no data are {scraper.records_with_no_data}-----")
            except Exception as e:
                print(e, f"!!!!!!!!!!!! error occurred while scraping data for file : {input_file_name}")
                end = time.time()
                print(f"------------------Process complete and took {end - start} for all files ----------------------------")
    except Exception as e:
        print(e, "!!!!!!!!!!!! error occurred while scraping data, if this timeout error retry once more ....")