# coding=utf-8
from Base.action import Action,browser


base_url = "https://mpss.mindray.com/Login.aspx?ru=9a4aoaZO3ejM9GQIU8snydU6sBSEvil1o2s%2bNFZrstNCZBoyZoGOxJjTzn%2bO%2bbN0"


class LoginPage(Action):
    username_loc = ("css selector", "input[id='login_name'][name='login_name']")
    password_loc = ("css selector", "input[id='password'][name='password1']")
    verify_code_loc = ("id", "authcodeimg")
    verify_code_text_loc = ("css selector", "input[id='txtauthcode'][name='txtauthcode']")
    login_button = ("css selector", "input[id='proxy_login'][class='login_btn']")

    def input_username(self):
        self.send_key(self.username_loc, "********")

    def input_password(self):
        self.send_key(self.password_loc, "********")

    def input_verify_code(self):
        self.send_key(self.verify_code_text_loc, self.get_verify_code(self.verify_code_loc))

    def click_login(self):
        self.click(self.login_button)

