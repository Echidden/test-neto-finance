"""
Bug_01: Поле «Номер карты» не должно принимать номер, начинающийся с 0
Ожидание: поле НЕ должно вводить 0 как первую цифру
Факт: 0 вводится, номер принимается как валидный
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_card_number_with_leading_zero_should_be_invalid(driver):
    driver.get(URL)
    
    # Карточка "Рубли"
    rub_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Рубли')]"))
    )
    rub_card.click()
    
    # Поле ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
    )
    
    # Вводим номер с 0 в начале
    card_input.send_keys("0123012301230123")
    
    # Проверяем реальное значение в поле
    actual_value = card_input.get_attribute("value")
    
    # Баг: если первая цифра 0 — тест падает
    assert not actual_value.startswith("0"), \
        f"BUG_01: Поле номера карты начинается с 0 ('{actual_value[:1]}'), что недопустимо"
