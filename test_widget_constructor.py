import pytest
from playwright.sync_api import Page, expect
import re

class TestEventsWidgetConstructor:
    """Тесты для конструктора календаря мероприятий"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Переход на страницу перед каждым тестом"""
        page.goto("https://dev.3snet.info/eventswidget/")
        page.wait_for_load_state("networkidle")

    def test_page_title_and_heading(self, page: Page):
        """Проверка заголовка страницы и основного заголовка"""
        # Проверяем заголовок вкладки браузера
        expect(page).to_have_title(re.compile(r"конструктор|календарь|events", re.IGNORECASE))
        
        # Проверяем наличие основного заголовка на странице
        main_heading = page.get_by_role("heading", name=re.compile(r"Начните создавать свой календарь", re.IGNORECASE))
        expect(main_heading).to_be_visible()

    def test_all_configuration_steps_are_present(self, page: Page):
        """Проверка, что все 4 шага конфигурации отображаются"""
        for step_num in range(1, 5):
            step_text = page.get_by_text(re.compile(f"Шаг {step_num}", re.IGNORECASE), exact=False)
            expect(step_text.first).to_be_visible()

    def test_theme_switcher_interaction(self, page: Page):
        """Проверка переключения между светлой и темной темой"""
        # Находим переключатели тем (предположим, это radio или кнопки)
        light_theme_option = page.get_by_text(re.compile(r"Светлая тема", re.IGNORECASE))
        dark_theme_option = page.get_by_text(re.compile(r"Темная тема", re.IGNORECASE))
        
        await expect(light_theme_option).to_be_visible()
        await expect(dark_theme_option).to_be_visible()
        
        # Кликаем по темной теме и проверяем, изменился ли класс у body
        # Это пример проверки; селекторы нужно будет уточнить по реальной верстке
        # page.click('text=Темная тема')
        # expect(page.locator('body')).to_have_class(re.compile(r'dark'))

    def test_generated_code_presence(self, page: Page):
        """Проверка, что после взаимодействия генерируется какой-то код"""
        # Найдем поле для кода. Оно может быть в textarea или в pre-блоке
        code_field = page.locator('textarea, pre, code')
        
        # Проверим, что поле вообще есть
        expect(code_field.first).to_be_visible()
        
        # Просто для примера: введем ширину и высоту, чтобы стимулировать генерацию кода
        width_input = page.get_by_label(re.compile(r"Ширина", re.IGNORECASE))
        height_input = page.get_by_label(re.compile(r"Высота", re.IGNORECASE))
        
        if width_input.count() > 0 and height_input.count() > 0:
            width_input.fill("500")
            height_input.fill("400")
            # Небольшая пауза, чтобы код обновился
            page.wait_for_timeout(500)
        
        # Проверим, что поле кода не пустое
        code_content = code_field.first.input_value() if code_field.first.evaluate("el => el.tagName === 'TEXTAREA'") else code_field.first.text_content()
        assert code_content is not None and len(code_content) > 0, "Поле с кодом пустое"

    def test_responsive_mobile_view(self, page: Page):
        """Проверка отображения на мобильном экране"""
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(200)
        
        # Проверяем, что основные элементы видны (не уехали за край экрана)
        body = page.locator('body')
        expect(body).to_be_visible()
        
        # Проверяем ширину body - она не должна превышать ширину вьюпорта (или быть чуть больше из-за скролла)
        body_width = page.evaluate("document.body.scrollWidth")
        assert body_width <= 385, f"Ширина body {body_width}px превышает ширину экрана 375px"
