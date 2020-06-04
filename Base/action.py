# coding=utf-8
# selenium二次封装
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 处理鼠标事件
from selenium.webdriver.support.select import Select  # 用于处理下拉框
from selenium.common.exceptions import *  # 用于处理异常
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # 用于处理元素等待
from PIL import Image, ImageEnhance
import pytesseract, re
import time
import sys


# reload(sys)
# sys.setdefaultcoding('utf-8')


def browser(browser):
    try:
        if browser == "chrome":
            driver = webdriver.Chrome()
            return driver
        elif browser == "firefox":
            driver = webdriver.Firefox()
            return driver
        elif browser == "ie":
            driver == webdriver.Ie()
            return driver
        elif browser == "phantomjs":
            driver = webdriver.PhantomJS()
            return driver
        else:
            print("Not found this browser, You can enter 'chrome','firefox','ie' or 'phantomjs'")
    except Exception as msg:
        print
        "%s" % msg


class Action(object):

    def __init__(self, driver):
        self.driver = driver

    def open(self, url, title='', timeout=10):
        u"""打开浏览器，并最大化，判断title是否为预期"""
        self.driver.get(url)
        self.driver.maximize_window()
        try:
            WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        except TimeoutException:
            print("open %s title error" % url)
        except Exception as msg:
            print("Error:%s" % msg)

    def find_element(self, locator, timeout=10):
        u"""定位元素，参数locator为原则"""
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            return element
        except:
            print("%s 页面未找到元素 %s" % (self, locator))

    def find_elements(self, locator, timeout=10):
        u"""定位一组元素"""
        elements = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
        return elements

    def click(self, locator):
        u"""封装点击操作"""
        element = self.find_element(locator)
        element.click()

    def send_key(self, locator, text):
        u"""发送文本后清除内容"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def is_text_in_element(self, text, locator, timeout=10):
        u"""判断是否定位到元素"""
        try:
            WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(locator, text))
            return True
        except TimeoutException:
            print("元素未定位到:" + str(locator))

    def is_title(self, title, timeout=10):
        u"""判断title完全相等"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        u"""判断是否包含title"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_select(self, locator, timeout=10):
        u"""判断元素是否被选中"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(locator))
        return result

    def is_select_be(self, locator, timeout=10, selected=True):
        u"""判断元素的状态"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(locator, selected))

    def is_alert_present(self, timeout=10):
        u"""判断页面有无alert弹出框，有alert返回alert，无alert返回FALSE"""
        try:
            return WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        except:
            print( "No Alert Present")

    def is_visibility(self, locator, timeout=10):
        u"""判断元素是否可见，可见返回本身，不可见返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator))

    def is_invisibility(self, locator, timeout=10):
        u"""判断元素是否可见，不可见，未找到元素返回True"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator))

    def is_clickable(self, locator, timeout=10):
        u"""判断元素是否可以点击，可以点击返回本身，不可点击返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(locator))

    def is_located(self, locator, timeout=10):
        u"""判断元素是否定位到（元素不一定是可见），如果定位到返回Element，未定位到返回FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))

    def find_element_click(self, locator):
        u"""鼠标悬停操作"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        u"""返回到旧的窗口"""
        self.driver.back()

    def forward(self):
        u"""前进到新窗口"""
        self.driver.forward()

    def close(self):
        u"""关闭窗口"""
        self.driver.close()

    def switch_frame(self,element):
        self.driver.switch_to.frame(element)

    def switch_alert(self):
        self.driver.switch_to_alert()

    def quit(self):
        u"""关闭driver和所有窗口"""
        self.driver.quit()

    def get_title(self):
        u"""获取当前窗口的title"""
        return self.driver.title

    def get_current_url(self):
        u"""获取当前页面url"""
        return self.driver.current_url

    def get_text(self, locator):
        u"""获取文本内容"""
        return self.find_element(locator).text

    def get_browser_log_level(self):
        u"""获取浏览器错误日志级别"""
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    list_value.append(value)
        if 'SEVERE' in list_value:
            return "SEVERE"
        elif 'WARNING' in list_value:
            return "WARNING"
        return "SUCCESS"

    def get_attribute(self, locator, name):
        u"""获取属性"""
        ele = self.find
        return self.find(locator).get_attribute(name)

    def get_screen_as_file(self, func):
        u"""异常自动截图"""
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except:
                self.screen()
                raise
        return inner

    def screen(self):
        u"""浏览器页面截图"""
        nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.driver.get_screenshot_as_file("%s.png" % nowtime)

    def js_execute(self, js):
        u"""执行js"""
        return self.driver.execute_script(js)

    def js_fours_element(self, locator):
        u"""聚焦元素"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_scroll_top(self):
        u"""滑动到页面顶部"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        u"""滑动到页面底部"""
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, locator, index):
        u"""通过所有index，0开始,定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        u"""通过value定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        u"""通过text定位元素"""
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def get_verify_code(self, locator):
        u"""获取图片验证码"""
        # 验证码图片保存地址
        screenImg = "D:/image/verifyCode.png"
        # 浏览器页面截图
        self.driver.get_screenshot_as_file(screenImg)

        # 定位验证码大小
        location = self.find_element(locator).location
        size = self.find_element(locator).size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        # 从文件读取截图，截取验证码位置再次保存
        img = Image.open(screenImg).crop((left, top, right, bottom))
        img.convert('L')  # 转换模式：L|RGB
        img = ImageEnhance.Contrast(img)  # 增加对比度
        img = img.enhance(2.0)  # 增加饱和度
        img.save(screenImg)

        # 再次读取验证码
        img = Image.open(screenImg)
        time.sleep(1)
        code = pytesseract.image_to_string(img)
        return code

