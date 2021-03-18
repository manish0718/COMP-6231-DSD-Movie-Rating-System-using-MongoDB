import modelling
import preprocessor


def final_result_toString(df_res, user_input_str='Men in Black II'):
    """
    the function that sort the result after tranning and return as list
    :param df_res:
    :param user_input_str:
    :return: list of top ten recommendation movies
    """
    # out put result in console

    result_list = df_res[df_res['antecedents'].apply(lambda x: len(x) == 1 and next(iter(x)) == user_input_str)]
    result_list = result_list[result_list['lift'] > 2]
    # print(result_list.head())

    # print the result
    movies = result_list['consequents'].values

    movie_list = []
    for movie in movies:
        for title in movie:
            if title not in movie_list:
                movie_list.append(title)

    # only return top ten movies

    return movie_list[0:10]


def test_ml_run(user_input_str='Men in Black II'):
    """
    the test case for ml running
    :param user_input_str: Men in Black II
    """
    result = modelling.interpret_results(modelling.tranning(preprocessor.preprocess()))
    print("your recommendation movies list is below: ")
    print(final_result_toString(result, user_input_str))


def ml_run(user_input_str):
    """
    the real ml runner used for passing list of str to web
    :param user_input_str:
    :return: list of recommendation movies for users
    """
    result = modelling.interpret_results(modelling.tranning(preprocessor.preprocess()))
    return final_result_toString(result, user_input_str)


if __name__ == "__main__":
    test_ml_run()
