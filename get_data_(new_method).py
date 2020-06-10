import requests
from bs4 import BeautifulSoup
import logging

path_1 = "https://s.cafef.vn/hastc/PVC-tong-cong-ty-hoa-chat-va-dich-vu-dau-khi-ctcp.chn"
path_2 = "https://s.cafef.vn/hastc/CSC-cong-ty-co-phan-tap-doan-cotana.chn"

path_3 = "https://s.cafef.vn/hose/VCB-ngan-hang-thuong-mai-co-phan-ngoai-thuong-viet-nam.chn"
path_4 = "https://s.cafef.vn/hose/VNM-cong-ty-co-phan-sua-viet-nam.chn"

path_5 = "https://s.cafef.vn/upcom/HHA-cong-ty-co-phan-van-phong-pham-hong-ha.chn"
path_6 = "https://s.cafef.vn/upcom/KSA-cong-ty-co-phan-cong-nghiep-khoang-san-binh-thuan.chn"

# <li class="clearfix">
#     <div class="l"><b>(*)&nbsp;&nbsp; <a href="/hose/HHS/chi-tiet-tinh-EPS.chn">EPS cơ bản</a></b> (nghìn đồng):</div>
#     <div class="r">
#         0.89
#     </div>
# </li>

# <li>
#     <span><a href="/hose/VCB/chi-tiet-tinh-EPS.chn">EPS cơ bản</a></span>
#     <span class="value">4.85</span>
# </li>

class GetIndex:
    def __init__(self, path):
        self.path = path
        self.all_data = None
        self.clawer_all_data()

    def clawer_all_data(self):
        self.all_data = BeautifulSoup(requests.get(self.path).text, "html.parser")

    def get_eps(self, text):
        d = self.all_data.find(text=text).find_parents('li')[0]
        if d.find_all('div'):
            return list(map(lambda x: x.get_text(strip=True), d.find_all('div')))
        elif d.find_all('span'):
            return list(map(lambda x: x.get_text(strip=True), d.find_all('span')))
        else:
            return None

    def get_pe(self, text):
        d = self.all_data.find_all('li')
        for s in d:
            if text in s.get_text(strip=True):
                if s.find_all('div'):
                    return list(map(lambda x: x.get_text(strip=True), s.find_all('div')))
                elif s.find_all('span'):
                    return list(map(lambda x: x.get_text(strip=True), s.find_all('span')))
                else:
                    return "Error"

list_path = [path_1, path_2, path_3, path_4, path_5, path_6]
for p in list_path:
    kt = GetIndex(p)
    d = kt.get_eps(text="EPS cơ bản")
    e = kt.get_eps(text="EPS pha loãng")
    try:
        f = kt.get_pe(text="P/E")
    except:
        f = "error"

    try:
        g = kt.get_pe(text="Giá trị sổ sách")
    except:
        g = "error"

    try:
        h = kt.get_pe(text="Hệ số beta")
    except:
        h = "error"

    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    print("---------------")