from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from django.test import Client, TestCase
from django.db.models import Max

from .models import User, Posts, Profile

class WebpageTests(StaticLiveServerTestCase):
    driver = None
    port = 8000

    @classmethod    
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def testform(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        self.assertEqual(driver.title, "Social Network")

# Create your tests here.
class NetworkTestCase(TestCase):

    def setUp(self):
        
        #Create Users
        user01 = User.objects.create_user(username="Test-01",password="test")
        user02 = User.objects.create_user(username="Test-02",password="test")
        user03 = User.objects.create_user(username="Test-03",password="test")
        user04 = User.objects.create_user(username="Test-04",password="test")

        #Create User profile
        Profile.objects.create(userId=user01)
        Profile.objects.create(userId=user02)
        Profile.objects.create(userId=user03)
        Profile.objects.create(userId=user04)

    def test_user_post(self):

        user01 = User.objects.get(username="Test-01")

        #Post 10 times
        for n in range(10):
            Posts.objects.create(postUser=user01, postDescription="Hello")

        post = Posts.objects.filter(postUser=user01)

        self.assertEqual(post.count(), 10)
        
    def test_user_follow(self):
        
        user01 = User.objects.get(username="Test-01")
        user02 = User.objects.get(username="Test-02")

        #follow Test-02
        loginUser = Profile.objects.get(userId=user01)
        loginUser.following.add(user02)

        #Test-01 add as follower of Test-02
        userFollowed = Profile.objects.get(userId=user02)
        userFollowed.followers.add(user01)

        self.assertEqual(loginUser.following.all().count(), 1)

        self.assertEqual(userFollowed.followers.all().count(), 1)

    def test_user_unfollow(self):
        
        user01 = User.objects.get(username="Test-01")
        user02 = User.objects.get(username="Test-02")
        user03 = User.objects.get(username="Test-03")
        user04 = User.objects.get(username="Test-04")

        #3 users Follows Test-02
        loginUser01 = Profile.objects.get(userId=user01)
        loginUser01.following.add(user02)
        
        loginUser03 = Profile.objects.get(userId=user03)
        loginUser03.following.add(user02)
        
        loginUser04 = Profile.objects.get(userId=user04)
        loginUser04.following.add(user02)

        #3 users added as followers of Test-02
        userFollowed = Profile.objects.get(userId=user02)
        userFollowed.followers.add(user01)
        userFollowed.followers.add(user03)
        userFollowed.followers.add(user04)

        #But Test-01 unfollow Test-02
        userFollowed.followers.remove(user01)
        loginUser01.following.remove(user02)
        
        self.assertEqual(loginUser01.following.all().count(), 0)
        self.assertEqual(loginUser03.following.all().count(), 1)
        
        self.assertEqual(userFollowed.followers.all().count(), 2)

    def test_user_like(self):

        user01 = User.objects.get(username="Test-01")
        user02 = User.objects.get(username="Test-02")
        user03 = User.objects.get(username="Test-03")
        user04 = User.objects.get(username="Test-04")

        #User Test-03 posted
        Posts.objects.create(postUser=user03, postDescription="Hello")

        #3 users likes the post of Test-03
        post = Posts.objects.get(id=1)
        post.likers.add(user01)
        post.likers.add(user02)
        post.likers.add(user04)

        self.assertEqual(post.likers.all().count(), 3)

    
    def test_user_unlike(self):

        user01 = User.objects.get(username="Test-01")
        user02 = User.objects.get(username="Test-02")
        user03 = User.objects.get(username="Test-03")

        #User Test-03 posted
        Posts.objects.create(postUser=user03, postDescription="Hello")

        #2 users likes the post of Test-03
        post = Posts.objects.get(id=1)
        post.likers.add(user01)
        post.likers.add(user02)

        #But Test-01 unlike the post of Test-03
        post.likers.remove(user01)

        self.assertEqual(post.likers.all().count(), 1)
