def returndataframe(self, csvPath, sheetName):
    self.excelDF = self.excelTableToDataFrame(csvPath, sheetName)
    return self.excelDF.copy().to_dict()