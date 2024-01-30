from constants import Constants
import pandas as pd
from dataclasses import dataclass




@dataclass(slots = True)
class DataCleaning:
    ''' In future we can extend this class methods or split data cleaning into smaller methods .'''
    uncleaned_data : pd.DataFrame
    original_data : pd.DataFrame
    
    def clean_data(self) -> pd.DataFrame:
        """
        This function is responsible data cleaning and formatting
        """
        data                              = self.uncleaned_data.copy()
        data                              = data.rename(columns={'Phone':'InternationalPhoneNumber'})
        
        phone                             = data['InternationalPhoneNumber'].str.extract(Constants.REGEX_PHONE)
        data['FormattedPhoneNumber']      = '(' + phone[0] + ')' + ' ' + phone[1] + '-' + phone[2]
        data['Company_name']              = data['Company_name'].str.extract(Constants.REGEX_NAME)
        address_split                     = data['Full_Address'].str.extract(Constants.REGEX_ADDRESS)
        data.loc[:,address_split.columns] = address_split
        data['MatchName']                 = self.original_data['namecitystate']
        activity_name                     = data['Activit_description'].str.extract(Constants.REGEX_ACTIVITY_NAME)
        data['Activit_description']       = activity_name[0].fillna(activity_name[1])
        
        data.loc[data.Activit_description.str.contains("€",na=False, regex=True), 'Activit_description'] = ''
        data.loc[data.Website.str.contains("www.google.com",na=False, regex=True), 'Website']            = ''
        
        # Read oringinal again to get all colums on on output
        original_data = self.original_data.rename(columns = Constants.NEW_COLUMN_NAMES)
        # merging original & searched data
        merged_data = pd.merge(data,original_data,left_index=True,right_index=True) 
        final_data = merged_data[~( data.Company_name.isna()|data.Full_Address.isna())]
        return final_data