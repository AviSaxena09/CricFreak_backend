"""This Class deals with loading all different DataFrame"""
# pylint: disable-msg = C0103, E0401
import pandas as pd
from BackendModule.ConfigFiles.directory_config import GetDirectory

class LoadData:
    """Method to load Dataframes"""
    @staticmethod
    def get_ODI_ver_1_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_ODI_ver_1_path())

    @staticmethod
    def get_T20_ver_1_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_T20_ver_1_path())

    @staticmethod
    def get_ODI_score_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_ODI_score_path())

    @staticmethod
    def get_T20_score_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_T20_score_path())

    @staticmethod
    def get_Player_Data_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_Player_Data_path())

    @staticmethod
    def get_API_info_df():
        """
        :return:
        """
        return pd.read_csv(GetDirectory.get_API_info_path())
