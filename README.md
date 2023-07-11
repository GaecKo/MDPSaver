# <h1 align="center"><ins> MDPSaver</ins></h1>

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


****
### Web Engine Integration
This version uses a web engine integration (`PySide6.QtWebEngineWidgets`) in order to do the frontend of the app. After long consideration, we decided that having a html / css frontend would be more efficient, easy & versatile. As it's a completely other maneer of working, we had to rebuilt the whole app. 

It's currently still in evaluation and there is a long way to go. 
