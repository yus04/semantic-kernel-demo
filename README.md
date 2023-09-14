# Usage

## Set up
```
cd <semantic-kernel-demo path>
```

set `.env`
```
AZURE_OPENAI_DEPLOYMENT_NAME=""
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
```

## Run
```
python main.py
```

## Output Example
```
You should "Sell" Microsoft stocks because there is a high probability that the stock price will fall. Selling stocks now can help you avoid potential losses and protect your investment. Additionally, if you believe that the market is heading towards a downturn, selling your stocks can provide you with liquidity to invest in other opportunities or meet your financial needs. It is important to regularly evaluate your portfolio and make informed decisions based on market trends and your financial goals.
```

# Future
logでplan等を出力できるといいかも

# Prompt Example
直近1か月分ののMicrosoftの株価を取得して、
今後に株価が上がりそうなら「買い」下がりそうなら「売り」と出力し、
そのように判断した理由も教えてください