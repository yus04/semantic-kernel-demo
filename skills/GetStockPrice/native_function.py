import pandas as pd
import datetime
import json
from pandas import DataFrame
from pandas_datareader.stooq import StooqDailyReader
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext

class GetStockPrice:
    @sk_function(
        description="get Stock Price of Microsoft",
        name = "GetStockPrice",
        input_description = "query from user's input"
    )
    def get_stock_price(self, context: SKContext) -> str:
        # 直近1カ月の日付を指定
        today = datetime.date.today()
        one_month_ago = today - datetime.timedelta(days=30)

        # Microsoftの株価を取得
        df_stock_price_month = StooqDailyReader("MSFT.US", start=one_month_ago, end=today).read()
        df_stock_price_today = df_stock_price_month.head(1)
        df_stock_price_month = df_stock_price_month.drop(df_stock_price_month.index[0])

        # 日付でソート
        df_stock_price_month = df_stock_price_month.sort_values('Date')
        # 欠損日がある場合には前の日の値で埋める
        df_stock_price_month = pd.DataFrame(df_stock_price_month).asfreq("D", method="ffill")

        # csv形式の文字列に変換
        csv_stock_price_today = df_stock_price_today.to_csv()
        csv_stock_price_month = df_stock_price_month.to_csv()

        stock_price = {
            "today": csv_stock_price_today,
            "month": csv_stock_price_month
        } 

        return json.dumps(stock_price)
