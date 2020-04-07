"""This .py file contains API methods and use Flask to make server LIVE"""
# pylint: disable-msg = C0103, E0401, W0702, W1201
import socket
import sys
sys.path.append("../")
import logging
from datetime import datetime
import project_config
from flask import Flask, request
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from BackendModule.Predictions import predictions_all_format
from BackendModule.ScrapingMethods.home_page_scraping import scrap_data
from BackendModule.ConfigFiles.directory_config import GetDirectory
from BackendModule.ConfigFiles import load_variable_config
from BackendModule.DataProcessess.data_processing import DataEncodeDecode_ODI, DataEncodeDecode_T20
from BackendModule.AnalysisProcessing.player_data_process import PlayerData

print("All Files and Libraries imported Successfully !")

IP_ADDRESS = "0.0.0.0"#socket.gethostbyname(socket.gethostname())
CLOUD_ADDRESS = "18.217.135.203"
PORT_NUMBER = 5100
APP = Flask(__name__, static_folder='WebServices')
CORS(APP)

now = datetime.now()
dt_string = now.strftime("\nON            :       %d/%m/%Y\nAT            :       %H:%M:%S")
logging.basicConfig(filename='logsession.log', level=logging.DEBUG)
logging.debug('SERVER STARTED at project config : ' +
              str(project_config.configuration) + ' : ' +
              project_config.developer_key)
logging.info(dt_string)
logging.warning('')


@APP.route('/info', methods=['GET', 'POST'])
@cross_origin()
def api_info():
    """
    :return:
    """
    load_variable_config.api_info_df['PORT_NUMBER'] = PORT_NUMBER
    load_variable_config.api_info_df['Server ID'] = CLOUD_ADDRESS
    return load_variable_config.api_info_df.to_html()


@APP.route('/get_con_summ', methods=['GET', 'POST'])
@cross_origin()
def country_summary_API():
    """
    :return:
    """
    try:
        cName = request.form['country']
        FORMAT = request.form['format']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if cName in project_config.common_wealth:
        try:
            obj = open(GetDirectory.get_country_summary_path(cName, FORMAT), "r")
            info = obj.read()
            obj.close()
            return info
        except:
            return "Server is Currently Facing issue retriving the File."
    else:
        return "Invalid Country Data Requested. Please make sure the value is in format : 'India' !"


@APP.route('/get_series_summ', methods=['GET', 'POST'])
@cross_origin()
def series_summary_API():
    """
    :return:
    """
    try:
        FORMAT = request.form['format']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    try:
        obj = open(GetDirectory.get_series_summary_path(FORMAT), "r")
        info = obj.read()
        obj.close()
    except:
        return "Server is Currently Facing issue retriving the File."
    return info


@APP.route('/predict_course_score', methods=['GET', 'POST'])
@cross_origin()
def predict_Course_Score():
    """
    :return:
    """
    values = ["city", "neutralvenue", "toss_winner", "toss_decision",
              "team_1", "team_2", "batsman", "non_striker", "bowler", "extras_run",
              "player_out", "wickets", "curr_score", "remaining_ball"]
    try:
        FORMAT = request.form['format']
        vals = list()
        for v in values:
            vals.append(str(request.form[v]))
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"

    if FORMAT == "ODI":
        in_vals = DataEncodeDecode_ODI.encode_tupple(values, vals)
        value_predicted = predictions_all_format.Prediction.predict_course(
            load_variable_config.ODI_model_final_score_predict, [in_vals])
    elif FORMAT == "T20":
        in_vals = DataEncodeDecode_T20.encode_tupple(values, vals)
        value_predicted = predictions_all_format.Prediction.predict_course(
            load_variable_config.T20_model_final_score_predict, [in_vals])
    else:
        return '{"Error" : Invalid Format Requested }'
    return """{ "range" : [""" + str((value_predicted // 10) * 10) + \
           ', ' + str((value_predicted // 10 + 1) * 10) + """] , "score" : """ + \
           str(value_predicted) + """ }"""


@APP.route('/predict_wicket', methods=['GET', 'POST'])
@cross_origin()
def predict_Wicket():
    """
    :return:
    """
    values = ['city', 'venue', 'neutralvenue', 'toss_decision',
              'toss_winner', 'inning_no', 'team_1', 'team_2',
              'team_bat', 'batsman', 'non_striker', 'bowler',
              'over', 'player_out', 'run', 'extras_run', 'total_run',
              'batsman_score', 'non_striker_score', 'current_score',
              'current_wicket']
    try:
        FORMAT = request.form['format']
        vals = list()
        for v in values:
            vals.append(str(request.form[v]))
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if FORMAT == "ODI":
        in_vals = DataEncodeDecode_ODI.encode_tupple(values, vals)
        obj = str(predictions_all_format.Prediction.predict_wicket(
            load_variable_config.ODI_model_1_wicket_prediction_knn,
            load_variable_config.ODI_model_2_wicket_prediction_svm,
            [in_vals], str(request.form['over'])))
    elif FORMAT == "T20":
        in_vals = DataEncodeDecode_ODI.encode_tupple(values, vals)
        obj = str(predictions_all_format.Prediction.predict_wicket(
            load_variable_config.T20_model_1_wicket_prediction_knn,
            load_variable_config.T20_model_2_wicket_prediction_svm,
            [in_vals], str(request.form['over'])))
    else:
        return '{"Error" : Invalid Format Requested }'
    return obj


@APP.route('/get_player_info', methods=['GET', 'POST'])
@cross_origin()
def get_playerData_info():
    """
    :return:
    """
    try:
        pid = request.form['player_id']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    return PlayerData.get_player_data(load_variable_config.player_data_df, 'player_id', int(pid))


@APP.route('/player_ranking', methods=['GET', 'POST'])
@cross_origin()
def retreive_player_ranking():
    """
    :return:
    """
    try:
        gn = request.form['gender']
        ft = request.form['format']
        tt = request.form['ttype']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if (gn in load_variable_config.gender) \
            and (ft in load_variable_config.ftypes) \
            and (tt in load_variable_config.ttypes):
        try:
            obj = open(GetDirectory.get_player_rank_file_path(gn, ft, tt), "r")
            info = obj.read()
            obj.close()
            return info
        except:
            return "Server is Currently Facing issue retriving the File."
    else:
        return "Invalid Parameter Data !!"


@APP.route('/team_ranking', methods=['GET', 'POST'])
@cross_origin()
def retreive_team_ranking():
    """
    :return:
    """
    try:
        gn = request.form['gender']
        ft = request.form['format']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if (gn in load_variable_config.gender) \
            and (ft in load_variable_config.ftypes):
        try:
            obj = open(GetDirectory.get_team_rank_file_path(gn, ft), "r")
            info = obj.read()
            obj.close()
            return info
        except:
            return "Server is Currently Facing issue retriving the File."
    else:
        return "Invalid Parameter Data !!"


@APP.route('/ipl_records', methods=['GET', 'POST'])
@cross_origin()
def retreive_ipl_records():
    """
    :return:
    """
    try:
        rtype = request.form['record_type']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if rtype in load_variable_config.ipl_record_function_inputs:
        try:
            obj = open(GetDirectory.get_ipl_record_file_path(rtype), "r")
            info = obj.read()
            obj.close()
            return info
        except:
            return "Server is Currently Facing issue retriving the File."
    else:
        return "Invalid Parameter Data !!"


@APP.route('/get_live_score', methods=['GET', 'POST'])
@cross_origin()
def get_live_score():
    """
    :return:
    """
    try:
        mtype = request.form['match_type']
    except:
        return "Incorrect Parameter in form data sent !!" \
               "For info try Address/info API (pass parameter passkey = 'API passkey given')"
    if (mtype in ['International', 'Domestic']):
        try:
            curr_score = scrap_data.live_score(mtype)
            return "{" + str(curr_score) + "}"
        except:
            return "Error Establishing Connection to HOST"
    else:
        return "Invalid Parameter Data !!"


@APP.route('/latest_news', methods=['GET', 'POST'])
@cross_origin()
def retreive_latest_news():
    """
    :return:
    """
    try:
        obj = open(GetDirectory.get_news_file_path(), "r")
        info = obj.read()
        obj.close()
        return info
    except:
        return "Server is Currently Facing issue retriving the File."


@APP.route('/upcoming_matches', methods=['GET', 'POST'])
@cross_origin()
def retreive_upcoming_matches():
    """
    :return:
    """
    try:
        obj = open(GetDirectory.get_upcoming_match_file_path(), "r")
        info = obj.read()
        obj.close()
        return info
    except:
        return "Server is Currently Facing issue retriving the File."


@APP.route('/kill_server', methods=['GET', 'POST'])
@cross_origin()
def kill_server():
    """
    :return:
    """
    try:
        pwd = request.form['pass_key']
    except:
        return '{ "Status" : "Invalid body parameter given (pass_key parameter missing)"}'
    if pwd == load_variable_config.server_pass_key:
        print("Server Closed using kill_server service")
        sys.exit()
    else:
        return '{ "Status" : "Invalid pass_key Given"}'


@APP.route('/get_logs', methods=['GET', 'POST'])
@cross_origin()
def send_logs():
    """
    :return:
    """
    file = open('logsession.log', 'r')
    log_data = '<html>'
    for each in file:
        log_data += each + '<br>'
    log_data += '</html>'
    return log_data


if __name__ == "__main__":
    print("Server Address                 : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/\n")
    print("getAPIinfo         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/info")
    print("getConSumm         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/get_con_summ")
    print("getSerSumm         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/get_series_summ")
    print("PrediScore         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/predict_course_score")
    print("PredWicket         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/predict_wicket")
    print("getPlaData         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/get_player_info")
    print("getPlaRnkg         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/player_ranking")
    print("getTemRnkg         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/team_ranking")
    print("getLastNws         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/latest_news")
    print("getUpcmgMt         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/upcoming_matches")
    print("getIPLRrds         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/ipl_records")
    print("getLIVScor         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/get_live_score")
    print("KillServer         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/kill_server")
    print("GetLogData         Api Address : http://" +
          IP_ADDRESS + ":" + str(PORT_NUMBER) + "/get_logs")
    try:
        print("\n\nServer is Live.")
        SERVER = WSGIServer((IP_ADDRESS, PORT_NUMBER), APP, log=APP.logger)
        SERVER.serve_forever()
    except:
        print("Unexpected Error Occurred !! Cannot HOST the SERVER !!")
