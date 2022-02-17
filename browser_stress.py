from selenium import webdriver
import LnkParse3
import time
import os
import sys
import json
import glob


def parse_lnk(lnk_path):
    ret_str = None

    with open(lnk_path, 'rb') as fp:
        lnk_props = LnkParse3.lnk_file(fp)
        lnk_json_data = lnk_props.get_json()
        str_to_find = "--profile-directory="

        if lnk_json_data['data'].get('command_line_arguments') is not None:
            profile_directory_found = lnk_json_data['data']['command_line_arguments'].find(str_to_find) + len(str_to_find)
            param = lnk_json_data['data']['command_line_arguments'][profile_directory_found:]

            browse_full_path = lnk_json_data['link_info']['local_base_path']

            if os.path.isfile(browse_full_path) is False:
                browse_full_path = None

        ret_obj = {"filename": lnk_path,  "profile_path": param, "browser_path": browse_full_path}

        return ret_obj


def ran_instance(executable_path, lnk_data, instance_info):
    chrome_opts = webdriver.ChromeOptions()
    data_dir = ""
    chrome_opts.binary_location = lnk_data["browser_path"]

    # check profile path
    if lnk_data["profile_path"] is not None:
        profile_folder_path = lnk_data["profile_path"].replace("\"", "")
        path = os.environ["LOCALAPPDATA"] + "\\"
        files = glob.glob(path + 'BraveSoftware\\Brave*')
        final_path = files[0] + "\\User Data"

        # data_dir = 'user-data-dir=' + final_path
        # chrome_opts.add_argument(data_dir)

        profile_dir = "profile-directory=" + profile_folder_path
        chrome_opts.add_argument(profile_dir)

    wdriv = webdriver.Chrome(executable_path=executable_path, options=chrome_opts)

    wdriv.get("brave://newtab")

    # loop main
    for c_num_refresh in range(instance_info["tabs"]["tab1"]["refresh_count"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x1")
        wdriv.refresh()
        time.sleep(instance_info["tabs"]["tab1"]["velocity_refresh"])

    # loop new tab
    wdriv.execute_script("window.open('brave://newtab','_blank');")
    wdriv.switch_to.window(wdriv.window_handles[1])
    for c_num_refresh in range(instance_info["tabs"]["tab2"]["refresh_count"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x2")
        wdriv.refresh()
        time.sleep(instance_info["tabs"]["tab2"]["velocity_refresh"])

    wdriv.close()

    # main tab again
    wdriv.switch_to.window(wdriv.window_handles[0])
    for c_num_refresh in range(instance_info["tabs"]["tab1_1"]["refresh_count"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x3")
        wdriv.refresh()
        time.sleep(instance_info["tabs"]["tab1_1"]["velocity_refresh"])

    print("[+] Closing browser instance")
    wdriv.quit()


def read_lnk(path):
    ret_data = []

    for file in os.listdir(path):
        final_path = path + "\\" + file
        lnk_info = parse_lnk(final_path)

        if lnk_info["browser_path"] is not None:
            ret_data.append(lnk_info)

        else:
            print("[!] Browser in " + lnk_info["filename"] + " not found!")

    return ret_data


def get_driver_path():
    driver_dir = os.getcwd() + "\\driver\\"
    drivers = os.listdir(driver_dir)

    if len(drivers) == 0x0:
        print("[!] FAIL! Chromium not found in " + driver_dir)
        exit(0x0)

    return driver_dir + drivers[0]


def ran():

    if len(sys.argv) is 0:
        print("[!] Need .lnk param")
        exit(0xF)

    with open("fail.log", "a") as fp_log:
        with open("config.json", "r") as fp_cfg:
            json_props = json.load(fp_cfg)
            lnk_files = read_lnk("links")
            exec_path = get_driver_path()
            print("[+] You Driver path:: " + exec_path)

            lnk_info = parse_lnk(sys.argv[1])
            ran_instance(exec_path, lnk_info, json_props)

ran()
