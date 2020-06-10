import requests
from bs4 import BeautifulSoup

path = "https://s.cafef.vn/Ajax/bank/BHoSoCongTy.\
        aspx?symbol=VCB&Type=2&PageIndex=0&PageSize=4&donvi=1"

# path = "https://s.cafef.vn/Ajax/Bank/BHoSoCongTy.aspx?
# symbol=BID&Type=1&PageIndex=0&PageSize=4&donvi=1"
# path = "https://s.cafef.vn/Ajax/HoSoCongTy.aspx?
# symbol=vnm&Type=2&PageIndex=0&PageSize=4"
#
# path = "https://s.cafef.vn/Ajax/HoSoCongTy.aspx?
# symbol=hhc&Type=2&PageIndex=0&PageSize=4"

# data = requests.get(path)
#
# print(data.text)

path = "https://s.cafef.vn/Lich-su-giao-dich-BID-1.chn"

data = {
    'ctl00$ContentPlaceHolder1$scriptmanager': 'ctl00$ContentPl\
        aceHolder1$ctl03$panelAjax|ctl00$ContentPlaceHolder1$ctl03$pager2',
    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ctl03$pager2',
    '__EVENTARGUMENT': 1,
    '__VIEWSTATE': '/wEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1\
        JlcXVpcmVQb3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZ\
        UhvbGRlcjEkY3RsMDMkYnRTZWFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ==',
    'ctl00$ContentPlaceHolder1$ctl03$txtKeyword': 'BID',
    'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate1$txtDatePicker': '',
    'ctl00$ContentPlaceHolder1$ctl03$dpkTradeDate2$txtDatePicker': '',
    'ctl00$UcFooter2$hdIP': '',
    '__VIEWSTATEGENERATOR': '2E2252AF',
    '__ASYNCPOST': 'true'
    }

a = requests.post(path,
                  data=data,
                  headers={
                      "Accept": "*/*",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,\
                        fr;q=0.7,en-US;q=0.6,en;q=0.5",
                      "Cache-Control": "no-cache",
                      "Connection": "keep-alive",
                      "Content-Length": "655",
                      "Content-Type": "application/x-www-form-urlencoded;\
                        charset=UTF-8",
                      "Host": "s.cafef.vn",
                      "Origin": "https://s.cafef.vn",
                      "Referer": "https://s.cafef.vn/Lich-su-giao-dich-BID-2.chn",
                      "Sec-Fetch-Dest": "empty",
                      "Sec-Fetch-Mode": "cors",
                      "Sec-Fetch-Site": "same-origin",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/83.0.4103.97 Safari/537.36",
                      "X-MicrosoftAjax": "Delta=true",
                  }
                  )

print(a.text)


class GetIndex:
    def __init__(self, path, cpn_code, category=None):
        self.path = path
        self.category = category
        self.cpn_code = cpn_code
        self.all_data = None
        self.clone_data()

    def clone_data(self):
        """
            Clone data from ajax link
        """
        if self.category:
            _path = f'https://s.cafef.vn/Ajax/{self.category}/BHoSoCongTy.aspx?\
                symbol={self.cpn_code}&Type=2&PageIndex=0&PageSize=4&donvi=1'
            data = requests.get(_path)
        else:
            _path = f'https://s.cafef.vn/Ajax/BHoSoCongTy.aspx?\
                symbol={self.cpn_code}&Type=2&PageIndex=0&PageSize=4'
            data = requests.get(_path)
        self.all_data = BeautifulSoup(data.text, "html.parser")

    def get_cnp_status(self):
        tbl = self.all_data.find('table')
        # rows = tbl.findAll('tr')
        return tbl


# getdata = GetIndex(path=None, cpn_code="VNM")
# print(getdata.get_cnp_status())
