# Chrome stress tests
Simple Pythont test script for Chrome/Chromium/Brave bench/stress tests lauching from .lnk (running  multi instances)



# Deploying :rocket:


### Before run..

Please check you Chrome/Chomium/Brave version

![Screenshot version](https://github.com/oPensyLar/chrome-tests/raw/master/images/chrome-version.png)


Download you driver from [Chromium.org](https://chromedriver.chromium.org/downloads)

![Screenshot download](https://github.com/oPensyLar/chrome-tests/raw/master/images/download-chrome-driver.png)


Drop Chrome driver in ```driver``` folder

Drop you .lnk files in ```links``` folder


Ok, now install Python deps

```
pip -r requeriments.txt
```


Last step, edit you config.json
```json
{
	"refresh_count" : 20,
	"velocity_refresh" : 0
}
```

* refresh_count
Times to refresh tab

* velocity_refresh
Secs to refresh x tab


Now ran :blush:

```
python main.py
```



### Script Tests env

*  Python3 (Anaconda works)
*  Windows 10/11 x64
*  Chrome/Chormium/Brave works



## Screenshots
---

![Screenshot index](https://github.com/oPensyLar/chrome-tests/raw/master/images/deploy.gif)
