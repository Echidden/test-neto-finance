"""
Bug_05: При отрицательном значении в поле ввода суммы перевода система дает провести перевод
Ожидание: перевод отрицательной суммы невозможен (кнопка неактивна)
Факт: кнопка активна, перевод -1000 отрабатывает, комиссия отрицательная
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_negative_amount_transfer_should_be_blocked(driver):
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
    
    # Поле ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='1000']"))
    )
    amount_input.clear()
    amount_input.send_keys("-1000")
    
    # Кнопка "Перевести"
    transfer_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button//span[text()='Перевести']"))
    )
    
    # Проверка: кнопка НЕ должна быть активна (но она активна → тест падает)
    assert not transfer_button.is_enabled(), \
        "BUG_05: Кнопка 'Перевести' активна при отрицательной сумме -1000"
    
    # Тест упадёт, если кнопка активна — это баг
    assert not transfer_button.is_enabled(), \
        "BUG_05: Кнопка 'Перевести' активна при отрицательной сумме -1000"
