import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import random

class TikTokBot:
    def __init__(self):
        self.driver = self.setup_browser()

    def setup_browser(self):
        # Setup browser untuk Selenium
        options = Options()
        options.add_experimental_option("detach", True)  # Agar browser tetap terbuka
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Menggunakan webdriver manager untuk menginstal ChromeDriver
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def register_account(self, username, email, password):
        # Membuka halaman pendaftaran TikTok
        self.driver.get("https://www.tiktok.com/signup")
        time.sleep(3)  # Tunggu halaman dimuat

        # Isi form pendaftaran dengan username, email, dan password
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(1)

        # Klik tombol "Sign up"
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Sign up")]').click()
        time.sleep(5)  # Tunggu agar pendaftaran selesai

    def login(self, username, password):
        # Membuka halaman login TikTok
        self.driver.get("https://www.tiktok.com/login")
        time.sleep(3)

        # Isi form login dengan username dan password
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        time.sleep(1)

        # Klik tombol "Log in"
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Log in")]').click()
        time.sleep(5)  # Tunggu agar login berhasil

    def open_video(self, url):
        # Membuka URL video TikTok
        self.driver.get(url)
        time.sleep(5)  # Tunggu 5 detik agar video dimuat dengan benar

    def watch_video(self):
        # Simulasi menonton video dengan menggulirkan video atau klik tombol play
        try:
            play_button = self.driver.find_element(By.XPATH, '//button[contains(@class, "play-button")]')
            play_button.click()
            time.sleep(3)  # Tunggu beberapa detik agar video diputar
        except:
            print("Tombol play tidak ditemukan.")
            time.sleep(5)  # Tunggu 5 detik jika tombol play tidak ada

    def like_video(self):
        # Klik tombol like setelah menonton video
        try:
            like_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/article/div/section[2]/button[1]')
            like_button.click()
            print("Video telah disukai!")
        except:
            print("Tombol like tidak ditemukan.")

    def repeat_watch_and_like(self, video_url, views, likes, accounts):
        # Menonton video berulang kali dan memberi like sesuai jumlah views dan likes yang diinginkan
        for _ in range(views):
            # Pilih akun secara acak
            account = random.choice(accounts)
            self.login(account['username'], account['password'])
            self.open_video(video_url)
            self.watch_video()
            print(f"Menonton video ke-{_ + 1}...")
            time.sleep(5)  # Tunggu beberapa detik sebelum memberi like
            if _ < likes:
                self.like_video()  # Menyukai video setelah menonton jika belum mencapai jumlah likes
            time.sleep(10)  # Tunggu antara menonton video, biarkan video selesai

    def run(self, accounts, video_url, views, likes):
        # Jalankan bot untuk menonton video dan memberi like menggunakan beberapa akun
        self.repeat_watch_and_like(video_url, views, likes, accounts)


if __name__ == "__main__":
    # Input URL video TikTok, jumlah views, dan jumlah likes
    video_url = input("Masukkan link TikTok: ")
    views = int(input("Masukkan jumlah views: "))
    likes = int(input("Masukkan jumlah likes: "))

    # Data akun TikTok yang ingin digunakan (nama akun, email, password)
    accounts = [
        {'username': 'username1', 'email': 'email1@example.com', 'password': 'password1'},
        {'username': 'username2', 'email': 'email2@example.com', 'password': 'password2'},
        {'username': 'username3', 'email': 'email3@example.com', 'password': 'password3'}
    ]

    bot = TikTokBot()

    # Membuat akun-akun TikTok terlebih dahulu
    for account in accounts:
        bot.register_account(account['username'], account['email'], account['password'])

    # Setelah pendaftaran selesai, bot akan menonton dan memberi like pada video TikTok
    bot.run(accounts, video_url, views, likes)
