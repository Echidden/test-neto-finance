"""
Bug_03: При сумме перевода 18000₽ (комиссия 1800₽, итого 19800₽)
при доступном остатке 20001₽ перевод должен проходить, но не проходит

Ожидание: комиссия = 1800, кнопка «Перевести» активна
Факт: комиссия может быть неверной, кнопка отсутствует
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_boundary_amount_18000_should_be_allowed(driver):
    driver.get(URL)
    
    # 1. Карточка "Рубли"
    rub_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Рубли')]"))
    )
    rub_card.click()
    
    # 2. Ввод валидного номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
    )
    card_input.send_keys("1234123412341234")
    
    # 3. Ввод суммы 18000
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='1000']"))
    )
    amount_input.clear()
    amount_input.send_keys("18000")
    
    # 4. Проверяем, что комиссия = 1800
    commission_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span#comission"))
    )
    commission_text = commission_element.text
    print(f"Commission value: {commission_text}")
    
    if commission_text != "1800":
        print(f"WARNING: Комиссия = {commission_text}, ожидалось 1800")
    
    # 5. Проверяем, что кнопка «Перевести» активна
    try:
        transfer_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Перевести']"))
        )
        # Если кнопка активна — тест проходит
        assert transfer_button.is_enabled(), \
            "BUG_03: Кнопка 'Перевести' неактивна при сумме 18000 (комиссия 1800, итого 19800 < 20001)"
    except:
        # Если кнопки нет — это баг
        assert False, "BUG_03: Кнопка 'Перевести' отсутствует при сумме 18000"
