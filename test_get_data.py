"""
Unit tests for the calculator library
"""

import get_data

pth = "https://s.cafef.vn"
state = "upcom"
company_name = "MNB-tong-cong-ty-may-nha-be-cong-ty-co-phan.chn"

data = get_data.GetIndex(pth, state, company_name)


class TestCalculator:

    def test_get_index_value(self):
        assert 2 <= len(data.get_index_value())

    def test_cpn_status(self):
        assert 2 <= len(data.get_cpn_status())
