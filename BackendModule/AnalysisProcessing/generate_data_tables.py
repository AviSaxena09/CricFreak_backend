"""This file contain classes to generate tables for statistics"""
# pylint: disable-msg = E0401, C0103, W0702, E1101, R0903
import pandas as pd
from BackendModule.DataProcessess import load_data_frame
from BackendModule.ConfigFiles.directory_config import GetDirectory


class GenerateSeriesSummary:
    """This class contains methods to create Series ODI T20 summary data tables"""

    @staticmethod
    def init_graph(FORMAT):
        """
        :param FORMAT:
        :return:
        """
        if FORMAT == "ODI":
            df = load_data_frame.LoadData.get_ODI_ver_1_df()
            score_match = load_data_frame.LoadData.get_ODI_score_df()
        elif FORMAT == "T20":
            df = load_data_frame.LoadData.get_T20_ver_1_df()
            score_match = load_data_frame.LoadData.get_T20_score_df()
        df = df.merge(score_match, on='match_id')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = pd.DatetimeIndex(df['date']).year
        return df

    @staticmethod
    def create_series_db(seriesName, df):
        """
        :param seriesName:
        :param df:
        :return:
        """
        df_series = df[(df['series'] == seriesName)]
        df_series = df_series[['match_id', 'date', 'season', 'series',
                               'competition', 'city', 'venue',
                               'neutralvenue', 'toss_winner',
                               'toss_decision', 'team_1', 'team_2', 'method',
                               'player_of_match', 'winner_runs', 'winner_wickets',
                               'win_runs', 'win_wickets', 'winner', 'final_score',
                               'year']]
        df_series = (df_series.groupby('match_id')).first()
        return df_series

    @staticmethod
    def create_series_summary(FORMAT, df, lst_series):
        """
        :param FORMAT:
        :param df:
        :param lst_series:
        :return:
        """
        rows = list()
        for seriesName in lst_series:
            r = GenerateSeriesSummary.series_data_row(
                GenerateSeriesSummary.create_series_db(seriesName, df),
                seriesName)
            rows.append(r)
        tb_col = ['Series', 'Season', 'Total Matches',
                  'Margin', 'Highest Score',
                  'Player(s) of the Match', 'Winner', 'Year']
        summ_series = pd.DataFrame(rows)
        summ_series.columns = tb_col
        summ_series = summ_series.sort_values(by='Year', ascending=False)
        return GenerateSeriesSummary.write_series_summ_json(FORMAT, summ_series)

    @staticmethod
    def series_data_row(dt, seriesName):
        """
        :param dt:
        :param seriesName:
        :return:
        """
        t1 = dt['team_1'].iloc[0]
        wt1 = wt2 = 0
        for i in range(0, len(dt)):
            if dt['winner'].iloc[i] == t1:
                wt1 += 1
            else:
                wt2 += 1
        row = [seriesName]
        row.append(dt['season'].iloc[0])
        row.append(len(dt))
        row.append(str(wt1) + "-" + str(wt2))
        row.append(dt['final_score'].max())
        row.append(list(dt['player_of_match'].unique()))
        row.append(dt['winner'].max())
        row.append(dt['year'].min())
        return row

    @staticmethod
    def write_series_summ_json(FORMAT, d):
        """
        :param FORMAT:
        :param d:
        :return:
        """
        out = d.to_json(orient='records')[1:-1].replace('},{', '},{')
        obj = """{""" + """    "Data":[""" + out + """]}"""
        obj.replace('\'', ' ')
        obj.replace('\n', ' ')
        f = open(GetDirectory.get_series_summary_path(FORMAT), "w")
        f.write(obj)
        f.close()


class GenerateCountrySummary:
    """This class contains methods to create Series ODI T20 summary data tables"""

    @staticmethod
    def create_country_wise_summary(FORMAT, df, con_name):
        """
        :param FORMAT:
        :param df:
        :param con_name:
        :return:
        """
        common_wealth = ['Afghanistan', 'Australia', 'Bangladesh',
                         'England', 'India', 'Ireland',
                         'New Zealand', 'Pakistan', 'South Africa',
                         'Sri Lanka', 'West Indies', 'Zimbabwe']
        common_wealth.remove(con_name)
        tb_col = ['Opponent', 'Matches', 'Won', 'Lost',
                  'Highest Total', 'Lowest Total', 'Average Score',
                  'Median Score', 'Won%', 'From', 'To']
        rows = list()
        for i in common_wealth:
            rows.append(GenerateCountrySummary.con_data_row(df[df['opponent'] == i], con_name, i))
        summ_con = pd.DataFrame(rows)
        summ_con.columns = tb_col
        GenerateCountrySummary.write_con_summ_json(FORMAT, summ_con, con_name)

    @staticmethod
    def con_data_row(d, con_name, o_name):
        """
        :param d:
        :param con_name:
        :param o_name:
        :return:
        """
        row = [o_name]
        try:
            row.append(len(d['match_id'].unique()))
        except:
            row.append(str("NA"))
        try:
            row.append(len(d[d['winner'] == con_name]['match_id'].unique()))
        except:
            row.append(str("NA"))
        try:
            row.append(len(d[d['winner'] == o_name]['match_id'].unique()))
        except:
            row.append(str("NA"))
        try:
            row.append(d['final_score'].max())
        except:
            row.append(str("NA"))
        try:
            row.append(d['final_score'].min())
        except:
            row.append(str("NA"))
        try:
            row.append(int(d['final_score'].mean()))
        except:
            row.append(str("NA"))
        try:
            row.append(int(d['final_score'].median()))
        except:
            row.append(str("NA"))
        try:
            row.append(round((row[2] / row[1]) * 100, 2))
        except:
            row.append(str("NA"))
        try:
            row.append(d['year'].min())
        except:
            row.append(str("NA"))
        try:
            row.append(d['year'].max())
        except:
            row.append(str("NA"))
        return row

    @staticmethod
    def write_con_summ_json(FORMAT, d, cname):
        """
        :param FORMAT:
        :param d:
        :param cname:
        :return:
        """
        out = d.to_json(orient='records')[1:-1].replace('},{', '},{')
        obj = """{""" + ''' "Country_Name" : [{"Country" : "''' + \
              cname + '''"}],''' + """ "Data":[""" + \
              out + """]}"""
        obj = obj.replace('\n', ' ')
        f = open(GetDirectory.get_country_summary_path(cname, FORMAT), "w")
        f.write(obj)
        f.close()
        return obj


class SupportDB:
    """Class providing common supporting functions"""

    @staticmethod
    def create_country_db(FORMAT, country_name, df):
        """
        :param FORMAT:
        :param country_name:
        :param df:
        :return:
        """
        if FORMAT == 'ODI':
            df = df.merge(load_data_frame.LoadData.get_ODI_score_df(), on='match_id')
        elif FORMAT == 'T20':
            df = df.merge(load_data_frame.LoadData.get_T20_score_df(), on='match_id')
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = pd.DatetimeIndex(df['date']).year
        df_country = df[(df['team_1'] == country_name) | (df['team_2'] == country_name)]
        df_country["team_1"] = df_country["team_1"].replace(country_name, '')
        df_country["team_2"] = df_country["team_2"].replace(country_name, '')
        df_country['opponent'] = df_country['team_1'] + df_country['team_2']
        df_country = df_country.drop(['team_1', 'team_2'], axis=1)
        return df_country
