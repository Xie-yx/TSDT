# from selenium import webdriver

# browser = webdriver.Chrome()

# #张三听说有一个在线待办事项的应用
# #他去看了这个应用的首页
# browser.get('http://localhost:8000')

# #他注意到网页里包含“To-Do”这个词
# assert 'To-Do' in browser.title,"Browser title was " + browser.title

# #应用有一个输入待办事项的文本输入框

# #他在文本输入框中输入了“Buy flowers”

# #他按了回车键键后，页面更新了
# #代办事项表格中显示了“1：Buy flowers”

# #页面中又显示了一个文本输入框，可以输入其他待办事项
# #他输入了“Send a gift to List”

# #页面再次更新，他的清单中显示了这两个代办事项

# #张三想知道这个网站是否会记住他的清单
# #他看到网站为他生成了一个唯一的URL

# #他访问了那个URL，发现他的代办事项列表还在
# #他满意的离开了

# browser.quit()


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        real_server = os.environ.get('REAL_SERVER')
        if real_server:
            self.live_server_url = 'http://' + real_server
        
    def tearDown(self):
        self.browser.quit()
        
    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return 
            except(AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
                
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三创建了一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy flowers")

        # 他注意到清单有一个唯一的URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists.+') #(1)

        # 新用户王五访问网站
        # 使用一个心得浏览器会话
        # 确保张三的信息不会从cookie泄露
        self.browser.quit()
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--incognito")  # 添加无痕模式
        self.browser = webdriver.Chrome(options=chrome_options)

        # 王五访问首页
        # 页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertNotIn('Give a gift to Lisi', page_text)

        # 王五输入了一个新待办事项，新建一个清单
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')


        # 王五获得了他的唯一URL
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url, '/lists/.+')
        self.assertNotEqual(wangwu_list_url, zhangsan_list_url)        

        # 这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy flowers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两人都很满意

                        
    def test_can_start_a_list_and_retrieve_it_later(self):
        
        # #张三听说有一个在线待办事项的应用
        # #他去看了这个应用的首页
        self.browser.get(self.live_server_url)
        
        #他注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)
        
        #应用有一个输入待办事项的文本输入框
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        #他在文本输入框中输入了“Buy flowers”
        inputbox.send_keys('Buy flowers')
        
        #他按回车键后，页面更新了
        #代办事项表格中显示了“1：Buy flowers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy flowers')
        
        
        #页面中又显示了一个文本输入框，可以输入其他待办事项
        #他输入了“Send a gift to List”
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        
         #页面再次更新，他的清单中显示了这两个代办事项
        self.wait_for_row_in_list_table('1: Buy flowers')
        self.wait_for_row_in_list_table('2: Give a gift to Lisi')


        #他满意的离开了。
            
    
    
    
    def test_layout_and_styling(self):
        #张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        
        #他看到输入框完美地居中显示。
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2 ,
            512,
            delta=10
            )
        
        #他新建了一个清单，看到输入框仍然完美的居中显示。
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2 ,
            512,
            delta=10
            )