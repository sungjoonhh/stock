import pandas as pd

class FileRader:
    def api_key_read(self, path) -> dict:
        ret_val = {}
        fp = open(path, 'r')
        read_line = fp.readlines()
        for itr in read_line:
            temp = itr.split(':')
            ret_val[temp[0]] = temp[1]
        return ret_val

