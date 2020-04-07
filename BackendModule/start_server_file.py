"""This file initiates and run all startup functions"""
# pylint: disable-msg = E0401, W0702
from BackendModule.ConfigFiles import config_odi_file, config_t20_file
from BackendModule.AnalysisProcessing.generate_data_tables import GenerateCountrySummary, \
    SupportDB, GenerateSeriesSummary
from BackendModule.DataProcessess import load_data_frame
from BackendModule.ScrapingMethods.home_page_scraping import scrap_data
from project_config import common_wealth, configuration

print("Current Main Directory is : ", configuration['BaseDirectory'])
print("Want to Generate New JSON objects for Country Summary : (1 / 0)")
ANS = int(input())
if ANS == 1:
    print("Generating Country Summary.......")
    DF_ODI_V1 = load_data_frame.LoadData.get_ODI_ver_1_df()
    DF_T20_V1 = load_data_frame.LoadData.get_T20_ver_1_df()
    for cName in common_wealth:
        GenerateCountrySummary.create_country_wise_summary('ODI',
                                                           SupportDB.create_country_db('ODI',
                                                                                       cName,
                                                                                       DF_ODI_V1),
                                                           cName)
        GenerateCountrySummary.create_country_wise_summary('T20',
                                                           SupportDB.create_country_db('T20',
                                                                                       cName,
                                                                                       DF_T20_V1),
                                                           cName)
        print(cName, "JSON Created Successfully")
#######################################################################
print("Want to Generate New JSON objects for Series Summary : (1 / 0)")
ANS = int(input())
if ANS == 1:
    print("Generating Series Summary.......")
    DF = GenerateSeriesSummary.init_graph("ODI")
    GenerateSeriesSummary.create_series_summary("ODI",
                                                DF,
                                                list(config_odi_file.config_ODI['series'].keys()))
    print("ODI summary Created Successfully.......")
    DF = GenerateSeriesSummary.init_graph("T20")
    GenerateSeriesSummary.create_series_summary("T20",
                                                DF,
                                                list(config_t20_file.config_T20['series'].keys()))
    print("T20 summary Created Successfully.......")
    print("Series Summary JSON Created Successfully")

##########################################################
print("Want to Generate New JSON objects for Home Page Using Scraping : (1 / 0)")
ANS = int(input())
if ANS == 1:
    gender = ['mens', 'womens']
    T_TYPES = ['ball', 'bat', 'all_rounder']
    F_TYPES = ['odi', 't20i', 'test']
    print("Performing Scraping.......")
    print("Retrieving upcoming Match Data.")
    scrap_data.upcoming_matches()
    print("Retrieving Latest News")
    scrap_data.news()
    print("Retreive Team Rankings")
    for gn in gender:
        for ft in F_TYPES:
            print("Creating FOR : ", gn, " ", ft)
            try:
                scrap_data.team_ranking(gn, ft)
                print("Created FOR : ", gn, " ", ft)
            except:
                print("Failed FOR : ", gn, " ", ft)

    print("Retreiving Player Rankings")
    for gn in gender:
        for ft in F_TYPES:
            for tt in T_TYPES:
                print("Creating FOR : ", gn, " ", ft, " ", tt)
                try:
                    scrap_data.player_ranking(gn, ft, tt)
                    print("Created FOR : ", gn, " ", ft, " ", tt)
                except:
                    print("Failed FOR : ", gn, " ", ft, " ", tt)

##########################################################
print("Want to Generate New JSON objects for IPL Records Using Scraping : (1 / 0)")
ANS = int(input())
if ANS == 1:
    IPL_RECORD_FUNC_INPUTS = ['most-runs', 'most-sixes', 'most-sixes-innings',
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

    for rtype in IPL_RECORD_FUNC_INPUTS:
        print("Generating file for ", rtype)
        try:
            scrap_data.ipl_records(rtype)
            print("\tCreated file for ", rtype)
        except:
            print("Unable to scrap data for ipl record ", rtype)

##########################################################


print("All Processes called Successfully")
