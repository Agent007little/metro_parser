from selenium import webdriver
import time

url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search&page=1"


def get_data_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url=url)
        time.sleep(1)

        with open("index_selenium.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


