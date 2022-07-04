from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

from django.test import Client, TestCase
from django.db.models import Max

from .models import User, Posts, Profile

#Client-side testing
class WebpageTests(StaticLiveServerTestCase):
    driver = None
    port = 8000

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

        #follow Test-02
        loginUser = Profile.objects.get(userId=user03)
        loginUser.following.add(user02)

        #Test-01 add as follower of Test-02
        userFollowed = Profile.objects.get(userId=user02)
        userFollowed.followers.add(user03)


        Posts.objects.create(postUser=user02, postDescription="Hello")

    @classmethod    
    def setUpClass(self):
        options = Options()
        #options.add_argument("--window-size=1920,1080")
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')

        ContentType.objects.clear_cache()
        super().setUpClass()

        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)        

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super().tearDownClass()

    def test_title(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        self.assertEqual(driver.title, "Social Network")

    def test_register(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Register").click()

        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-05")
        email = driver.find_element(By.NAME, "email")
        email.send_keys("test05@test.com")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        confirmation = driver.find_element(By.NAME, "confirmation")
        confirmation.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        self.assertEqual(driver.current_url, "http://localhost:8000/")    
    
    def test_login(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()

        self.assertEqual(driver.current_url, "http://localhost:8000/login")

    def test_pagination_page4(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-03")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        for i in range(20):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").click()

        #on page 3, add posts
        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").click()
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 1)

    def test_pagination_page3(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-03")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        for i in range(20):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").click()
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 1)

    def test_pagination_page2(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-03")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

       
        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        self.assertFalse(driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").is_displayed())
        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[3]/input").click()

        #on page 2, add posts and page 3 displayed
        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        self.assertTrue(driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").is_displayed())
        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").click()
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 1)
    
    def test_pagination_page1(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-03")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        #same page, add posts and page 2 displayed
        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        self.assertTrue(driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[3]/input").is_displayed())

        #same page, add posts and page 3 displayed
        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()
        
        time.sleep(1)

        self.assertTrue(driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[4]/input").is_displayed())
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 10)

    def test_pagination(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-03")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()
        
        #number of posts is 1 and previous and next button is not displayed
        self.assertFalse(driver.find_element(By.ID, "previous").is_displayed())
        self.assertFalse(driver.find_element(By.ID, "next").is_displayed())

        for i in range(10):
            addNewPost = driver.find_element(By.NAME, "addNewPost")
            addNewPost.send_keys("Hello, World")
            driver.find_element(By.ID, "submit").click()

        time.sleep(1)

        #number of posts is 11 and next button is displayed
        self.assertTrue(driver.find_element(By.ID, "next").is_displayed())

        #click page number 2
        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[3]/input").click()
        
        time.sleep(1)
        
        #went to last page and previous button is diplayed while next button is not displayed
        self.assertTrue(driver.find_element(By.ID, "previous").is_displayed())
        self.assertFalse(driver.find_element(By.ID, "next").is_displayed())

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 1)

        #going back to page 1 by clicking page number 1
        driver.find_element(By.XPATH, "//*[@id='mainContainer']/nav/ul/li[2]/input").click()
        
        time.sleep(1)

        #went to first page and previous button is not diplayed while next button is displayed
        self.assertFalse(driver.find_element(By.ID, "previous").is_displayed())
        self.assertTrue(driver.find_element(By.ID, "next").is_displayed())

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 10)

        #click next button
        driver.find_element(By.ID, "next").click()
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 1)

        #going back to page 1 by clicking previous button
        driver.find_element(By.ID, "previous").click()
        
        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 10)

    def test_following(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-04")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        #Go to following page and check no post
        driver.find_element(By.LINK_TEXT, "Following").click()

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertEqual(len(numberOfPost), 0)

        #Go to test-02 profile and follow
        driver.find_element(By.LINK_TEXT, "All Posts").click()

        time.sleep(1)

        driver.find_element(By.LINK_TEXT, "Test-02").click()

        driver.find_element(By.ID, "follow").click()

        #Go to own profile and check following count
        driver.find_element(By.LINK_TEXT, "Test-04").click()

        followingCount = driver.find_element(By.CLASS_NAME, "followingCount")
        
        self.assertEqual(int(followingCount.text), 1)
        
        #Go to following page and check following user posts
        driver.find_element(By.LINK_TEXT, "Following").click()

        time.sleep(1)
        
        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertGreater(len(numberOfPost), 0)

    def test_profile(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-01")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()


        driver.find_element(By.LINK_TEXT, "Test-02").click()

        #number of posts
        postingCount = driver.find_element(By.ID, "postingCount")

        self.assertGreater(int(postingCount.text), 0)
        
        #follow user
        followersCount = driver.find_element(By.CLASS_NAME, "followersCount")
        
        self.assertEqual(int(followersCount.text), 1)

        driver.find_element(By.ID, "follow").click()
        
        followersCount = driver.find_element(By.CLASS_NAME, "followersCount")
        
        self.assertEqual(int(followersCount.text), 2)

        #unfollow user
        followersCount = driver.find_element(By.CLASS_NAME, "followersCount")
        
        self.assertEqual(int(followersCount.text), 2)

        driver.find_element(By.ID, "following").click()
        
        followersCount = driver.find_element(By.CLASS_NAME, "followersCount")
        
        self.assertEqual(int(followersCount.text), 1)

    def test_post(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-01")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        self.assertFalse(driver.find_element(By.ID, "submit").is_enabled())
        
        #post
        addNewPost = driver.find_element(By.NAME, "addNewPost")
        addNewPost.send_keys("Hello, World")

        self.assertTrue(driver.find_element(By.ID, "submit").is_enabled())

        driver.find_element(By.ID, "submit").click()

        time.sleep(1)

        numberOfPost = driver.find_elements(By.ID, "posts")

        self.assertFalse(driver.find_element(By.ID, "submit").is_enabled())

        self.assertEqual(len(numberOfPost), 2)

    def test_like_unlike(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-01")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        time.sleep(1)

        #like
        span = driver.find_element(By.XPATH, "//*[@id='like-4']/span[1]").click()

        time.sleep(1)

        numberOflikes = driver.find_element(By.XPATH, "//*[@id='like-4']/span[2]")

        self.assertEqual(numberOflikes.text, "  1   like")

        
        #unlike
        span = driver.find_element(By.XPATH, "//*[@id='like-4']/span[1]").click()

        time.sleep(1)

        numberOflikes = driver.find_element(By.XPATH, "//*[@id='like-4']/span[2]")

        self.assertEqual(numberOflikes.text, "  0   like")

    
    def test_edit(self):
        driver = self.driver
        url = self.live_server_url
        driver.get(url)

        driver.find_element(By.LINK_TEXT, "Log In").click()
        
        #Login
        username = driver.find_element(By.NAME, "username")
        username.send_keys("Test-01")
        password = driver.find_element(By.NAME, "password")
        password.send_keys("test")
        driver.find_element(By.CLASS_NAME, "btn").click()

        #post
        addNewPost = driver.find_element(By.NAME, "addNewPost")
        addNewPost.send_keys("First post")
        driver.find_element(By.ID, "submit").click()

        time.sleep(1)

        edit = driver.find_element(By.ID, "edit-2").click()
        editPost = driver.find_element(By.ID, "editPost-2")
        editPost.clear()
        editPost.send_keys("Edited First post")
        driver.find_element(By.ID, "edit-2").click()
        
        time.sleep(1)

        editedPost = driver.find_element(By.ID, "post-content-2")

        self.assertEqual(editedPost.text, "Edited First post")

#Server-side testing
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
