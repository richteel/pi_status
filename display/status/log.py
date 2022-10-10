from genericpath import exists
import os
import time
import sys


class log(object):
    def __init__(self, time_format="%Y-%m-%d %H:%M:%S", log_file="", err_file="", verbose_file=""):
        self.time_format = time_format
        self.log_file = log_file
        self.err_file = err_file
        self.verbose_file = verbose_file
        if self.err_file and os.path.exists(self.err_file):
            self.err_print()
        if self.log_file and os.path.exists(self.log_file):
            self.log_print()
        if self.verbose_file and os.path.exists(self.verbose_file):
            self.verbose_print()

    def _create_log_dir(self, filename):
        if not filename:
            return False

        log_path = os.path.realpath(os.path.dirname(filename))

        if os.path.exists(log_path):
            return True

        try:
            os.mkdir(log_path)
        except FileExistsError as error:
            self._err_print(
                "Create Log Directory Error: Log folder already exists -> {0}".format(error))
        except FileNotFoundError as error:
            self._err_print(
                "Create Log Directory Error: Specified folder does not exist -> {0}".format(error))

        return os.path.exists(log_path)

    def _err_print(self, *args, **kwargs):
        s = time.localtime()
        log_text = time.strftime(self.time_format, s)
        for arg in args:
            log_text += "\t{0}".format(arg)
        print(log_text, file=sys.stderr, flush=True, **kwargs)

        return log_text

    def _log_print(self, *args, **kwargs):
        s = time.localtime()
        log_text = time.strftime(self.time_format, s)
        for arg in args:
            log_text += "\t{0}".format(arg)
        print(log_text, file=sys.stdout, flush=True, **kwargs)

        return log_text

    def err_print(self, *args, **kwargs):
        log_text = ""

        if len(args) > 0:
            log_text = self._err_print(*args, **kwargs)

        if not self.err_file:
            return

        if not self._create_log_dir(self.log_file):
            return

        with open(self.err_file, "a") as f:
            print(log_text, file=f, flush=True, **kwargs)

    def log_print(self, *args, **kwargs):
        log_text = ""

        if len(args) > 0:
            log_text = self._log_print(*args, **kwargs)

        if not self.log_file:
            return

        if not self._create_log_dir(self.log_file):
            return

        with open(self.log_file, "a") as f:
            print(log_text, file=f, flush=True, **kwargs)

    def verbose_print(self, *args, **kwargs):
        if not self.verbose_file:
            return

        s = time.localtime()
        log_text = time.strftime(self.time_format, s)

        if len(args) == 0:
            log_text = ""

        if not self._create_log_dir(self.log_file):
            return

        with open(self.verbose_file, "a") as f:
            for arg in args:
                log_text += "\t{0}".format(arg)
            print(log_text, file=f, flush=True, **kwargs)
