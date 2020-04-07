"""PreProcessing of Data"""
# pylint: disable-msg = E0401, C0103, W0702, C0200, R0903
from BackendModule.ConfigFiles.config_odi_file import config_ODI
from BackendModule.ConfigFiles.config_t20_file import config_T20

class DataPreProcess:
    """This class contain method to manipulate data"""

    @staticmethod
    def cal_range(df, cols):
        """
        :param df:
        :param cols:
        :return:
        """
        col_range = dict()
        for i in cols:
            val = dict()
            val['min'] = df[i].min()
            val['max'] = df[i].max()
            col_range[i] = val
        return col_range


class DataEncodeDecode_ODI:
    """Method to encode decode and get key from data"""
    @staticmethod
    def get_key(val, my_dict):
        """
        function to return key for any value
        :param val:
        :param my_dict:
        :return:
        """
        for key, value in my_dict.items():
            if val == value:
                return key
        return "BAD Value"

    @staticmethod
    def encode_tupple(col, row):
        """
        Convert String to Numerical Value
        :param col:
        :param row:
        :return:
        """
        new_row = list()
        for i in range(0, len(col)):
            try:
                new_row.append(config_ODI[col[i]][row[i]])
            except:
                new_row.append(float(row[i]))
        return new_row

    @staticmethod
    def decode_tupple(col, row):
        """
        Convert Numerical to String Value
        :param col:
        :param row:
        :return:
        """
        new_row = list()
        for i in range(0, len(col)):
            new_row.append(DataEncodeDecode_ODI.get_key(row[i], config_ODI[col[i]]))
        return new_row

class DataEncodeDecode_T20:
    """Method to encode decode and get key from data"""
    @staticmethod
    def get_key(val, my_dict):
        """
        function to return key for any value
        :param val:
        :param my_dict:
        :return:
        """
        for key, value in my_dict.items():
            if val == value:
                return key
        return "BAD Value"

    @staticmethod
    def encode_tupple(col, row):
        """
        Convert String to Numerical Value
        :param col:
        :param row:
        :return:
        """
        new_row = list()
        for i in range(0, len(col)):
            try:
                new_row.append(config_T20[col[i]][row[i]])
            except:
                new_row.append(float(row[i]))
        return new_row

    @staticmethod
    def decode_tupple(col, row):
        """
        Convert Numerical to String Value
        :param col:
        :param row:
        :return:
        """
        new_row = list()
        for i in range(0, len(col)):
            new_row.append(DataEncodeDecode_T20.get_key(row[i], config_T20[col[i]]))
        return new_row
