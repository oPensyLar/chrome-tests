# Chrome stress tests
Simple Pythont test script for Chrome/Chromium bench/stress tests (running  multi instances)



# Deploying :rocket:


### Before run..

Please check you Chrome/Chomium version


Now download you driver from:




Ok, now install Python deps

```
pip -r requeriments.txt
```


last step, edit you config.json
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

:white_check_mark: Python3 (Anaconda works)
:white_check_mark: Windows 10/11 x64
:white_check_mark: Chrome/Chormium works



## Screenshots
---

![Screenshot index](https://i.imgur.com/TPZsef6.png)
