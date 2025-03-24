from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import tempfile

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox")          # 禁用沙箱
        # chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享内存问题
        chrome_options.add_argument("--headless=new")        # 无头模式（可选）
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title),"Browser title was " + self.browser.title
        self.fail("Finish the test!")



    # 应用有一个输入代办事项的文本输入框

    # 他在文本输入框中输入了"Buy flowers"

    # 他按了回车键后，页面更新了
    # 代办事项表格中显示了"1: Buy flowers"

    # 页面中又显示了一个文本输入框，可以输入其他代办事项
    # 他输入了"Send a gift to Lisi"

    # 页面再次更新，清单中显示了这两个代办

    # 张三想知道这个网站是否会记住他的清单
    # 他看到网站为他生成了要给唯一的URL

    # 他访问那个URL，发现待办列表还在

if __name__ == '__main__':
    unittest.main()