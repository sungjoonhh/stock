# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
sys.path.append('C:\\Users\\user\\Anaconda3\\libs')
import postLib
import pandas as pd
import numpy as np
from FileReader import FileRader
from dartConnect import dartConnect

def main ():

    filereader = FileRader()
    api_dict = filereader.api_key_read('C:\\Users\\user\\Documents\\api_key.txt')
    api_key = api_dict['api_key']
    # name = '삼성전자'
    name = input("종목명: ")
    ds_fs = dartConnect.dart_download_company(name,api_key)


    post = postLib.PostgresDataClass(host='localhost', database='analysis', user='postgres', password='postgres')

    ds_fs = ds_fs[ds_fs.columns.drop(list(ds_fs.filter(regex='class')))]
    ds_fs = ds_fs.drop(['concept_id', 'label_en'], axis=1)
    ds_fs = ds_fs.replace('', None)

    unpivot = ds_fs.melt(id_vars=['label_ko'], var_name='date', value_name='values')
    unpivot['name'] = name
    unpivot['date'] = pd.to_datetime(unpivot['date'].str.split('-').str[1])
    unpivot = unpivot.where(unpivot.notnull(), None)

    unpivot = unpivot[['name', 'label_ko', 'values', 'date']]

    result_data = [tuple(x) for x in unpivot.values]

    post.insert_list(result_data, 'stock.financial_statements')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
