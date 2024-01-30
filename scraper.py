from dataclasses import dataclass
from playwright.sync_api import sync_playwright
from typing import List
import time
import pandas as pd

@dataclass
class Scraper:
    page : sync_playwright
    input_file_name : str
    all_data = []
    records_with_no_data = []
    company_data_list : List[str]
        
    def scrape_data(self):
        print(f"----- file : {self.input_file_name} loaded -----")
        
        for count,company_address in enumerate(list(self.company_data_list), start = 1):

            # record_start = time.time()
            self.page.locator("xpath=//textarea[@name='q']").fill(company_address)

            time.sleep(2.5) # waiting so that google doesn't detect unsual traffic & block us
            self.page.keyboard.press("Enter")

            self.page.wait_for_load_state("domcontentloaded")
            time.sleep(1.5) # waiting before compute of data

            if self.find_text_element(self.page,'SPZz6b'):
                self.all_data.append(pd.DataFrame.from_dict(self.single_page_extract(self.page)))
            else:
                self.records_with_no_data.append(count)
                # print(f"NO DATA for record no : {count} ")
    
    def find_text_element(self,html_element,element,selector_type = None,multiple_values = None) -> str:
        """ 
        The functions responsible for extracting the needed data from a specific html element,
        in addition to that this function server as the error handling when html element doesn't exist
        """
        try:
            if multiple_values is not None:
                return self.extract_single_value(html_element.query_selector_all(f".{element}"),"activity_desc")
            if not selector_type:
                return html_element.query_selector(f".{element}").inner_text()
            elif selector_type=="attri":
                if (html_element.query_selector(element)) is not None:
                    return html_element.get_attribute(f"xpath={element}","href")
            else:
                if (html_element.query_selector(element)) is not None:
                    return html_element.locator(f"xpath={element}").inner_text()
        except Exception as e:
            pass
        return None

    def extract_single_value(self,elements,attri) -> str:
        if attri == "activity_desc":
            elements_list = [ element.text_content() for element in elements if element is not None]
            return max(elements_list, key=len)

    def single_page_extract(self,html_element) -> list:
        """
        The function takes a single html page for a single company and 
        extract all information's at once and appends dataframe to global list
        """
        data = {
            "Company_name"       : [self.find_text_element(html_element,'SPZz6b')],
            "Activit_description": [self.find_text_element(html_element,'YhemCb',multiple_values = True)],
            "Full_Address"       : [self.find_text_element(html_element,'LrzXr')],
            "Phone"              : [self.find_text_element(html_element,"//a[@data-dtype='d3ph']","xpath")],
            "Website"            : [self.find_text_element(html_element,"//a[@class='ab_button']","attri")],
            "Status"             : [self.find_text_element(html_element,"//*[@id='Shyhc']","xpath")],
            "date"               : pd.to_datetime('today'),
        }
        
        self.all_data.append(pd.DataFrame.from_dict(data))