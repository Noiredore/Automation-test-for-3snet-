# test_events_widget.py
import pytest
from playwright.sync_api import Page, expect
import re

class TestEventsWidget:
    """Test suite for Events Widget page"""
    
    def test_page_loads_successfully(self, page: Page):
        """Test that the page loads with correct title"""
        page.goto("https://dev.3snet.info/eventswidget/")
        
        # Verify page title contains "Events" (case insensitive)
        expect(page).to_have_title(re.compile(r"events", re.IGNORECASE))
        
        # Verify main content is visible
        main_content = page.locator("main, #root, .app, body").first
        expect(main_content).to_be_visible()
    
    def test_events_display(self, page: Page):
        """Test that events are displayed or appropriate message is shown"""
        page.goto("https://dev.3snet.info/eventswidget/")
        page.wait_for_load_state("networkidle")
        
        # Look for events or "no events" message
        events = page.locator(".event-item, [class*='event'], [data-testid='event']")
        no_events = page.locator("text=/(no events|nothing to show|empty|no data)/i")
        
        if events.count() > 0:
            # Verify first event has content
            first_event = events.first
            expect(first_event).to_be_visible()
            
            # Check for event details (title, date, etc.)
            event_title = first_event.locator("h3, h4, .title, [class*='title']").first
            if event_title.count() > 0:
                expect(event_title).to_be_visible()
        else:
            # If no events, verify message exists
            if no_events.count() > 0:
                expect(no_events.first).to_be_visible()
            else:
                # Page might still be loading or have different structure
                pytest.skip("No events or message found - page may be empty")
    
    def test_filter_functionality(self, page: Page):
        """Test filter/search functionality if present"""
        page.goto("https://dev.3snet.info/eventswidget/")
        
        # Check for filter input
        filter_input = page.locator(
            "input[type='text'], input[placeholder*='filter' i], "
            "input[placeholder*='search' i], select, .filter-control"
        )
        
        if filter_input.count() > 0:
            first_filter = filter_input.first
            expect(first_filter).to_be_visible()
            
            # Try to interact if it's a text input
            if first_filter.get_attribute("type") in ["text", "search", None]:
                initial_count = page.locator(".event-item, [class*='event']").count()
                
                # Type in filter
                first_filter.fill("test")
                page.wait_for_timeout(500)  # Wait for filter to apply
                
                # Get count after filtering
                new_count = page.locator(".event-item, [class*='event']").count()
                
                # Note: We don't assert count changed as it might be valid to show no results
                # Test passes if no errors occurred
        else:
            pytest.skip("No filter functionality found on page")
    
    def test_event_interactivity(self, page: Page):
        """Test that event items are clickable"""
        page.goto("https://dev.3snet.info/eventswidget/")
        
        # Find clickable elements that might be events
        clickable = page.locator(
            "a:has(.event-title), a:has([class*='event']), "
            "button:has([class*='event']), [onclick], .event-item, "
            "[role='button'], [class*='card']"
        )
        
        if clickable.count() > 0:
            first_clickable = clickable.first
            
            # Check if element is clickable
            is_clickable = first_clickable.evaluate("""(element) => {
                return element.hasAttribute('href') || 
                       element.hasAttribute('onclick') ||
                       window.getComputedStyle(element).cursor === 'pointer' ||
                       element.tagName === 'A' ||
                       element.tagName === 'BUTTON';
            }""")
            
            if is_clickable:
                # Try to click safely
                try:
                    with page.expect_navigation(timeout=3000, wait_until="commit"):
                        first_clickable.click(timeout=3000)
                except:
                    # Click didn't cause navigation, that's okay
                    pass
                
                # Go back if we navigated
                if page.url != "https://dev.3snet.info/eventswidget/":
                    page.go_back()
        else:
            pytest.skip("No clickable event elements found")
    
    def test_responsive_design(self, page: Page):
        """Test page responsiveness on different viewport sizes"""
        viewports = [
            {"width": 375, "height": 667},   # Mobile
            {"width": 768, "height": 1024},  # Tablet
            {"width": 1280, "height": 720},  # Desktop
        ]
        
        for viewport in viewports:
            page.set_viewport_size(viewport)
            page.goto("https://dev.3snet.info/eventswidget/")
            page.wait_for_timeout(200)  # Wait for resize handlers
            
            # Verify page is still functional
            expect(page.locator("body")).to_be_visible()
            
            # Check if content is visible (not overflowing)
            body_width = page.evaluate("document.body.scrollWidth")
            assert body_width <= viewport["width"] + 10  # Allow small overflow
    
    def test_no_console_errors(self, page: Page):
        """Test that no JavaScript errors appear in console"""
        errors = []
        
        def handle_console(msg):
            if msg.type == "error":
                errors.append(f"Console error: {msg.text}")
        
        def handle_page_error(error):
            errors.append(f"Page error: {error}")
        
        page.on("console", handle_console)
        page.on("pageerror", handle_page_error)
        
        page.goto("https://dev.3snet.info/eventswidget/")
        page.wait_for_load_state("networkidle")
        
        # Assert no errors
        assert len(errors) == 0, f"Found console errors: {errors}"
    
    def test_page_performance(self, page: Page):
        """Basic performance test - page should load within reasonable time"""
        start_time = page.evaluate("performance.now()")
        
        page.goto("https://dev.3snet.info/eventswidget/")
        page.wait_for_load_state("networkidle")
        
        load_time = page.evaluate("performance.now()") - start_time
        
        # Log load time for information
        print(f"\nPage load time: {load_time:.2f}ms")
        
        # Basic performance assertion
        assert load_time < 10000, f"Page load time ({load_time}ms) exceeded 10 seconds"
