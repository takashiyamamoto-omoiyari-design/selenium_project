    import openai
    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from dotenv import load_dotenv

    # .envファイルを読み込む
    load_dotenv()

    # OpenAI APIキーを環境変数から取得
    openai.api_key = os.getenv('OPENAI_API_KEY')

    def get_selector_from_openai(page_url, description):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"URL: {page_url}\nDescription: {description}\nProvide the CSS selector for the element described."}
            ],
            max_tokens=50
        )
        return response.choices[0].message['content'].strip()

    def main():
        # ページURLと要素の説明を設定
        page_url = 'https://omoiyari-design.co.jp/fk/'
        description = 'The link in the list item under the div with id post-7'

        # OpenAI APIを使ってセレクタを取得
        element_selector = get_selector_from_openai(page_url, description)

        # Chromeドライバーを自動的に管理
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            # ログインページに移動
            driver.get('https://omoiyari-design.co.jp/fk/wp-login.php?loggedout=true&wp_lang=ja')

            # ユーザー名とパスワードを入力
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#user_login'))
            )
            username.send_keys('takashiyamamoto')

            password = driver.find_element(By.CSS_SELECTOR, '#user_pass')
            password.send_keys('BgmpxkmE')

            # ログインボタンをクリック
            login_button = driver.find_element(By.CSS_SELECTOR, '#wp-submit')
            login_button.click()

            # ページがロードされるのを待つ
            driver.get(page_url)
            print("Accessed the page.")
            
            # OpenAI APIで取得したセレクタを使用
            element_to_click = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, element_selector))
            )
            element_to_click.click()
            time.sleep(5)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()
            print("ブラウザを閉じました。")

    if __name__ == "__main__":
        main()