from concurrent import futures
from selenium import webdriver
import time
import os
import LnkParse3
import json


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


def ran_instance(executable_path, data_instance, cfg_instance):
    chrome_opts = webdriver.ChromeOptions()

    # check profile path
#    if data_instance["profile_path"] is not None:
#        data_dir = 'user-data-dir=' + data_instance["profile_path"]
#        chrome_opts.add_argument(data_dir)

    chrome_opts.binary_location = data_instance["browser_path"]

    wdriv = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_opts)

    # loop main
    wdriv.get("chrome://new-tab-page")

    for c_num_refresh in range(cfg_instance["num_refresh"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x1")
        wdriv.refresh()
        time.sleep(cfg_instance["velocity_refresh"])

    # loop new tab
    wdriv.execute_script('''window.open("chrome://new-tab-page","_blank");''')
    wdriv.switch_to.window(wdriv.window_handles[1])
    for c_num_refresh in range(cfg_instance["num_refresh"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x2")
        wdriv.refresh()
        time.sleep(cfg_instance["velocity_refresh"])

    wdriv.close()

    # main tab again
    wdriv.switch_to.window(wdriv.window_handles[0])
    for c_num_refresh in range(cfg_instance["num_refresh"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x3")
        wdriv.refresh()

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


def real_deploy(exec_path, lnk_props, cfg):
    print("[+] Running " + lnk_props["filename"])
    ran_instance(exec_path, lnk_props, cfg)


def get_driver_path():
    driver_dir = os.getcwd() + "\\driver\\"
    drivers = os.listdir(driver_dir)

    if len(drivers) == 0x0:
        print("[!] FAIL! Chromium not found in " + driver_dir)
        exit(0x0)

    return driver_dir + drivers[0]


def deploy_threads():
    with open("config.json", "r") as fp:
        json_props = json.load(fp)
        lnk_props = read_lnk("links")
        exec_path = get_driver_path()
        data_cfg = {"num_refresh": json_props["refresh_count"], "velocity_refresh": json_props["velocity_refresh"]}
        thread_list = list()

        print("[+] You Driver path:: " + exec_path)

        with futures.ThreadPoolExecutor() as executor:
            future_test_results = [executor.submit(real_deploy, exec_path, one_lnk_prop, data_cfg) for one_lnk_prop in lnk_props]
            for future_test_result in future_test_results:
                try:
                    test_result = future_test_result.result()

                except Exception as exc:
                    print('thread generated an exception: {:0}'.format(exc))

        print("[+] Finish script")


deploy_threads()
