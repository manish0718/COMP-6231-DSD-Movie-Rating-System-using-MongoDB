import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

from os import path

resourcePath = '/resource'
dictPath = '/dict'
count = 0


def seeDetail(dataframe):
    print(dataframe.describe().T)
    print(dataframe.isnull().sum())
    print(dataframe.head())
    print(dataframe.info())


def fromCsvToJsonDict(p_filepath):
    l_RawData = pd.read_csv(p_filepath)
    jsonData = pd.DataFrame.to_json(l_RawData)
    return jsonData

def fromDataframeToJson(p_dataframe):
    return pd.DataFrame.to_json(p_dataframe)

def data_loading(p_filepath):
    if path.exists(p_filepath):
        print("loading data success, path:" + p_filepath)
        return pd.read_csv(p_filepath)
    else:
        print("Error: file path not exist")
        return None


# this method the classify users whether watch the movie or not. watched =1, not watched =0. return dataframe pivot
def pivot(p_dataframe):
    df_pivot = p_dataframe.pivot(index='userId', columns='title', values='rating').fillna(0)
    df_pivot = df_pivot.astype('int64')

    def encode_ratings(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    df_pivot = df_pivot.applymap(encode_ratings)
    return df_pivot


def preprocess():
    print("preprocessing data...")
    movies_data = data_loading("resource/movies_metadata.csv")
    rating_data = data_loading("resource/ratings_small.csv")

    # plt.figure(figsize=(10, 5))
    # ax = sns.countplot(data=rating_data, x='rating')
    # labels = (rating_data['rating'].value_counts().sort_index())
    # plt.title('Distribution of Ratings')
    # plt.xlabel('Ratings')
    #
    # for i, v in enumerate(labels):
    #     ax.text(i, v + 100, str(v), horizontalalignment='center', size=14, color='black')
    # plt.show()



    # clean data that wont help
    print("removing useless data")
    title_mask = movies_data["title"].isna()
    movies_data = movies_data.loc[title_mask == False]

    # merge rating and movies these two dataframe
    movies_data = movies_data.astype({'id': 'int64'})
    dataframe = pd.merge(rating_data, movies_data[{'id', 'title'}], left_on='movieId', right_on='id')
    # seeDetail(merged_dataframe)

    # timestamp is not important anymore, so drop
    dataframe.drop(['timestamp', 'id'], axis=1, inplace=True)

    # movieid and id are duplicated, keep only one
    dataframe = dataframe.drop_duplicates(['userId', 'title'])
    df_pivot = pivot(dataframe)
    seeDetail(df_pivot)

    #write json to file
    json.dump(fromDataframeToJson(dataframe),open('resource/dict.json','w',encoding='utf-8'),indent=4)


if __name__ == "__main__":
    preprocess()
