# <h1 align="center"><ins> MDPSaver</ins> v1.0.1 ![Python](.git_files/python.ico) ![Windows](.git_files/Windows.ico)</h1>

<p align="center">
	<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/GaecKo/MDPSaver?color=lightblue" />
	<img alt="Number of lines of code" src="https://img.shields.io/tokei/lines/github/GaecKo/MDPSaver?color=critical" />
	<img alt="Code language count" src="https://img.shields.io/github/languages/count/GaecKo/MDPSaver?color=yellow" />
	<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/GaecKo/MDPSaver?color=blue" />
	<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/GaecKo/MDPSaver?color=green" />
</p>
<h1 align="center">

[![Support via PayPal](https://cdn.rawgit.com/twolfson/paypal-github-button/1.0.0/dist/button.svg)](https://paypal.me/ArthurDeNeyer?country.x=BE&locale.x=fr_FR) 

</h1>

****

**🔑 Welcome to my Password Manager App.**

### <ins> Introduction </ins> 
This app makes it easy for you to:
* **Add** your passwords
* **See** your added passwords
* **Generate** / **Create** passwords for you

All of these are done with the `pycryptodome` and `cryptography` module, to make sure everything is **secure**. By making use of these modules no lambda person will be able to access your **encrypted data**. 

**General way of working**: An **Access Password** (AP) that you create will be your **key 🔑** to all of your **saved password 🏠**. Without this AP, *none* of your password will be *readable*! All the password that you will add will be encrypted using a key which is derived from your AP, using *Fernet*, *base64.urlsafe_b64encode*, ...

Status:  `▰▰▰▰▰▰▰▰▰▰ 100%` 

* [Installation](#installation)
    - [<ins> Windows Executable (.exe) </ins>](#-ins--windows-executable--exe-------ins-)
    - [<ins> Python Script (.py) </ins> ](#-ins--python-script---ins----python--git-files-pythonico-)
* [Update](#update)
* [Update notice](#update-notice)
* [Walkthrough](#walkthrough)
    - [<ins> Starting Screen </ins>](#-ins--starting-screen---ins-)
    - [<ins> Main Menu </ins>](#-ins--main-menu---ins-)
        * [<ins> 1) Access my Passwords 🔎</ins>](#-ins--1--access-my-passwords-----ins-)
        * [<ins> 2) Add a password ➕</ins>](#-ins--2--add-a-password----ins-)
        * [<ins> 3) Generate Random Password 🔀</ins>](#-ins--3--generate-random-password-----ins-)
        * [<ins> 4) Change Username ✒️</ins>](#-ins--4--change-username-----ins-)
        * [<ins> 5) Change Access Password 🔏</ins>](#-ins--5--change-access-password-----ins-)
        * [<ins> 6) Help / Tutorial ❓</ins>](#-ins--6--help---tutorial----ins-)
        * [<ins> 7) Leave ❌</ins>](#-ins--7--leave----ins-)
        * [<ins> 8) System Settings ⚙️</ins>](#-ins--8--system-settings-----ins-)
* [SpeedTest](#speedtest)
    - [<ins> With **50 passwords** :</ins>](#-ins--with---50-passwords------ins-)
    - [<ins> With **100 passwords** :</ins>](#-ins--with---100-passwords------ins-)
    - [<ins> How I did it (*story time*): </ins>](#-ins--how-i-did-it---story-time------ins-)
* [Notes](#notes)


****
## Installation 

#### <ins> Windows Executable (.exe) 🪟 </ins>
* Here is a [video](https://youtu.be/CvxW0uoeJtI) on how to install MDPSaver (Easy Method)

Or follow these steps:
1) Download and extract (unzip) the files. 
2) Go into the exe folder: `./MDPSaver-master/MDP_EXE/`
3) Righ click on `MDPSaver.exe` and create a shortcut to it
4) Rename and move the shortcut on your desktop
5) Double click on the shortcut which is on your desktop, if a red window opens up, click on `more information`and then `install anyway` 
* Check the video if you have any trouble! You can also contact me on discord: `GaecKo#7545`


#### <ins> Python Script </ins> ![Python](.git_files/python.ico) 

1) This app is 100% python based. To launch it as a normal python script, you need [python3.x](https://www.python.org/downloads/) to be installed on your device.
    * Please make sure that you cross the pip option in the installation wizard as well!
2) Once done, you will need to install some modules:
    * `pip install cryptography`
    * `pip install pycryptodome`
    * `pip install pwinput`
    * `pip install colorama`
    * if `pip` doesn't work, try using `pip3`
    * You now have the prerequired modules to continue!

3) Download and unzip the files
4) Go into the app folder: `./MDPSaver-master/MDP_APP/`
5) You should see all the python scripts, open a terminal in that folder and type  `python MDPSaver.py` or `python3 MDPSaver.py`
    * If you have any issues like:
        * `FileNotFoundError`
        * `Module not found`, ...
    * Make sure you opened a terminal **IN** the `MDP_APP/` folder! It should look like: 
    
    `X:\...\MDPSaver-master\MDPSaver-master\MDP_APP>python MDPSaver.py`
* The program should be running! Each time you want to launch MDPSaver, you need to repeat step 4 and 5!
* If you have any problem using the app, contact me on Discord: `GaecKo#7545`
****

## Update
* If you used last version of MDPSaver, here is a [video](https://www.youtube.com/watch?v=y8biYrRKB9s) on how to update your old data to the new MDPSaver.  

****

## Update notice
I have been working on a new functionnality just recently called "Search Filter" which allows you to filter and show site with corresponding password / email / username. It's usefull if you wish for example to see all the sites that have the same password / ... .

It's only available on the python version. Please also check [Notes](#notes) for more information. 

****

## Walkthrough 
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
* This menu should only be used if you plan on testing things with the code or if you have issues with the program and that loosing your password doesn't afraid you.

****
## SpeedTest 🚀
* Something I kept in mind during the project was to have a program wich is quick and simple. Starting the project I used a encode and decode function which turned out to be not that safe, as there was an already known way on how to crack them. I then switched to an official security system (`Fernet` from `cryptography`, allied with `pycryptodome`), that I used with a key which was direved using the Access Password. That way, and with 380 000 iterations, each saved password is encrypted and safe. 

* But how about speed ? Well after hours spent on data managing and improved encryption, I now have a system which is fast enough to ensure fluent usage. 

* If you want to test speed by yourself:
    * `.\MDPSaver-master\MDPSaver-master\MDP_APP>python SpeedTest.py`
    * You will be asked how many password you want to test with, just wait a bit and some results should be displayed! 

* Result (could be influenced by the machine you use):

#### <ins> With **50 passwords**</ins>

* High security system with no improvement:
    ![Old50](.git_files/Old50.png)
* High security system with improvement:
    ![New50](.git_files/New50.png)

#### <ins> With **100 passwords**</ins>
* High security system with no improvement:
    ![Old100](.git_files/Old100.png)
* High security system with improvement:
    ![New100](.git_files/New100.png)

#### <ins> How I did it (*story time* 📖)</ins> 
* I used to save password this way:

        ```
        encrypted site 1 | encrypted username 1 | encrypted password 1
        encrypted site 2 | encrypted username 2 | encrypted password 2
        encrypted site 3 | encrypted username 3 | encrypted password 3
                                        ...
        ```
    It was then easy to decrypt using `string.split(" | ")` and then `decrypt(AP, string[0]), ...`. 
    
    I then simplified the process by directly encrypting the whole phrase, including the " | ". That made the encrypting and decrypting **3x** faster. (I figured that out while explaining the method to [@drudru18](https://github.com/drudru18), thanks mate 💘)

    I would have something like this: 

    `encrypt(AP, site + " | " + username + " | " + password)`

    To then first `string = decrypt(AP, whole phrase)` and then `string.split(" | ")`. 
    
* I then figured out that the long processus of encrypting and decrypting was due to the key creation. This key is derived using the AP and is each time exactly the same. So, instead of creating for each encryption / decryption a key (which is each time the same), I would simply save it once into a program variable and re-used it for each encryption / decryption. That avoided *380 000* iterations each time. 

* To sum up, I went from:

    ```
    (3 encryption / decryption per password ) * 380 000 * numbers of password
    -> 3 * 380 000 * n = 1 140 00 iterations per password
    ```
    **TO**
    ```
    380 000 + ((1 encryption / decryption per password) * numbers of password)
    -> = 380 000 + n iterations for all of the password!
    ```
    That's how it went from `78 ms` per password to `0.24 ms`, so about `325x` quicker! Of course, as the key is loaded once, you can add / load passwords thousand of times, in the same instance of the program, and you will have almost no encryption / decryption time. 


## Notes 

* The new functionnality won't be added to the .exe version, as it would require to recompile the whole program.

* Also, as you can see within the python files:

    ```txt
            ==== ⚠ DISCLAIMER ⚠ ====
    This code is not suitable for professional use. As of the current state of the code, this 
    whole program is not sustainable and thus depreciated. 
    
    If you wish to rebuilt the program, feel free to do it and I'll check the PR! 
    ```

    This means that I won't work on this project anymore. I might add some new features, but I won't work on the code itself. 
