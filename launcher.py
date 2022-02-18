import json
import numpy
import subprocess
import os
import threading


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


def browser_instances_ran():
    with open("config.json", "r") as fp:
        folder_lnk = "links"
        json_props = json.load(fp)
        split_on = json_props["concurrent_instances"]
        lnk_files = os.listdir(folder_lnk)
        print("[+] Links found:: " + str(len(lnk_files)))
        list_split_on = int(len(lnk_files) / split_on)
        print("[+] list_split_on:: " + str(list_split_on))
        nmp_array = numpy.array_split(numpy.array(lnk_files), list_split_on)
        print("[+] div:: " + str(len(nmp_array)))
        threads_lst = []

        for current_iter in range(json_props["total_iterations"]):
            print("[+] Global iteration:: " + str(current_iter))

            for c_array in nmp_array:
                for one_array in c_array:
                    lnk_full_path = os.getcwd() + "\\" + folder_lnk + "\\" + one_array
                    thr_obj = threading.Thread(target=ran_python_script, args=["python", "browser_stress.py",  lnk_full_path])
                    thr_obj.start()
                    threads_lst.append(thr_obj)

                check_threads(threads_lst)


                print("[+] Next...")
        print("[+] Finish script")


browser_instances_ran()
