import requests
from bs4 import BeautifulSoup
import os

# import logging
# import configparser

pth = "https://s.cafef.vn"
state = "hastc"
company_name = "PVC-tong-cong-ty-hoa-chat-va-dich-vu-dau-khi-ctcp.chn"


# config = configparser.ConfigParser()
# config.read('config.cfg')

# data = requests.get("https://s.cafef.vn/Ajax/Bank/
# BHoSoCongTy.aspx?symbol=VCB&Type=1&PageIndex=0&PageSize=4&donvi=1")
#
# print(data.text)


class GetIndex:
    """
        @author Quoc Huy Do
        get data from cafef.vn of any cpn
    """

    def __init__(self, _path, state, cpn_name):
        self.path = _path
        self.state = state
        self.cpn_name = cpn_name
        self.all_data = None
        self.get_data()

    def get_full_path(self):
        """
         Create fullpath
        @return:
        """
        return os.path.join(self.path, self.state, self.cpn_name)

    def get_data(self):
        """
            request data
        """
        _data = requests.get(self.get_full_path())
        self.all_data = BeautifulSoup(_data.text, "html.parser")

    def get_index_value_group_style(self):
        """
            get value when eps in group each
        @return:
        """
        info = self.all_data.find("div", {"class": "dl-thongtin clearfix"})
        data = info.find_all("ul")[-1]
        li = data.find_all('li')
        dta = []
        for o in li:
            dta.append(list(map(
                lambda x: x.get_text(strip=True), o.find_all("div"))
            ))
        return dta

    def get_index_value_list_st(self):
        """
            get value when eps not in group each
        @return:
        """
        info = self.all_data.find("div", {"class": "tidown"})
        lst_val = info.find('ul').find_all("li")
        iv = []
        for o in lst_val:
            iv.append(list(map(
                lambda x: x.get_text(strip=True), o.find_all("span"))
            ))
        return iv

    def get_index_value(self):
        """
            return company index
        @return:
        """
        try:
            index_value = self.get_index_value_group_style()
        except "N":
            index_value = self.get_index_value_list_st()

        return index_value

    def get_cpn_status(self):
        """
            return companatus
        @return:
        """
        info = self.all_data.find("div", {"id": "divHoSoCongTyAjax"})
        table = info.find('table')
        rows = table.find_all('tr')
        d = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            d.append([ele for ele in cols if ele])
        data_info = list(filter(lambda x: True if len(x) >= 4 else False, d))
        return data_info

data = GetIndex(pth, state, company_name)

e = data.get_index_value()
d = data.get_cpn_status()

print(e)
print(d)
