import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
import numpy as np
import datetime as dt


logging.basicConfig(level=logging.INFO,
                    filename='get_data_detail.log',
                    filemode='w',
                    format=(
                            '%(levelname)s:\t'
                            '%(filename)s:'
                            '%(funcName)s():'
                            '%(lineno)d\t'
                            '%(message)s'
                            )
                    )

logger = logging.getLogger()
FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(FORMAT)

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '655',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'X-MicrosoftAjax': 'Delta=true',
}

data = {
    'ctl00$ContentPlaceHolder1$scriptmanager': 'ctl00$ContentPlaceHolder\
    1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager1',
    'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker': '',
    'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker': '',
    'ctl00$UcFooter2$hdIP': '',
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ctl03$pager1',
    '__VIEWSTATE': '/wEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1JlcXVpcmVQ\
    b3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY3RsMDMkYnRTZ\
    WFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ==',
    '__VIEWSTATEGENERATOR': '2E2252AF',
    '__ASYNCPOST': 'true',
}


class GetDataDetail:
    def __init__(self, dt, hd):
        self.data = dt
        self.headers = hd
        self.data_detail = []

        self.lbl_11 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Thay đổi (+/-%)',
                       'GD KL - KL', 'GD KL - GT', 'GD TT - KL', 'GD TT - GT',
                       'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
        self.lbl_12 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Thay đổi (+/-%)',
                       'GD KL - KL', 'GD KL - GT', 'GD TT - KL', 'GD TT - GT',
                       'Giá tham chiếu', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']
        self.lbl_13 = ['Ngày', 'Giá điều chỉnh', 'Giá đóng cửa', 'Giá bình quân',
                       'Thay đổi (+/-%)', 'GD KL - KL', 'GD KL - GT', 'GD TT - KL',
                       'GD TT - GT', 'Giá tham chiếu', 'Giá mở cửa', 'Giá cao nhất', 'Giá thấp nhất']

    def crawl_all_data(self, cpn_code):
        dt = self.data
        dt['ctl00$ContentPlaceHolder1$ctl03$txtKeyword'] = cpn_code
        for i in range(1, 15):
            dt['__EVENTARGUMENT'] = i
            d = BeautifulSoup(
                    requests.post(
                        "https://s.cafef.vn/Lich-su-giao-dich-VCB-1.chn",
                        data=dt, headers=self.headers).text, "html.parser")
            rows = d.find('table').find_all('tr')[2:]
            if len(rows[0].find_all('td')[0:-3]) < 11:
                for t in rows:
                    d = list(map(lambda x: x.get_text(strip=True), t.find_all('td')))
                    self.data_detail.append(list(filter(lambda x: True if x else False, d)))
            else:
                for t in rows:
                    d = list(map(lambda x: x.get_text(strip=True), t.find_all('td')[0:-3]))
                    self.data_detail.append(list(filter(lambda x: True if x else False, d)))

        if len(self.data_detail[0]) == 11:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_11)
        elif len(self.data_detail[0]) == 12:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_12)
        elif len(self.data_detail[0]) == 13:
            df = pd.DataFrame(self.data_detail, columns=self.lbl_13)
        else:
            df = None
            logging.error("Length not match data <-> lable")

        return df


gd = GetDataDetail(dt=data, hd=headers)