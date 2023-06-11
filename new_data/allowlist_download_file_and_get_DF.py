def download_file_and_get_DF(self, path):
    self.download_dir = os.path.normpath(os.path.join(current_path, '..', '..', 'Downloads'))
    file_path = self.click_and_wait_for_download_to_complete(download_link_xpath=path, default_download_dir=self.download_dir)
    return pd.read_csv(file_path)