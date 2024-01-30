from collections import namedtuple
from typing import Dict


# Trying to create object of namedtuple class so that , they are immutable .
class Constants():
    '''Regular expression to extract the data '''
    REGEX_ADDRESS       = r"""(?P<Address>.*?)\,\s(?P<CITY>.*?)\,\s(?P<State>.*)\s(?P<Zip>\d+)"""
    REGEX_PHONE         = r"""\+\d\s(\d+)\-(\d+)-(\d+)"""
    REGEX_NAME          = r"""(?:(.+?\\n.*|.*))"""
    # REGEX_COUNTRY       = r"""(US)"""
    REGEX_ACTIVITY_NAME = r"""^(?:(?:(.*)\sin\s.*)|(.*))$"""
    
    ''' mapping dictionary'''
    NEW_COLUMN_NAMES : Dict  = {'COMPANY_NAME':'O_NAME',
                                'ADDRESS':'O_ADDRESS',
                                'CITY':'O_CITY',
                                'STATE':'O_STATE',
                                'ZIP':'O_ZIP'
                                }