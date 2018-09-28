# -*- coding: utf-8 -*-

from OptionPrice import OptionPrice


def test_optionprice_init_quote_dict():
    optionprice = OptionPrice()
    optionprice.init_quote_dict()
    assert '201NA300' in optionprice.bid1_dict
    assert '201NA300' in optionprice.ask1_dict
    pass
