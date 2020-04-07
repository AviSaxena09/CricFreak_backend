"""This file contain configuration for file directories"""
# pylint: disable-msg = E0401, C0103
import project_config
MAIN_DIRECTORY = project_config.configuration['BaseDirectory']

class GetDirectory:
    """Class containing all the methods for getting directory"""
    @staticmethod
    def get_ODI_ver_1_path():
        """
        :return:
        """
        return MAIN_DIRECTORY+ r"/Data/ODI_clean_ver_1.csv"

    @staticmethod
    def get_T20_ver_1_path():
        """
        :return:
        """
        return MAIN_DIRECTORY+ r"/Data/T20_Data/T20_clean_ver_1.csv"

    @staticmethod
    def get_ODI_score_path():
        """
        :return:
        """
        return MAIN_DIRECTORY+ r"/Data/score.csv"

    @staticmethod
    def get_T20_score_path():
        """
        :return:
        """
        return MAIN_DIRECTORY+ r"/Data/T20_Data/score_t20.csv"

    @staticmethod
    def get_Player_Data_path():
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/Player_Data.csv"

    @staticmethod
    def get_country_summary_path(cname, FORMAT):
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/Stats_JSON/country_summary/" + \
               FORMAT \
               +"/" + cname +r".json"

    @staticmethod
    def get_series_summary_path(FORMAT):
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/Stats_JSON/Series_summary/" + \
               FORMAT \
               +"/series_summ" + r".json"

    @staticmethod
    def get_API_info_path():
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/API_info/api_info_data.csv"

    @staticmethod
    def get_final_score_Prediction_path(FORMAT):
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/PredictionModels/" + \
               FORMAT \
               +"_CoursePrediction_LinearRegre_ver_1.pkl"

    @staticmethod
    def get_wicket_prediction_knn_path(FORMAT):
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/PredictionModels/"+FORMAT+\
               "_wicket_knn_model_v1.pkl"

    @staticmethod
    def get_wicket_prediction_svm_path(FORMAT):
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/PredictionModels/" + FORMAT + \
               "_wicket_svm_model_v1.pkl"

    @staticmethod
    def get_news_file_path():
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/HomePage/news.json"

    @staticmethod
    def get_team_rank_file_path(gender, ftype):
        """
        :param gender:
        :param ftype:
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/HomePage/team_ranking_"+gender+"_"+ftype+".json"

    @staticmethod
    def get_player_rank_file_path(gender, ftype, ttype):
        """
        :param gender:
        :param ftype:
        :param ttype:
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/HomePage/player_ranking_" +\
               gender + "_" + ftype +"_"+ttype+ ".json"

    @staticmethod
    def get_upcoming_match_file_path():
        """
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/HomePage/upcoming_match.json"

    @staticmethod
    def get_ipl_record_file_path(rtype):
        """
        :param rtype:
        :return:
        """
        return MAIN_DIRECTORY + r"/Data/IPL_Records/"+rtype+".json"
