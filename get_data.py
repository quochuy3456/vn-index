import requests
from bs4 import BeautifulSoup
import os
import logging
import configparser

pth = "https://s.cafef.vn/"
state = "hastc"
company_name = "HDA-cong-ty-co-phan-hang-son-dong-a.chn"

config = configparser.ConfigParser()
config.read('config.cfg')


class GetIndex:
    def __init__(self, _path, state, cpn_name):
        self.path = _path
        self.state = state
        self.cpn_name = cpn_name
        self.all_data = None
        self.get_data()

    def get_full_path(self):
        return os.path.join(self.path, self.state, self.cpn_name)

    def get_data(self):
        _data = requests.get(self.get_full_path())
        self.all_data = BeautifulSoup(_data.text, "html.parser")

    def get_index_value_group_style(self):
        info = self.all_data.find("div", {"class": "dl-thongtin clearfix"})
        data = info.find_all("ul")
        print(data)

    def get_index_value(self):
        info = self.all_data.find("div", {"class": "tidown"})
        if info:
            lst_val = info.find('ul').find_all("li")
            index_value = []
            for o in lst_val:
                index_value.append(list(map(lambda x: x.text, o.find_all("span"))))
            return index_value
        else:
            return None

    def get_cpn_status(self):
        info = self.all_data.find("div", {"id": "divHoSoCongTyAjax"})
        table = info.find('table')
        rows = table.find_all('tr')
        data_info = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data_info.append([ele for ele in cols if ele])
        data_info = list(filter(lambda x: True if len(x) >= 4 else False, data_info))
        return data_info[:]


data = GetIndex(pth, state, company_name)

b = data.get_index_value_group_style()
e = data.get_index_value()
d = data.get_cpn_status()

print(e)
print(d)