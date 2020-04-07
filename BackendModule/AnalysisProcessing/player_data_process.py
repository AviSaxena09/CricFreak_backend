"""This py file contains classes for player data analysis"""
# pylint: disable-msg = E0401, C0103, W0702,R0913
import pandas as pd
class PlayerData:
    """Contain method to analyse player data and create jsons"""
    @staticmethod
    def get_player_data(df, cl, val):
        """
        :param df:
        :param cl:
        :param val:
        :return:
        """
        df = df[df[cl] == val]
        if len(df) == 0:
            return "Invalid Player ID"
        df = df.to_dict(orient='records')
        general_col = ['player_id', 'NAME', 'COUNTRY', 'Full name',
                       'Birthdate', 'Birthplace', 'Age', 'Major teams',
                       'Batting style', 'Bowling style', 'Other']
        bat = ['BATTING_Tests_Mat', 'BATTING_Tests_Inns', 'BATTING_Tests_NO',
               'BATTING_Tests_Runs', 'BATTING_Tests_HS',
               'BATTING_Tests_Ave', 'BATTING_Tests_BF',
               'BATTING_Tests_SR', 'BATTING_Tests_100', 'BATTING_Tests_50',
               'BATTING_Tests_4s', 'BATTING_Tests_6s', 'BATTING_Tests_Ct',
               'BATTING_Tests_St', 'BATTING_ODIs_Mat',
               'BATTING_ODIs_Inns', 'BATTING_ODIs_NO', 'BATTING_ODIs_Runs',
               'BATTING_ODIs_HS', 'BATTING_ODIs_Ave', 'BATTING_ODIs_BF',
               'BATTING_ODIs_SR', 'BATTING_ODIs_100', 'BATTING_ODIs_50',
               'BATTING_ODIs_4s', 'BATTING_ODIs_6s', 'BATTING_ODIs_Ct',
               'BATTING_ODIs_St', 'BATTING_T20Is_Mat', 'BATTING_T20Is_Inns',
               'BATTING_T20Is_NO', 'BATTING_T20Is_Runs', 'BATTING_T20Is_HS',
               'BATTING_T20Is_Ave', 'BATTING_T20Is_BF', 'BATTING_T20Is_SR',
               'BATTING_T20Is_100', 'BATTING_T20Is_50', 'BATTING_T20Is_4s',
               'BATTING_T20Is_6s', 'BATTING_T20Is_Ct', 'BATTING_T20Is_St',
               'BATTING_T20s_Mat', 'BATTING_T20s_Inns', 'BATTING_T20s_NO',
               'BATTING_T20s_Runs', 'BATTING_T20s_HS', 'BATTING_T20s_Ave',
               'BATTING_T20s_BF', 'BATTING_T20s_SR', 'BATTING_T20s_100',
               'BATTING_T20s_50', 'BATTING_T20s_4s', 'BATTING_T20s_6s',
               'BATTING_T20s_Ct', 'BATTING_T20s_St']
        ball = ['BOWLING_Tests_Mat', 'BOWLING_Tests_Inns', 'BOWLING_Tests_Balls',
                'BOWLING_Tests_Runs', 'BOWLING_Tests_Wkts', 'BOWLING_Tests_Ave',
                'BOWLING_Tests_Econ', 'BOWLING_Tests_SR', 'BOWLING_Tests_4w',
                'BOWLING_Tests_5w', 'BOWLING_Tests_10', 'BOWLING_ODIs_Mat',
                'BOWLING_ODIs_Inns', 'BOWLING_ODIs_Balls', 'BOWLING_ODIs_Runs',
                'BOWLING_ODIs_Wkts', 'BOWLING_ODIs_Ave', 'BOWLING_ODIs_Econ',
                'BOWLING_ODIs_SR', 'BOWLING_ODIs_4w', 'BOWLING_ODIs_5w',
                'BOWLING_ODIs_10', 'BOWLING_T20Is_Mat', 'BOWLING_T20Is_Inns',
                'BOWLING_T20Is_Balls', 'BOWLING_T20Is_Runs', 'BOWLING_T20Is_Wkts',
                'BOWLING_T20Is_Ave', 'BOWLING_T20Is_Econ', 'BOWLING_T20Is_SR',
                'BOWLING_T20Is_4w', 'BOWLING_T20Is_5w', 'BOWLING_T20Is_10',
                'BOWLING_T20s_Mat', 'BOWLING_T20s_Inns', 'BOWLING_T20s_Balls',
                'BOWLING_T20s_Runs', 'BOWLING_T20s_Wkts', 'BOWLING_T20s_Ave',
                'BOWLING_T20s_Econ', 'BOWLING_T20s_SR', 'BOWLING_T20s_4w',
                'BOWLING_T20s_5w', 'BOWLING_T20s_10']
        bat_col = ['Match Type', '_Mat', '_Inns', '_NO', '_Runs', '_HS',
                   '_Ave', '_BF', '_SR', '_100', '_50', '_4s',
                   '_6s', '_Ct', '_St']
        ball_col = ['Match Type', '_Mat', '_Inns', '_Balls', '_Runs', '_Wkts',
                    '_Ave', '_Econ', '_SR', '_4w', '_5w',
                    '_10']
        match_type = ['Tests', 'ODIs', 'T20Is', 'T20s']
        bat_rows = list()
        ball_rows = list()
        gen_row = list()
        for m in match_type:
            row = [m]
            for n in bat:
                if m in n:
                    row.append((df[0][n]))
            bat_rows.append(row)
            row = [m]
            for n in ball:
                if m in n:
                    row.append((df[0][n]))
            ball_rows.append(row)
        for m in general_col:
            gen_row.append(df[0][m])

        return PlayerData.create_json_player_display(bat_rows,
                                                     ball_rows,
                                                     gen_row,
                                                     bat_col, ball_col, general_col)

    @staticmethod
    def create_json_player_display(bat_rows, ball_rows, gen_row, bat_col, ball_col, general_col):
        """
        :param bat_rows:
        :param ball_rows:
        :param gen_row:
        :param bat_col:
        :param ball_col:
        :param general_col:
        :return:
        """
        tb_bat = pd.DataFrame(bat_rows, columns=bat_col)
        tb_ball = pd.DataFrame(ball_rows, columns=ball_col)
        gen_tb = pd.DataFrame([gen_row], columns=general_col)
        return '{"General_table" : [' + \
               ((gen_tb.to_json(orient='records')).replace('\'', '')).replace('\\', '')\
               + '], "Bat_table" : [' + \
               tb_bat.to_json(orient='records')\
               + '], "Ball_table" : [' + \
               tb_ball.to_json(orient='records')\
               + '] }'

    @staticmethod
    def get_player_data_old(d, cl, val):
        """
        :param d:
        :param cl:
        :param val:
        :return:
        """
        d = d[d[cl] == val]
        if len(d) == 0:
            return "Invalid Player ID"
        return '{ "Data" : ' + (d.to_json(orient='records')) + "}"
