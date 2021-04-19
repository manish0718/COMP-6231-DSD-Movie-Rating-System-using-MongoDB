
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import csr_matrix
from os import path
from IPython.core.interactiveshell import InteractiveShell

from backend import database as mongo_db

InteractiveShell.ast_node_interactivity = "all"
resourcePath = '/resource'
dictPath = '/dict'
count = 0
df_pivot = None

BeautifulSoup = None


def seeDetail(dataframe):
    """
    see collection detail (test use)
    :param dataframe:
    """
    print(dataframe.describe().T)
    print(dataframe.isnull().sum())
    print(dataframe.head())
    print(dataframe.info())


def data_loading_fromcsv(p_filepath):
    """
    get data from local csv file
    :param p_filepath:
    :return:
    """
    if path.exists(p_filepath):
        print("*******************************************************")
        print("loading data success, path:" + p_filepath)
        print("*******************************************************")
        return pd.read_csv(p_filepath)
    else:
        print("Error: file path not exist")
        return None


def get_data(collection_name):
    """
    get collection from mongodb atlas
    :param collection_name:
    :return: panda dataframe
    """
    return mongo_db.get_collection(collection_name)


def pivot(p_dataframe):
    """
    this method the classify users whether watch the movie or not. watched =1, not watched =0. return dataframe pivot
    :param p_dataframe:
    :return: dataframe pivot
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


def raw_process():
    """
    data preprocess
        using pivot on the dataframe. To do so you need to first make sure there are no duplicate records for
    the combination of userId and title.
    """
    global BeautifulSoup

    movies_data = get_data("movies_metadata")
    rating_data = get_data("ratings_small")

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
    BeautifulSoup = dataframe.drop_duplicates(['userId', 'title'])
    BeautifulSoup.to_csv("beautifulSoup.csv", index = False, header=True)


def apriori_preprocess():
    """
    apriori preprocess
    :return: pviot
    """
    print("*******************************************************")
    print(" Apriori preprocessing...")
    print("*******************************************************")
    global BeautifulSoup

    # if path.exists("beautifulSoup.csv"):
    #     l_df=pd.read_csv("beautifulSoup.csv")
    #     return pivot(l_df)

    if BeautifulSoup is None:
        raw_process()

    return pivot(BeautifulSoup)


def knn_preprocess():
    """
    knn machine learning
    :return: preprocess data
    """
    print("*******************************************************")
    print("Knn preprocessing...")
    print("*******************************************************")
    global BeautifulSoup

    # if path.exists("beautifulSoup.csv"):
    #     l_df=pd.read_csv("beautifulSoup.csv")
    #     # Reshape the data using pivot function
    #     df_for_knn = l_df.pivot(index='title', columns='userId', values='rating').fillna(0)
    #     # use sparse matrix representation of this matrix
    #     df_for_knn_sparse = csr_matrix(df_for_knn.values)
    #     return df_for_knn_sparse, df_for_knn

    if BeautifulSoup is None:
        raw_process()

    # Reshape the data using pivot function
    df_for_knn = BeautifulSoup.pivot(index='title', columns='userId', values='rating').fillna(0)
    # use sparse matrix representation of this matrix
    df_for_knn_sparse = csr_matrix(df_for_knn.values)
    return df_for_knn_sparse, df_for_knn

if __name__ == '__main__':
    raw_process()