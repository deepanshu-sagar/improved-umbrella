def search_in_df(self, actual_df, expected_df):
    cols = list(actual_df.columns)
    rowsCount = expected_df.count()[0]
    actual_df_values = actual_df.values
    expected_df_values = expected_df.values
    actual_df_values = actual_df_values.astype('unicode')
    expected_df_values = expected_df_values.astype('unicode')
    actual_df = pd.DataFrame(data=actual_df_values, columns=actual_df.columns)
    expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
    new_df = pd.merge(actual_df, expected_df, on=cols, how='left', indicator='Exist')
    new_df['Exist'] = np.where(new_df.Exist == 'both', True, False)
    print('Merged DF')
    print(new_df)
    resultList = list(new_df['Exist'])
    print(resultList)
    flag = True
    for result in resultList:
        if result:
            print('Expected data found ')
        else:
            print('Expected data Not found ')
            flag = False
    if not flag:
        print('all records didnt match')
    else:
        print('all records matched')