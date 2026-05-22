"""
Bug_04: При значении 0 в поле ввода суммы перевода система дает провести перевод
Ожидание: перевод 0 невозможен (кнопка не появляется)
Факт: кнопка активна, перевод 0 отрабатывает
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_zero_amount_transfer_should_be_blocked(driver):
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
    card_input.send_keys("1234123412341234")
    
    # Поле ввода суммы (появляется после ввода карты)
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='1000']"))
    )
    amount_input.clear()
    amount_input.send_keys("0")
    
    # Кнопка "Перевести" (баг: она активна при сумме 0)
    transfer_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button//span[text()='Перевести']"))
    )
    
    # Проверка: кнопка НЕ должна быть активна (но она активна → тест падает)
    assert not transfer_button.is_enabled(), \
        "BUG_04: Кнопка 'Перевести' активна при сумме перевода 0"
