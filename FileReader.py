import pandas as pd

class FileRader:
    def read_data(self, path) -> dict:
        """

        :rtype: object
        """
        ret_val = {}
        fp = open(path, 'r')
        read_line = fp.readlines()
        for itr in read_line:
            temp = itr.split('=')
            ret_val[temp[0]] = temp[1].replace('\n','')
        return ret_val

