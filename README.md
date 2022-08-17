# <ins> MDPSaver </ins>

Welcome to my **Password Manager App.** 


### <ins> Introduction </ins> 
This app makes it easy for you to:
* **Add** your passwords
* **See** your added passwords
* **Generate** / **Create** passwords for you

All of these are done with the `pycryptodome` and `cryptography` module, to make sure everything is **secure**. By making use of these modules no lambda person will be able to access your **encrypted data**. 

**General way of working**: An **Access Password** (AP) that you create will be your **key 🔑** to all of your **saved password 🏠**. Without this AP, *none* of your password will be *readable*! All the password that you will add will be encrypted using a key which is derived from your AP, using *Fernet*, *base64.urlsafe_b64encode*, ...

### <ins> Walkthrough </ins>
Here is a walkthrough of the app

#### <ins> Starting Screen </ins>
![Starting Screen](.git_files/StartingScreen.gif)

#### <ins> Main Menu </ins>
* This is the Main Menu in which you can access all of the app functionnalities.
![Main Menu](.git_files/MainMenu.png?raw=true "Main Menu")

##### <ins> 1) Access my Passwords 🔎</ins>
* You can easily access your already saved password by typing one in the main menu:
![AccessPassword](.git_files/AccessPassword.gif)
* You can then:
    * Type the number **corresponding** to the password
    * Type a **keyword** which will display corresponding password
    * Type **+** or **last password number + 1** to directly access "Add a password"
    ![AddPassword+](.git_files/AddPassword%2B.gif)
    * Press enter to leave

* If you reach a saved password:
![AccessPasswordModification](.git_files/AccessPasswordModification.gif)
* You can then:
    * **Reveal** the password
    * **Delete** the password
    * **Change** the password
    * **Change** the *username / email*
    * Go back

##### <ins> 2) Add a password ➕</ins>
* To **add a *password***, type 2 in the main menu:
![AddPassword](.git_files/AddPassword.gif)
* You can then add the Site, Username / email and the password

##### <ins> 3) Generate Random Password 🔀</ins>
* The app can also generate Random Password for you. This can be usefull when signing up on new website/ ...
* The app lets you directly add the generated password to your saved password 
![GeneratePassword](.git_files/GeneratePassword.gif)
* 4 ways of generation:
    * *Weak*: only letters + numbers | size 8~12
    * *Medium*: letters + numbers + symbols | size 10~20
    * *Strong*: long + letters + numbers + symbols | size 15~25
    * *Custom*: with(out) symbols + with(out) numbers | custom size


##### <ins> 4) Change Username ✒️</ins>
* If needed, you can change your **Username**:
![ChangeUsername](.git_files/ChangeUsername.gif)

##### <ins> 5) Change Access Password 🔏</ins>
* If needed, you can change your **Access Password**:
![ChangeAccessPassword](.git_files/ChangeAccessPassword.gif)
    * You will need to recreate a question and answer!

##### <ins> 6) Help / Tutorial ❓</ins>
* You can access a tutorial:

![Tutorial](.git_files/Tutorial.png)

##### <ins> 7) Leave ❌</ins>
* To properly exit the program, just type 7:
![Exit](.git_files/Leave.gif)
* If you are using the .exe version, the cmd window might close.

##### <ins> 8) System Settings ⚙️</ins>
* You can access some deep app setting by typing 8:
![SystemSettings](.git_files/SystemSettings.gif)
* You can then:
    * Hard Reboot Everything (reset everything)
    * Delete all password (reset data.txt)
    * Reset personnal data (this means that you will need to reconfigure the app, new AP, new question, ... If you use the same AP your password won't be lost, but it's kind of risky...)

### <ins> Installation </ins>
* Here is a tutorial on how to install this app.

#### <ins> Windows Executable (.exe) 🪟</ins>

#### <ins> Python Script </ins> ![Python](.git_files/python.ico) 

* This app is 100% python based. To launch it as a normal python script, you need [python3.x](https://www.python.org/downloads/) to be installed on your device.
    * Please make sure that you cross the pip option in the installation wizard as well!
* Once done, you will need to install some modules:

    * `pip3 install cryptography`
    * `pip3 install pwinput`
    * `pip3 install colorama`
    * if `pip3` doesn't work, just use `pip`

* You now have the prerequisites to continue. 