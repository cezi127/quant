# -*- coding: utf-8 -*-
#

from cached_property import cached_property

from .backend import DataBackend
from ..utils import lru_cache, get_str_date_from_int, get_int_date


class TushareDataBackend(DataBackend):

    @cached_property
    def ts(self):
        try:
            import tushare as ts
            return ts
        except ImportError:
            print("-" * 50)
            print(">>> Missing tushare. Please run `pip install tushare`")
            print("-" * 50)
            raise

    @cached_property
    def stock_basics(self):
        return self.ts.get_stock_basics()

    @cached_property
    def code_name_map(self):
        code_name_map = self.stock_basics[["name"]].to_dict()["name"]
        return code_name_map

    def convert_code(self, order_book_id):
        return order_book_id.split(".")[0]

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start, end, freq):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        code = self.convert_code(order_book_id)
        is_index = False
        if ((order_book_id.startswith("0") and order_book_id.endswith(".XSHG")) or
            (order_book_id.startswith("3") and order_book_id.endswith(".XSHE"))
            ):
            is_index = True
        ktype = freq
        if freq[-1] == "m":
            ktype = freq[:-1]
        elif freq == "1d":
            ktype = "D"
        # else W M

        #df = self.ts.get_k_data(code, start=start, end=end, index=is_index, ktype=ktype)
        token='14f436f81370363854a7c1e6b5ab799df07ce0c3c9734685284a7b31'
        self.ts.set_token(token)        
        pro=self.ts.pro_api()
        df = pro.daily(ts_code=order_book_id, start_date=start, end_date=end)
        df["volume"] = df["vol"]
        if freq[-1] == "m":
            df["datetime"] = df.apply(
                lambda row: int(row["trade_date"].split(" ")[0].replace("-", "")) * 1000000 + int(row["trade_date"].split(" ")[1].replace(":", "")) * 100, axis=1)
        elif freq in ("1d", "W", "M"):
            df["datetime"] = df["trade_date"].apply(lambda x: int(x) * 1000000)
        
        del df["ts_code"]
        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        token='14f436f81370363854a7c1e6b5ab799df07ce0c3c9734685284a7b31'
        self.ts.set_token(token)
        pro=self.ts.pro_api()
        info = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        #info = self.ts.get_stock_basics()
        order_book_id_list = info.ts_code.sort_values().tolist()
        # order_book_id_list = [
        #     (str(code) + ".XSHG" if str(code).startswith("6") else str(code) + ".XSHE")
        #     for code in code_list
        # ]
        return order_book_id_list

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        start = get_str_date_from_int(start)
        end = get_str_date_from_int(end)
        #df = self.ts.get_k_data("000001", index=True, start=start, end=end)
        pro = self.ts.pro_api()
        df = pro.trade_cal(exchange='', start_date=start, end_date=end)
        trading_dates = [get_int_date(date) for date in df.date.tolist()]
        return trading_dates

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """
        code = self.convert_code(order_book_id)
        return "{}[{}]".format(order_book_id, self.code_name_map.get(code))
