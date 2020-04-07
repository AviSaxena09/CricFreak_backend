"""This File Contains Classes to Scrap Content"""
# pylint: disable-msg = C0103, E0401, W0702
import requests
import pandas as pd
from bs4 import BeautifulSoup
from BackendModule.ConfigFiles.directory_config import GetDirectory


class scrap_data:
    """This Class Contains Methods to Scrap home page data from various source"""

    @staticmethod
    def news():
        """
        :return:
        """
        pd.options.display.max_colwidth = 140
        url = "https://www.cricbuzz.com/cricket-news/latest-news"
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to Retrieve Data !!!")
            return
        soup = BeautifulSoup(response.content, 'lxml')
        My_table = soup.find('div', {'id': 'news-list'})
        cols = ['heading', 'brief_Info', 'timestamp', 'link', 'photo_link']
        heading = My_table.find_all('h2')
        headline = list()
        for i in range(0, len(heading)):
            h = heading[i].text
            headline.append(h)
        intro = My_table.find_all('div', {'class': 'cb-nws-intr'})
        briefs = list()
        for i in range(0, len(intro)):
            b = intro[i].text
            briefs.append(b)
        hrefs = list()
        for i in range(0, len(heading)):
            ref = heading[i].find('a')
            temp = ref['href']
            hrefs.append(temp)
        link = 'https://www.cricbuzz.com'
        hrefs = [link + sub for sub in hrefs]
        time = My_table.find_all('span', {'class': 'cb-nws-time'})
        timestamp = list()
        for i in range(0, len(time)):
            t = time[i].text
            timestamp.append(t)
        photo = My_table.find_all('meta', {'itemprop': 'url'})
        photo_url = list()
        for i in photo:
            p = i['content']
            photo_url.append(p)
        for i in range(0, len(photo_url)):
            photo_url[i] = photo_url[i].replace(photo_url[i][:6], '')
        photo_url = [link + sub for sub in photo_url]
        news = pd.DataFrame(list(zip(headline, briefs, timestamp, hrefs, photo_url)), columns=cols)
        dt = news.to_dict(orient='records')
        data = "["
        for i in range(0, len(dt)):
            if i != 0:
                data += ","
            data += scrap_data.make_element(dt[i])
        data += "]"
        return scrap_data.write_data_file(data, GetDirectory.get_news_file_path())

    @staticmethod
    def team_ranking(gender, ftype):
        """
        :param gender:
        :param ftype:
        :return:
        """
        url = "https://www.icc-cricket.com/rankings/" + gender + "/team-rankings/" + ftype
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to retreive DATA !!!!")
            return
        soup = BeautifulSoup(response.content, 'lxml')
        My_table = soup.find('table', {'class': 'table'})
        table_head = My_table.find('thead')
        for i in table_head:
            th_cell = table_head.find_all('th')
            col = [i.text for i in th_cell]
        table_body = My_table.find('tbody')
        rows = list()
        td_row = My_table.find_all('tr', {'class': 'table-body'})
        for j in td_row:
            td_cell = j.find_all('td')
            value = [i.text for i in td_cell]
            rows.append(value)
        for r in rows:
            for i in range(0, len(r)):
                r[i] = str(r[i]).strip()
        ranking_table = pd.DataFrame(rows, columns=col)
        ranking_table = ranking_table.head(12)
        obj = '{"Type" :' + '[' + '"' + ftype + '"' + ']' + ',' + ' "Data" :' + str(
            ranking_table.to_json(orient='records')) + ' }'
        return scrap_data.write_data_file(obj,
                                          GetDirectory.get_team_rank_file_path(gender,
                                                                               ftype))

    @staticmethod
    def upcoming_matches():
        """
        :return:
        """
        pd.options.display.max_colwidth = 140
        url = "https://www.news18.com/cricketnext/cricket-schedule/"
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to Retrieve Data !!!!! ")
            return
        soup = BeautifulSoup(response.content, 'lxml')
        My_table = soup.find('div', {'class': 'whtbg10'})
        team = My_table.find_all('div', {'class': 'team'})
        teams = list()
        for i in team:
            t = i.text
            teams.append(t)
        loc = My_table.find_all('div', {'class': 'played'})
        venues = list()
        for i in loc:
            v = i.text
            venues.append(v)
        match = My_table.find_all('div', {'class': 'team-date'})
        match_info = list()
        for i in match:
            m = i.text
            match_info.append(m)
        a = My_table.find_all('a')
        hrefs = list()
        for i in a:
            ref = i['href']
            hrefs.append(ref)
        hrefs.pop(0)
        cols = ['Match_Info', 'Teams', 'Venue', 'Links']
        upcoming_matches = pd.DataFrame(list(zip(match_info, teams, venues, hrefs)), columns=cols)
        dt = upcoming_matches.to_dict(orient='records')
        data = "["
        for i in range(0, len(dt)):
            if i != 0:
                data += ","
            data += scrap_data.make_element(dt[i])
        data += "]"
        return scrap_data.write_data_file(data, GetDirectory.get_upcoming_match_file_path())

    @staticmethod
    def player_ranking(gender, ftype, ttype):
        """
        :param gender:
        :param ftype:
        :param ttype:
        :return:
        """
        url = "https://www.icc-cricket.com/rankings/" + gender + "/player-rankings/" + ftype
        try:
            response = requests.get(url)
        except:
            print("Failed !!")
            return
        if response.status_code != 200:
            print("Failed to Retrive Data !!")
        soup = BeautifulSoup(response.content, 'lxml')
        # Main Table
        My_table = soup.find_all('table', {'class': 'table'})
        # Top values of tables(Top Ranker)
        top = soup.find_all('div', {'class': 'rankings-block__banner'})
        # Table Head
        table_head = My_table[0].find('thead')
        for i in table_head:
            th_cell = table_head.find_all('th')
            col = [i.text for i in th_cell]
        # Getting all table toppers
        types = list()
        for j in range(0, len(top)):
            for i in top[j]:
                div = top[j].find_all('div')
                top_all = [i.text for i in div]
            types.append(top_all)
        for p in types:
            p.pop(1)
            p.pop(3)

        # Getting Table Content
        def types_data(n):
            """
            :param n:
            :return:
            """
            table_body = My_table[n].find('tbody')
            rows = list()
            rows.append(types[n])
            td_row = My_table[n].find_all('tr', {'class': 'table-body'})
            for j in td_row:
                td_cell = j.find_all('td')
                value = [i.text for i in td_cell]
                rows.append(value)
            for r in rows:
                for i in range(0, len(r)):
                    r[i] = str(r[i]).strip()
            df = pd.DataFrame(rows, columns=col)
            return df

        if ttype == 'bat':
            bat = types_data(0)
            obj = '{"Type" :' + '[' + '"' + ftype + '"' + ']' + ',' + ' "Data" :' + str(
                bat.to_json(orient='records')) + ' }'
            return scrap_data.write_data_file(obj, GetDirectory.get_player_rank_file_path(gender,
                                                                                          ftype,
                                                                                          ttype))
        elif ttype == 'ball':
            ball = types_data(1)
            obj = '{"Type" :' + '[' + '"' + ftype + '"' + ']' + ',' + ' "Data" :' + str(
                ball.to_json(orient='records')) + ' }'
            return scrap_data.write_data_file(obj, GetDirectory.get_player_rank_file_path(gender,
                                                                                          ftype,
                                                                                          ttype))
        elif ttype == 'all_rounder':
            all_rounder = types_data(2)
            obj = '{"Type" :' + '[' + '"' + ftype + '"' + ']' + ',' + ' "Data" :' + str(
                all_rounder.to_json(orient='records')) + ' }'
            return scrap_data.write_data_file(obj, GetDirectory.get_player_rank_file_path(gender, ftype, ttype))

    @staticmethod
    def ipl_records(rec_type):
        """
        :param rec_type:
        :return:
        """
        url = "https://www.iplt20.com/stats/all-time/" + rec_type
        response = requests.get(url)
        if response.status_code != 200:
            return "Error Retreiving Records ...."
        soup = BeautifulSoup(response.content, 'lxml')
        # Main Table
        My_table = soup.table
        #####Header of table
        header = My_table.find_all('th')
        col = [i.text for i in header]
        for i in range(0, len(col)):
            col[i] = str(col[i]).strip()
        ###Getting values of Table
        rows = list()
        td_row = My_table.find_all('tr')
        for j in td_row:
            td_cell = j.find_all('td')
            value = [i.text for i in td_cell]
            rows.append(value)
        rows.pop(0)
        ###Cleaning Data
        for r in rows:
            for i in range(0, len(r)):
                r[i] = r[i].replace('\n', '')
                r[i] = str(r[i]).strip()
        ###Removing Spaces
        for i in range(0, len(rows)):
            rows[i][1] = " ".join(rows[i][1].split())
        ipl_stats = pd.DataFrame(rows, columns=col)
        ipl_stats = ipl_stats.head(10)
        obj = ipl_stats.to_json(orient='records')
        return scrap_data.write_data_file(obj, GetDirectory.get_ipl_record_file_path(rtype=rec_type))

    @staticmethod
    def write_data_file(dt, path):
        """
        :param dt:
        :param path:
        :return:
        """
        f = open(path, "w")
        f.write(dt)
        f.close()

    @staticmethod
    def live_score(mtype):
        """
        :param mtype:
        :return:
        """
        url = "http://static.cricinfo.com/rss/livescores.xml"
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed To Connect to SERVER ay this MOMENT !!"
        soup = BeautifulSoup(response.content, 'lxml')
        My_table = soup.find_all('item')
        inter_country = ['Australia', 'India', 'England',
                         'Pakistan', 'South Africa', 'New Zealand',
                         'Sri Lanka', 'West Indies', 'Zimbabwe',
                         'Bangladesh', 'Kenya', 'Ireland',
                         'Canada', 'Netherlands', 'Scotland',
                         'Afghanistan', 'USA']
        international = list()
        domestic = list()
        international_url = list()
        domestic_url = list()
        for data in My_table:
            des = data.find('description').text
            link = data.find('guid').text
            flag = 0
            for country in inter_country:
                if country in des:
                    flag = 1
            if flag == 1:
                international.append(des)
                international_url.append(link)
            else:
                domestic.append(des)
                domestic_url.append(link)
        if len(international) == 0:
            international.append('No Match in progress..')
        if mtype == 'International':
            return international
        elif mtype == 'Domestic':
            return domestic

    @staticmethod
    def make_element(d):
        """
        :param d:
        :return:
        """
        data = "{ "
        ky = list(d.keys())
        l_ele = ky.pop()
        for k in ky:
            data += '"' + k + '" : "' + (d[k]) + '" , '
        data += '"' + l_ele + '" : "' + (d[l_ele]) + '"'
        data += "}"
        return data.replace("\'", " ")
