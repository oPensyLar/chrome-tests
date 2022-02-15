import json
import numpy
import subprocess
import os


def browser_instances_ran():
    with open("config.json", "r") as fp:
        folder_lnk = "links"
        json_props = json.load(fp)
        split_on = json_props["concurrent_instances"]
        lnk_files = os.listdir(folder_lnk)
        list_split_on = int(len(lnk_files) / split_on)
        nmp_array = numpy.array_split(numpy.array(lnk_files), list_split_on)
        process_lst = []

        for current_iter in range(json_props["total_iterations"]):
            print("[+] Global iteration:: " + str(current_iter))

            for c_array in nmp_array:
                for one_array in c_array:
                    lnk_full_path = os.getcwd() + "\\" + folder_lnk + "\\" + one_array
                    proc = subprocess.Popen(["python", "browser_stress.py",  lnk_full_path])
                    process_lst.append(proc)

                procs_alive = True

                while procs_alive:
                    for current_proc in process_lst:
                        if current_proc.poll() is None:
                            procs_alive = True
                            break

                        else:
                            procs_alive = False

                print("[+] Next...")
        print("[+] Finish script")


browser_instances_ran()
