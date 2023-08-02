import subprocess

from PySide6.QtCore import QObject, Slot, QUrl, Signal

from controller import Controller, Recover


class Bridge(QObject, Controller, Recover):
    # Login Signals
    successful_login = Signal()
    failed_login = Signal()
    create_account_login = Signal()
    recovery_login = Signal()

    # Startup Signals
    successful_startup = Signal()
    failed_startup = Signal()
    back_login_startup = Signal()

    # Recovery Signals
    successful_recovery = Signal()
    failed_recovery = Signal()
    cancel_recovery = Signal()

    # main app signals
    add_password_view = Signal()
    menu_view = Signal()

    def __init__(self, parent=None):
        Controller.__init__(self, parent)  # initialize controller class, all its methods are now accessible
        QObject.__init__(self)

    def __init_recover__(self):
        # Initiate recovery class, all its methods are now accessible,
        # it needs the controller (self) in order to work
        Recover.__init__(self, self)

    @Slot(str)
    def printJS(self, string):
        print("JS: " + string)

    ###### App Methods ######
    @Slot()
    def callAddPassword(self):
        self.add_password_view.emit()

    @Slot(str, str, str, str)
    def callPushPassword(self, target, username, password, icon):
        self.__push_password__(target, username, password, icon)


    @Slot()
    def backToMenu(self):
        self.menu_view.emit()

    ###### Recovery Methods ######
    @Slot(str, result=bool)
    def submitAnswer(self, answer):
        if self.verify_answer(answer):
            return True
        return False

    @Slot(str, result=str)
    def getQuestion(self, username):
        self.username = username  # re-attribute username to the one asked for recovery
        return self.get_personnal_question()


    @Slot(str, str, str, str, result=bool)
    def submitNewInformations(self, new_password, new_question, new_answer, old_answer):
        if self.applicate_recovery(new_password, new_question, new_answer, old_answer):
            return True
        return False

    @Slot()
    def successfulRecovery(self):
        self.successful_recovery.emit()

    @Slot()
    def cancelRecovery(self):
        self.cancel_recovery.emit()

    ###### Login Methods ######
    @Slot(str, str, result=bool)
    def submitLogin(self, username, password):
        if self.check_login(username, password):
            print(f"Login Success")
            self.load_app(username, password)
            return True
        else:
            print(f"Login Failed")
            return False

    @Slot()
    def callMain(self):
        print("Main Called")
        self.successful_login.emit()

    @Slot()
    def callStartup(self):
        print("Startup Called")
        self.create_account_login.emit()

    @Slot(str)
    def callRecovery(self, username):
        # Initiate Recovery class
        self.__init_recover__()

        print("Recovery Called")

        # articifically set username for recovery, will be overwritten by user later on
        self.username = username

        self.recovery_login.emit()

    @Slot(str)
    def printf(self, string):
        print(string)

    ###### Startup Methods ######
    @Slot(str, str, str, str)
    def submitAccount(self, username, password, question, answer):

        if self.initiate_db_settings(username, password, question, answer):
            print(f"Startup Success")
            self.successful_startup.emit()
        else:
            self.failed_startup.emit()


    @Slot()
    def callLogin(self):
        print("Back Login Called")
        self.back_login_startup.emit()

