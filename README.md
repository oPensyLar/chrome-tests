# Chrome stress tests
Simple Pythont test script for Chrome/Chromium bench/stress tests (running  multi instances)



# Deploying :rocket:


### Before run..

Please check you Chrome/Chomium version

![Screenshot version](https://github.com/oPensyLar/chrome-tests/raw/master/images/chrome-version.png)


Now download you driver from [Chromium.org](https://chromedriver.chromium.org/downloads)

![Screenshot download](https://github.com/oPensyLar/chrome-tests/raw/master/images/download-chrome-driver.png)


Ok, now install Python deps

```
pip -r requeriments.txt
```


Last step, edit you config.json
```json
{
	"driver_path" : "P:\\tools\\chromium-driver\\chromedriver_win32-97\\chromedriver.exe",
	"refresh_count" : 20,
	"velocity_refresh" : 0
}
```

* refresh_count
Times to refresh tab

* velocity_refresh
Secs to refresh tab

* driver_path
Path you driver (please check you Chrome version before download driver)


Now ran :blush:

```
python main.py
```



### Script Tests env

*  Python3 (Anaconda works)
*  Windows 10/11 x64
*  Chrome/Chormium works



## Screenshots
---

![Screenshot index](https://github.com/oPensyLar/chrome-tests/raw/master/images/deploy.gif)
