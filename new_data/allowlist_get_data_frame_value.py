def get_data_frame_value(self, data_frame, test='', column=''):
    column_position = '0'
    header_list = data_frame['Test Cases/Test Data']
    print('header_list=' + str(header_list))
    for (i, j) in header_list.items():
        if str(j) == column:
            column_position = i
    test_cases = data_frame
    print('Checking')
    print(test)
    print(column)
    for (v, k) in test_cases.items():
        print('checking with')
        print(str(v).lower())
        if str(v).lower() == str(str(test).lower()):
            key_found = v
            print('key_found: ' + str(k))
            print(data_frame[key_found][int(column_position)])
            return data_frame[key_found][int(column_position)]
        else:
            print('key not found')