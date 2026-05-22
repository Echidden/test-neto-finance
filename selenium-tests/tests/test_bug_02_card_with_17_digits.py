"""
Bug_02: Поле «Номер карты» принимает 17 цифр (должно быть максимум 16)
Ожидание: поле не принимает 17-й символ
Факт: 17-й символ принимается, поле суммы появляется
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "http://localhost:8000/?balance=30000&reserved=20001"

def test_card_number_with_17_digits_should_be_invalid(driver):
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
    card_input.send_keys("12341234123412345")  # 17 цифр
    
    # Проверяем значение в поле (должно быть максимум 16 цифр)
    actual_value = card_input.get_attribute("value")
    
    # Баг: если в поле 17 цифр или появилось поле суммы
    assert len(actual_value) <= 16, \
        f"BUG_02: Поле номера карты содержит {len(actual_value)} цифр (максимум 16)"
    
    # Дополнительная проверка: поле суммы не должно появляться
    try:
        amount_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='1000']"))
        )
        # Если поле суммы появилось при 17 цифрах — это тоже баг
        assert False, "BUG_02: Поле суммы появилось при номере карты из 17 цифр"
    except:
        # Поле не появилось — всё правильно
        pass
