from textblob import TextBlob
import pickle
import sklearn
import pandas as pd

def predictPrice(data):
    # load model from file
    data['index'] = 0
    data['high'] = float(data['high'])
    data['low'] = float(data['low'])
    data['close'] = float(data['close'])
    data['volume'] = float(data['volume'])
    data['adjclose'] = float(data['adjclose'])
    data['date'] = data['date']
    data['headline'] = data['headline']
    data['polarity'] = TextBlob(data['headline']).sentiment[0]
    data['subjectivity'] = TextBlob(data['headline']).sentiment[1]
    loaded_model = pickle.load(open("model.sav", "rb"))

    # Get data from user

    def boolean_shock(percent, df, col):
        data = df.filter(["date", col], axis=1)  # df.copy()
        data.set_index("date", inplace=True)
        data["percentchg"] = (
            data[col].pct_change()
        ) * 100  # percentage change compare to previous volume using pct_change() function
        data["shock"] = data["percentchg"].apply(
            lambda x: 1 if x >= percent else 0)
        data.drop(col, axis=1, inplace=True)
        return data.dropna()


    def reverseboolean_shock(percent, df, col):
        data = df.filter(["date", col], axis=1)  # df.copy()
        data.set_index("date", inplace=True)
        data = data.reindex(index=data.index[::-1])
        data["percentchg"] = (data[col].pct_change()) * 100
        data["shock"] = data["percentchg"].apply(lambda x: 1 if x > percent else 0)
        data.drop(col, axis=1, inplace=True)
        data = data.reindex(index=data.index[::-1])
        
        return data.dropna()


    def priceboolean_shock(percent, df):
        df['date'] = pd.to_datetime(df['date'])
        data = df.filter(['date', 'high', 'low', 'close'], axis=1)  # df.copy()
        data.set_index('date', inplace=True)
        data['priceavg'] = (data['high'] + data['low'] + data['close']) / 3
        data['shock'] = (data['priceavg'].pct_change()) * 100
        data['shock'] = data['shock'].apply(lambda x: 1 if x >= percent else 0)
        data.drop(['high', 'low', 'close'], axis=1, inplace=True)
        return data


    def pricereverseboolean_shock(percent, df):
        data = df.filter(['date', 'high', 'low', 'close'], axis=1)  # df.copy()
        data.set_index('date', inplace=True)
        data = data.reindex(index=data.index[::-1])
        data['reversepriceavg'] = (data['high'] + data['low'] + data['close']) / 3
        data['shock'] = (data['reversepriceavg'].pct_change()) * 100
        data['shock'] = data['shock'].apply(lambda x: 1 if x >= percent else 0)
        data.drop(['high', 'low', 'close'], axis=1, inplace=True)
        data = data.reindex(index=data.index[::-1])
        return data.dropna()


    builder = pd.DataFrame(data, index=[0])
    builder['date'] = pd.to_datetime(builder['date'])
    builder["month"] = builder['date'].dt.month
    builder["day"] = builder['date'].dt.day
    builder["dayofweek"] = builder['date'].dt.dayofweek
    builder["week"] = builder['date'].dt.isocalendar().week
    builder['movingavg4weeks'] = round(builder['close'].rolling(
        window=(4*5), min_periods=1).mean().shift(), 2)
    builder['movingavg16weeks'] = round(builder['close'].rolling(
        window=(16*5), min_periods=1).mean().shift(), 2)  # add 12 weeks to 4 weeks
    builder['movingavg28weeks'] = round(builder['close'].rolling(
        window=(28*5), min_periods=1).mean().shift(), 2)  # add 12 weeks to 16 weeks
    builder['movingavg40weeks'] = round(builder['close'].rolling(
        window=(40*5), min_periods=1).mean().shift(), 2)  # add 12 weeks to 28 weeks
    builder['movingavg52weeks'] = round(builder['close'].rolling(
        window=(52*5), min_periods=1).mean().shift(), 2)  # add 12 weeks to 40 weeks
    builder['window10days'] = round(builder['close'].rolling(
        window=10, min_periods=1).mean().shift(), 2)
    builder['window50days'] = round(builder['close'].rolling(
        window=50, min_periods=1).mean().shift(), 2)
    builder['volumeshock'] = round(boolean_shock(
        10, builder, 'volume').reset_index()['shock'], 2)
    builder['closeshock2'] = round(reverseboolean_shock(
        2, builder, 'close').reset_index()['shock'], 2)
    builder['closeshock5'] = round(reverseboolean_shock(
        5, builder, 'close').reset_index()['shock'], 2)
    builder['closeshock10'] = round(reverseboolean_shock(
        10, builder, 'close').reset_index()['shock'], 2)
    builder['priceshock'] = round(priceboolean_shock(
        10, builder).reset_index()['shock'], 2)
    builder['reversebooleanshock2'] = round(reverseboolean_shock(
        2, builder, 'close').reset_index()['shock'], 2)
    builder['reversebooleanshock5'] = round(reverseboolean_shock(
        5, builder, 'close').reset_index()['shock'], 2)
    builder['pricereverseshock2'] = round(
        pricereverseboolean_shock(2, builder).reset_index()['shock'], 2)
    builder['polarity'] = round(builder['polarity'], 2)
    builder['subjectivity'] = round(builder['subjectivity'], 2)
    builder['price'] = round(
        (builder['high'] + builder['low'] + builder['close']) / 3, 2)
    builder['close'] = round(builder['close'], 2)



    finalInput = builder.filter(["index", "month", "day", "dayofweek", "week", "movingavg4weeks", "movingavg16weeks", "movingavg28weeks", "movingavg40weeks", "movingavg52weeks", "window10days",
                                "window50days", "volumeshock", "closeshock2", "closeshock5", "closeshock10", "priceshock", "reversebooleanshock2", "reversebooleanshock5", "pricereverseshock2", "polarity", "subjectivity"], axis=1)

    finalInput = finalInput.fillna(0)

    prediction = loaded_model.predict(finalInput)
    return prediction
