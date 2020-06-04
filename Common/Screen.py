# coding=utf-8
import time

class Screen(object):
    def __init__(self, driver):
        self.driver = driver

    def __call__(self, func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                from Common.function import project_path
                nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(project_path()+"/Image/"+"%s.png" % nowtime)
                raise
        return inner

