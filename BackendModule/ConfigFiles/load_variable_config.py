"""Load Prediction Files"""
# pylint: disable-msg = E0401, C0103, W0702
import pickle
from BackendModule.ConfigFiles import directory_config
from BackendModule.DataProcessess import load_data_frame

print('Setting Server Password..........')
server_pass_key = 'Admin1234'
api_init_key = 'Admin1234'
api_info_df = load_data_frame.LoadData.get_API_info_df()
print("Loading Variable for API Parameters....")
gender = ['mens', 'womens']
ttypes = ['ball', 'bat', 'all_rounder']
ftypes = ['odi', 't20i', 'test']
ipl_record_function_inputs = ['most-runs', 'most-sixes', 'most-sixes-innings',
                              'highest-scores', 'best-batting-strike-rate',
                              'best-batting-strike-rate-innings', 'best-batting-average',
                              'most-fifties', 'most-centuries',
                              'most-fours', 'fastest-fifties', 'fastest-centuries',
                              'most-fours-innings', 'most-wickets',
                              'best-bowling-innings', 'best-bowling-average',
                              'best-bowling-economy', 'best-bowling-strike-rate-innings',
                              'best-bowling-strike-rate', 'most-runs-conceded-innings',
                              'most-hat-tricks', 'most-dot-balls',
                              'most-maidens', 'most-four-wickets']

print("Starting Loading of Models, Dataframes and Variable......")
print("Loading Models.............................")
ODI_model_final_score_predict = pickle.load(
    open(directory_config.GetDirectory.get_final_score_Prediction_path("ODI"),
         'rb'))
T20_model_final_score_predict = pickle.load(
    open(directory_config.GetDirectory.get_final_score_Prediction_path("T20"),
         'rb'))
print("LOADING Wicket MODELS....")
try:
    ODI_model_1_wicket_prediction_knn = pickle.load(
        open(directory_config.GetDirectory.get_wicket_prediction_knn_path("ODI"),
             'rb'))
    ODI_model_2_wicket_prediction_svm = pickle.load(
        open(directory_config.GetDirectory.get_wicket_prediction_svm_path("ODI"),
             'rb'))
    print("\nModels Loaded Sucessfully for ODI")
except:
    print("can't load models ...ODI wicket")
print("Loading T20 models")
try:
    T20_model_1_wicket_prediction_knn = pickle.load(
        open(directory_config.GetDirectory.get_wicket_prediction_knn_path("T20"),
             'rb'))
    T20_model_2_wicket_prediction_svm = pickle.load(
        open(directory_config.GetDirectory.get_wicket_prediction_svm_path("T20"),
             'rb'))
    print("\nModels Loaded Sucessfully for T20")
except:
    print("can't load models for T20")
print("\nModels Loaded procedure completed for T20")

#########################################################################################3
print("Loading DataFrames .  .  .  . . .................................")

player_data_df = load_data_frame.LoadData.get_Player_Data_df()
print("\nDataframes Loaded Successfully .\n")
print("All Files and Variables Loaded into SERVER.PY ........")
print("System Ready !!")

print(directory_config.GetDirectory.get_wicket_prediction_svm_path("T20"))
