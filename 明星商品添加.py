from selenium import webdriver
import time


class Zutuan():
    def __init__(self):
        """打开浏览器"""
        self.driver = webdriver.Chrome()

    def open_zutuan(self,url):
        """传入组团url"""
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(0.01)

    def option_element(self,email,password):
        """手写xpath定位元素"""
        self.driver.find_element_by_xpath('//div[@class="login a"]/i').click()
        time.sleep(0.01)
        self.driver.find_element_by_xpath('//div[@class="a-title"]').click()
        self.driver.find_element_by_xpath('//input[@type="text" or @class="userName"]').send_keys(email)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//div[@class="button"]').click()
        time.sleep(0.1)

    def select_commodity(self,content):
        """搜索组团商品"""
        #self.driver.refresh()
		self.content = content
        self.driver.find_element_by_xpath('//input[@type="text"]').send_keys(content)
        self.driver.find_element_by_xpath('//div[@class="search"]').click()
		return content()
		
    def result(self):
        """判断搜索商品成功后的提示信息，断言页面是否成功"""
        if self.content in self.driver.page_source:
            print('商品搜索成功，测试通过')
        else:
            print('搜索错误，测试失败')

    def closed(self):
        """关闭浏览器"""
        time.sleep(1)
        self.driver.quit()

def main():
    # TODO 根据操作顺序，调用方法执行
    zt = Zutuan()
    zt.open_zutuan('http://www.zutuan.cn/index.html#/')
    zt.option_element()
    zt.select_commodity('苹果')
    zt.result()
    zt.closed()


if __name__ == '__main__':
    main()


class View_details(Zutuan):
    """把商品添加为明星单品，这里有个坑，即窗口句柄的问题
    解决思路，先分别打印跳转之前和跳转之后的句柄，
    打印出来是列表，然后用switch_to.window通过下标取值的方式，选择跳转到哪个窗口"""
    def check_commodity(self,number):
        # 跳转之前打印句柄
        headle1 = self.driver.window_handles
        print(headle1)
        self.driver.find_element_by_xpath('//a[@target="_blank"]/img').click()
        time.sleep(2)
        # 跳转之后打印句柄
        headle = self.driver.window_handles
        print(len(headle))
        print(headle)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//div[@class="child start"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@class="el-dialog__body"]//input[@type="text"]').send_keys(number)
        time.sleep(1)
        self.driver.find_element_by_xpath('//button[@type="button" and @class="el-button el-button--danger"]').click()
        time.sleep(1)


    def result(self):
        """重写父类方法，判断商品添加成功后的提示信息，断言页面是否成功"""
        if '添加成功' in self.driver.page_source:
            print('商品添加成功，测试通过')
        else:
            print('添加失败，测试失败')
        time.sleep(1)
        # 调用父类方法关闭
        super().closed()

def main():
    vd = View_details()
    vd.open_zutuan('http://www.zutuan.cn/index.html#/')
    vd.option_element()
    vd.select_commodity('苹果')
    vd.check_commodity(800)
    vd.result()


if __name__ == '__main__':
    main()
