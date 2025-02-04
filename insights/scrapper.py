import random
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.utils import timezone
from .models import Page, Post, SocialMediaUser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


class FacebookScraper:
    def __init__(self):
        self.driver = self._init_browser()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _init_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,124)}.0.0.0 Safari/537.36")
        options.add_argument("--window-size=1920,1080")
        
        # Add stealth configurations
        service = Service(r"C:/Users/dell/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")

        driver = webdriver.Chrome(service=service, options=options)
        
        # Evade headless detection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = {runtime: {}};
            """
        })
        return driver

    def scrape_page(self, username):
        try:
            url = f'https://www.facebook.com/{username}'
            self.driver.get(url)
            print("Scraping followers...")

            WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]'))
        )

            
            # Wait for page load
            self.driver.implicitly_wait(10)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            page_data = {
                'username': username,
                'name': self._get_page_name(soup),
                'url': url,
                'fb_id': self._extract_fb_id(soup),
                'profile_pic': self._get_profile_pic(soup),
                'email': self._get_email(soup),
                'website': self._get_website(soup),
                'category': self._get_category(soup),
                'followers_count': self._get_followers_count(soup),
                'likes_count': self._get_likes_count(soup),
                'creation_date': self._get_creation_date(soup)
            }
            
            return {
                'page': page_data,
                'posts': self.scrape_posts(),
                'followers': self.scrape_followers()
            }
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            self.driver.save_screenshot('error_screenshot.png')
            raise
    def _get_page_name(self, soup):
        return soup.find('title').text.strip().split('|')[0].strip()

    def _extract_fb_id(self, soup):
        # Facebook ID is often in meta tags
        meta = soup.find('meta', {'property': 'al:android:url'})
        if meta:
            return meta['content'].split('/')[-1]
        return None

    def _get_profile_pic(self, soup):
        img = soup.find('image', {'xlink:href': True})
        return img['xlink:href'] if img else None

    def _get_email(self, soup):
        # Email might be in page description
        desc = soup.find('meta', {'name': 'description'})
        if desc:
            return next((word for word in desc['content'].split() if '@' in word), None)
        return None

    def _get_website(self, soup):
        link = soup.find('a', {'href': True, 'aria-label': 'Website'})
        return link['href'] if link else None

    def _get_category(self, soup):
        category = soup.find('div', text=lambda t: t and 'Category' in t)
        return category.find_next_sibling('div').text if category else None

    def _get_followers_count(self, soup):
        return self._parse_count(soup, 'followers')

    def _get_likes_count(self, soup):
        return self._parse_count(soup, 'likes')

    def _parse_count(self, soup, metric):
        element = soup.find('div', text=lambda t: t and f'{metric}' in t.lower())
        return int(element.text.split()[0].replace(',', '')) if element else 0

    def scrape_posts(self):
        # Scroll to load posts (Facebook uses lazy loading)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.implicitly_wait(2)
        print("Scraping posts...")

        
        posts = []
        post_elements = self.driver.find_elements(By.XPATH, '//div[@role="article"]')[:40]
        
        for element in post_elements:
            post_html = element.get_attribute('outerHTML')
            post_soup = BeautifulSoup(post_html, 'html.parser')
            
            posts.append({
                'fb_post_id': element.get_attribute('id'),
                'content': post_soup.get_text(separator=' ', strip=True),
                'likes': self._parse_post_metric(post_soup, 'Like'),
                'shares': self._parse_post_metric(post_soup, 'Share'),
                'timestamp': timezone.now()  # Actual timestamp requires more complex parsing
            })
        
        return posts
    def _get_creation_date(self, soup):
        date_element = soup.find('div', class_='creation-date')  # Change this according to your HTML structure
        if date_element:
            return date_element.text.strip()
        return None

    def _parse_post_metric(self, soup, metric):
        element = soup.find('span', text=lambda t: t and metric in t)
        return int(element.text.split()[0]) if element else 0

    

    def scrape_followers(self):
        try:
            # Dismiss initial popups
            self._dismiss_popups()

            # Scroll to the followers section
            self._scroll_to_element('//a[contains(@href, "followers")]')

            # Use ActionChains for human-like interaction
            actions = ActionChains(self.driver)
            followers_link = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "followers") and @role="link"]'))
            )

            # Hover and click with randomization
            actions.move_to_element(followers_link).pause(random.uniform(0.5, 1.5)).click().perform()

            # Wait for followers modal to load completely
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//img[@referrerpolicy="origin-when-cross-origin"]'))
            )

            # Simulate human-like scroll to load followers
            self._simulate_human_scroll()

            # Extract follower data
            followers = []
            follower_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "follower-class")]')

            for follower in follower_elements:
                # Replace with actual parsing logic for follower data
                followers.append({
                    'fb_id': follower.get_attribute('data-fb-id'),
                    'name': follower.find_element(By.XPATH, './/span[contains(@class, "name-class")]').text,
                    'profile_pic': follower.find_element(By.XPATH, './/img').get_attribute('src')
                })

            return followers
        except TimeoutException as e:
            print(f"Timeout scraping followers: {str(e)}")
            return []
        except Exception as e:
            print(f"Error scraping followers: {str(e)}")
            return []

    def _dismiss_popups(self):
        try:
            self.driver.execute_script("""
                const selectors = [
                    '[aria-label="Close"]',
                    '[data-cookiebanner="accept_button"]',
                    '[role="dialog"] button'
                ];
                selectors.forEach(selector => {
                    const element = document.querySelector(selector);
                    if (element) element.click();
                });
            """)
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"Popup dismissal failed: {str(e)}")

    def _scroll_to_element(self, xpath):
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(0.8, 1.8))

    def _simulate_human_scroll(self):
        scroll_pause_time = random.uniform(0.3, 1.0)
        screen_height = self.driver.execute_script("return window.innerHeight")
        for i in range(3):
            scroll_height = screen_height * (i + 1)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height})")
            time.sleep(scroll_pause_time)


    def save_to_db(self, data):
        # Save Page
        page, created = Page.objects.update_or_create(
            username=data['page']['username'],
            defaults={
                'name': data['page']['name'],
                'url': data['page']['url'],
                'fb_id': data['page']['fb_id'],
                'profile_pic': data['page']['profile_pic'],
                'email': data['page']['email'],
                'website': data['page']['website'],
                'category': data['page']['category'],
                'followers_count': data['page']['followers_count'],
                'likes_count': data['page']['likes_count'],
                'creation_date': data['page']['creation_date']
            }
        )

        # Save Posts
        for post_data in data['posts']:
            Post.objects.update_or_create(
                fb_post_id=post_data['fb_post_id'],
                defaults={
                    'page': page,
                    'content': post_data['content'],
                    'likes': post_data['likes'],
                    'shares': post_data['shares'],
                    'timestamp': post_data['timestamp']
                }
            )

        # Save Followers
        for follower_data in data['followers']:
            user, _ = SocialMediaUser.objects.update_or_create(
                fb_id=follower_data['fb_id'],
                defaults={
                    'name': follower_data['name'],
                    'profile_pic': follower_data['profile_pic']
                }
            )
            page.followers.add(user)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()