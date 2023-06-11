def excelTableToDataFrame(self, excelPath, sheetName):
    df = pd.read_excel(open(excelPath, 'rb'), sheet_name=sheetName)
    return df