    # coding: utf-8
import os
import glob
import requests
import platform
import sys
import pandas as pd
import time
from robot.api import logger
import random
import string
from robot.libraries.OperatingSystem import OperatingSystem
import mysql.connector
import platform
import json   
import pandas as pd
from robot.libraries.BuiltIn import BuiltIn 
current_path = os.path.dirname(__file__)
angularCoreComponentDir = os.path.join(current_path, "..", "..", "CommonScripts")
sys.path.append(angularCoreComponentDir)
common_workflow = os.path.join(current_path, "..")
from AngularCoreComponents7 import AngularCoreComponents7
import time, base64, os, sys, Selenium2Library
from robot.api import logger
from selenium.webdriver import Remote, Firefox, Chrome
from robot.libraries.BuiltIn import BuiltIn
import numpy as np

current_path = os.path.dirname(__file__)
dbdir = os.path.join(current_path, "..", "..", "PythonScripts", "DB")
sys.path.append(dbdir)

from robot.libraries.BuiltIn import BuiltIn
from BasePage import BasePage
from SeleniumWrapper import SeleniumWrapper
from GlobalUtilityKeywords import randomString,randomNumber,compareDataFrames
from Publisher_platform_level_allowlist import *
from AllowlistDB import AllowlistDB

if '2.7' not in platform.python_version():
    unicode = str

class allowlist(BasePage):
    
    CHROME_CAPABILITIES = {
        'browserName': 'chrome',
        # 'proxy': { \
        # 'proxyType': 'manual',
        # 'sslProxy': '50.59.162.78:8088',
        # 'httpProxy': '50.59.162.78:8088'
        # },
        'goog:chromeOptions': {
            'args': [
                '--incognito',
                '--disable-extensions'
            ],
            'prefs': {
                # 'download.default_directory': "",
                # 'download.directory_upgrade': True,
                'download.prompt_for_download': False,
                'plugins.always_open_pdf_externally': True,
                'safebrowsing_for_trusted_sources_enabled': False,
                'default_content_setting_values.cookies':2
            }
        }
    }

    def __init__(self):
        
        """
        Constructor
        """
        BasePage.__init__(self)
        self.sw = SeleniumWrapper()
        self.acc7 = AngularCoreComponents7()
        self.activity_file_name="mqbecltpsb.csv"
        print ("init..")
        self.DB=AllowlistDB()
        
    def logout_from_admin(self):
        """
        Logout on Admin Page
        :return:
        """
        headerXpath = "//pmac-header"
        userInfoXpath = headerXpath + "//*[@data-pm-id='gh-user-info']"
        logOutXpath = headerXpath + "//*[@data-pm-id='gh-log-out']"
        default_timeout = self.s2l.set_selenium_implicit_wait(2)
        self.s2l.element_should_be_visible(headerXpath)
        self.s2l.element_should_be_visible(userInfoXpath)
        self.s2l.click_element(userInfoXpath)
        self.s2l.element_should_be_visible(logOutXpath)
        self.s2l.click_element(logOutXpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        
    def logout_publisher_via_admin(self):
        """
        Logout from Publisher
        :return:
        """
        headerXpath = "//pmac-header"
        userInfoXpath = headerXpath + "//*[@data-pm-id='gh-user-info']"
        logOutXpath = headerXpath + "//*[@data-pm-id='gh-log-out']"
        default_timeout = self.s2l.set_selenium_implicit_wait(2)
        self.s2l.select_window("MAIN")
        self.s2l.element_should_be_visible(headerXpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.element_should_be_visible(userInfoXpath)
        self.s2l.click_element(userInfoXpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.element_should_be_visible(logOutXpath)
        self.s2l.click_element(logOutXpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        
    def search_and_login_as_publisher(self, pub_id):
        """
        search publisher and login
        :param pub_id: publisher id to login with
        :return: None
        """
        pub_id = unicode(pub_id)
        default_timeout = self.s2l.set_selenium_implicit_wait(2)
        search_pub_xpath = "//pmcc-input/input[@data-pm-id='search-pub']"
        search_btn_xpath = "//button[@data-pm-id='search-btn']"
        radio_btn_xpath = "//*[@data-pm-id='radio-" + pub_id + "']"
        login_pub_btn_xpath = "//*[@data-pm-id='login']"
        dashboard_title_xpath = "(//h1[contains(text(), 'Dashboard')])[1] | //h1//*[contains(text(), 'Dashboard')]"
        BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', search_pub_xpath)
        self.s2l.input_text(search_pub_xpath, pub_id)
        self.s2l.click_element(search_btn_xpath)
        BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'element_should_be_visible', radio_btn_xpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.click_element(radio_btn_xpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.click_element(login_pub_btn_xpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.select_window("NEW")
        BuiltIn().wait_until_keyword_succeeds('150 sec', '2 sec', 'element_should_be_visible', dashboard_title_xpath)
        
    def login_as_publisher_via_admin(self, admin_login_id, admin_password, pub_id,
                                     okta_username=None, okta_password=None, timeout=60):
        """
        Method to login to publisher via admin
        :param admin_login_id: admin username
        :param admin_password: admin password
        :param pub_id:
        :param okta_username:
        :param okta_password:
        :param timeout:
        :return:
        """
        self.login_as_admin(admin_login_id, admin_password, okta_username, okta_password, timeout=timeout)
        self.search_and_login_as_publisher(pub_id)
        
    def login_as_admin(self, admin_login_id, admin_password, okta_username="None", okta_password=None,
                       login_type="Publisher", timeout=60):
        """
        Method to login with admin
        :param admin_login_id: username
        :param admin_password: password
        :return:
        """
        default_timeout = self.s2l.set_selenium_implicit_wait(1)
        # Admin Login Page Xpaths
        username_xpath =  '//*[@id="okta-signin-username"]'
        password_xpath = '//*[@id="okta-signin-password"]'
        login_btn_xpath = '//*[@id="okta-signin-submit"]'
        # Okta Page Xpaths
        okta_username_xpath = '//*[@id="okta-signin-username"]'
        okta_password_xpath = '//*[@id="okta-signin-password"]'
        okta_submit_xpath = '//*[@id="okta-signin-submit"]'
        search_pub_title_xpath = "//*[@class='pmcc-page-content']//h1"  # //pmcc-search-publisher/h1
        campaign_manager_xpath = "//div/h1"
        self.s2l.maximize_browser_window()
        start_time = time.time()
        okta_connecting= "(//h1)[1]"
        
        BuiltIn().wait_until_keyword_succeeds('240 sec', '5 sec', 'element_should_contain',
                                                      okta_connecting, 'Connecting to')

        is_okta_login_page = BuiltIn().run_keyword_and_return_status("Click Element", okta_username_xpath)
        print ("okta")
        print (is_okta_login_page)
        if is_okta_login_page:
            print ("okta page")
            self.s2l.input_text(okta_username_xpath, "user_302@pubmatic.com")
            self.s2l.input_text(okta_password_xpath, "Asdf@123")
            self.s2l.click_element(okta_submit_xpath)
            print("okta login clicked")
            print ("checking status")
            BuiltIn().wait_until_keyword_succeeds("120 sec", "1 sec", "Click Element", username_xpath)
            print ("checking status done")
        
        admin_page= "(//h2)[1]"
        BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain',
                                                      admin_page, 'Log In to Your Account')

        
        is_admin_page = BuiltIn().run_keyword_and_return_status("Click Element", username_xpath)
        is_admin_page=True
        print("is_admin_page="+str(is_admin_page))
        if is_admin_page:
            print("in admin login flow")
            #time.sleep(10)
            #self.s2l.reload_page()
            #time.sleep(30)
            print (admin_login_id)
            self.s2l.input_text(username_xpath, admin_login_id)
            #time.sleep(3)
            self.s2l.input_text(password_xpath, admin_password)
            #time.sleep(3)
            self.s2l.click_element(login_btn_xpath)
            #time.sleep(3)
            if login_type == "Publisher":
                BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain',
                                                      search_pub_title_xpath, 'Search Publisher')
            elif login_type == "Admin":
                BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain',
                                                      search_pub_title_xpath, 'Search Publisher')
            elif login_type == "Demand":
                BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain',
                                                      campaign_manager_xpath, 'Campaign Manager')
        
        print("exiting login method")
        self.s2l.set_selenium_implicit_wait(default_timeout)
        
    def navigate_to(self, menu_identifier, sub_menu_identifier):
        """
        Method to navigate to page
        :param menu_identifier:
        :param sub_menu_identifier:
        :return:
        """
        
        default_timeout = self.s2l.set_selenium_implicit_wait(2)
        menuXpath = "//*[@data-pm-id='{}']".format(menu_identifier)
        subMenuXpath = "//*[@data-pm-id='{}']".format(sub_menu_identifier)
        BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_be_visible',
                                                      menuXpath)
        

        self.s2l.element_should_be_visible(menuXpath)
        self.s2l.click_element(menuXpath)

        self.s2l.set_selenium_implicit_wait(default_timeout)
        self.s2l.element_should_be_visible(subMenuXpath)
        self.s2l.click_element(subMenuXpath)
        self.s2l.set_selenium_implicit_wait(default_timeout)
        
    def open_browser_with_download_capabilities(self, url, browser='gc',remote_url=None):
        """

        :param url:
        :param browser:
        :param remote_url:
        :return:
        """
        driver = None
        if remote_url is not None:
            if browser.lower() == 'gc' or browser.lower() == 'chrome':
                driver = Remote(remote_url, self.CHROME_CAPABILITIES)
            else:
                pass
                # TODO: Add Firefox Capabilities
        else:
            if browser.lower() == 'gc' or browser.lower() == 'chrome':
                driver = Chrome(desired_capabilities=self.CHROME_CAPABILITIES)
            else:
                pass
                # TODO: Add Firefox Browser

        driver.get(url)
        driver.set_script_timeout(30)
        self.s2l.register_driver(driver, alias='wd')
         

    def verify_page_title(self):
        print ("cheking page title and components")
        
        
    """ multi sql execute function """
    def execute_sql_db_multi(self, sql, db_server, db_user, db_password,db_port,db):
        mydb = mysql.connector.connect(
            host=str(db_server),
            user=str(db_user),
            port=str(db_port),
            passwd=str(db_password),
            database=str(db)
        )
        mycursor = mydb.cursor()
        select_out=[]
        for result in mycursor.execute(sql, multi=True):
            if result.with_rows:
                out = result.fetchall()
                select_out.append(out)
            else:
                pass

        mydb.commit()
        return select_out

    def activity_operations_validator(self, db_server, db_port, db_user, db_password,file_name):
        mydb = mysql.connector.connect(
            host=str(db_server),
            user=str(db_user),
            port=str(db_port),
            passwd=str(db_password),
            database="ActivityLog"
        )

 
        flag = False
        for i in range(1, 200): 
            mycursor = mydb.cursor()
            sql = "select status  from bulk_operations where  file_name ='"+str(file_name)+"'; "
            print(sql)
            mycursor.execute(sql)
            data = mycursor.fetchone()
            if isinstance(data, tuple):
                for x in data:
                    print(x)
                    if x == "1":
                        flag = True
                        # return
            if flag == True:
                print("bulk operation validated!")
                
                return
            time.sleep(1)
            print("sleeping")
            mydb.commit()
        
        raise Exception("bulk operation failed!") 
    def upload_allowlist(self, test_data,db_server,db_port,db_user,db_password, ui_setup , token,komli_db_host,activity_db_host,common_db_user_name,common_db_password,common_db_port ):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        print ("test_data="+str(test_data))
        upload_content=test_data["upload_content"]
        populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
        db_cleanup=str(test_data["db_cleanup"]).lower().strip()
        print ("db_cleanup flag="+str(db_cleanup))
        if(db_cleanup=="true"):
           start = time.time()
           self.clean_up_allowlist_upload(test_data,db_server,db_port,db_user,db_password)
           end = time.time()
           print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
        
        start = time.time()
        self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        end = time.time()
        print("Runtime of the global_channel_partner_blocklist_filter is {end - start}")
 
        start = time.time()
        self.global_publisher_blocklist_filter(test_data, komli_db_host,common_db_port, common_db_user_name, common_db_password)
        end = time.time()
        print("Runtime of the global_publisher_blocklist_filter is "+str(end - start))
        
        start = time.time()
        self.heimdall_cache_refresh(ui_setup, token)
        end = time.time()
        print("Runtime of the heimdall_cache_refresh is "+str(end - start))
        
        start = time.time()
        self.populate_data(test_data,db_server,db_port,db_user,db_password,komli_db_host,common_db_port, common_db_user_name, common_db_password)
        end = time.time()
        print("Runtime of the populate_data is "+str(end - start))
  
        self.current_path = os.path.dirname(__file__)
        print("current_path= "+str(current_path))

        letters = string.ascii_lowercase
        file_name= ( ''.join(random.choice(letters) for i in range(10)) )
        file_name=file_name+".csv"
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        f = open(file_path, "w")
        f.write(str(upload_content))
        f.close()
        
        print("file_path= "+str(file_path)) 
        BuiltIn().log(file_path, level="INFO")
        self.acc7.pmccFileUpload('upload-control', file_path)
        self.acc7.validatePmccFileUpload('upload-control', file_path)
        self.acc7.pmccButton('upload-btn')
        time.sleep(2) 
        
        
        self.activity_operations_validator(activity_db_host,common_db_port, common_db_user_name, common_db_password, file_name)
        self.activity_file_name=file_name
        #self.validate_allowlist_upload( test_data,db_server,db_port,db_user,db_password)
        start=time.time()
        self.validate_failed_files(ui_setup,token ,test_data,db_server,db_port,db_user,db_password)
        end = time.time()
        print("Runtime of the populate_data is "+str(end - start))
        
   
        start=time.time()
        self.validate_allowlist_stats(test_data, db_server, db_port, db_user, db_password)
        end = time.time()
        print("Runtime of the populate_data is "+str(end - start))
        
        
    def upload_allowlist_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password, ui_setup , token,komli_db_host,activity_db_host,common_db_user_name,common_db_password,common_db_port ,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password,cleanup="True",deleted_data="False",uri_prefix=""):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        #print (activity_db_host,common_db_user_name,common_db_password,common_db_port)
    
        if deleted_data == "False":
            #self.s2l.reload_page()
            upload_content=test_data["upload_content"]
            processed_file_data=test_data["processed_file"]
            failed_file_data=test_data["failed_file"]
            
            #print (failed_file_data)
            #print (processed_file_data)
            populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
            db_cleanup=str(test_data["db_cleanup"]).lower().strip()
            #print ("db_cleanup flag="+str(db_cleanup))
            if cleanup=="True":
                print("INSIDE CLEANUP")
                print("DB_CLEANUP:", db_cleanup, " FIN")
                if(db_cleanup=="true"):
                    print("INSIDE DB_CLEANUP")
                    start = time.time()
                    self.clean_up_allowlist_upload_new(test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password,komli_db_host,common_db_user_name,common_db_password,common_db_port)
                    end = time.time()
               #print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
               
               
                self.hawkeye_app_details_add_del(test_data,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password)

                self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    
                self.global_publisher_blocklist_filter_new(test_data, komli_db_host,common_db_port, common_db_user_name, common_db_password)
                
                self.platform_allowlist_filter_new(test_data, fraud_db_server,fraud_db_port, fraud_db_user, fraud_db_password)

                self.publisher_blocklist_filter(test_data, fraud_db_server, fraud_db_port, fraud_db_user,
                                                   fraud_db_password)
            
            self.heimdall_cache_refresh(ui_setup, token)

       
            self.current_path = os.path.dirname(__file__)
            print("current_path= "+str(self.current_path))
      
            letters = string.ascii_lowercase
            file_name= ( ''.join(random.choice(letters) for i in range(10)) )
            file_name=file_name+".csv"
            file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
            print (file_path)

            with open(file_path,"w+") as f:
                f.write(str(upload_content))

            
            self.infra_upload(uri_prefix, "/heimdall/adminLevelPublisherAllowlist/", file_path)
            
            #upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
            #self.refresh="//button/pmcc-icon[@name='refresh']"
            #while upload_status == "Processing":
            #    print (upload_status)
            #    self.s2l.click_element(self.refresh)
            #    time.sleep(2)
            #    upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
            #print ("Completed")
            #time.sleep(180)
            #print (upload_status)
             
#            self.validate_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#             self.s2l.reload_page()
#             self.wait_for_spinner_to_disappear(120)
#             print ("triple dots action")
#             time.sleep(10)
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#               
#             failed_file="//ul[@class='action-menu']//li[2]"
#             processed_file="//ul[@class='action-menu']//li[3]"
#               
#             self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#             #print (self.download_dir)
#               
#             failed_file_df=self.download_file_and_get_DF(failed_file)
             
#             #print ("failed_file_df")
#             #failed_file_df = failed_file_df.drop([''], axis=1)
#              
#             with open(self.download_dir+"/failed_file.csv","w") as f:
#                 f.write(failed_file_data)
#                  
#             actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#              
#             failed_file_df_from_test_data = pd.read_csv(file_path)
#              
#             #print (failed_file_df)
#              
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#               
#               
#             processed_file_df=self.download_file_and_get_DF(processed_file)
            
#             print ("processed_file_df")
#             #processed_file_df = processed_file_df.drop([''], axis=1)
#              
#             with open(self.download_dir+"/processed_file.csv","w") as f:
#                 f.write(processed_file_data)
#                  
#             actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#              
#             print ("comparing downloaded processed file and test data processed file")
#             print (actual_processed_file_df)
#             self.search_in_df(actual_processed_file_df, processed_file_df)
#              
#             print ("comparing downloaded failed file and test data failed file")
#             print (actual_failed_file_df)
#             self.search_in_df(actual_failed_file_df, failed_file_df)
#      
#              
#             from pathlib import Path
#       
#             [f.unlink() for f in Path(self.download_dir).glob("*csv") if f.is_file()]
#              
#             return file_name 
#       
#             #self.delete_BulkOps(file_name, activity_db_host,common_db_user_name,common_db_password,common_db_port)
#              
#             self.s2l.reload_page()
            
            
        elif deleted_data == "True":
            upload_content_del=test_data["upload_content_del"]
            processed_file_data=test_data["processed_file_del"]
            failed_file_data=test_data["failed_file_del"]
            
            
            if cleanup=="True":
                if(db_cleanup=="true"):
                   start = time.time()
                   self.clean_up_allowlist_upload_new(test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password,komli_db_host,common_db_user_name,common_db_password,common_db_port)
                   end = time.time()
               #print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
               
               
            
                self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    
                self.global_publisher_blocklist_filter_new(test_data, komli_db_host,common_db_port, common_db_user_name, common_db_password)
            
            self.heimdall_cache_refresh(ui_setup, token)
            
            self.current_path = os.path.dirname(__file__)
            print("current_path= "+str(self.current_path))
      
            letters = string.ascii_lowercase
            file_name= ( ''.join(random.choice(letters) for i in range(10)) )
            file_name=file_name+".csv"
            file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
            print (file_path)

            with open(file_path,"w+") as f:
                f.write(str(upload_content_del))

            
            self.infra_upload(uri_prefix, "/heimdall/adminLevelPublisherAllowlist/", file_path)
            
#             self.validate_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#             self.s2l.reload_page()
#             self.wait_for_spinner_to_disappear(60)
#             print ("triple dots action")
#             time.sleep(10)
#             
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#              
#             failed_file="//ul[@class='action-menu']//li[2]"
#             processed_file="//ul[@class='action-menu']//li[3]"
#              
#             self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#             #print (self.download_dir)
#              
#             failed_file_df=self.download_file_and_get_DF(failed_file)
#             #print ("failed_file_df")
#             #failed_file_df = failed_file_df.drop([''], axis=1)
#             
#             with open(self.download_dir+"/failed_file.csv","w") as f:
#                 f.write(failed_file_data)
#                 
#             actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#             
#             failed_file_df_from_test_data = pd.read_csv(file_path)
#             
#             #print (failed_file_df)
#             
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#              
#              
#             processed_file_df=self.download_file_and_get_DF(processed_file)
#             #print ("processed_file_df")
#             #processed_file_df = processed_file_df.drop([''], axis=1)
#             
#             with open(self.download_dir+"/processed_file.csv","w") as f:
#                 f.write(processed_file_data)
#                 
#             actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#             
#             print ("comparing downloaded processed file and test data processed file")
#             self.search_in_df(actual_processed_file_df, processed_file_df)
#             
#             print ("comparing downloaded failed file and test data failed file")
#             self.search_in_df(actual_failed_file_df, failed_file_df)
#     
#             
#             from pathlib import Path
#      
#             [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()]
             
#                     
#             #self.s2l.click_element(self.close_upload_form)
#             return file_name

    
    def upload_admin_pubsite_allowlist_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password, ui_setup , token,Komli_db_server,BulkOps_db_server,activity_db_host,common_db_user_name,common_db_password,common_db_port,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,cleanup="True",deleted_data="False"):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        import time
        print (activity_db_host,common_db_user_name,common_db_password,common_db_port)
    
        if deleted_data == "False":
            upload_content=test_data["upload_content"]
            processed_file_data=test_data["processed_file"]
            failed_file_data=test_data["failed_file"]
            
            #print (failed_file_data)
            #print (processed_file_data)
            
            
            populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
            db_cleanup=str(test_data["db_cleanup"]).lower().strip()
            
            
            
            print ("db_cleanup flag="+str(db_cleanup))
            if cleanup=="True":
                if(db_cleanup=="true"):
                   start = time.time()
                   self.clean_up_pub_site_allowlist_upload_new(test_data,Komli_db_server,BulkOps_db_server,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,common_db_port,common_db_user_name,common_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)
                   end = time.time()
                   print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
                   
                self.hawkeye_app_details_add_del(test_data,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)
                   
                self.global_channel_partner_blocklist_filter(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)
    
                self.global_publisher_blocklist_filter_new(test_data, Komli_db_server,common_db_port, common_db_user_name, common_db_password)
                
                self.platform_allowlist_filter_new(test_data, fraud_db_server,fraud_db_port, fraud_db_user, fraud_db_password)

                self.publisher_blocklist_filter(test_data, fraud_db_server, fraud_db_port, fraud_db_user,
                                                fraud_db_password)
                
            self.heimdall_cache_refresh(ui_setup, token)
             
       
            self.current_path = os.path.dirname(__file__)
            print("current_path= "+str(self.current_path))
      
            letters = string.ascii_lowercase
            file_name= ( ''.join(random.choice(letters) for i in range(10)) )
            file_name=file_name+".csv"
            file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
            print (file_path)

            with open(file_path,"w+") as f:
                f.write(str(upload_content))

            
            self.infra_upload(ui_setup.split('//')[1], "/heimdall/publisherWhitelist", file_path)
            #print (upload_status)
            
#             self.validate_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#             self.s2l.reload_page()
#             self.wait_for_spinner_to_disappear(60)
#             print ("triple dots action")
#             time.sleep(10)
#              
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#              
#             failed_file="//ul[@class='action-menu']//li[2]"
#             processed_file="//ul[@class='action-menu']//li[3]"
#              
#             self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#             #print (self.download_dir)
#              
#             failed_file_df=self.download_file_and_get_DF(failed_file)
#             #print ("failed_file_df")
#             #failed_file_df = failed_file_df.drop([''], axis=1)
#              
#             with open(self.download_dir+"/failed_file.csv","w") as f:
#                 f.write(failed_file_data)
#                  
#             actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#              
#             failed_file_df_from_test_data = pd.read_csv(file_path)
#              
#             #print (failed_file_df)
#              
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#              
#              
#             processed_file_df=self.download_file_and_get_DF(processed_file)
#             #print ("processed_file_df")
#             #processed_file_df = processed_file_df.drop([''], axis=1)
#              
#             with open(self.download_dir+"/processed_file.csv","w") as f:
#                 f.write(processed_file_data)
#                  
#             actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#              
#             print ("comparing downloaded processed file and test data processed file")
#             self.search_in_df(actual_processed_file_df, processed_file_df)
#              
#             print ("comparing downloaded failed file and test data failed file")
#             self.search_in_df(actual_failed_file_df, failed_file_df)
#      
#              
#             from pathlib import Path
#      
#             [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()] 
#      
#             #self.delete_BulkOps(file_name, activity_db_host,common_db_user_name,common_db_password,common_db_port)
#             return file_name
             
            #self.s2l.reload_page()
            
            
        elif deleted_data == "True":
            upload_content_del=test_data["upload_content_del"]
            processed_file_data=test_data["processed_file_del"]
            failed_file_data=test_data["failed_file_del"]
            
            self.current_path = os.path.dirname(__file__)
            print("current_path= "+str(self.current_path))
      
            letters = string.ascii_lowercase
            file_name= ( ''.join(random.choice(letters) for i in range(10)) )
            file_name=file_name+".csv"
            file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
            print (file_path)

            with open(file_path,"w+") as f:
                f.write(str(upload_content_del))

            
            self.infra_upload(ui_setup.split('//')[1], "/heimdall/publisherWhitelist", file_path)
            #print (upload_status)
            
#             self.validate_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#             self.s2l.reload_page()
#             self.wait_for_spinner_to_disappear(60)
#             print ("triple dots action")
#             time.sleep(10)
#             
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#             
#             failed_file="//ul[@class='action-menu']//li[2]"
#             processed_file="//ul[@class='action-menu']//li[3]"
#             
#             self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#             #print (self.download_dir)
#             
#             failed_file_df=self.download_file_and_get_DF(failed_file)
#             #print ("failed_file_df")
#             #failed_file_df = failed_file_df.drop([''], axis=1)
#             
#             with open(self.download_dir+"/failed_file.csv","w") as f:
#                 f.write(failed_file_data)
#                 
#             actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#             
#             failed_file_df_from_test_data = pd.read_csv(file_path)
#             
#             #print (failed_file_df)
#             
#             action_triple_dop="//table//tbody[@data-pm-id='bulk-upload-table-body']//td[text()='{}']//preceding::td//pmcc-table-actions[@data-pm-id='row-table-action']".format(file_name)
#             self.s2l.click_element(action_triple_dop)
#             
#             
#             processed_file_df=self.download_file_and_get_DF(processed_file)
#             #print ("processed_file_df")
#             #processed_file_df = processed_file_df.drop([''], axis=1)
#             
#             with open(self.download_dir+"/processed_file.csv","w") as f:
#                 f.write(processed_file_data)
#                 
#             actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#             
#             print ("comparing downloaded processed file and test data processed file")
#             self.search_in_df(actual_processed_file_df, processed_file_df)
#             
#             print ("comparing downloaded failed file and test data failed file")
#             self.search_in_df(actual_failed_file_df, failed_file_df)
#     
#             
#             from pathlib import Path
#     
#             [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()]
#             
#                     
#             #self.s2l.click_element(self.close_upload_form)
#             return file_name



    def upload_plat_allowlist_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password, ui_setup ,token,activity_db_host,common_db_user_name,common_db_password,common_db_port,uri_prefix,komli_db_host,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,cache_refresh="True"):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        print (activity_db_host,common_db_user_name,common_db_password,common_db_port)
        #self.s2l.reload_page()
        upload_content=test_data["upload_content"]
        processed_file_data=test_data["processed_file"]
        failed_file_data=test_data["failed_file"]
        
        #print (failed_file_data)
        #print (processed_file_data)
        
        
        populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
        db_cleanup=str(test_data["db_cleanup"]).lower().strip()
        print ("db_cleanup flag="+str(db_cleanup))
        if(db_cleanup=="true"):
           start = time.time()
           self.clean_up_plat_allowlist_upload_new(test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)
           end = time.time()
           print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
         
        if  cache_refresh=="False":
            self.heimdall_cache_refresh(ui_setup, token) 
         
        self.hawkeye_app_details_add_del(test_data,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)
        
        self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)

        self.global_publisher_blocklist_filter_new(test_data, komli_db_host,common_db_port, common_db_user_name, common_db_password)
            
        self.insert_app_details(test_data,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)    
        
        self.heimdall_cache_refresh(ui_setup, token)
         
        self.current_path = os.path.dirname(__file__)
        print("current_path= "+str(self.current_path))
      
        letters = string.ascii_lowercase
        file_name= ( ''.join(random.choice(letters) for i in range(10)) )
        file_name=file_name+".csv"
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        print (file_path)

        with open(file_path,"w+") as f:
            f.write(str(upload_content))

            
        self.infra_upload(uri_prefix, "/heimdall/bulkPlatformAllowlist", file_path)
        #print (upload_status)
        
#         self.validate_plat_upload_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#         
#         self.s2l.reload_page()
#         self.wait_for_spinner_to_disappear(60)
#         print ("triple dots action")
#         time.sleep(10)
#         
#         upload_button = "//button[@data-pm-id='bulk-upload-btn']"
#         self.s2l.click_element(upload_button)
#         
#         action_triple_dop="//table[@class='pmcc-table pmcc-table-sortable']//tbody//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         failed_file="//li[.='Download Failed Entries (CSV)']"
#         processed_file="//li[.='Download Processed Entries (CSV)']"
#         
#         self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#         #print (self.download_dir)
#         
#         failed_file_df=self.download_file_and_get_DF(failed_file)
#         #print ("failed_file_df")
#         #failed_file_df = failed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/failed_file.csv","w") as f:
#             f.write(failed_file_data)
#             
#         actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#         
#         failed_file_df_from_test_data = pd.read_csv(file_path)
#         
#         #print (failed_file_df)
#         
#         action_triple_dop="//table[@class='pmcc-table pmcc-table-sortable']//tbody//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         
#         processed_file_df=self.download_file_and_get_DF(processed_file)
#         #print ("processed_file_df")
#         #processed_file_df = processed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/processed_file.csv","w") as f:
#             f.write(processed_file_data)
#             
#         actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#         
#         print ("comparing downloaded processed file and test data processed file")
#         self.search_in_df(actual_processed_file_df, processed_file_df)
#         
#         print ("comparing downloaded failed file and test data failed file")
#         self.search_in_df(actual_failed_file_df, failed_file_df)
#     
#         
#         from pathlib import Path
#     
#         [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()] 
#     
#         self.delete_BulkOps(file_name, activity_db_host,common_db_user_name,common_db_password,common_db_port)
#         
#         self.s2l.reload_page()
#             
#         for data in processed_file_data.split('\n')[1:]:
#             print (data)
#             self.validate_plat_ui_table(data,db_user,db_password,db_server,db_port,common_db_user_name,common_db_password,activity_db_host,common_db_port,uri_prefix,token)      
#     
    
    def upload_pub_allowlist_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password, ui_setup ,token,activity_db_host,common_db_user_name,common_db_password,common_db_port,uri_prefix,user,komli_db_host,spoofer_server_url,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        #self.s2l.reload_page()
        print (activity_db_host,common_db_user_name,common_db_password,common_db_port)
    
        upload_content=test_data["upload_content"]
        processed_file_data=test_data["processed_file"]
        failed_file_data=test_data["failed_file"]
        
        pixalate_spoofer_data=test_data["pixalate_data"]
        
        
        
        populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
        db_cleanup=str(test_data["db_cleanup"]).lower().strip()
        print ("db_cleanup flag="+str(db_cleanup))
        if(db_cleanup=="true"):
           start = time.time()
           self.clean_up_pub_allowlist_upload_new(test_data, fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,user)
           end = time.time()
           print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
           
           
        if str(pixalate_spoofer_data)!="none":
            print  ("data to add for p&m")
            print (pixalate_spoofer_data)
            m_p_data = pixalate_spoofer_data.split('\n')
            for data in m_p_data:
                file_name = data.split('###')[0]
                pixalate_data = data.split('###')[1]
                self.update_spoofer_response_file(spoofer_server_url, file_name + "_pixelate_spoofer.csv", pixalate_data)
                     
            print("returning from spoofer population")
        else:
            print ("nothing to add to p&m")
           
        self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)

        self.global_publisher_blocklist_filter_new(test_data, komli_db_host,common_db_port, common_db_user_name, common_db_password)
            
        self.publisher_blocklist_filter(test_data, fraud_db_server, fraud_db_port, fraud_db_user,
                                                   fraud_db_password)
        self.heimdall_cache_refresh(ui_setup, token)
         
       
        self.current_path = os.path.dirname(__file__)
        print("current_path= "+str(self.current_path))
      
        letters = string.ascii_lowercase
        file_name= ( ''.join(random.choice(letters) for i in range(10)) )
        file_name=file_name+".csv"
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        print (file_path)

        with open(file_path,"w+") as f:
            f.write(str(upload_content))

      
        #self.infra_upload(ui_setup.split('//')[1], "/heimdall/topLevelAdContainer/", file_path)
        
        self.infra_upload1(ui_setup.split('//')[1], f"resourceUrl=/heimdall/publisherAllowlist?entityId={user}&mode=upload&doIQScan=true", file_path)
        #print (upload_status)
        
#         self.validate_pub_upload_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#         self.s2l.reload_page()
#         self.wait_for_spinner_to_disappear(60)
#         print ("triple dots action")
#         time.sleep(10)
#         
#         upload_button = "//button[@data-pm-id='add-domain-btn']"
#         self.s2l.click_element(upload_button)
#         
#         self.s2l.wait_until_element_is_visible("//pmcc-singleselect", 60)
#         time.sleep(5)
#         
#         drop_down = "//pmcc-dropdown[@data-pm-id='method-dropdown']"
#         self.s2l.click_element(drop_down)
#         
#         Bulk_upload = "//li[@data-pm-id='inline-menu-item'][2]"
#         self.s2l.click_element(Bulk_upload)
#         
#         
#         self.wait_for_spinner_to_disappear(60)
#         
#         action_triple_dop="//div[@class='pmcc-table-scrollable']//table//tbody//tr//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         failed_file="//li[.='Download All Failed Entries (CSV)']"
#         processed_file="//li[.='Download All Processed Entries (CSV)']"
#         
#         self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#         #print (self.download_dir)
#         
#         failed_file_df=self.download_file_and_get_DF(failed_file)
#         #print ("failed_file_df")
#         #failed_file_df = failed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/failed_file.csv","w") as f:
#             f.write(failed_file_data)
#             
#         actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#         
#         failed_file_df_from_test_data = pd.read_csv(file_path)
#         
#         #print (failed_file_df)
#         
#         action_triple_dop="//div[@class='pmcc-table-scrollable']//table//tbody//tr//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         
#         processed_file_df=self.download_file_and_get_DF(processed_file)
#         #print ("processed_file_df")
#         #processed_file_df = processed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/processed_file.csv","w") as f:
#             f.write(processed_file_data)
#             
#         actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#         
#         print ("comparing downloaded processed file and test data processed file")
#         self.search_in_df(actual_processed_file_df, processed_file_df)
#         
#         print ("comparing downloaded failed file and test data failed file")
#         self.search_in_df(actual_failed_file_df, failed_file_df)
#     
#         
#         from pathlib import Path
#     
#         [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()] 
#     
#         self.delete_BulkOps(file_name, activity_db_host,common_db_user_name,common_db_password,common_db_port)
#         
#         self.s2l.reload_page()
#             
#         for data in processed_file_data.split('\n')[1:]:
#             print (data)
#             self.validate_publisher_ui_table(data,db_user,db_password,db_server,db_port,common_db_user_name,common_db_password,activity_db_host,common_db_port,uri_prefix,token,user)      
#         
#         for data in failed_file_data.split('\n')[1:]:
#             print (data)
#             self.validate_download_all_pub_allow(data.split(',')[0],uri_prefix,token,user)      
#             
#         self.s2l.reload_page()
        
    def upload_pub_site_allowlist_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password, ui_setup ,Komli_db_server,BulkOps_db_server,activity_db_host,common_db_user_name,common_db_password,common_db_port,uri_prefix, token,user,spoofer_server_url,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        #self.s2l.reload_page()
        #print (db_server,db_port,db_user,db_password, ui_setup , token,Komli_db_server,BulkOps_db_server,activity_db_host,common_db_user_name,common_db_password,common_db_port,user)
    
        upload_content=test_data["upload_content"]
        processed_file_data=test_data["processed_file"]
        failed_file_data=test_data["failed_file"]
        pixalate_spoofer_data=test_data["pixalate_data"]
        
        #print (failed_file_data)
        #print (processed_file_data)
        
        self.global_channel_partner_blocklist_filter(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)

        self.global_publisher_blocklist_filter_new(test_data, Komli_db_server,common_db_port, common_db_user_name, common_db_password)
        
        self.platform_allowlist_filter_new(test_data, fraud_db_server,fraud_db_port, fraud_db_user, fraud_db_password)
            
        self.heimdall_cache_refresh(ui_setup, token)
        
        
        populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
        db_cleanup=str(test_data["db_cleanup"]).lower().strip()
        print ("db_cleanup flag="+str(db_cleanup))
        if(db_cleanup=="true"):
           start = time.time()
           self.clean_up_pub_pub_site_allowlist_upload_new(test_data,Komli_db_server,BulkOps_db_server,common_db_port,common_db_user_name,common_db_password,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,user)
           end = time.time()
           print("Runtime of the clean_up_allowlist_upload is "+str(end - start))
        
        if str(pixalate_spoofer_data)!="none":
            print  ("data to add for p&m")
            print (pixalate_spoofer_data)
            m_p_data = pixalate_spoofer_data.split('\n')
            for data in m_p_data:
                file_name = data.split('###')[0]
                pixalate_data = data.split('###')[1]
                self.update_spoofer_response_file(spoofer_server_url, file_name + "_pixelate_spoofer.csv", pixalate_data)
                     
            print("returning from spoofer population")
        else:
            print ("nothing to add to p&m")
         
       
        self.current_path = os.path.dirname(__file__)
        print("current_path= "+str(current_path))
     
        letters = string.ascii_lowercase
        file_name= ( ''.join(random.choice(letters) for i in range(10)) )
        file_name=file_name+".csv"
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        #f = open(file_path, "w")
        #f.write(str(upload_content))
        #.close()
         
        print("file_path= "+str(file_path))
        with open(file_path,"w+") as f:
            f.write(str(upload_content))

      
        #self.infra_upload(ui_setup.split('//')[1], "/heimdall/topLevelAdContainer/", file_path)
        
        self.infra_upload1(ui_setup.split('//')[1], f"resourceUrl=/heimdall/topLevelAdContainer/?entityId={user}&mode=upload&doIQScan=true", file_path)
 
        #BuiltIn().log(file_path, level="INFO")
        #time.sleep(15)
        
        #Bulk_Upload = "//pmcc-btn-menu[@data-pm-id='bulk-upload-button-menu']"
        #self.s2l.click_element(Bulk_Upload)
        
        #self.s2l.wait_until_element_is_visible("//li[@data-pm-id='inline-menu-item'][3]", 100)
        
        # upload_domains = "//li[@data-pm-id='inline-menu-item'][3]"
        # self.s2l.click_element(upload_domains)
        #
        # self.s2l.wait_until_element_is_visible("//button[@data-pm-id='upload-btn']", 100)
        # #time.sleep(5)
        #
        #
        # self.acc7.pmccFileUploadpubSite("bulk-site-upload", file_path)
        #
        # print ("file selected")
        # self.wait_for_spinner_to_disappear(100)
        #
        # self.acc7.pmccButton("upload-btn")
        #
        # upload_status_xpath = "(//div[@class='pmcc-table-scrollable']//table//tbody//tr//td[text()='{}']//ancestor::tr//td)[7]"
        # file_name = os.path.basename(file_path)
        # upload_status_xpath = upload_status_xpath.format(file_name)
        # upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
        # self.refresh="//button/pmcc-icon[@name='refresh']"
        # while upload_status == "Processing":
        #     print (upload_status)
        #     self.s2l.click_element(self.refresh)
        #     time.sleep(10)
        #     upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
        # print ("Completed")
        # time.sleep(60)
        #print (upload_status)
        
#         self.validate_pub_site_upload_bulk_upload_table(file_name,activity_db_host,common_db_user_name, common_db_password,common_db_port)
#         self.s2l.reload_page()
#         self.wait_for_spinner_to_disappear(60)
#         print ("triple dots action")
#         time.sleep(10)
#         
#         Bulk_Upload = "//pmcc-btn-menu[@data-pm-id='bulk-upload-button-menu']"
#         self.s2l.click_element(Bulk_Upload)
#         
#         #self.s2l.wait_until_element_is_visible("//li[@data-pm-id='inline-menu-item'][3]", 100)
#         
#         upload_domains = "//li[@data-pm-id='inline-menu-item'][3]"
#         self.s2l.click_element(upload_domains)
#         
#         self.s2l.wait_until_element_is_visible("//button[@data-pm-id='upload-btn']", 100)
#         
#         
#         action_triple_dop="//div[@class='pmcc-table-scrollable']//table//tbody//tr//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         failed_file="//li[.='Download All Failed Entries (CSV)']"
#         processed_file="//li[.='Download All Processed Entries (CSV)']"
#         
#         self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
#         #print (self.download_dir)
#         
#         failed_file_df=self.download_file_and_get_DF(failed_file)
#         #print ("failed_file_df")
#         #failed_file_df = failed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/failed_file.csv","w") as f:
#             f.write(failed_file_data)
#             
#         actual_failed_file_df = pd.read_csv(self.download_dir+"/failed_file.csv")
#         
#         failed_file_df_from_test_data = pd.read_csv(file_path)
#         
#         #print (failed_file_df)
#         
#         action_triple_dop="//div[@class='pmcc-table-scrollable']//table//tbody//tr//td[text()='{}']//ancestor::tr//*[@data-pm-id='table-action-btn']".format(file_name)
#         self.s2l.click_element(action_triple_dop)
#         
#         
#         processed_file_df=self.download_file_and_get_DF(processed_file)
#         #print ("processed_file_df")
#         #processed_file_df = processed_file_df.drop([''], axis=1)
#         
#         with open(self.download_dir+"/processed_file.csv","w") as f:
#             f.write(processed_file_data)
#             
#         actual_processed_file_df = pd.read_csv(self.download_dir+"/processed_file.csv")
#         
#         print ("comparing downloaded processed file and test data processed file")
#         self.search_in_df(actual_processed_file_df, processed_file_df)
#         
#         print ("comparing downloaded failed file and test data failed file")
#         self.search_in_df(actual_failed_file_df, failed_file_df)
#     
#         
#         from pathlib import Path
#     
#         [f.unlink() for f in Path(self.download_dir).glob("*") if f.is_file()] 
#     
#         self.delete_BulkOps(file_name, activity_db_host,common_db_user_name,common_db_password,common_db_port)
#         
#         self.s2l.reload_page()
#         
#         
#             
#         for data in processed_file_data.split('\n')[1:]:
#             print (data)
#             #self.validate_publisher_ui_table(data,db_user,db_password,db_server,db_port,common_db_user_name,common_db_password,activity_db_host,common_db_port,uri_prefix,token,user)
#             self.validate_view_domain_ui_table(data,common_db_user_name,common_db_password,BulkOps_db_server,common_db_port,uri_prefix,token,user)
#             
                  
        
    def validate_plat_ui_table(self,test_data,db_user_name,db_password,db_host,db_port, activity_logs_db_user_name,activity_logs_db_password,activity_logs_db_host,activity_logs_db_port,uri_prefix,token):
        
        self.find_domain_platform_allowlist(test_data.split(',')[0])
        df_db=self.get_platform_allowlist_db_data(test_data.split(',')[0],db_user_name,db_password,db_host,int(db_port))
        print ("dataframe database")
        print (df_db)
        print (test_data.split(',')[1])
        if test_data.split(',')[1] != "CTV": 
            print (test_data.split(',')[1])
            crc_64=self.calculate_crc64(test_data.split(',')[0])
            print (str(crc_64))
        else:
            if test_data.split(',')[2] == "Roku":
                store="3"
            else:
                store="999999"
                
            crc = "{0}_{1}".format(store,test_data.split(',')[0])
            
            crc_64=self.calculate_crc64(crc)
            print (crc_64)
            
        
        df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform','store_id':'Store'}, inplace=True)
        
        df_ui=self.acc7.pmccTable("dt-table")
        df_ui=df_ui.drop([''], axis=1)
        df_ui=df_ui.drop('Last Modified', axis=1)

        print ("DB DATAFRAME")
        BuiltIn().log(df_db)

        print ("UI DATAFRAME")
        BuiltIn().log(df_ui)

        self.search_in_df(df_ui, df_db)
        
        self.validate_download_all_plat_allow(test_data.split(',')[0],uri_prefix,token) 

    def validate_publisher_ui_table(self,test_data,db_user_name,db_password,db_host,db_port, activity_logs_db_user_name,activity_logs_db_password,activity_logs_db_host,activity_logs_db_port,uri_prefix,token,user):
        
        self.find_domain_publisher_allowlist(test_data.split(',')[0])
        print ("find completed")
        df_db=self.get_publisher_allowlist_db_data(test_data.split(',')[0],db_user_name,db_password,db_host,int(db_port))
        print ("dataframe database")
        print (df_db)
        print (test_data.split(',')[1])
        if test_data.split(',')[1] != "CTV": 
            print (test_data.split(',')[1])
            crc_64=self.calculate_crc64(test_data.split(',')[0])
            print (str(crc_64))
        else:
            if test_data.split(',')[2] == "Roku":
                store="3"
            else:
                store="999999"
                
            crc = "{0}_{1}".format(store,test_data.split(',')[0])
            
            crc_64=self.calculate_crc64(crc)
            print (crc_64)
            
        
        df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform','store_id':'Store'}, inplace=True)
        
        df_ui=self.acc7.pmccTable("dt-table")
        df_ui=df_ui.drop([''], axis=1)
        df_ui=df_ui.drop('Status', axis=1)
        df_ui=df_ui.drop('Error Description', axis=1)

        print ("DB DATAFRAME")
        print (df_db)

        print ("UI DATAFRAME")
        print (df_ui)

        self.search_in_df(df_ui, df_db)
        
        self.validate_download_all_pub_allow(test_data.split(',')[0],uri_prefix,token,user) 
        
    def validate_view_domain_ui_table(self,test_data,db_user_name,db_password,db_host,db_port, uri_prefix,token,user):
        
        print ("validate_view_domain_ui_table")
        self.wait_for_spinner_to_disappear(100)
        site_search="//input[@id='search']"
        self.s2l.input_text(site_search,test_data.split(',')[0])
        self.s2l.press_key(site_search,u"\\13")
        self.wait_for_spinner_to_disappear(100)
        time.sleep(5)
        view_domain_action = "(//pmcc-icon[@data-pm-id='table-action-btn'])[2]"
        self.s2l.click_element(view_domain_action)
        
        view_domains = "//li[.='View Domains']"
        self.s2l.click_element(view_domains)
        self.wait_for_spinner_to_disappear(100)
        
        #filtered_allowlist = "(//button[@class='pmcc-btn-sm pmcc-secondary'])[2]"

        self.find_domain_publisher_site_allowlist(test_data.split(',')[1])
        print ("view domain search completed")
        
        df_db=self.get_publisher_site_allowlist_db_data(test_data.split(',')[1],user,db_user_name,db_password,db_host,int(db_port))
        print ("dataframe database")
        print (df_db)
        print (test_data.split(',')[1])
        if test_data.split(',')[1] != "CTV": 
            print (test_data.split(',')[1])
            crc_64=self.calculate_crc64(test_data.split(',')[0])
            print (str(crc_64))
        else:
            if test_data.split(',')[2] == "Roku":
                store="3"
            else:
                store="999999"
                
            crc = "{0}_{1}".format(store,test_data.split(',')[0])
            
            crc_64=self.calculate_crc64(crc)
            print (crc_64)
            
        
        #df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform','store_id':'Store'}, inplace=True)
        
        df_ui=self.acc7.pmccTable("dt-table")
        df_ui=df_ui.drop([''], axis=1)
        #df_ui['CTV App Store'] = df_ui['CTV App Store'].replace('NA', 'NA')
        #df_ui=df_ui.drop(['CTV App Store'], axis=1)
        #df_ui=df_ui.drop('Status', axis=1)
        #df_ui=df_ui.drop('Error Description', axis=1)

        print ("DB DATAFRAME")
        print (df_db)

        print ("UI DATAFRAME")
        print (df_ui)

        self.search_in_df(df_ui, df_db)
        
        
        
        filtered_allowlist= "//button[text()=' Filtered Allowlist ']"
        filtered_allowlist_df=self.download_file_and_get_DF(filtered_allowlist)
        
        print ("filtered_allowlist df")
        print (filtered_allowlist_df)
        
        
        #filtered_allowlist_df=filtered_allowlist_df.drop(['Description'], axis=1)
        filtered_allowlist_df=filtered_allowlist_df.drop(['Site Identifier'], axis=1)
        filtered_allowlist_df=filtered_allowlist_df.drop(['Platform (Web/Mobile Web/Mobile App iOS/Mobile App Android/CTV)'], axis=1)
        filtered_allowlist_df['Description'] = filtered_allowlist_df['Description'].replace(np.nan, '')
        filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'] = filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'].replace(np.nan, 0)
        #filtered_allowlist_df=filtered_allowlist_df.drop(['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'], axis=1)
        
        filtered_allowlist_df = filtered_allowlist_df.rename(columns={'Domain/App Store URL/CTV App ID/App ID/Bundle ID': 'Domain Name'})
        
        print ("modified filtered_allowlist df")
        
        print (filtered_allowlist_df)
        
        self.search_in_df(filtered_allowlist_df, df_db)
        self.s2l.reload_page()
        
        go_back= "//button[text()=' Go Back ']"
        
        self.s2l.click_element(go_back)
        
        #all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
        time.sleep(5)
        self.wait_for_spinner_to_disappear(100)
        #self.validate_download_all_pub_allow(test_data.split(',')[0],uri_prefix,token,user) 

        
    def validate_download_all_plat_allow(self,search_url,uri_prefix,token):
        
        url = "https://" + uri_prefix + "/heimdall/platformAllowlist/downloadAll"
     
        headers = {
           'pubtoken': token
        }
    
        response = requests.request("GET", url, headers=headers)
    
        if (response.status_code != 200):
            raise Exception("called downloadAll with token " + str(token))
        else:
            print ("downloadAll completed..!")
                
            
        if search_url in response.text:
            print ("found")
        else:
            raise Exception ("notification is incorrect")
            
    def validate_download_all_pub_allow(self,search_url,uri_prefix,token,user):
        
        url = "https://" + uri_prefix + "/heimdall/publisherAllowlist/download?pageNumber=1&pageSize=10&pubId={1}&query=adservingEntity:{0},pubId:{1},".format(search_url,user)
     
        headers = {
           'pubtoken': token
        }
    
        response = requests.request("GET", url, headers=headers)
    
        if (response.status_code != 200):
            raise Exception("called downloadAll with token " + str(token))
        else:
            print ("downloadAll completed..!")
                
            
        if search_url in response.text:
            print ("validate_download_all_pub_allow completed : found")
        else:
            raise Exception ("notification is incorrect")
            
        
    def find_domain_platform_allowlist(self, domain_name):
        """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
        self.search_domain="//input[@data-pm-id='search-domain-input']"

        if domain_name is not None and domain_name != '':
            domain_name = unicode(domain_name)
            self.s2l.input_text(self.search_domain, domain_name)
            self.s2l.press_key(self.search_domain,u"\\13")
            self.wait_for_spinner_to_disappear(60)
        else:
            BuiltIn().log("Search Domain Function should be called in case of searching with Substring or Exact name",
                          level='WARN')
            
    def find_domain_publisher_allowlist(self, domain_name):
        """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
        self.search_domain="//input[@data-pm-id='search-domain-app-id-input']"

        if domain_name is not None and domain_name != '':
            domain_name = unicode(domain_name)
            self.s2l.input_text(self.search_domain, domain_name)
            self.s2l.press_key(self.search_domain,u"\\13")
            self.wait_for_spinner_to_disappear(60)
        else:
            BuiltIn().log("Search Domain Function should be called in case of searching with Substring or Exact name",
                          level='WARN')
            
    def find_domain_publisher_site_allowlist(self, domain_name):
        """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
        print("find_domain_publisher_site_allowlist")
        self.search_domain="//input[@id='search']"

        if domain_name is not None and domain_name != '':
            domain_name = unicode(domain_name)
            self.s2l.input_text(self.search_domain, domain_name)
            self.s2l.press_key(self.search_domain,u"\\13")
            self.wait_for_spinner_to_disappear(60)
        else:
            BuiltIn().log("Search Domain Function should be called in case of searching with Substring or Exact name",
                          level='WARN')
        
    def validate_platform_allowlist_download_all(self,search_url,uri_prefix,token,noti):
        if noti == "Domain / App ID added successfully.":
            url = "http://" + uri_prefix + "/heimdall/platformAllowlist/downloadAll"
     
            headers = {
                'pubtoken': token
            }
    
            response = requests.request("GET", url, headers=headers)
    
            if (response.status_code != 200):
                raise Exception("called downloadAll with token " + str(token))
            else:
                print ("downloadAll completed..!")
                
            print (response.text)
            
            if search_url in response.text:
                print ("found")
            else:
                BuiltIn().fail("notification is incorrect")
            
        else:
            print ("Nothing to validate in download all.")
    
    def get_platform_allowlist_db_data(self, tld_names,db_user,db_password, db_host, port):
        """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
        mydb= mysql.connector.connect(
          host=str(db_host),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(port),
          database="fraud_mgmt"
        )

        #mycursor = mydb.cursor() 

        #tld_names = ",".join([u'"' + tld_name.strip() + u'"' for tld_name in tld_names.split(',')])
        rows_query = "SELECT adserving_entity as 'Domain / App ID', platform_id as Platform, store_id as Store FROM fraud_mgmt.platform_allowlist" \
                         " WHERE adserving_entity ='{}';".format(tld_names)

        
        all_df = pd.read_sql(rows_query, mydb)
#         all_df['Last Modified'] = ["{dt:%b} {dt:%d}, {dt.year} / {dt:%H}:{dt:%M}:{dt:%S}".format(dt=datetime.strptime(
#             str(date_time), '%Y-%m-%d %H:%M:%S')) for date_time in all_df['Last Modified']]

        platform_replace_values = {1: 'WEB', 2: 'MOBILE_WEB', 4: 'MOBILE_APP_IOS', 5: 'MOBILE_APP_ANDROID', 7:'CTV'}
        store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
        all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
        all_df['Store'] = all_df['Store'].map(store_id_replace_values)
        print (all_df)
        return (all_df)
    
    def get_publisher_allowlist_db_data(self, tld_names,db_user,db_password, db_host, port):
        """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
        print ("running get_publisher_allowlist_db_data")
        mydb= mysql.connector.connect(
          host=str(db_host),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(port),
          database="fraud_mgmt"
        )

        #mycursor = mydb.cursor() 

        #tld_names = ",".join([u'"' + tld_name.strip() + u'"' for tld_name in tld_names.split(',')])
        rows_query = "SELECT adserving_entity as 'Domain / App ID', platform_id as Platform, store_id as Store FROM fraud_mgmt.publisher_allowlist" \
                         " WHERE adserving_entity ='{}';".format(tld_names)

        print (rows_query)
        all_df = pd.read_sql(rows_query, mydb)
#         all_df['Last Modified'] = ["{dt:%b} {dt:%d}, {dt.year} / {dt:%H}:{dt:%M}:{dt:%S}".format(dt=datetime.strptime(
#             str(date_time), '%Y-%m-%d %H:%M:%S')) for date_time in all_df['Last Modified']]

        platform_replace_values = {1: 'Web', 2: 'Mobile Web', 4: 'Mobile App IOS', 5: 'Mobile App Android', 7:'CTV'}
        store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
        all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
        all_df['Store'] = all_df['Store'].map(store_id_replace_values)
        print (all_df)
        return (all_df)
    
    def get_publisher_site_allowlist_db_data(self, tld_names,user,db_user,db_password, db_host, port):
        """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
        mydb= mysql.connector.connect(
          host=str(db_host),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(port),
          database="BulkOpsMgmt"
        )

        #mycursor = mydb.cursor() 

        #tld_names = ",".join([u'"' + tld_name.strip() + u'"' for tld_name in tld_names.split(',')])
        rows_query = "SELECT tld_name as 'Domain Name', status as Status, store_id as 'CTV App Store', description as Description FROM BulkOpsMgmt.staging_publisher_aggregator_site_tld" \
                         " WHERE tld_name ='{0}' and pub_id= {1};".format(tld_names,str(user))

        print (rows_query)
        all_df = pd.read_sql(rows_query, mydb)
#         all_df['Last Modified'] = ["{dt:%b} {dt:%d}, {dt.year} / {dt:%H}:{dt:%M}:{dt:%S}".format(dt=datetime.strptime(
#             str(date_time), '%Y-%m-%d %H:%M:%S')) for date_time in all_df['Last Modified']]

#         platform_replace_values = {1: 'Web', 2: 'Mobile Web', 4: 'Mobile App IOS', 5: 'Mobile App Android', 7:'CTV'}
#         store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
        
        status_replace_values = {0:'Approved'}
        store_replace_values = {0:'NA',3:'Roku',999999:'Other'}
        
#         all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
#         all_df['Store'] = all_df['Store'].map(store_id_replace_values)
        
        all_df['Status'] = all_df['Status'].map(status_replace_values)
        all_df['CTV App Store'] = all_df['CTV App Store'].map(store_replace_values)
        print (all_df)
        return (all_df)
        
    def download_file_and_get_DF(self,path):
        #fileName= uploadedFileName.split('.')[1]+".csv"
        #self.s2l.click_element(path)
        #self.wait_for_spinner_to_disappear(30)
        self.download_dir = os.path.normpath(os.path.join(current_path, "..", "..", "Downloads"))
        file_path = self.click_and_wait_for_download_to_complete(download_link_xpath=path,default_download_dir=self.download_dir)
        return pd.read_csv(file_path)
    
    def click_and_wait_for_download_to_complete(self, download_link_xpath=None, default_download_dir=None,
                                                start_wait_timeout=30, retry_interval=5, function_to_exec=None, hoverable_xpath=None,
                                                **params):

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
            BuiltIn().fail("One of the parameter is required (download_link_xpath, default_download_dir)"
                           "\nNone of the metioned parameters were passed")
        elif download_link_xpath is not None and function_to_exec is not None:
            BuiltIn().fail("Both download_link_xpath and function_to_exec passed.\nPlease pass one of the two options")

        if default_download_dir is None:
            BuiltIn().fail("Default download directory is compulsory field. Pass a valid Directory Path")
        elif not os.path.isdir(default_download_dir):
            BuiltIn().fail("default_download_dir value passed is not a valid directory")

        current_window_handle = self.s2l.driver.current_window_handle
        #print(self.s2l.driver.capabilities)

        try:
            browser_version = int(self.s2l.driver.capabilities['version'].split('.')[0])
        except (KeyError, AttributeError, IndexError):
            browser_version = int(self.s2l.driver.capabilities.get("browserVersion").split('.')[0])
        def get_all_file_in_download_manager():
            """
            :return:
            """
            new_tab_query = """window.open('')"""
            if not self.s2l.get_location().startswith("chrome://downloads"):
                self.s2l.execute_javascript(new_tab_query)
                time.sleep(2)
                # self.s2l.select_window("NEW")
                self.s2l.switch_window("NEW")
                self.s2l.go_to("chrome://downloads")
            if browser_version >= 80:
                return self.s2l.execute_javascript("""
                return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').items;
                """)
            else:
                return self.s2l.execute_javascript("""
                                return downloads.Manager.get().items_;
                                """)

        def get_download_state_by_id(id):
            """

            :param id:
            :return:
            """
            if browser_version >= 80:

                script = """return document.querySelector('downloads-manager').shadowRoot
                .querySelector('#downloadsList').items.filter(e => e.id === '{id}').map(e => e.state);""".format(
                    id=id)
            else:
                script = """return downloads.Manager.get().items_.filter(e => e.id === '{id}').map(e => e.state);"""\
                    .format(id=id)
            return self.s2l.execute_javascript(script)[0]

        def get_file_content(path):

            elem = self.s2l.driver.execute_script(
                "var input = window.document.createElement('INPUT'); "
                "input.setAttribute('type', 'file'); "
                "input.hidden = true; "
                "input.onchange = function (e) { e.stopPropagation() }; "
                "return window.document.documentElement.appendChild(input); ")

            elem._execute('sendKeysToElement', {'value': [path], 'text': path})

            result = self.s2l.driver.execute_async_script(
                "var input = arguments[0], callback = arguments[1]; "
                "var reader = new FileReader(); "
                "reader.onload = function (ev) { callback(reader.result) }; "
                "reader.onerror = function (ex) { callback(ex.message) }; "
                "reader.readAsDataURL(input.files[0]); "
                "input.remove(); ", elem)

            if not result.startswith('data:'):
                raise Exception("Failed to get file content: %s" % result)

            return base64.b64decode(result[result.find('base64,') + 7:])

        # Get all previously downloaded files
        files_before_download = get_all_file_in_download_manager()

        previous_ids = [e['id'] for e in files_before_download]
        current_time = time.time()

        self.s2l.close_window()
        # self.s2l.select_window(current_window_handle)
        self.s2l.switch_window(current_window_handle)
        if not hoverable_xpath is None:
            self.s2l.mouse_over(hoverable_xpath)
            self.s2l.wait_until_element_is_visible(download_link_xpath, 60)

        if download_link_xpath is not None:
            self.s2l.click_element(download_link_xpath)
        else:
            function_to_exec(**params)

        new_file_download_id = None

        while new_file_download_id is None and ((time.time() - current_time) < start_wait_timeout):
            files_list_after_click = get_all_file_in_download_manager()
            current_ids = [e['id'] for e in files_list_after_click]
            if len(set(current_ids).difference(previous_ids)) == 1:
                new_file_download_id = list(set(current_ids).difference(previous_ids))[0]
                print(new_file_download_id)
                break
            elif len(set(current_ids).difference(previous_ids)) > 1:
                BuiltIn().fail("Multiple Download started with IDs: '{}'".format(
                    set(current_ids).difference(previous_ids)))
            else:
                time.sleep(retry_interval)

        if new_file_download_id is None:
            BuiltIn().fail("Cannot Start Downloading After waiting for {} seconds".format(start_wait_timeout))
        else:
            time.sleep(retry_interval)
            download_state = get_download_state_by_id(new_file_download_id)
            while download_state == "IN_PROGRESS":
                time.sleep(retry_interval)
                download_state = get_download_state_by_id(new_file_download_id)
                print("Download state: {}".format(download_state))
            if download_state == "COMPLETE":
                all_files = get_all_file_in_download_manager()
                file_path = [f['file_path'] if 'file_path' in f.keys()
                             else f['filePath'] for f in filter(lambda e: e['id'] == new_file_download_id, all_files)][0]
                file_content = get_file_content(file_path)

                # Writing file to desired location
                new_file_location = os.path.normpath(os.path.join(default_download_dir, os.path.basename(file_path)))
                print ("Copying File to: {}".format(new_file_location))

                with open(new_file_location, 'wb') as fp:
                    fp.write(file_content)
            else:
                BuiltIn().fail("File download is not in progress and neither completed. Current State: {}".format(
                    download_state))

        self.s2l.close_window()
        # self.s2l.select_window(current_window_handle)
        self.s2l.switch_window(current_window_handle)
        return new_file_location

    def delete_BulkOps(self,fileName,db_host,db_user_name, db_password,db_port):
        self.DB.delete_BulkOps_db_data(fileName,db_host, db_user_name, db_password, int(db_port))
        
    def update_oo(self,db_host,db_user_name, db_password,db_port,user,value):
        self.DB.update_oo(db_host, db_user_name, db_password, int(db_port),user,value)

    def update_pub_blocklist(self,db_host,db_user_name, db_password,db_port,user,value):
        self.DB.update_pub_blocklist(db_host, db_user_name, db_password, int(db_port),user,value)
        
    def validate_admin_pub_upload(self,data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,oo=-1):
        self.DB.validate_admin_pub_upload(data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,oo)
        self.DB.validate_storeName_in_store_urls(data,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password)
    
    def validate_admin_pub_upload_deleted(self,data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,oo=-1):
        self.DB.validate_admin_pub_upload_deleted(data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,oo)
    
        
    def validate_admin_pub_site_upload(self,data,Bulk_db,Komli_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user,oo=-1):
        self.DB.validate_admin_pub_site_upload(data, Bulk_db,Komli_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user,oo)
        
    def validate_updated_crc_888888(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user):
        self.DB.validate_updated_crc_888888(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user)
    
    
    def update_crc_to_0_pub_site(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user):
        self.DB.update_crc_to_0_pub_site(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user)
    
    def update_store_id_0_pub_site(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user):
        self.DB.update_store_id_0_pub_site(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user)
    
    
    def update_status_to_6_pub_site(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user):
        self.DB.update_status_to_6_pub_site(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user)
    
    def update_updatetime_pub_site(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user,updatetime):
        self.DB.update_updatetime_pub_site(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user,updatetime)
    
    def update_updatetime_all_pub_site(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user,updatetime):
        self.DB.update_updatetime_all_pub_site(data,db_host, Bulk_db,Komli_db,int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user,updatetime)
    
    
    def update_status_to_6_pub(self,data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port):
        self.DB.update_status_to_6_pub(data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port)
    
    def update_updatetime_pub(self,data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,updatetime):
        self.DB.update_updatetime_pub(data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,updatetime)
    
    def update_updatetime_all_pub(self,data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,updatetime):
        self.DB.update_updatetime_all_pub(data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,updatetime)
    
    
    def validate_admin_pub_site_upload_deleted(self,data,Bulk_db,Komli_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user):
        self.DB.validate_admin_pub_site_upload_deleted(data,Bulk_db,Komli_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user)
    
    
    def validate_pub_upload(self,data,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port):
        self.DB.validate_pub_upload(data,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port)
    
    def validate_plat_upload(self,data,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,version=1):
        self.DB.validate_plat_upload(data,fraud_db_host, int(fraud_db_port),fraud_db_user_name, fraud_db_password,crawl_db_host, int(crawl_db_port),crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,version)
    
    def update_crawler_v_to_2(self,data,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port):
        self.DB.update_crawler_v_to_2(data,fraud_db_host, int(fraud_db_port),fraud_db_user_name, fraud_db_password,crawl_db_host, int(crawl_db_port),crawl_db_user_name, crawl_db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port)
    
    
    def validate_gssb(self,data,db_host,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port):
        self.DB.validate_gssb(data,db_host, int(db_port),db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port)
    
    
    def validate_pub_pub_site_upload(self,data,Bulk_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,Komli_db,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user):
        self.DB.validate_pub_pub_site_upload(data, Bulk_db,fraud_db_host,fraud_db_port,fraud_db_user_name, fraud_db_password,crawl_db_host,crawl_db_port,crawl_db_user_name, crawl_db_password,Komli_db,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,common_db_user_name,common_db_password,common_db_port,user)
        
    def validate_bulk_upload_table(self,fileName,db_host,db_user_name, db_password,db_port):
        df_db = self.DB.get_BulkOps_db_data(fileName,db_host, db_user_name, db_password, int(db_port))
        #print (df_db)
        #df_ui = self.acc7.pmccTable("sortable-table")
        df_ui = self.acc7.pmccTable("//table[@class='pmcc-table pmcc-fixed-header']",None,None,True)
        #print (df_ui)
        df_ui = df_ui.drop(['User'], axis=1)
        #print (df_ui.keys())
        df_ui = df_ui.drop([''], axis=1)
        df_ui = df_ui.drop(['Upload Date'], axis=1)
        #print (df_ui)
        BuiltIn().log("DB DATAFRAME")
        

        BuiltIn().log("UI DATAFRAME")
        BuiltIn().log(df_ui)
        self.search_in_df_bulk(df_ui, df_db)
        print ("validate_bulk_upload_table completed")
        
    def validate_plat_upload_bulk_upload_table(self,fileName,db_host,db_user_name, db_password,db_port):
        df_db = self.DB.get_BulkOps_db_data(fileName,db_host, db_user_name, db_password, int(db_port))
        #print (df_db)
        #df_ui = self.acc7.pmccTable("sortable-table")
        df_ui = self.acc7.pmccTable("//iq-bulk-upload-allowlist-domain//table",None,None,True)
        #print (df_ui)
        df_ui = df_ui.drop(['User'], axis=1)
        #print (df_ui.keys())
        df_ui = df_ui.drop([''], axis=1)
        df_ui = df_ui.drop(['Upload Date'], axis=1)
        #print (df_ui)
        BuiltIn().log("DB DATAFRAME")
        

        BuiltIn().log("UI DATAFRAME")
        BuiltIn().log(df_ui)
        self.search_in_df_bulk(df_ui, df_db)
        
    def validate_pub_upload_bulk_upload_table(self,fileName,db_host,db_user_name, db_password,db_port):
        df_db = self.DB.get_BulkOps_db_data(fileName,db_host, db_user_name, db_password, int(db_port))
        #print (df_db)
        #df_ui = self.acc7.pmccTable("sortable-table")
        df_ui = self.acc7.pmccTable_pub("//pmcc-scrollable-table//table[@class='pmcc-table']","//pmcc-scrollable-table//div[@class='header-container has-scroll']//table//thead//th",None,None,True)
        #print (df_ui)
        df_ui = df_ui.drop(['User'], axis=1)
        #print (df_ui.keys())
        df_ui = df_ui.drop([''], axis=1)
        df_ui = df_ui.drop(['Upload Date'], axis=1)
        #print (df_ui)
        BuiltIn().log("DB DATAFRAME")
        

        BuiltIn().log("UI DATAFRAME")
        BuiltIn().log(df_ui)
        self.search_in_df_bulk(df_ui, df_db)
        
    def validate_pub_site_upload_bulk_upload_table(self,fileName,db_host,db_user_name, db_password,db_port):
        df_db = self.DB.get_BulkOps_db_data(fileName,db_host, db_user_name, db_password, int(db_port))
        #print (df_db)
        #df_ui = self.acc7.pmccTable("sortable-table")
        df_ui = self.acc7.pmccTable_pub("//pmcc-scrollable-table//table[@class='pmcc-table']","//pmcc-scrollable-table//div[@class='header-container has-scroll']//table//thead//th",None,None,True)
        #print (df_ui)
        df_ui = df_ui.drop(['User'], axis=1)
        #print (df_ui.keys())
        df_ui = df_ui.drop([''], axis=1)
        df_ui = df_ui.drop(['Upload Date'], axis=1)
        #print (df_ui)
        BuiltIn().log("DB DATAFRAME")
        

        BuiltIn().log("UI DATAFRAME")
        BuiltIn().log(df_ui)
        self.search_in_df_bulk(df_ui, df_db)
        
    def search_in_df_bulk(self,actual_df,expected_df):
        cols= list(actual_df.columns)
        rowsCount=expected_df.count()[0]

        actual_df_values = actual_df.values
        expected_df_values=expected_df.values

        actual_df_values=actual_df_values.astype('unicode')
        expected_df_values = expected_df_values.astype('unicode')

        actual_df = pd.DataFrame(data=actual_df_values,columns=actual_df.columns)
        expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
        
        #print ("search_in_df")
        #print (actual_df)
        #print (expected_df)
        #print (actual_df==expected_df)

        new_df = pd.merge(actual_df, expected_df, on=cols, how='left', indicator='Exist')
        new_df['Exist'] = np.where(new_df.Exist == 'both', True, False)
        print("Merged DF")
        print(new_df)

        resultList = list(new_df['Exist'])
        print (resultList)
        flag = False
        for result in resultList:
            if result:
                print ("Expected data found ")
                flag=True
                
            else:
                print("Expected data Not found ")
                
        if flag:
            print ("all records matched")
        else:
            raise Exception ("all records didnt match")

    def search_in_df(self,actual_df,expected_df):
        cols= list(actual_df.columns)
        rowsCount=expected_df.count()[0]

        actual_df_values = actual_df.values
        expected_df_values=expected_df.values

        actual_df_values=actual_df_values.astype('unicode')
        expected_df_values = expected_df_values.astype('unicode')

        actual_df = pd.DataFrame(data=actual_df_values,columns=actual_df.columns)
        expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
        
        #print ("search_in_df")
        #print (actual_df)
        #print (expected_df)
        #print (actual_df==expected_df)

        new_df = pd.merge(actual_df, expected_df, on=cols, how='left', indicator='Exist')
        new_df['Exist'] = np.where(new_df.Exist == 'both', True, False)
        print("Merged DF")
        print(new_df)

        resultList = list(new_df['Exist'])
        print (resultList)
        flag = True
        for result in resultList:
            if result:
                print ("Expected data found ")
                
            else:
                print("Expected data Not found ")
                flag=False
        if not flag:
            print ("all records didnt match")
        else:
            print ("all records matched")
        
    def search_in_df_single(self,actual_df,expected_df):
        cols= list(actual_df.columns)
        rowsCount=expected_df.count()[0]

        actual_df_values = actual_df.values
        expected_df_values=expected_df.values

        actual_df_values=actual_df_values.astype('unicode')
        expected_df_values = expected_df_values.astype('unicode')

        actual_df = pd.DataFrame(data=actual_df_values,columns=actual_df.columns)
        expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
        
        print ("search_in_df")
        print (actual_df)
        print (expected_df)
        print (actual_df==expected_df)
        found= (actual_df==expected_df)
        print ("found : " + str(found))
        print (type(found))
        if found:
            print ("Expected data found ")
        else:
            raise Exception ("Expected data Not found ")

   
    def wait_for_spinner_to_disappear(self, timeout=60):
        """
        Waits for the spinner to disappear
        :return: None
        """
        defaultTimeout = self.s2l.set_selenium_implicit_wait(1)
        spinner_available = BuiltIn().run_keyword_and_return_status("element_should_be_visible", '//pmcc-spinner')
        start_time = time.time()
        while spinner_available and start_time + timeout > time.time():
            spinner_available = BuiltIn().run_keyword_and_return_status("element_should_be_visible", '//pmcc-spinner')
        # BuiltIn().wait_until_keyword_succeeds('{} sec'.format(timeout), '2 sec', 'page_should_not_contain_element',
        #                                       '//pmcc-spinner')
        if spinner_available:
            BuiltIn().fail("pmcc-spinner didn't disappear in {} sec".format(timeout))
        self.s2l.set_selenium_implicit_wait(defaultTimeout)
   
    def populate_data(self, test_data,db_server,db_port,db_user,db_password,komli_db_host,common_db_port, common_db_user_name, common_db_password): 
        publisher_allowlist_records=test_data["populate_publisher_allowlist_records"]
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(db_port),
          database="fraud_mgmt"
        )

        mycursor = mydb.cursor() 
        start=time.time()
        delete_sql = " delete from  fraud_mgmt.publisher_allowlist where adserving_entity in ("
        insert_sql= " insert ignore into fraud_mgmt.publisher_allowlist(pub_id,adserving_entity,platform_id,store_id,application_profile_id,crc_64)values"
        publisher_allowlist_records=test_data["populate_publisher_allowlist_records"]
        if (str(publisher_allowlist_records).lower().strip()!="none"): 
            records=publisher_allowlist_records.split("\n")
            for record in records:   
                data=record.split(",")
                tld_name=data[1]                
                tld_name_tmp=str(tld_name).replace("'", "")
                crc_64=self.calculate_crc64(tld_name_tmp) 
 
                delete_sql =delete_sql+ str(tld_name)+ "," 
                 
                insert_sql =insert_sql+  "("+str(record)+",-1,'"+str(crc_64)+"'),"
  
                  
        delete_sql=delete_sql[:-1]
        delete_sql=delete_sql+");"
        print(delete_sql)
        mycursor.execute(delete_sql)
        mydb.commit()
         
        insert_sql=insert_sql[:-1]
        print(insert_sql)
        mycursor.execute(insert_sql)
        mydb.commit()
        end=time.time()
        print ("Time taken= "+str(end-start))
              
     
     
        mydb= mysql.connector.connect(
          host=str(komli_db_host),
          user=str(common_db_user_name), 
          passwd=str(common_db_password),
          port=str(common_db_port),
          database="KomliAdServer"
        )

        mycursor = mydb.cursor() 
        publisher_allowlist_records=test_data["populate_publisher_site_tld_records"]   
        delete_sql="delete from  KomliAdServer.publisher_aggregator_site_tld where pub_id=301 and tld_name in ("   
        insert_sql="insert ignore into KomliAdServer.publisher_aggregator_site_tld (pub_id,site_id,tld_name,adserving_entity,platform_id,deleted,crc_32,application_profile_id)values"
        if (str(publisher_allowlist_records).lower().strip()!="none"):
            records=publisher_allowlist_records.split("\n") 
            for record in records:
                data=record.split(",")
                crc_32=data[2] 
                delete_sql=delete_sql+str(crc_32)+","
 
                
                insert_sql=insert_sql+"("+str(record)+",CRC32("+str(crc_32)+"),-1),"
 
        
        delete_sql=delete_sql[:-1]
        delete_sql=delete_sql+");"
        print(delete_sql)  
        mycursor.execute(delete_sql)
        mydb.commit()    
#         
        insert_sql=insert_sql[:-1]
        print(insert_sql)
        mycursor.execute(insert_sql)
        mydb.commit()   
         
        
    def clean_up_allowlist_upload(self, test_data,db_server,db_port,db_user,db_password): 
        print("insite clean_up_allowlist_upload...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(db_port),
          database="fraud_mgmt"
        )

        mycursor = mydb.cursor() 
        records=publisher_allowlist_records.split("#")
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            
            sql = "delete from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;"
            print (sql)
            mycursor.execute(sql)
             
            mydb.commit()
            
    def clean_up_allowlist_upload_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password,komli_db_host,common_db_user_name,common_db_password,common_db_port): 
        #print("insite clean_up_allowlist_upload...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        #print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        print (q)
        self.execute_sql_db_multi(q, komli_db_host,  common_db_user_name,common_db_password,common_db_port, "KomliAdServer")
 
        records=publisher_allowlist_records.split("\n")
        print("records are: ", records)
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity).lower()+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;")
            else:
                sql_texts.append( "delete from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from fraud_mgmt.staging_publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity).lower()+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;")
            else:
                sql_texts.append( "delete from fraud_mgmt.staging_publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='"+str(adserving_entity).lower()+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+";")
            else:
                sql_texts.append( "delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+";")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from ads_txt_crawler.ads_txt_domains where tld_name='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from ads_txt_crawler.store_urls where app_bundle_id='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, crawl_db_server,  crawl_db_user, crawl_db_password,crawl_db_port, "ads_txt_crawler")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, hawk_db_server,  hawk_db_user, hawk_db_password,hawk_db_port, "HawkEye")
        
        
    def clean_up_pub_allowlist_upload_new(self, test_data, fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,user): 
        print("insite clean_up_allowlist_upload...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
        platf = {"Web":"1", 
                    "Mobile Web": "2",
                    "Mobile App Android": "5",
                    "Mobile App iOS": "4",
                    "CTV": "7"}
        
        storef = {"Roku" : "3",
                 "Other" : "999999",
                 "":"0"
            }
 
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            
            
            sql_texts.append( "delete from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platf[platform_id])+" and store_id="+str(storef[store_id])+" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            
            sql_texts.append( "delete from fraud_mgmt.staging_publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platf[platform_id])+" and store_id="+str(storef[store_id])+" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            
            sql_texts.append( "delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='"+str(adserving_entity)+"' and platform_id= "+str(platf[platform_id])+" ;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from ads_txt_crawler.ads_txt_domains where tld_name='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from ads_txt_crawler.store_urls where app_bundle_id='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, crawl_db_server,  crawl_db_user, crawl_db_password,crawl_db_port, "ads_txt_crawler")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, hawkeye_db_server,  hawkeye_db_user, hawkeye_db_password,hawkeye_db_port, "HawkEye")
        
        
    def clean_up_pub_pub_site_allowlist_upload_new(self, test_data,Komli_db_server,BulkOps_db_server,common_db_port,common_db_user_name,common_db_password,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,user): 
        print("insite clean_up_allowlist_upload...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        #print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
 
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            site_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            if store_id=='':
                store_id=0
            
            sql_texts.append( "delete from KomliAdServer.publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, Komli_db_server,  common_db_user_name, common_db_password,common_db_port, "KomliAdServer")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            site_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            if store_id=='':
                store_id=0
            
            sql_texts.append( "delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, BulkOps_db_server,  common_db_user_name, common_db_password,common_db_port, "BulkOpsMgmt")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=user
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            
            sql_texts.append( "delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" ;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        #print (db_server,  db_user, db_password,db_port)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from ads_txt_crawler.ads_txt_domains where tld_name='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from ads_txt_crawler.store_urls where app_bundle_id='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, crawl_db_server,  crawl_db_user, crawl_db_password,crawl_db_port, "ads_txt_crawler")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, hawkeye_db_server,  hawkeye_db_user, hawkeye_db_password,hawkeye_db_port, "HawkEye")
        
        
    def clean_up_pub_site_allowlist_upload_new(self, test_data,Komli_db_server,BulkOps_db_server,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,common_db_port,common_db_user_name,common_db_password,hawk_db_server,hawk_db_port,hawk_db_user,hawk_db_password): 
        print("insite clean_up_allowlist_upload...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        #print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
 
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            adserving_entity= data[2]  
            platform_id=data[3]
            store_id=data[4]
            
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from KomliAdServer.publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity).lower()+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
            else:
                sql_texts.append( "delete from KomliAdServer.publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, Komli_db_server,  common_db_user_name,common_db_password,common_db_port, "KomliAdServer")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            adserving_entity= data[2]  
            platform_id=data[3]
            store_id=data[4]
            
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity)+"';")
            else:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, Komli_db_server,  common_db_user_name,common_db_password,common_db_port, "KomliAdServer")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            adserving_entity= data[2]  
            platform_id=data[3]
            store_id=data[4]
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity).lower()+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
            else:
                sql_texts.append( "delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id=" + str(site_id) + " and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id) +" and application_profile_id=-1;")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, BulkOps_db_server,  common_db_user_name,common_db_password,common_db_port, "BulkOpsMgmt")
        
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            adserving_entity= data[2]  
            platform_id=data[3]
            store_id=data[4]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from ads_txt_crawler.ads_txt_domains where tld_name='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from ads_txt_crawler.store_urls where app_bundle_id='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, crawl_db_server,  crawl_db_user, crawl_db_password,crawl_db_port, "ads_txt_crawler")
        
        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            adserving_entity= data[2]  
            platform_id=data[3]
            store_id=data[4]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, hawk_db_server,  hawk_db_user, hawk_db_password,hawk_db_port, "HawkEye")
        
    def clean_up_plat_allowlist_upload_new(self, test_data,fraud_db_server,fraud_db_port,fraud_db_user,fraud_db_password,crawl_db_server,crawl_db_port,crawl_db_user,crawl_db_password,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password): 
        print("insite clean_up_allowlist_upload...!")
        plat_allowlist_records=test_data["platform_allowlist_records"]
        #print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(plat_allowlist_records).lower().strip()=="none"):
            return
        
        platf = {"Web":"1", 
                    "Mobile Web": "2",
                    "Mobile App Android": "5",
                    "Mobile App iOS": "4",
                    "CTV": "7"}
        
        storef = {"Roku" : "3",                  
                  'tvOS':4,'Fire TV':5, 'LG TV':6,'Vizio':7,'Samsung':8,
                  "Other" : "999999",
                  "":"0"
            }
        #print (db_server,db_port,db_user,db_password)
        
        records=plat_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            
            sql_texts.append( "delete from fraud_mgmt.platform_allowlist where adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platf[platform_id])+" and store_id="+str(storef[store_id])+";")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, fraud_db_server,  fraud_db_user, fraud_db_password,fraud_db_port, "fraud_mgmt")
        
        
        records=plat_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["Web","Mobile Web"]:
                sql_texts.append( "delete from ads_txt_crawler.ads_txt_domains where tld_name='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from ads_txt_crawler.store_urls where app_bundle_id='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, crawl_db_server,  crawl_db_user, crawl_db_password,crawl_db_port, "ads_txt_crawler")
        
        records=plat_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            adserving_entity= data[0]  
            platform_id=data[1]
            store_id=data[2]
            #print ("clean_up_allowlist_upload_new")
            #print (pub_id,adserving_entity,platform_id,store_id)
            if store_id=='':
                store_id=0
            if platform_id in ["Web","Mobile Web"]:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity).lower()+"';")
            else:
                sql_texts.append( "delete from HawkEye.category_fetch_ad_container where ad_container='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, hawkeye_db_server,  hawkeye_db_user, hawkeye_db_password,hawkeye_db_port, "HawkEye")
        

        
    def clean_up_gssb(self, test_data,Komli_db_server,db_port,db_user,db_password): 
        print("insite clean_up_gssb...!")
        publisher_allowlist_records=test_data["publisher_allowlist_records"]
        #print("got this data for cleanup"+str(publisher_allowlist_records))
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return

        records=publisher_allowlist_records.split("\n")
        sql_texts=[]
        for record in records: 
            data=record.split(",")
            adserving_entity= data[0]  
            platform_id=data[1]
            if platform_id in ["1","2"]:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity)+"';")
            else:
                sql_texts.append( "delete from KomliAdServer.global_supply_side_blocklist where domain='"+str(adserving_entity)+"';")
        
        q = ('\n'.join(sql_texts))
        
        print (q)
        self.execute_sql_db_multi(q, Komli_db_server,  db_user, db_password,db_port, "KomliAdServer")
        
        
        
        
 
    def validate_allowlist_upload(self, test_data,test_case,db_server,db_port,db_user,db_password,komli_db_host,activity_db_host,common_db_user_name,common_db_password,common_db_port ): 
       # print("got this as test_data "+ str(test_data))
        print("got this as test_case "+ str(test_case)) 
        publisher_allowlist_records=self.get_data_frame_value(test_data, test_case, "publisher_allowlist_records")
        
        print ("publisher_allowlist_records= "+str(publisher_allowlist_records))
        
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(db_port),
          database="fraud_mgmt"
        )

        mycursor = mydb.cursor() 
        records=publisher_allowlist_records.split("\n")
        for record in records: 
            data=record.split(",")
            pub_id=data[0]
            adserving_entity= data[1]  
            platform_id=data[2]
            store_id=data[3]
            is_deleted=str(data[4]).strip()
            
            sql = "select pub_id from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and store_id="+str(store_id)+" and application_profile_id=-1;"
            print (sql)
            mycursor.execute(sql)
            result=mycursor.fetchall()
            print (result)
            db_result=""
            if len(result)!=0:
                db_result=result[0][0]
            mydb.commit()
            if str(db_result)==str(pub_id):
                print ("publisher_allowlist validation done!")
                self.validate_publisher_aggregater(test_data,test_case, komli_db_host, common_db_port, common_db_user_name, common_db_password)
            else:
                if (str(is_deleted)=="1"):
                    print("publisher_allowlist delete validation done!")
                    self.validate_publisher_aggregater(test_data,test_case,komli_db_host, common_db_port, common_db_user_name, common_db_password)
                else:
                    raise Exception("publisher_allowlist validation failed")
            
    def validate_allowlist_stats(self, test_data,db_server,db_port,db_user,db_password): 
        return
       # print("got this as test_data "+ str(test_data))
        print("got this as test_case stats "+ str(test_case)) 
        publisher_allowlist_records=self.get_data_frame_value(test_data, test_case, "publisher_allowlist_stats")
        
        print ("publisher_allowlist_stats= "+str(publisher_allowlist_records))
        
        if (str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(db_port),
          database="fraud_mgmt"
        )

        mycursor = mydb.cursor() 
        records=publisher_allowlist_records.split("\n")
        for record in records: 
            data=record.split("#")
            allowlist_type=data[0]
            total_records= data[1]  
            processed_records=data[2]
            failed_records=data[3]
            failed_stats=data[4]
            history_lookups=data[5]
            
            sql = "select pub_id from fraud_mgmt.publisher_allowlist where pub_id="+str(pub_id)+" and allowlist_type='"+str(allowlist_type)+"' and total_records= "+str(total_records)+" and processed_records="+str(processed_records)+" and failed_records="+str(failed_records)+" and history_lookups="+str(history_lookups)+";"
            print (sql)
            mycursor.execute(sql)
            result=mycursor.fetchall()
            print (result)
            db_result=""
            if len(result)!=0:
                db_result=result[0][0]
            mydb.commit()
            if str(db_result)==str(pub_id):
                print ("publisher_allowlist stats validation done!")
               
            else:  
                raise Exception("publisher_allowlist stats validation failed")
            

    def validate_publisher_aggregater(self, test_data,test_case,db_server,db_port,db_user,db_password): 
        
         #publisher_allowlist_records=test_data["publisher_site_tld_records"]
         publisher_allowlist_records=self.get_data_frame_value(test_data, test_case, "publisher_site_tld_records")
         if(str(publisher_allowlist_records).lower().strip()=="none"):
            return
        
         mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user), 
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )

         mycursor = mydb.cursor() 
         records=publisher_allowlist_records.split("\n")
        
         for record in records: 
            data=record.split(",")
            pub_id=data[0]
            site_id=data[1]
            tld_name= data[2]
            adserving_entity=data[3]
            platform_id=data[4]
            deleted=data[5]
            
            sql = "select pub_id from KomliAdServer.publisher_aggregator_site_tld where pub_id="+str(pub_id)+" and site_id= "+str(site_id)+" and adserving_entity='"+str(adserving_entity)+"' and platform_id= "+str(platform_id)+" and tld_name='"+str(tld_name)+"' and deleted="+str(deleted)+" and application_profile_id=-1;"
            print (sql)
            mycursor.execute(sql)
            result=mycursor.fetchall()
            print (result)
            db_result=result[0][0]
            mydb.commit()
            if str(db_result)==str(pub_id):
                print ("validate_publisher_aggregater validation done!")
            else: 
                raise Exception("validate_publisher_aggregater validation failed")
            
    def calculate_crc64(self,string):

        crc64_tab = [0x0000000000000000, 0x7ad870c830358979, 0xf5b0e190606b12f2, 0x8f689158505e9b8b, 0xc038e5739841b68f, 0xbae095bba8743ff6, 0x358804e3f82aa47d, 0x4f50742bc81f2d04, 0xab28ecb46814fe75, 0xd1f09c7c5821770c, 0x5e980d24087fec87, 0x24407dec384a65fe, 0x6b1009c7f05548fa, 0x11c8790fc060c183, 0x9ea0e857903e5a08, 0xe478989fa00bd371, 0x7d08ff3b88be6f81, 0x07d08ff3b88be6f8, 0x88b81eabe8d57d73, 0xf2606e63d8e0f40a, 0xbd301a4810ffd90e, 0xc7e86a8020ca5077, 0x4880fbd87094cbfc, 0x32588b1040a14285, 0xd620138fe0aa91f4, 0xacf86347d09f188d, 0x2390f21f80c18306, 0x594882d7b0f40a7f, 0x1618f6fc78eb277b, 0x6cc0863448deae02, 0xe3a8176c18803589, 0x997067a428b5bcf0, 0xfa11fe77117cdf02, 0x80c98ebf2149567b, 0x0fa11fe77117cdf0, 0x75796f2f41224489, 0x3a291b04893d698d, 0x40f16bccb908e0f4, 0xcf99fa94e9567b7f, 0xb5418a5cd963f206, 0x513912c379682177, 0x2be1620b495da80e, 0xa489f35319033385, 0xde51839b2936bafc, 0x9101f7b0e12997f8, 0xebd98778d11c1e81, 0x64b116208142850a, 0x1e6966e8b1770c73, 0x8719014c99c2b083, 0xfdc17184a9f739fa, 0x72a9e0dcf9a9a271, 0x08719014c99c2b08, 0x4721e43f0183060c, 0x3df994f731b68f75, 0xb29105af61e814fe, 0xc849756751dd9d87, 0x2c31edf8f1d64ef6, 0x56e99d30c1e3c78f, 0xd9810c6891bd5c04, 0xa3597ca0a188d57d, 0xec09088b6997f879, 0x96d1784359a27100, 0x19b9e91b09fcea8b, 0x636199d339c963f2, 0xdf7adabd7a6e2d6f, 0xa5a2aa754a5ba416, 0x2aca3b2d1a053f9d, 0x50124be52a30b6e4, 0x1f423fcee22f9be0, 0x659a4f06d21a1299, 0xeaf2de5e82448912, 0x902aae96b271006b, 0x74523609127ad31a, 0x0e8a46c1224f5a63, 0x81e2d7997211c1e8, 0xfb3aa75142244891, 0xb46ad37a8a3b6595, 0xceb2a3b2ba0eecec, 0x41da32eaea507767, 0x3b024222da65fe1e, 0xa2722586f2d042ee, 0xd8aa554ec2e5cb97, 0x57c2c41692bb501c, 0x2d1ab4dea28ed965, 0x624ac0f56a91f461, 0x1892b03d5aa47d18, 0x97fa21650afae693, 0xed2251ad3acf6fea, 0x095ac9329ac4bc9b, 0x7382b9faaaf135e2, 0xfcea28a2faafae69, 0x8632586aca9a2710, 0xc9622c4102850a14, 0xb3ba5c8932b0836d, 0x3cd2cdd162ee18e6, 0x460abd1952db919f, 0x256b24ca6b12f26d, 0x5fb354025b277b14, 0xd0dbc55a0b79e09f, 0xaa03b5923b4c69e6, 0xe553c1b9f35344e2, 0x9f8bb171c366cd9b, 0x10e3202993385610, 0x6a3b50e1a30ddf69, 0x8e43c87e03060c18, 0xf49bb8b633338561, 0x7bf329ee636d1eea, 0x012b592653589793, 0x4e7b2d0d9b47ba97, 0x34a35dc5ab7233ee, 0xbbcbcc9dfb2ca865, 0xc113bc55cb19211c, 0x5863dbf1e3ac9dec, 0x22bbab39d3991495, 0xadd33a6183c78f1e, 0xd70b4aa9b3f20667, 0x985b3e827bed2b63, 0xe2834e4a4bd8a21a, 0x6debdf121b863991, 0x1733afda2bb3b0e8, 0xf34b37458bb86399, 0x8993478dbb8deae0, 0x06fbd6d5ebd3716b, 0x7c23a61ddbe6f812, 0x3373d23613f9d516, 0x49aba2fe23cc5c6f, 0xc6c333a67392c7e4, 0xbc1b436e43a74e9d, 0x95ac9329ac4bc9b5, 0xef74e3e19c7e40cc, 0x601c72b9cc20db47, 0x1ac40271fc15523e, 0x5594765a340a7f3a, 0x2f4c0692043ff643, 0xa02497ca54616dc8, 0xdafce7026454e4b1, 0x3e847f9dc45f37c0, 0x445c0f55f46abeb9, 0xcb349e0da4342532, 0xb1eceec59401ac4b, 0xfebc9aee5c1e814f, 0x8464ea266c2b0836, 0x0b0c7b7e3c7593bd, 0x71d40bb60c401ac4, 0xe8a46c1224f5a634, 0x927c1cda14c02f4d, 0x1d148d82449eb4c6, 0x67ccfd4a74ab3dbf, 0x289c8961bcb410bb, 0x5244f9a98c8199c2, 0xdd2c68f1dcdf0249, 0xa7f41839ecea8b30, 0x438c80a64ce15841, 0x3954f06e7cd4d138, 0xb63c61362c8a4ab3, 0xcce411fe1cbfc3ca, 0x83b465d5d4a0eece, 0xf96c151de49567b7, 0x76048445b4cbfc3c, 0x0cdcf48d84fe7545, 0x6fbd6d5ebd3716b7, 0x15651d968d029fce, 0x9a0d8ccedd5c0445, 0xe0d5fc06ed698d3c, 0xaf85882d2576a038, 0xd55df8e515432941, 0x5a3569bd451db2ca, 0x20ed197575283bb3, 0xc49581ead523e8c2, 0xbe4df122e51661bb, 0x3125607ab548fa30, 0x4bfd10b2857d7349, 0x04ad64994d625e4d, 0x7e7514517d57d734, 0xf11d85092d094cbf, 0x8bc5f5c11d3cc5c6, 0x12b5926535897936, 0x686de2ad05bcf04f, 0xe70573f555e26bc4, 0x9ddd033d65d7e2bd, 0xd28d7716adc8cfb9, 0xa85507de9dfd46c0, 0x273d9686cda3dd4b, 0x5de5e64efd965432, 0xb99d7ed15d9d8743, 0xc3450e196da80e3a, 0x4c2d9f413df695b1, 0x36f5ef890dc31cc8, 0x79a59ba2c5dc31cc, 0x037deb6af5e9b8b5, 0x8c157a32a5b7233e, 0xf6cd0afa9582aa47, 0x4ad64994d625e4da, 0x300e395ce6106da3, 0xbf66a804b64ef628, 0xc5bed8cc867b7f51, 0x8aeeace74e645255, 0xf036dc2f7e51db2c, 0x7f5e4d772e0f40a7, 0x05863dbf1e3ac9de, 0xe1fea520be311aaf, 0x9b26d5e88e0493d6, 0x144e44b0de5a085d, 0x6e963478ee6f8124, 0x21c640532670ac20, 0x5b1e309b16452559, 0xd476a1c3461bbed2, 0xaeaed10b762e37ab, 0x37deb6af5e9b8b5b, 0x4d06c6676eae0222, 0xc26e573f3ef099a9, 0xb8b627f70ec510d0, 0xf7e653dcc6da3dd4, 0x8d3e2314f6efb4ad, 0x0256b24ca6b12f26, 0x788ec2849684a65f, 0x9cf65a1b368f752e, 0xe62e2ad306bafc57, 0x6946bb8b56e467dc, 0x139ecb4366d1eea5, 0x5ccebf68aecec3a1, 0x2616cfa09efb4ad8, 0xa97e5ef8cea5d153, 0xd3a62e30fe90582a, 0xb0c7b7e3c7593bd8, 0xca1fc72bf76cb2a1, 0x45775673a732292a, 0x3faf26bb9707a053, 0x70ff52905f188d57, 0x0a2722586f2d042e, 0x854fb3003f739fa5, 0xff97c3c80f4616dc, 0x1bef5b57af4dc5ad, 0x61372b9f9f784cd4, 0xee5fbac7cf26d75f, 0x9487ca0fff135e26, 0xdbd7be24370c7322, 0xa10fceec0739fa5b, 0x2e675fb4576761d0, 0x54bf2f7c6752e8a9, 0xcdcf48d84fe75459, 0xb71738107fd2dd20, 0x387fa9482f8c46ab, 0x42a7d9801fb9cfd2, 0x0df7adabd7a6e2d6, 0x772fdd63e7936baf, 0xf8474c3bb7cdf024, 0x829f3cf387f8795d, 0x66e7a46c27f3aa2c, 0x1c3fd4a417c62355, 0x935745fc4798b8de, 0xe98f353477ad31a7, 0xa6df411fbfb21ca3, 0xdc0731d78f8795da, 0x536fa08fdfd90e51, 0x29b7d047efec8728]
    
        string = str(string)
        crc = 0
        for i in range(0, len(string)):
            crc = crc64_tab[(crc%256) ^ ord(string[i])] ^ (crc >> 8)
        print(("CRC generated for string : '%s' is : %d" %(string,crc)))
        return crc    
    
    def global_channel_partner_blocklist_filter(self ,test_data,db_server,db_port,db_user,db_password):
        request_line=test_data["gcpb_filter"]
        if (str(request_line).lower().strip()=="none"):
            return
        insert_sql="insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values"
        delete_sql="delete from KomliAdServer.global_channel_partner_block_list where "
        #print ("inside GCPBL filter")
        if request_line=="none":
            print ("no daata to process")
            return
        req_lines=request_line.split("\n")
        sql_texts_del=[]
        sql_texts_add=[]
        for line in req_lines:
            req_data=line.split(",")
            domain=req_data[0] 
            platform=req_data[1]
            action=req_data[2].lower()
#             if platform in ["1","2"]:
#                 domain=domain.lower()
            
            if action=='add':
                sql_texts_del.append( "delete from KomliAdServer.global_channel_partner_block_list where domain='"+domain+"';")
                sql_texts_add.append( "insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('"+domain+"',"+platform+");")
                #self.gcpb_add(domain, platform, db_server, db_port, db_user, db_password)
            elif action=='remove':
                self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
               
            else:
                print ("invalid action found for domain " +str(domain) )
                
        q1 = ('\n'.join(sql_texts_del))
        print (q1)
        self.execute_sql_db_multi(q1, db_server,  db_user, db_password,db_port, "KomliAdServer")
        
        q2 = ('\n'.join(sql_texts_add))
        print (q2)
        self.execute_sql_db_multi(q2, db_server,  db_user, db_password,db_port, "KomliAdServer")
                
 
    def gcpb_add(self,domain,platform,db_server,db_port,db_user,db_password):
        self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
        print ("adding domain")
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        mycursor = mydb.cursor()
        sql = "insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('"+domain+"',"+platform+");"
        print (sql)
        mycursor.execute(sql)
        mydb.commit()  
            
        
    def gcpb_remove(self,domain,platform,db_server,db_port,db_user,db_password): 
        print ("removing domain") 
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        mycursor = mydb.cursor()
        sql = "delete from KomliAdServer.global_channel_partner_block_list where domain='"+domain+"';"
        print (sql)
        mycursor.execute(sql)
        mydb.commit()  
        
        
    def global_publisher_blocklist_filter(self ,test_data,db_server,db_port,db_user,db_password):
        request_line=test_data["gssb_filter"]
        if (str(request_line).lower().strip()=="none"):
            return
        insert_sql="insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id)values"
        delete_sql="delete from KomliAdServer.global_supply_side_blocklist where "
        print ("inside GPBL filter")
        if request_line=="none":
            print ("no daata to process")
            return
        req_lines=request_line.split("\n")
        for line in req_lines:
            req_data=line.split(",")
            domain=req_data[0] 
            platform=req_data[1]
            action=req_data[2].lower()
            if action=='add':
                print ("adding")
                self.gssb_add(domain, platform, db_server, db_port, db_user, db_password)
            elif action=='remove':
                self.gssb_remove(domain, platform, db_server, db_port, db_user, db_password)
                
            else:
                print ("invalid action found for domain " +str(domain) )
                
    def global_publisher_blocklist_filter_new(self ,test_data,db_server,db_port,db_user,db_password):
        request_line=test_data["gssb_filter"]
        if (str(request_line).lower().strip()=="none"):
            return
        insert_sql="insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id)values"
        delete_sql="delete from KomliAdServer.global_supply_side_blocklist where "
        #print ("inside GPBL filter")
        if request_line=="none":
            print ("no daata to process")
            return
        req_lines=request_line.split("\n")
        sql_texts_del=[]
        sql_texts_add=[]
        for line in req_lines:
            req_data=line.split(",")
            #print ("len(req_data)")
            #print (len(req_data))
            domain=req_data[0] 
            platform=req_data[1]
            if len(req_data)==4:
                store_id=req_data[2]
                action=req_data[3].lower()
            else:
                store_id=0
                action=req_data[2].lower()
                
#             if platform in ["1","2"]:
#                 domain=domain.lower()
            if action=='add':
                #print ("adding")
                sql_texts_del.append("delete from KomliAdServer.global_supply_side_blocklist where domain='"+domain+"' and store_id="+str(store_id)+";")
                sql_texts_add.append("insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('"+domain+"',"+platform+","+str(store_id)+",'automation');")
                #self.gssb_add_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
            elif action=='remove':
                self.gssb_remove_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
                
            else:
                print ("invalid action found for domain " +str(domain) )

        q1 = ('\n'.join(sql_texts_del))
        print (q1)
        self.execute_sql_db_multi(q1, db_server,  db_user, db_password,db_port, "KomliAdServer")
        
        q2 = ('\n'.join(sql_texts_add))
        print (q2)
        self.execute_sql_db_multi(q2, db_server,  db_user, db_password,db_port, "KomliAdServer")

    def hawkeye_app_details_add_del(self ,test_data,db_server,db_port,db_user,db_password):
        request_line=test_data["hawkeye_app_details"]
        if (str(request_line).lower().strip()=="none"):
            return
        # insert_sql="insert into HawkEye.app_details(canonical_id,platform_id,store_id) values"
        # delete_sql="delete from HawkEye.app_details where "
        #print ("inside GPBL filter")
        if request_line=="none":
            print ("no daata to process")
            return
        req_lines=request_line.split("\n")
        sql_texts_del=[]
        sql_texts_add=[]
        for line in req_lines:
            req_data=line.split(",")
            #print ("len(req_data)")
            #print (len(req_data))
            canonical_id=req_data[0] 
            platform=req_data[1]
            if len(req_data)==4:
                store_id=req_data[2]
                action=req_data[3].lower()
            else:
                store_id=0
                action=req_data[2].lower()
                
#             if platform in ["1","2"]:
#                 domain=domain.lower()
            if action=='add':
                #print ("adding")
                sql_texts_del.append("delete from HawkEye.app_details where canonical_id='"+canonical_id+"' and store_id="+str(store_id)+";")
                sql_texts_add.append("insert ignore HawkEye.app_details(canonical_id,platform_id,store_id,source) values('"+canonical_id+"',"+platform+","+str(store_id)+",'automation');")
                #self.gssb_add_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
            elif action=='remove':
                self.hawkeye_app_details_remove_new(canonical_id, platform,store_id, db_server, db_port, db_user, db_password)
                
            else:
                print ("invalid action found for domain " +str(canonical_id) )

        q1 = ('\n'.join(sql_texts_del))
        print (q1)
        self.execute_sql_db_multi(q1, db_server,  db_user, db_password,db_port, "HawkEye")
        
        q2 = ('\n'.join(sql_texts_add))
        print (q2)
        self.execute_sql_db_multi(q2, db_server,  db_user, db_password,db_port, "HawkEye")

    def publisher_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
        request_line = test_data["pub_block_filter"]
        if (str(request_line).lower().strip() == "none"):
            return

        # print ("inside GPBL filter")
        if request_line == "none":
            print("no daata to process")
            return
        req_lines = request_line.split("\n")
        sql_texts_del = []
        sql_texts_add = []
        for line in req_lines:
            req_data = line.split(",")
            # print ("len(req_data)")
            # print (len(req_data))
            pubid = req_data[0]
            domain = req_data[1]
            platform = req_data[2]
            if len(req_data) == 5:
                store_id = req_data[3]
                action = req_data[4].lower()
            else:
                store_id = 0
                action = req_data[3].lower()

            #             if platform in ["1","2"]:
            #                 domain=domain.lower()
            if action == 'add':
                # print ("adding")
                sql_texts_del.append(
                    "delete from fraud_mgmt.pub_blocklist where domain='" + domain + "' and store_id=" + str(
                        store_id) + ";")
                sql_texts_add.append(
                    "insert ignore fraud_mgmt.pub_blocklist(pub_id,domain,platform_id,store_id)values(" +pubid + ",'" + domain + "'," + platform + "," + str(
                        store_id) + ");")
                # self.gssb_add_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
            else:
                print("invalid action found for domain " + str(domain))

        q1 = ('\n'.join(sql_texts_del))
        print(q1)
        self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, "fraud_mgmt")

        q2 = ('\n'.join(sql_texts_add))
        print(q2)
        self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, "fraud_mgmt")

    def platform_allowlist_filter_new(self ,test_data,db_server,db_port,db_user,db_password):
        request_line=test_data["plat_filter"]
        if (str(request_line).lower().strip()=="none"):
            return
        insert_sql="insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values"
        delete_sql="delete from fraud_mgmt.platform_allowlist where "
        #print ("inside GPBL filter")
        if request_line=="none":
            print ("no daata to process")
            return
        req_lines=request_line.split("\n")
        sql_texts_del=[]
        sql_texts_add=[]
        for line in req_lines:
            req_data=line.split(",")
            #print ("len(req_data)")
            #print (len(req_data))
            domain=req_data[0] 
            platform=req_data[1]
            if len(req_data)==4:
                store_id=req_data[2]
                action=req_data[3].lower()
            else:
                store_id=0
                action=req_data[2].lower()
                
#             if platform in ["1","2"]:
#                 domain=domain.lower()
            if action=='add':
                #print ("adding")
                sql_texts_del.append("delete from fraud_mgmt.platform_allowlist where adserving_entity='"+domain+"' and store_id="+str(store_id)+";")
                sql_texts_add.append("insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values('"+domain+"',"+platform+","+str(store_id)+");")
                #self.gssb_add_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
            else:
                print ("invalid action found for domain " +str(domain) )

        q1 = ('\n'.join(sql_texts_del))
        print (q1)
        self.execute_sql_db_multi(q1, db_server,  db_user, db_password,db_port, "fraud_mgmt")
        
        q2 = ('\n'.join(sql_texts_add))
        print (q2)
        self.execute_sql_db_multi(q2, db_server,  db_user, db_password,db_port, "fraud_mgmt")
                               
    def gssb_add(self,domain,platform,db_server,db_port,db_user,db_password):
        self.gssb_remove(domain, platform, db_server, db_port, db_user, db_password)
        print ("adding domain")
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        
        mycursor = mydb.cursor()
        sql = "insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,reason)values('"+domain+"',"+platform+",'automation');"
        print (sql)
        mycursor.execute(sql)
        mydb.commit()
        
    def gssb_remove(self,domain,platform,db_server,db_port,db_user,db_password):
        print ("removing domain") 
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        mycursor = mydb.cursor()
        sql = "delete from KomliAdServer.global_supply_side_blocklist where domain='"+domain+"';"
        print (sql)
        mycursor.execute(sql)
        mydb.commit() 
        
    def gssb_add_new(self,domain,platform,store_id,db_server,db_port,db_user,db_password):
        self.gssb_remove_new(domain, platform,store_id, db_server, db_port, db_user, db_password)
        print ("adding domain")
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        
        mycursor = mydb.cursor()
        sql = "insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('"+domain+"',"+platform+","+str(store_id)+",'automation');"
        print (sql)
        mycursor.execute(sql)
        mydb.commit()
        
    def gssb_remove_new(self,domain,platform,store_id,db_server,db_port,db_user,db_password):
        print ("removing domain") 
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="KomliAdServer"
        )
        mycursor = mydb.cursor()
        sql = "delete from KomliAdServer.global_supply_side_blocklist where domain='"+domain+"' and store_id="+str(store_id)+";"
        print (sql)
        mycursor.execute(sql)
        mydb.commit()  

    def hawkeye_app_details_remove_new(self,canonical_id,platform,store_id,db_server,db_port,db_user,db_password):
        print ("removing domain from hawkeye db - app details table") 
            
        mydb= mysql.connector.connect(
          host=str(db_server),
          user=str(db_user),
          passwd=str(db_password),
          port=str(db_port),
          database="HawkEye"
        )
        mycursor = mydb.cursor()
        sql = "delete from HawkEye.app_details where canonical_id='"+canonical_id+"'and platform_id='"+platform+"' and store_id="+str(store_id)+";"
        print (sql)
        mycursor.execute(sql)
        mydb.commit() 
        
    def validate_failed_files(self,api_endpoint,token,test_data,db_server,db_port,db_user,db_password):
        failed_records=test_data["failed_records"]
        if (str(failed_records).lower().strip()=="none"):
            return
        file_id=self.get_fileid_from_name(db_server, db_port, db_user, db_password)
        print ("validating data for file")

        url = str(api_endpoint)+"/infrastructure/bulkOperations/"+str(file_id)+"/failedRecords"
        
        querystring = {"PubToken": str(token)}
        
        headers = {
            'PubToken': str(token),
            'cache-control': "no-cache",
            'Postman-Token': "7946c2a1-f182-4913-9f66-ff415d03b5c8"
            }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
        api_response=response.text 
        print(api_response)
        api_response=str(api_response).split("\n")
        failed_records=failed_records.split("\n")
        print("failed_records= "+str(failed_records))
        for record in failed_records:
            data=record.split(",")
            domain=data[0]
            failed_description=data[1]
            
            for domain_item in api_response:
                if str(len(str(domain_item)))=="0":
                    continue
                #print(domain_item)
                extracted_domain_app=str(domain_item).split(",")[1]
                print(extracted_domain_app)
                if str(extracted_domain_app)==str('"'+domain+'"'):
                    print("comparing record")
                    print(domain_item)
                    print(domain)
                    if str(failed_description) in domain_item:
                        print("failure file record is validated ")
                        
                    else: 
                        print(record)
                        
                        raise Exception ("Failed file validation is failed for record "+str(record))    
            
            
        
    
    def get_fileid_from_name(self,db_server,db_port,db_user,db_password):
        mydb = mysql.connector.connect(
            host=str(db_server),
            user=str(db_user),
            port=str(db_port),
            passwd=str(db_password),
            database="ActivityLog"
        )

 
        mycursor = mydb.cursor()
        sql = "select id  from bulk_operations where  file_name ='"+str(self.activity_file_name)+"'; "
        print(sql)
        mycursor.execute(sql)
        data = mycursor.fetchone()
        if isinstance(data, tuple):
            for x in data:
                return x
            print("sleeping")
            mydb.commit()
        
        raise Exception("Bulk file not found")        
    
    def heimdall_cache_refresh(self, api_endpoint,token): 
        url = str(api_endpoint)+"/heimdall/cache-refresh"
        
        payload = ""
        headers = {
            'Content-Type': "application/json",
            'pubtoken': str(token),
            'cache-control': "no-cache",
            'Postman-Token': "604f3d8a-f148-49e1-ba8d-e79416b77e74"
            }
        
        response = requests.request("GET", url, data=payload, headers=headers)
        
        print(response.text) 
        
    def returndataframe(self,csvPath,sheetName):
        self.excelDF=self.excelTableToDataFrame(csvPath,sheetName)
        #with open ('dataframe.json','w+') as f:
        #    f.write(str(self.excelDF.copy().to_dict()))
        return self.excelDF.copy().to_dict()
    
    def get_data_frame_value(self,data_frame,test='',column=''):
        column_position="0"
        header_list = (data_frame['Test Cases/Test Data']) 
        print("header_list="+str(header_list))
        for i,j in header_list.items():
            if str(j)==column:
                column_position=i
                
        test_cases = data_frame 
        # print ("printing")
#         print (test)
#         print (column)
#         print (test_cases)
        print("Checking")
        print (test)
        print(column)
        for v,k in test_cases.items(): 
            #print (str(v).lower(),str(test).lower())
            print("checking with")
            print(str(v).lower())
            if (str(v).lower()==str(str(test).lower())):
                key_found= v
                print ("key_found: " + str(k)) 
                print(data_frame[key_found][int(column_position)])
                return (data_frame[key_found][int(column_position)])
            else:
                print ("key not found")
#                 # raise Exception ('key not found')
#             
#         print (data_frame[column])
#         print (int(key_found))
#         print (data_frame[column][int(key_found)])
#         return (data_frame[column][int(key_found)])
        
  
    def excelTableToDataFrame(self,excelPath,sheetName):
        df=pd.read_excel(open(excelPath,'rb'),sheet_name=sheetName)
        return df
    
    def update_spoofer_response_file(self, spoofer_server_url, file_name, response_txt):
        print("spoof started")
        url = "http://" + spoofer_server_url + "/updatespoofdata"
        payload = response_txt
        headers = {'file_name': file_name}
        response = requests.request("POST", url, data=payload, headers=headers)
        print("completed")
        
    
    def heimdall_cache_refresh_app_onboarding_check(self,uri,token,value):
        import requests
        import json
        
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
  "allowlisting.ctv.app.onboarding.check": "{}".format(value)
})
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh with token " + str(token))
        else:
            print ("heimdall_cache_refresh completed..!")

    def heimdall_cache_refresh_canonical_regex(self,uri,token):
       
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        print(url)
        payload = json.dumps({
            "canonical.regex.validation.3": "^[0-9]+$",
            "canonical.regex.validation.4": "^[0-9]+$",
            "canonical.regex.validation.5": "^[a-zA-Z0-9]+$",
            "canonical.regex.validation.6": "^[0-9]+$",
            "canonical.regex.validation.7": "^[a-zA-Z.]+$",
            "canonical.regex.validation.8": "^[a-zA-Z0-9]+$",
            "canonical.regex.validation.9": "^[a-zA-Z.]+$"

            })
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_app_Config_cache_refresh with token " + str(token))
        else:
            print ("heimdall_app_Config_cache_refresh completed..!")
            
    def heimdall_cache_refresh_canonical_supported_store_ids(self,uri,token):   

        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
            "canonical.support.valid.store.ids" : "3#4#5#6#7#8#999999"
            })
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh_canonical_supported_store_ids with token " + str(token))
        else:
            print ("heimdall_cache_refresh_canonical_supported_store_ids completed..!")
           
    def heimdall_cache_refresh_lookup_storeIds(self,uri,token,value):
        import requests
        import json
        
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
  "allowlisting.ctv.ratingserver.lookup.storeIds": "{}".format(value),
  "resttemplate.retry.delay.seconds":1,
  "resttemplate.retry.max.attempt":1
})
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh with token " + str(token))
        else:
            print ("heimdall_cache_refresh completed..!")
            
    def heimdall_cache_refresh_ratingserver_na_action(self,uri,token,value):
        import requests
        import json
        
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
  "allowlisting.ctv.ratingserver.na.action": "{}".format(value)
})
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh with token " + str(token))
        else:
            print ("heimdall_cache_refresh completed..!")
            
    def heimdall_cache_refresh_ratingserver_other_action(self,uri,token,value):
        import requests
        import json
        
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
  "allowlisting.ctv.ratingserver.other.action": "{}".format(value)
})
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh with token " + str(token))
        else:
            print ("heimdall_cache_refresh completed..!")
            
            
    def heimdall_cache_refresh_ratingserver_other_action(self,uri,token,value):
        import requests
        import json
        
        url = "https://{}/heimdall/appconfig/refresh".format(uri)
        
        payload = json.dumps({
  "allowlisting.ctv.ratingserver.other.action": "{}".format(value)
})
        headers = {
          'pubtoken': '{}'.format(token),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 200):
            print (response.status_code)
            raise Exception("called heimdall_cache_refresh with token " + str(token))
        else:
            print ("heimdall_cache_refresh completed..!")


    def topLevelAdContainer_updateCTVApps(self,uri,token):
        import requests
        import json
        
        url = "https://{}/heimdall/topLevelAdContainer/updateCTVApps?pubIdsLimit=100&recordLimit=5000".format(uri)
        
        payload={}
        headers = {
          'pubtoken': '{}'.format(token)
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 202):
            print (response.status_code)
            raise Exception("failed topLevelAdContainer_updateCTVApps with token " + str(token))
        else:
            print ("topLevelAdContainer_updateCTVApps completed..!")
            
    def reProcess_pub_site(self,uri,token):
        import requests
        import json
        
        url = "https://ci-va2qa-mgmt.pubmatic.com/heimdall/topLevelAdContainer/reProcess?noOfDays=1"
        
        payload={}
        headers = {
          'pubtoken': '{}'.format(token)
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 202):
            print (response.status_code)
            raise Exception("failed reProcess_pub_site with token " + str(token))
        else:
            print ("reProcess_pub_site completed..!")
        import time
        time.sleep(60)
            
    def reProcess_pub(self,uri,token):
        import requests
        import json
        
        url = "https://ci-va2qa-mgmt.pubmatic.com/heimdall/publisherAllowlist/reProcess?noOfDays=1"
        
        payload={}
        headers = {
          'pubtoken': '{}'.format(token)
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.text)
        if (response.status_code != 202):
            print (response.status_code)
            raise Exception("failed reProcess_pub with token " + str(token))
        else:
            print ("reProcess_pub completed..!")
            
    def add_to_gssb(self,data,db_host,Bulk_db,Komli_db,db_port,db_user_name, db_password,hawkeye_db_user,hawkeye_db_password, hawkeye_db_host, hawkeye_port,user):
        self.global_publisher_blocklist_filter_new(data, Komli_db,db_port, db_user_name, db_password)
        
        
    def upload_gssb(self, test_data,db_server,db_port,db_user,db_password, ui_setup ,token,activity_db_host,common_db_user_name,common_db_password,common_db_port,uri_prefix,komli_db_host,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password,cache_refresh="True"):

        """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
        print (activity_db_host,common_db_user_name,common_db_password,common_db_port)
    
        upload_content=test_data["upload_content"]
        processed_file_data=test_data["processed_file"]
        failed_file_data=test_data["failed_file"]
        
        #print (failed_file_data)
        #print (processed_file_data)
        
        
        populate_publisher_site_tld_records=test_data["populate_publisher_site_tld_records"]
        db_cleanup=str(test_data["db_cleanup"]).lower().strip()
        print ("db_cleanup flag="+str(db_cleanup))
        if(db_cleanup=="true"):
           start = time.time()
           self.clean_up_gssb(test_data,komli_db_host,db_port,db_user,db_password)
           end = time.time()
           print("Runtime of the upload_gssb is "+str(end - start))
         
        if  cache_refresh=="False":
            self.heimdall_cache_refresh(ui_setup, token) 
         
       
        self.current_path = os.path.dirname(__file__)
        print("current_path= "+str(current_path))
     
        letters = string.ascii_lowercase
        file_name= ( ''.join(random.choice(letters) for i in range(10)) )
        file_name=file_name+".csv"
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        f = open(file_path, "w")
        f.write(str(upload_content))
        f.close()
        
         
        print("file_path= "+str(file_path)) 
        BuiltIn().log(file_path, level="INFO")
        time.sleep(5)
        
        
        
        upload_button = "//button[@data-pm-id='showUploadDomainPopupButton']"
        self.s2l.click_element(upload_button)
        
        self.s2l.wait_until_element_is_visible("//input[@data-pm-id='file-input']", 60)
        
        self.acc7.pmccFileUpload("upload-control", file_path)
        
        print ("file selected")
        #time.sleep(10)

        self.acc7.pmccButton("upload-btn")
        
        self.wait_for_spinner_to_disappear(120)
         
        upload_status_xpath = "(//table[@class='pmcc-table pmcc-table-sortable']//tbody//td[text()='{}']//ancestor::tr//span)[2]"
        file_name = os.path.basename(file_path)
        upload_status_xpath = upload_status_xpath.format(file_name)
        upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
        self.refresh="//button/pmcc-icon[@name='refresh']"
        while upload_status == "Processing":
            print (upload_status)
            self.s2l.click_element(self.refresh)
            time.sleep(2)
            upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
        print ("Completed")
                    
    def insert_app_details(self,test_data,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password):                
        self.DB.insert_app_details(test_data,hawkeye_db_server,hawkeye_db_port,hawkeye_db_user,hawkeye_db_password)    
        
        
    def loginAsPublisher(self, URI, publisherLoginID, publisherPassword, selectAccount=None, isSecureLogin=False,
                         gitLoginRequired=False, gitUserName=None, gitPassword=None):
        """
        Login to a publisher page
        :param URI: URL without http:// ex: appbeta.pubmatic.com
        :param publisherLoginID: publisher Login ID
        :param publisherPassword: publisher Login password
        :param selectAccount: string value of account to be selected from singleselect component
        :param isSecureLogin: bool True/False, true if https required, false if http
        :param gitLoginRequired bool True/False
        :param gitUserName: git login username
        :param gitPassword: git login password
        :return: None
        """
        default_timeout = self.s2l.set_selenium_implicit_wait(2)
        if gitLoginRequired:
            if gitUserName is not None and gitPassword is not None:
                self.gitLogin(gitUserName, gitPassword)
            else:
                BuiltIn().fail("git username or password required to login to git")
        if isSecureLogin:
            URL = "https://"
        else:
            URL = "http://"
        URL = URL + URI + "/login/publisher"
        usernameXpath = "id=okta-signin-username"
        passwordXpath = "id=okta-signin-password"
        loginButtonXpath = "id=okta-signin-submit"
        dashBoardXpath = "//h1[contains(@class, 'pmcc-page-tite')]"
        self.s2l.maximize_browser_window()
        
        #cookiesXpath = "id=_evidon-accept-button"
        #self.s2l.click_element(cookiesXpath)

        #self.s2l.go_to(URL)
        BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', usernameXpath)
        self.s2l.input_text(usernameXpath, publisherLoginID)
        self.s2l.input_text(passwordXpath, publisherPassword)
        self.s2l.click_element(loginButtonXpath)
        #loginButtonXpath_pub = "id=submit"
        
        BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'element_should_contain', "//div[@data-pm-id='email']",'user_302@pubmatic.com')
        
        if selectAccount is not None:
            self.selectAccount(selectAccount)

        #BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'element_should_contain', dashBoardXpath, 'Dashboard')
        #self.s2l.set_selenium_implicit_wait(default_timeout) 
        
        
    def selectAccount(self, selectAccountValue):
        """
        selects an account after publisher/admin login
        :param selectAccountValue: string account value to be selected from singleselect
        :return: None
        """
        selectAccountSingleSelectXpath = "//pmcc-singleselect[@data-pm-id='accounts-dropdown']"
        accountSelectInputBoxXpath = "//*[@data-pm-id='search-input']//input"
        accountSelectXpath = "//*[@class='pmcc-table pmcc-table-borderless']//tbody//tr//td//span[text()='{}']".format(selectAccountValue)
        loginButtonXpath = "//button[@data-pm-id='continue-btn']"
        BuiltIn().wait_until_keyword_succeeds('30 sec', '2 sec', 'page_should_contain_element',
                                              selectAccountSingleSelectXpath)
        self.s2l.click_element(selectAccountSingleSelectXpath)
        BuiltIn().wait_until_keyword_succeeds('10 sec', '2 sec', 'page_should_contain_element',
                                              accountSelectInputBoxXpath)
        self.s2l.input_text(accountSelectInputBoxXpath, selectAccountValue)
        BuiltIn().wait_until_keyword_succeeds('20 sec', '2 sec', 'page_should_contain_element',
                                              accountSelectXpath)
        BuiltIn().wait_until_keyword_succeeds('10 sec', '2 sec', 'click_element', accountSelectXpath)
        BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', loginButtonXpath)   
        
        
        
    def infra_upload(self,uri,post_api,file_path):
        url = f"https://{uri}/infrastructure/bulkOperations?mode=upload&resourceUrl={post_api}?entityId=0"
        payload={}
        headers = {
                  'PubToken': 'token337'
                }
        with open (file_path,"rb") as f:
            data = f.read()
        print (data)
        files = {'file': open(file_path, 'rb')}
        print (url)
        print (headers)
        print (payload)
        print (files)
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        code= (response.status_code)
        print (code)
        if (code)==201:
            import time
            if '/heimdall/publisherWhitelist' in url:
                print ("sleeping for 40 sec")
                time.sleep(40)
            elif 'topLevelAdContainer' in url:
                print ("sleeping for 40 sec")
                time.sleep(40)
            else:
                print ("sleeping for 20 sec")
                time.sleep(20)
        else :
            assert response.status_code == 201 


                
                
    def infra_upload1(self,uri,post_api,file_path):
        url = f"https://{uri}/infrastructure/bulkOperations?{post_api}"
        payload={}
        headers = {
                  'PubToken': 'token337'
                }
        files = {'file': open(file_path, 'rb')}
        print (url)
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        code= (response.status_code)
        print (code)
        if (code)==201:
            import time
            if '/heimdall/publisherWhitelist' in url:
                print ("sleeping for 40 sec")
                time.sleep(40)
            elif 'topLevelAdContainer' in url:
                print ("sleeping for 40 sec")
                time.sleep(40)
            elif 'publisherAllowlist' in url:
                print ("sleeping for 90 sec")
                time.sleep(120)
            else:
                print ("sleeping for 20 sec")
                time.sleep(20)
            

    def update_canonical_flag(self,test_data,uri,pub_id,fraud_db_host,user_name,password,port):
        if test_data["onboard_canonical_for_ctv"] == "ON":
            flag = 1
        else:
            flag= 0
        url = f"{uri}/heimdall/canonical/onboarding?pub_id={pub_id}&onboarding_canonical={flag}"
        payload={}
        headers = {
                'PubToken': 'token337',
                'Content-Type': 'application/json'
                }
        print (url)
        response = requests.request("POST", url, headers=headers, data=payload)
        print (response.text)
        # expected = '[{"Status": " : successfully updated 1 records. Updated onboarding_canonical flag for publisherId: '+{pub_id}+'"}]'
        assert response.status_code == 200
        self.validate_onboard_canonical_flag_in_db(pub_id,flag,fraud_db_host,user_name,password,port)
        # assert response.text == expected


    def validate_onboard_canonical_flag_in_db(self,pub_id,flag,fraud_db_host,user_name,password,port):

        mydb = mysql.connector.connect(
            host=str(fraud_db_host),
            user=str(user_name),
            port=str(port),
            passwd=str(password),
            database=str('fraud_mgmt')
        )
        query = f"select onboarding_canonical from publisher_iq_settings where pub_id={pub_id} and onboarding_canonical={flag}"
        mycursor = mydb.cursor()
        print (query)
        mycursor.execute(query)
        result=mycursor.fetchone()
        print (result)
        if result is None:
            assert flag != flag
            
        