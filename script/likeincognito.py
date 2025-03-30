import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

class TikTokBot:
    def __init__(self):
        self.xpaths = {
            "likes": "/html/body/div[6]/div/div[2]/div[1]/div/div[3]/div/button",  
            "video_url_box": "/html/body/div[8]/div/form/div/input",
            "search_box": "/html/body/div[8]/div/form/div/div/button",
            "submit_button": '//*[@id="c2VuZE9nb2xsb3dlcnNfdGlrdG9r"]/div[1]/div/form/button',
            "countdown_1": '//html/body/div[8]/div/div/span[1]',
            "countdown_2": '//*[@id="login-countdown"]'
        }
        self.driver = self.setup_browser()
        self.option = 4  
        self.tasks = {4: ("Likes", 8, "c2VuZC9mb2xs6a2VfdGlrdG9r")}  
        self.success_count = 0  

    def setup_browser(self):
        options = uc.ChromeOptions()
        # options.add_argument("--user-data-dir=C:/Users/toram/AppData/Local/Google/Chrome/User Data")
        # options.add_argument("--profile-directory=Default")
        options.add_argument("--incognito")  
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")

        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def open_website(self, url):
        console.print(f"[cyan]Membuka situs:[/] [bold]{url}[/]")
        self.driver.get(url)
        time.sleep(5)

    def wait_for_xpath(self, xpath, retries=3, delay=2):
        for _ in range(retries):
            try:
                WebDriverWait(self.driver, delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                return True
            except:
                console.print(f"[red]Elemen {xpath} tidak ditemukan, mencoba lagi...[/]")
                time.sleep(delay)
        return False

    def wait_for_cooldown(self):
        try:
            countdown_element = None
            countdown_text = ""

            if self.is_element_present(self.xpaths["countdown_1"]):
                countdown_element = self.driver.find_element(By.XPATH, self.xpaths["countdown_1"])
                countdown_text = countdown_element.text
            elif self.is_element_present(self.xpaths["countdown_2"]):
                countdown_element = self.driver.find_element(By.XPATH, self.xpaths["countdown_2"])
                countdown_text = countdown_element.text

            if countdown_element:
                minutes_seconds_format_1 = re.search(r'(\d+)\s*minute\(s\)\s*(\d+)\s*seconds?', countdown_text)
                minutes_seconds_format_2 = re.search(r'(\d+)\s*minute\(s\)\s*(\d+)\s*second\(s\)', countdown_text)
                seconds_only_format = re.search(r'(\d+)\s*second\(s\)', countdown_text)

                if minutes_seconds_format_1:
                    minutes = int(minutes_seconds_format_1.group(1))
                    seconds = int(minutes_seconds_format_1.group(2))
                elif minutes_seconds_format_2:
                    minutes = int(minutes_seconds_format_2.group(1))
                    seconds = int(minutes_seconds_format_2.group(2))
                elif seconds_only_format:
                    minutes = 0
                    seconds = int(seconds_only_format.group(1))
                else:
                    console.print("[red]Format countdown tidak dikenali, lanjutkan tanpa menunggu.[/]")
                    return False

                cooldown_seconds = minutes * 60 + seconds + 5  
                console.print(f"[yellow]Menunggu cooldown selama {cooldown_seconds} detik...[/]")

                with Progress(
                    SpinnerColumn(),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Menunggu cooldown...[/]", total=cooldown_seconds)
                    while not progress.finished:
                        time.sleep(1)
                        progress.update(task, advance=1)

                return True
            else:
                console.print("[green]Tidak ada countdown ditemukan, lanjutkan![/]")
                return False

        except Exception as e:
            console.print(f"[red]Error saat menunggu cooldown: {e}[/]")
            time.sleep(5)
            return False

    def is_element_present(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    def click_likes_button(self):
        if self.wait_for_xpath(self.xpaths["likes"]):
            like_button = self.driver.find_element(By.XPATH, self.xpaths["likes"])
            self.driver.execute_script("arguments[0].scrollIntoView();", like_button)
            like_button.click()
            console.print("[green]Tombol Likes diklik![/]")
            time.sleep(2)
        else:
            console.print("[red]Tombol Likes tidak ditemukan![/]")

    def enter_video_url(self, tiktok_link, div):
        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        if self.wait_for_xpath(video_url_box):
            self.driver.find_element(By.XPATH, video_url_box).send_keys(tiktok_link)
            console.print(f"[blue]Link TikTok dimasukkan:[/] {tiktok_link}")
        else:
            console.print("[red]Field video URL tidak ditemukan![/]")

    def click_search_button(self, div):
        search_box = f'/html/body/div[{div}]/div/form/div/div/button'
        if self.wait_for_xpath(search_box):
            self.driver.find_element(By.XPATH, search_box).click()
            console.print("[green]Tombol search diklik![/]")
            time.sleep(2)
        else:
            console.print("[red]Tombol search tidak ditemukan![/]")

    def execute_task(self, tiktok_link):
        try:
            div = self.tasks[self.option][1]
            task_id = self.tasks[self.option][2]

            self.enter_video_url(tiktok_link, div)
            self.click_search_button(div)

            if self.wait_for_cooldown():
                self.click_search_button(div)

            time.sleep(2)
            submit_button_xpath = self.xpaths["submit_button"].replace("{task_id}", task_id)
            if self.wait_for_xpath(submit_button_xpath):
                self.driver.find_element(By.XPATH, submit_button_xpath).click()
                self.success_count += 1
                console.print(f"[green]Submit berhasil! Task ke-{self.success_count} berhasil![/]")
            else:
                console.print("[red]Tombol submit tidak ditemukan![/]")

        except Exception as e:
            console.print(f"[red]Error saat menjalankan tugas: {e}[/]")

    def run(self):
        console.print("[cyan bold]TikTok Bot - Zefoy Automation[/]")
        console.print("[bold yellow]Created by: Kondang[/]\n")
        console.print("[green]⚡ Selamat datang di bot otomatis TikTok Likes![/]")

        tiktok_link = input("🎥 Masukkan link TikTok: ")
        self.open_website("https://zefoy.com")

        self.click_likes_button()

        while True:
            self.execute_task(tiktok_link)
            console.print("[cyan]Task selesai, memulai lagi...[/]\n")
            time.sleep(5)

if __name__ == "__main__":
    bot = TikTokBot()
    bot.run()
