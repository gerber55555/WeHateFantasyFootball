import os
import pandas as pd


# Get file names in data directory
def get_files_names(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(directory + '/' + f)]


# Read data directory
def read_sentiment_files(directory):
    files = get_files_names(directory)
    week_to_sentiment_list = [(int(file.split('.')[0]), pd.read_csv(f"{directory}/{file}")) for file in files]
    return dict(week_to_sentiment_list)


# Regress on the data
def regress(week_to_sentiment_dict):

    pass


if __name__ == '__main__':
    pass