# -*- coding: utf-8 -*-

from OptionPrice import OptionPrice


class TestClass(object):
    optionprice = OptionPrice()

    def test_optionprice_init_quote_dict_one(self):
        self.optionprice.init_quote_dict()
        assert '201NA300' in self.optionprice.bid1_dict

    def test_optionprice_init_quote_dict_two(self):
        self.optionprice.init_quote_dict()
        assert '201NA300' in self.optionprice.ask1_dict



