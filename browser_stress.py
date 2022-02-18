from selenium import webdriver
import LnkParse3
import time
import os
import sys
import json
import glob
import shutil


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


def get_user_data_dir_tmp(flag):

    if flag is 0x1:
        tmp = os.environ["tmp"] + "\\brave-test\\"
        if os.path.isdir(tmp) is False:
            os.mkdir(tmp)

        tmp += "user_data\\"
        if os.path.isdir(tmp) is False:
            os.mkdir(tmp)

        return tmp

    return None


def ran_instance(executable_path, param2, lnk_data, instance_info):
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.binary_location = lnk_data["browser_path"]

    # check profile path
    if lnk_data["profile_path"] is not None:
        # Get profile target from original path
        profile_folder_path = lnk_data["profile_path"].replace("\"", "")
        path = os.environ["LOCALAPPDATA"] + "\\"
        files = glob.glob(path + 'BraveSoftware\\Brave*')
        current_user_data = files[0] + "\\User Data\\"
        current_user_data_dir = current_user_data + profile_folder_path

        # cp current User Data to tmp dir
        new_user_data_dir = get_user_data_dir_tmp(0x1)
        user_data_folders = os.listdir(new_user_data_dir)
        new_user_data_dir += profile_folder_path + "-" + str(len(user_data_folders))
        origin_base_folder = os.getcwd() + "\\" + "base"
        shutil.copytree(origin_base_folder, new_user_data_dir)
        data_dir = 'user-data-dir=' + new_user_data_dir
        chrome_opts.add_argument(data_dir)

        # cp target Profile to tmp dir
        new_profile_dir = new_user_data_dir + "\\" + profile_folder_path + "\\"
        shutil.copytree(current_user_data_dir, new_profile_dir)

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
    wdriv.execute_script("window.open('','_blank');")
    # wdriv.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    wdriv.switch_to.window(wdriv.window_handles[1])
    wdriv.get("brave://newtab")

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
    if len(sys.argv) is not 2:
        print("[!] You don't ranme!")
        exit(0xF)

    with open("fail.log", "a") as fp_log:
        with open("config.json", "r") as fp_cfg:
            json_props = json.load(fp_cfg)
            exec_path = get_driver_path()
            print("[+] You Driver path:: " + exec_path)
            print("[+] You lnk:: " + sys.argv[1])

            lnk_info = parse_lnk(sys.argv[1])
            ran_instance(exec_path, None, lnk_info, json_props)


ran()
