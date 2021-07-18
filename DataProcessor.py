import pandas as pd
from dartConnect import dartConnect
from FileReader import FileRader

class dartConnect:
    def api_key_read(self, path):
        filereader = FileRader()
        api_dict = filereader.read_data('C:\\Users\\user\\Documents\\api_key.txt')
        api_key = api_dict['api_key']
        return api_key

    def dart_manipulate(self,name,api_key) -> dict:
        ds_fs = dartConnect.dart_download_company(name, api_key)

        ds_fs = ds_fs[ds_fs.columns.drop(list(ds_fs.filter(regex='class')))]
        ds_fs = ds_fs.drop(['concept_id', 'label_en'], axis=1)
        ds_fs = ds_fs.replace('', None)

        # unpivot = ds_fs.melt(id_vars=['label_ko'], var_name='date', value_name='values')
        # unpivot['name'] = name
        # unpivot['date'] = pd.to_datetime(unpivot['date'].str.split('-').str[1])
        # unpivot = unpivot.where(unpivot.notnull(), None)

        # unpivot = unpivot[['name', 'label_ko', 'values', 'date']]

        # result_data = [tuple(x) for x in unpivot.values]

        # post = postLib.PostgresDataClass(host='localhost', database='analysis', user='postgres', password='postgres')
        # post.insert_list(result_data, 'stock.financial_statements')
        return None