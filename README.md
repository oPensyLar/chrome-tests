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

	"concurrent_instances": 20,
	"total_iterations" : 10,

	"tabs" : {

		"tab1":
		{
			"refresh_count" : 90,
			"velocity_refresh" : 0
		},

		"tab2":
		{
			"refresh_count" : 80,
			"velocity_refresh" : 0
		},

		"tab1_1":
		{
			"refresh_count" : 40,
			"velocity_refresh" : 0
		}
	}
}
```

* total_iterations
Total loops to lauch

* concurrent_instances
Process concurrent lauch

* tab1, tab2, tab1_1
Tab1 = first tab, Tab2 = second tab, Tab1_1 = close tab2 back tab1


Now ran :blush:

```
python launcher.py
```



### Script Tests env

*  Python3 (Anaconda works)
*  Windows 10/11 x64
*  Chrome/Chormium/Brave/Brave Nightly works



## Screenshots
---

![Screenshot index](https://github.com/oPensyLar/chrome-tests/raw/master/images/deploy.gif)
