# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
sys.path.append('C:\\Users\\user\\Anaconda3\\libs')
import postLib
import dart_fss as dart
import pandas as pd
import numpy as np
from FileReader import FileRader

def main ():

    filereader = FileRader()
    api_dict = filereader.api_key_read('C:\\Users\\user\\Documents\\api_key.txt')


    api_key = api_dict['api_key']
    # name = '삼성전자'
    name = input("종목명: ")

    dart.set_api_key(api_key=api_key)
    corp_list = dart.get_corp_list()
    # a = dart.get_corp_list()
    print(corp_list)

    samsung = corp_list.find_by_corp_name(name, exactly=True)[0]
    fs = samsung.extract_fs(bgn_de='20200101', report_tp=['annual','quarter'])

    # tms = fs[0]
    tms2 = fs['is']

    fs.save()

    ds_fs = pd.DataFrame()
    ds_fs = ds_fs.append(tms2)

    #%%
    column_list = []

    for j,k in ds_fs.columns.tolist() :
        if "연결재무제표" in k :
            column_list.append(str(j))
        else :
            column_list.append(str(k))


    ds_fs.columns = column_list

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
