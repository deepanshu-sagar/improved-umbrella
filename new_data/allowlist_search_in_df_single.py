def search_in_df_single(self, actual_df, expected_df):
    cols = list(actual_df.columns)
    rowsCount = expected_df.count()[0]
    actual_df_values = actual_df.values
    expected_df_values = expected_df.values
    actual_df_values = actual_df_values.astype('unicode')
    expected_df_values = expected_df_values.astype('unicode')
    actual_df = pd.DataFrame(data=actual_df_values, columns=actual_df.columns)
    expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
    print('search_in_df')
    print(actual_df)
    print(expected_df)
    print(actual_df == expected_df)
    found = actual_df == expected_df
    print('found : ' + str(found))
    print(type(found))
    if found:
        print('Expected data found ')
    else:
        raise Exception('Expected data Not found ')