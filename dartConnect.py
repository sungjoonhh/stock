import dart_fss as dart
import pandas as pd
from FileReader import FileReader


class dartConnect:
    def __init__(self):
        api_key =self.api_key_read()
        dart.set_api_key(api_key=api_key)
        self.corp_list = dart.get_corp_list()

    def dart_download_company(self,name, api_key):
        company = self.dart.corp_list.find_by_corp_name(name, exactly=True)[0]
        fs = company.extract_fs(bgn_de='20200101', report_tp=['annual', 'quarter'])

        tms2 = fs['is']

        fs.save()

        ds_fs = pd.DataFrame()
        ds_fs = ds_fs.append(tms2)

        # %%
        column_list = []

        for j, k in ds_fs.columns.tolist():
            if "연결재무제표" in k:
                column_list.append(str(j))
            else:
                column_list.append(str(k))

        ds_fs.columns = column_list

    def get_company_code(self,name):
        return self.corp_list.find_by_corp_name(name, exactly=True)[0]


    def api_key_read(self):
        file = FileReader()
        api_dict = file.read_data('C:\\Users\\user\\Documents\\api_key.txt')
        api_key = api_dict['api_key']
        return api_key