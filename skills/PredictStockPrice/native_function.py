import json
import numpy as np
import pandas as pd
from io import StringIO
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from semantic_kernel.skill_definition import sk_function
from semantic_kernel import SKContext

class PredictStockPrice:
    @sk_function(
        description="predict stock price of Microsoft",
        name = "predict",
        input_description = "stock price of Microsoft"
    )
    def predict(self, context: SKContext) -> str:
        # 株価の受け取り
        json_str = context['input']
        json_data = json.loads(json_str)
        csv_stock_price_today = json_data['today']
        csv_stock_price_month = json_data['month']

        # DataFrameに変換
        df_today = pd.read_csv(StringIO(csv_stock_price_today))
        df_month = pd.read_csv(StringIO(csv_stock_price_month))

        # 特徴量とターゲットを選択
        # 特徴量は過去の株価
        # ターゲットは次の日の株価の変動
        df_month['Price_Difference'] = df_month['Close'].shift(-1) - df_month['Close']
        # 欠損値を削除
        df_month.dropna(inplace=True)

        # 特徴量
        X = df_month[['Open', 'High', 'Low', 'Volume']]
        # ターゲット
        y = df_month['Price_Difference']

        # データをトレーニングセットとテストセットに分割
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        # 線形回帰モデルを作成
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 今後の株価予測(今日の株価で予想)
        today_open = df_today['Open'].iloc[-1]
        today_high = df_today['High'].iloc[-1]
        today_low = df_today['Low'].iloc[-1]
        today_volume = df_today['Volume'].iloc[-1]
        X_today = np.array([today_open, today_high, today_low, today_volume]).reshape(1, -1)
        X_today = pd.DataFrame(X_today, columns = ['Open', 'High', 'Low', 'Volume'])
        predicted_direction = model.predict(X_today)

        if predicted_direction > 0:
            # json_data = {
            #     "result": "Stock prices may rise",
            #     "stock_price": df_month.to_csv()
            # }
            # return json.dumps(json_data)
            return "Stock prices may rise"
        else:
            # json_data = {
            #     "result": "Stock price may go down",
            #     "stock_price": df_month.to_csv()
            # }
            # return json.dumps(json_data)
            return "Stock price may go down"
