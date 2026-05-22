"""
Bug_05: При отрицательном значении в поле ввода суммы перевода система дает провести перевод
Ожидание: перевод отрицательной суммы невозможен (кнопка неактивна)
Факт: кнопка активна, перевод -1000 отрабатывает, комиссия отрицательная
"""

from selenium.webdriver.common.by import By

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_negative_amount_transfer_should_be_blocked(driver):
    driver.get(URL)
    
    # Клик по карточке "Рубли"
    rub_card = driver.find_element(By.XPATH, "//div[contains(text(), 'Рубли')]")
    rub_card.click()
    
    # Ввод номера карты
    card_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Номер карты']")
    card_input.send_keys("1234123412341234")
    
    # Ввод отрицательной суммы
    amount_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Сумма']")
    amount_input.send_keys("-1000")
    
    # Проверка: кнопка "Перевести" не должна быть активна
    transfer_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Перевести')]")
    
    # Тест упадёт, если кнопка активна — это баг
    assert not transfer_button.is_enabled(), \
        "BUG_05: Кнопка 'Перевести' активна при отрицательной сумме -1000"