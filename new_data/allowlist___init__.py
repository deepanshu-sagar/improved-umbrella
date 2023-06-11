def __init__(self):
    """
        Constructor
        """
    BasePage.__init__(self)
    self.sw = SeleniumWrapper()
    self.acc7 = AngularCoreComponents7()
    self.activity_file_name = 'mqbecltpsb.csv'
    print('init..')
    self.DB = AllowlistDB()