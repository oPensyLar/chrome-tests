from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os
import LnkParse3


def parse_lnk(lnk_path):
    ret_str = None

    with open(lnk_path, 'rb') as fp:
        lnk_props = LnkParse3.lnk_file(fp)
        lnk_json_data = lnk_props.get_json()
        str_to_find = "--profile-directory="

        if lnk_json_data['data'].get('command_line_arguments') is not None:
            start_on = lnk_json_data['data']['command_line_arguments'].find(str_to_find) + len(str_to_find)
            ret_str = lnk_json_data['data']['command_line_arguments'][20:]

        ret_obj = {"filename": lnk_path,  "profile_path": ret_str}

        return ret_obj


def ran_instance(executable_path, data_instance):
    chrome_opts = webdriver.ChromeOptions()

    # check profile path
    if data_instance["args"]["profile_path"] is not None:
        data_dir = 'user-data-dir=' + data_instance["profile_folder"]["'profile_path'"]
        chrome_opts.add_argument(data_dir)

    wdriv = webdriver.Chrome(executable_path=executable_path, options=chrome_opts)

    # loop main
    wdriv.get("chrome://new-tab-page")
    for c_num_refresh in range(data_instance["num_refresh"]):
        wdriv.refresh()
        time.sleep(2)

    # loop new tab
    wdriv.execute_script('''window.open("chrome://new-tab-page","_blank");''')
    wdriv.switch_to.window(wdriv.window_handles[1])
    for c_num_refresh in range(data_instance["num_refresh"]):
        wdriv.refresh()
        time.sleep(6)

    wdriv.close()

    # main tab again
    wdriv.switch_to.window(wdriv.window_handles[0])
    for c_num_refresh in range(data_instance["num_refresh"]):
        wdriv.refresh()
        time.sleep(2)

    print("[+] Closing browser instance")
    wdriv.quit()


def read_lnk(path):
    ret_data = []

    for file in os.listdir(path):
        final_path = path + "\\" + file
        ret_data.append(parse_lnk(final_path))

    return ret_data


def deploy():
    lnk_cmds_line = read_lnk("links")
    exec_path = "P:\\tools\\chromium-driver\\chromedriver_win32-97\\chromedriver.exe"

    for cmd_line in lnk_cmds_line:
        data_cfg = {"num_refresh": 10, "velocity_refresh": 10, "args": cmd_line}
        ran_instance(exec_path, data_cfg)

    print("[+] Finish script")


deploy()
