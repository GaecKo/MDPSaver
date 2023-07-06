## MDPSaver: GUI

### General
#### Front End:

* [ ] Personnalized top bar

* [ ] Finish window of Recovery Page (`reco.py` & `MDPStyle/recovery.css`)
    * [ ] Connect it to `main.py`

* [ ] Start window of general app (`app.py` & `MDPStyle/app.css`) 
    * [ ] ...

* [ ] Clean unused Widgets (lots of deletion needed)

* [ ] Custom widget for password box (`utils/?`)

* [ ] Better User Experience
    * [ ] Custom app color
    * [ ] Custom text selection color
    * [ ] QMessageBox should be reworked


#### Back End (`MDPDatabase/*`):
* [ ] Add multiple user system (@GaecKo)
    * [  ] Optimized database querying 

* [ ] Recovery bug: site & username get switched in recovery process

#### Controller (`MDPSaver.py` & `controller.py`):
* [ ] Automatic suspend of app after x minutes (@GaecKo)
* [ ] Log system (@GaecKo)

#### Other:
* [ ] Check for all `TODO` & `XXX` within code
* [ ] Better/More comments 
* [ ] `settings.json` to load personnalized settings of user