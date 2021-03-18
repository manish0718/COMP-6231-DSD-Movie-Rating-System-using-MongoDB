"""
machine learning tools
"""

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


def tranning(df_pivot):
    """
    Apriori modelling:
    The apriori model calculates the probability to determine how likely a user will watch movie M2
    if he has already watched a movie M1. It does so by computing support, confidence and lift for different
    combinations of movies.
    :param df_pivot:
    :return:
    """
    print("Training model...")
    frequent_itemset = apriori(df_pivot, min_support=0.07, use_colnames=True)
    # print(frequent_itemset.head())
    """
        The apriori algorithm has given you the support, using association_rules you can compute the other paramters
        like confidence and lift.
    """
    rules = association_rules(frequent_itemset, metric="lift", min_threshold=1)
    # rules.head()
    print("Training finished")
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



