import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, accuracy_score
from sklearn.preprocessing import StandardScaler


def get_train_data():
    df = pd.read_csv("trimestri1623_modena.csv")
    return df


def preprocessing_data_bollinger(df):
    df = df.drop(['ora', 'Unnamed: 0'], axis=1)
    df = df[df['descCarburante'].isin(['Benzina'])]
    df = df[df['isSelf'] == 1]
    df = df.sort_values(by='data')
    df = df.drop_duplicates(subset=['idImpianto', 'data'])
    df['data'] = pd.to_datetime(df['data'], format='mixed')
    df_media_giornaliera = df.groupby('data')['prezzo'].mean()
    df = df_media_giornaliera.to_frame()
    df = df.reset_index()
    df['giorno'] = df['data'].dt.dayofweek + 1
    df['mese'] = df['data'].dt.month
    df['trimestre'] = df['data'].dt.quarter
    df['anno'] = df['data'].dt.year
    df['date_offset'] = (df['data'].dt.month * 100 + df['data'].dt.day - 320) % 1300
    df['stagione'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300],
                            labels=['0', '1', '2', '3'])
    df['domani'] = df['prezzo'].shift(-1)
    df = df.drop('date_offset', axis=1)
    periodo_sma = 7
    df['SMA'] = df['prezzo'].rolling(window=periodo_sma).mean()
    df['deviazione_standard'] = df['prezzo'].rolling(window=periodo_sma).std()
    df['banda_superiore'] = df['SMA'] + 0.7 * df['deviazione_standard']
    df['banda_inferiore'] = df['SMA'] - 0.7 * df['deviazione_standard']
    df['classe'] = np.where(df['domani'] > df['prezzo'], 1, 0)
    df = df.dropna()
    df = df.set_index('data')
    return df


def model_and_predictors():
    model = RandomForestClassifier(n_estimators=20, min_samples_split=5, min_samples_leaf=6, criterion='gini',
                                   random_state=1)
    predictors = ['prezzo', 'giorno', 'mese', 'trimestre', 'anno', 'stagione', 'SMA', 'deviazione_standard',
                  'banda_superiore', 'banda_inferiore']

    return model, predictors


def predict(x_train, y_train, x_test, y_test, model, scaler, predictors):
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    test = pd.DataFrame(scaler.inverse_transform(x_test), columns=predictors)
    preds = pd.Series(preds, index=test.index, name="predizioni")
    combined = pd.concat([y_test.reset_index(drop=True), preds.reset_index(drop=True)], axis=1)
    return combined


def backtest(data, model, predictors, start=1, step=30):
    scaler = StandardScaler()
    all_predictions = []

    for i in range(start, data.shape[0], step):
        print(i)
        train = data.iloc[0: i].copy()
        x_train = train[predictors]
        y_train = train['classe']
        x_train = scaler.fit_transform(x_train)

        test = data.iloc[i:(i + step)].copy()
        x_test = test[predictors]
        y_test = test['classe']
        x_test = scaler.fit_transform(x_test)

        predictions = predict(x_train, y_train, x_test, y_test, model, scaler, predictors)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)


def print_results(predictions):
    print(predictions["predizioni"].value_counts())
    print(precision_score(predictions["classe"], predictions["predizioni"]))
    print(accuracy_score(predictions["classe"], predictions["predizioni"]))


def dump_weights(model):
    percorso_locale = "/Users/zampifre/Desktop/pesi_modello_benzina.joblib"
    joblib.dump(model, percorso_locale)


if __name__ == '__main__':
    df = get_train_data()
    df = preprocessing_data_bollinger(df)
    model, predictors = model_and_predictors()
    predictions = backtest(df, model, predictors)
    print_results(predictions)
    dump_weights(model)
