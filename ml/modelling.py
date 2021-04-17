"""
machine learning tools
"""

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from sklearn.neighbors import NearestNeighbors


def apriori_tranning(df_pivot):
    """
    Apriori modelling:
    The apriori model calculates the probability to determine how likely a user will watch movie M2
    if he has already watched a movie M1. It does so by computing support, confidence and lift for different
    combinations of movies.
    :param df_pivot:
    :return:
    """
    print("*******************************************************")
    print("apriori Training model...")
    print("*******************************************************")
    frequent_itemset = apriori(df_pivot, min_support=0.07, use_colnames=True)
    # print(frequent_itemset.head())
    """
        The apriori algorithm has given you the support, using association_rules you can compute the other paramters
        like confidence and lift.
    """
    rules = association_rules(frequent_itemset, metric="lift", min_threshold=1)
    # rules.head()
    print("*******************************************************")
    print("apriori Training finished")
    print("*******************************************************")
    return rules


def interpret_results(rules):
    """
    Sort the result by descending order of lift. So that the most likely movie that the
    user will watch is recommended first.
    :param rules:
    :return:
    """
    df_res = rules.sort_values(by=['lift'], ascending=False)
    # df_res.head()
    return df_res


def knn_modelling_output(df_for_knn_sparse, df_for_knn, user_input_str='Batman Returns'):
    recommendation_list = []
    """
    modelling part
    """
    print("*******************************************************")
    print("knn modelling...")
    print("*******************************************************")
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(df_for_knn_sparse)
    # query_index = np.random.choice(df_for_knn.shape[0])
    distances, indices = model_knn.kneighbors(df_for_knn.loc[user_input_str].values.reshape(1, -1), n_neighbors=6)
    # distances, indices = model_knn.kneighbors(df_for_knn.iloc[query_index, :].values.reshape(1, -1), n_neighbors=6)
    print("*******************************************************")
    print("knn modelling finished")
    print("*******************************************************")
    """
    output part
    """
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print("*******************************************************")
            print("Recommendations for movie: {0}\n".format(user_input_str))
            print("*******************************************************")
        else:
            # print("{0}: {1}, with distance of {2}".format(i, df_for_knn.index[indices.flatten()[i]],
            #                                               distances.flatten()[i]))
            recommendation_list.append(df_for_knn.index[indices.flatten()[i]])
    return recommendation_list
