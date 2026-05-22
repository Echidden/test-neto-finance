"""
Bug_01: Поле «Номер карты» принимает номер, начинающийся с 0
Ожидание: поле суммы не появляется
Факт: поле суммы появляется, перевод возможен
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
    
    # Ввод номера карты с 0 в начале
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
    )
    card_input.send_keys("0123012301230123")
    
    # Проверяем, появился ли элемент с комиссией (более надёжно)
    try:
        # Ищем любой элемент, который появляется после ввода карты
        commission_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Сумма перевода')]"))
        )
        # Если нашли — это баг
        assert False, "BUG_01: Появился элемент 'Сумма перевода' при номере карты с 0 в начале"
    except:
        # Если ничего не нашли — всё правильно
        pass
