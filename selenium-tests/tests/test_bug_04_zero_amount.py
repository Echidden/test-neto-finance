"""
Bug_04: При значении 0 в поле ввода суммы перевода система дает провести перевод
Ожидание: перевод 0 невозможен (кнопка не появляется)
Факт: кнопка активна, перевод 0 отрабатывает
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_zero_amount_transfer_should_be_blocked(driver):
    driver.get(URL)
    
    # Клик по карточке "Рубли"
    rub_card = driver.find_element(By.XPATH, "//div[contains(text(), 'Рубли')]")
    rub_card.click()
    
    # Ввод номера карты (валидный 16-значный)
    card_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Номер карты']")
    card_input.send_keys("1234123412341234")
    
    # Ввод суммы 0
    amount_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Сумма']")
    amount_input.send_keys("0")
    
    # Проверка: кнопка "Перевести" не должна быть активна/доступна
    transfer_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Перевести')]")
    
    # Тест упадёт, если кнопка есть и активна — это и есть баг
    assert not transfer_button.is_enabled(), \
        "BUG_04: Кнопка 'Перевести' активна при сумме 0, хотя не должна быть"