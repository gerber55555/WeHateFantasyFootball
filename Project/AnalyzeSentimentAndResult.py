import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import argparse
import matplotlib.pyplot as plt


# Get file names in data directory
def get_files_names(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(directory + '/' + f)]


# Read data directory
def read_sentiment_files(directory):
    files = get_files_names(directory)
    week_to_sentiment_list = [(int(file.split('.')[0]), pd.read_csv(f"{directory}/{file}")) for file in files]
    return dict(week_to_sentiment_list)


# Remove all empty data and calculate average sentiment
def preprocess_data(df, position_to_filter):
    df = df[df['Actual Points'] != 0]
    df = df[df['NumOfDataPoints'] != 0]

    final_fields_to_use = ['Actual Points', 'Projected Points', 'Sentiment', 'Position']
    if position_to_filter is not None:
        df = df[df['Position'] == position_to_filter]
        final_fields_to_use = ['Actual Points', 'Projected Points', 'Sentiment']
    df['Projected Points'] = (df['Projected Points'] / 17).round(5)
    df['Sentiment'] = (df['Sentiment'] / df['NumOfDataPoints']).round(5)
    df = df[final_fields_to_use]
    df = pd.get_dummies(data=df, drop_first=True)
    return df


# Preprocess and concat all the data from every week into one numpy array
def preprocess_and_concat_data(data_dict, position_to_filter, look_back):
    all_data = None
    sorted_keys = sorted(data_dict.keys())
    for key in sorted_keys:
        value = data_dict[key].set_index('Full Name')
        if look_back and key == sorted_keys[0]:
            continue
        if look_back:
            joined_value = value.join(data_dict[key - 1][['Actual Points', 'Full Name']].set_index('Full Name'),
                                      on=['Full Name'], how="inner", lsuffix="_l", rsuffix="_r")
            joined_value = joined_value.rename(columns={'Actual Points_r': 'Actual Points'})
            joined_value = joined_value[['Actual Points', 'Projected Points', 'Sentiment', 'NumOfDataPoints', 'Position']]
            value = joined_value
        new_value = preprocess_data(value, position_to_filter)
        if all_data is None:
            print("coefficients are:")
            for i in range(2, len(new_value.columns) + 1):
                print(f"x{i-1}: {new_value.columns[i-1]}")
            all_data = new_value.to_numpy()
        else:
            all_data = np.concatenate((all_data, new_value.to_numpy()), axis=0)
    return all_data


# Regress on the data
def regress(preprocessed_data):
    x_train, x_test, y_train, y_test = train_test_split(preprocessed_data[:, 1:], preprocessed_data[:, 0], test_size=0.1)
    model = LinearRegression()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    plt.scatter(y_test, predictions)
    x = np.linspace(0, int(np.array(np.max([np.max(y_test), np.max(predictions)]))) + 1, 100)
    plt.plot(x, x, 'r')
    plt.xlabel("Actual Score")
    plt.ylabel("Predicted Score")
    plt.show()
    x_train_sm = sm.add_constant(preprocessed_data[:, 1:])
    ls = sm.OLS(preprocessed_data[:, 0], x_train_sm).fit()
    print(ls.summary())


def analyze_sentiment(directory, position, look_back):
    weekly_data = read_sentiment_files(directory)
    preprocessed_data = preprocess_and_concat_data(weekly_data, position, look_back)
    regress(preprocessed_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-dd', '--data-directory', dest="dir", default="data", help="directory the data is stored in")
    parser.add_argument('-p', '--position', dest="position", help="optional position to filter by (QB, RB, WR, TE, K)")
    parser.add_argument('-lb', '--look-back', dest="lb", default=False, action="store_true",
                        help="Look back one week and regress on last weeks score")
    args = parser.parse_args()
    analyze_sentiment(args.dir, args.position, args.lb)
