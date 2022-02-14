import threading
import subprocess


class ThreadProgram(object):

    def __init__(self, path_exec):
        self.p_exec = path_exec
        self.process = None
        self.std_out = None
        self.std_error = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.p_exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.std_out, self.std_error = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)

        if thread.is_alive():
            self.process.terminate()
            thread.join()