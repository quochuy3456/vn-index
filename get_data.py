import requests
from bs4 import BeautifulSoup
import os
import logging
import configparser

pth = "https://s.cafef.vn/hose/"
company_name = "VCB-ngan-hang-thuong-mai-co-phan-ngoai-thuong-viet-nam.chn"

config = configparser.ConfigParser()
config.read('config.cfg')


class GetIndex:
    def __init__(self, _path, cpn_name):
        self.path = _path
        self.cpn_name = cpn_name
        self.all_data = None
        self.get_data()

    def get_full_path(self):
        return os.path.join(self.path + self.cpn_name)

    def get_data(self):
        _data = requests.get(self.get_full_path())
        self.all_data = BeautifulSoup(_data.text, "html.parser")

    def get_eps_via_class(self):
        eps = self.all_data.find("div", {"class": "tidown"})
        lst_val = eps.find('ul').find_all("li")
        outcome = []
        for o in lst_val:
            outcome.append(list(map(lambda x: x.text, o.find_all("span"))))
        return outcome


data = GetIndex(pth, company_name)

d = data.get_eps_via_class()

print(d)