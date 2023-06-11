def click_and_wait_for_download_to_complete(self, download_link_xpath=None, default_download_dir=None, start_wait_timeout=30, retry_interval=5, function_to_exec=None, hoverable_xpath=None, **params):
    """

        :param download_link_xpath:
        :param default_download_dir:
        :param start_wait_timeout:
        :param retry_interval:
        :param function_to_exec:
        :param params:
        :param hoverable_xpath:
        :return:
        """
    if download_link_xpath is None and function_to_exec is None:
        BuiltIn().fail('One of the parameter is required (download_link_xpath, default_download_dir)\nNone of the metioned parameters were passed')
    elif download_link_xpath is not None and function_to_exec is not None:
        BuiltIn().fail('Both download_link_xpath and function_to_exec passed.\nPlease pass one of the two options')
    if default_download_dir is None:
        BuiltIn().fail('Default download directory is compulsory field. Pass a valid Directory Path')
    elif not os.path.isdir(default_download_dir):
        BuiltIn().fail('default_download_dir value passed is not a valid directory')
    current_window_handle = self.s2l.driver.current_window_handle
    try:
        browser_version = int(self.s2l.driver.capabilities['version'].split('.')[0])
    except (KeyError, AttributeError, IndexError):
        browser_version = int(self.s2l.driver.capabilities.get('browserVersion').split('.')[0])

    def get_all_file_in_download_manager():
        """
            :return:
            """
        new_tab_query = "window.open('')"
        if not self.s2l.get_location().startswith('chrome://downloads'):
            self.s2l.execute_javascript(new_tab_query)
            time.sleep(2)
            self.s2l.switch_window('NEW')
            self.s2l.go_to('chrome://downloads')
        if browser_version >= 80:
            return self.s2l.execute_javascript("\n                return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').items;\n                ")
        else:
            return self.s2l.execute_javascript('\n                                return downloads.Manager.get().items_;\n                                ')

    def get_download_state_by_id(id):
        """

            :param id:
            :return:
            """
        if browser_version >= 80:
            script = "return document.querySelector('downloads-manager').shadowRoot\n                .querySelector('#downloadsList').items.filter(e => e.id === '{id}').map(e => e.state);".format(id=id)
        else:
            script = "return downloads.Manager.get().items_.filter(e => e.id === '{id}').map(e => e.state);".format(id=id)
        return self.s2l.execute_javascript(script)[0]

    def get_file_content(path):
        elem = self.s2l.driver.execute_script("var input = window.document.createElement('INPUT'); input.setAttribute('type', 'file'); input.hidden = true; input.onchange = function (e) { e.stopPropagation() }; return window.document.documentElement.appendChild(input); ")
        elem._execute('sendKeysToElement', {'value': [path], 'text': path})
        result = self.s2l.driver.execute_async_script('var input = arguments[0], callback = arguments[1]; var reader = new FileReader(); reader.onload = function (ev) { callback(reader.result) }; reader.onerror = function (ex) { callback(ex.message) }; reader.readAsDataURL(input.files[0]); input.remove(); ', elem)
        if not result.startswith('data:'):
            raise Exception('Failed to get file content: %s' % result)
        return base64.b64decode(result[result.find('base64,') + 7:])
    files_before_download = get_all_file_in_download_manager()
    previous_ids = [e['id'] for e in files_before_download]
    current_time = time.time()
    self.s2l.close_window()
    self.s2l.switch_window(current_window_handle)
    if not hoverable_xpath is None:
        self.s2l.mouse_over(hoverable_xpath)
        self.s2l.wait_until_element_is_visible(download_link_xpath, 60)
    if download_link_xpath is not None:
        self.s2l.click_element(download_link_xpath)
    else:
        function_to_exec(**params)
    new_file_download_id = None
    while new_file_download_id is None and time.time() - current_time < start_wait_timeout:
        files_list_after_click = get_all_file_in_download_manager()
        current_ids = [e['id'] for e in files_list_after_click]
        if len(set(current_ids).difference(previous_ids)) == 1:
            new_file_download_id = list(set(current_ids).difference(previous_ids))[0]
            print(new_file_download_id)
            break
        elif len(set(current_ids).difference(previous_ids)) > 1:
            BuiltIn().fail("Multiple Download started with IDs: '{}'".format(set(current_ids).difference(previous_ids)))
        else:
            time.sleep(retry_interval)
    if new_file_download_id is None:
        BuiltIn().fail('Cannot Start Downloading After waiting for {} seconds'.format(start_wait_timeout))
    else:
        time.sleep(retry_interval)
        download_state = get_download_state_by_id(new_file_download_id)
        while download_state == 'IN_PROGRESS':
            time.sleep(retry_interval)
            download_state = get_download_state_by_id(new_file_download_id)
            print('Download state: {}'.format(download_state))
        if download_state == 'COMPLETE':
            all_files = get_all_file_in_download_manager()
            file_path = [f['file_path'] if 'file_path' in f.keys() else f['filePath'] for f in filter(lambda e: e['id'] == new_file_download_id, all_files)][0]
            file_content = get_file_content(file_path)
            new_file_location = os.path.normpath(os.path.join(default_download_dir, os.path.basename(file_path)))
            print('Copying File to: {}'.format(new_file_location))
            with open(new_file_location, 'wb') as fp:
                fp.write(file_content)
        else:
            BuiltIn().fail('File download is not in progress and neither completed. Current State: {}'.format(download_state))
    self.s2l.close_window()
    self.s2l.switch_window(current_window_handle)
    return new_file_location