import json
import numpy
import subprocess
import os
import time
from concurrent import futures
import shutil
import glob
from selenium import webdriver
import LnkParse3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


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


def check_threads(threads_lst):
    threads_running = True

    while threads_running:
        for current_thr in threads_lst:
            if current_thr.is_alive():
                threads_running = True
                break

            else:
                threads_running = False


def ran_python_script(interpreter, dotpy, lnk_path):
    proc = subprocess.Popen([interpreter, dotpy, lnk_path])
    std_out, std_error = proc.communicate()
    # print("stdout: " + std_error)

    if std_error is not None:
        print("stderr: " + std_error)
        exit(0)


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


def ran_instance(executable_path, param2, lnk_data, instance_info, root_path):
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
        new_user_data_dir = root_path
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

    wdriv.set_page_load_timeout(200)

    try:
        wdriv.get("brave://newtab")

    except TimeoutException:
        print("Closing instance")
        wdriv.service.stop()
        return
        # wdriv.quit()
        # wdriv.close()

    # loop main
    for c_num_refresh in range(instance_info["tabs"]["tab1"]["refresh_count"]):
        print("Iter:: " + str(c_num_refresh) + " step:: 0x1")
        wdriv.refresh()
        time.sleep(instance_info["tabs"]["tab1"]["velocity_refresh"])

    # loop new tab
    wdriv.execute_script("window.open('','_blank');")
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


def get_driver_path():
    driver_dir = os.getcwd() + "\\driver\\"
    drivers = os.listdir(driver_dir)

    if len(drivers) == 0x0:
        print("[!] FAIL! Chromium not found in " + driver_dir)
        exit(0x0)

    return driver_dir + drivers[0]


def fn1(root_dir, json_props, lnk_folder, lnk_name):
    exec_path = get_driver_path()
    lnk_full_path = lnk_folder + "\\" + lnk_name
    lnk_info = parse_lnk(lnk_full_path)

    # def ran_instance(executable_path, param2, lnk_data, instance_info, root_path):
    ran_instance(exec_path, None, lnk_info, json_props, root_dir)


def browser_instances_ran():
    with open("config.json", "r") as fp:
        tmp_path = get_user_data_dir_tmp(0x1)
        folder_lnk = "links"
        json_props = json.load(fp)
        split_on = json_props["concurrent_instances"]
        lnk_files = os.listdir(folder_lnk)
        list_split_on = int(len(lnk_files) / split_on)
        nmp_array = numpy.array_split(numpy.array(lnk_files), list_split_on)
        threads_lst = []

        for current_iter in range(json_props["total_iterations"]):
            print("[+] Global iteration:: " + str(current_iter))

            for c_array in nmp_array:
                with futures.ThreadPoolExecutor() as executor:
                    future_test_results = [executor.submit(fn1, tmp_path, json_props, folder_lnk, one_array) for one_array in c_array]

                    for future_test_result in future_test_results:
                        test_result = future_test_result.result()

                print("[+] Next...")

        print("[+] Finish script")
        if os.path.isdir(tmp_path):
            try:
                shutil.rmtree(tmp_path)
            except:
                exit(0)


def test_one_instance():
    with open("config.json", "r") as fp:
        json_props = json.load(fp)
        root_dir = get_user_data_dir_tmp(0x1)
        exec_path = get_driver_path()
        lnk_full_path = "links\\4.lnk"
        lnk_info = parse_lnk(lnk_full_path)

        ran_instance(exec_path, None, lnk_info, json_props, root_dir)



browser_instances_ran()
# test_one_instance()
