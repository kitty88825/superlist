from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        # 將 URL 解析為網站的根目錄("/")，指向我們製作的特定 view 函式
        # view 函式會回傳 HTML
