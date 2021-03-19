import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from os import path

resourcePath = '/resource'
dictPath = '/dict'
count = 0
df_pivot=None


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



def pivot(p_dataframe):
    """
    this method the classify users whether watch the movie or not. watched =1, not watched =0. return dataframe pivot
    :param p_dataframe:
    :return:
    """
    df_pivot = p_dataframe.pivot(index='userId', columns='title', values='rating').fillna(0)
    df_pivot = df_pivot.astype('int64')

    def encode_ratings(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    df_pivot = df_pivot.applymap(encode_ratings)
    return df_pivot


def apriori_preprocess():
    """
    using pivot on the dataframe. To do so you need to first make sure there are no duplicate records for
    the combination of userId and title.
    :return: pviot
    """
    print("preprocessing apriori data...")
    movies_data = data_loading("../resource/movies_metadata.csv")
    rating_data = data_loading("../resource/ratings_small.csv")

    plt.figure(figsize=(10, 5))
    ax = sns.countplot(data=rating_data, x='rating')
    labels = (rating_data['rating'].value_counts().sort_index())
    plt.title('Distribution of Ratings')
    plt.xlabel('Ratings')

    for i, v in enumerate(labels):
        ax.text(i, v + 100, str(v), horizontalalignment='center', size=14, color='black')
    plt.show()



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
    # seeDetail(df_pivot)

    #write json to file
    json.dump(fromDataframeToJson(dataframe), open('../resource/dict.json', 'w', encoding='utf-8'), indent=4)

    return df_pivot

def knn_preprocess():
    """
    knn machine learning
    :return:
    """
    """
    preprocess part
    """
    print("knn preprocessing...")
    ratings_df = pd.read_csv("../resource/ratings_small.csv")
    movies_df = pd.read_csv("../resource/movies_metadata.csv")

    # Merge the two dataframe to keep only userId, movieId, rating and title data
    movies_df.drop(movies_df.index[19730], inplace=True)
    movies_df.drop(movies_df.index[29502], inplace=True)
    movies_df.drop(movies_df.index[35585], inplace=True)
    movies_df.id = movies_df.id.astype(np.int64)
    ratings_df = pd.merge(ratings_df, movies_df[['title', 'id']], left_on='movieId', right_on='id')
    ratings_df.drop(['timestamp', 'id'], axis=1, inplace=True)
    print("rating documents shape:", ratings_df.shape)
    print("null check:\n", ratings_df.isnull().sum())

    # number of ratings for each movie
    ratings_count = \
        ratings_df.groupby(by="title")['rating'].count().reset_index().rename(columns={'rating': 'totalRatings'})[
            ['title', 'totalRatings']]

    ratings_total = pd.merge(ratings_df, ratings_count, on='title', how='left')
    # statistics for the totalRatings
    print(ratings_count['totalRatings'].describe())

    # About top 21% of the movies received more than 20 votes. Let's remove all the other movies
    # so that we are only left with significant movies (in terms of total votes count)
    votes_count_threshold = 20
    ratings_top = ratings_total.query('totalRatings > @votes_count_threshold')

    # Make data consistent by ensuring there are unique entries for [title,userId] pairs
    if not ratings_top[ratings_top.duplicated(['userId', 'title'])].empty:
        ratings_top = ratings_top.drop_duplicates(['userId', 'title'])

    # Reshape the data using pivot function
    df_for_knn = ratings_top.pivot(index='title', columns='userId', values='rating').fillna(0)
    # use sparse matrix representation of this matrix
    df_for_knn_sparse = csr_matrix(df_for_knn.values)
    return df_for_knn_sparse, df_for_knn



