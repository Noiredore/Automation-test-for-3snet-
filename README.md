# README.md

# Events Widget Page Tests

Автоматические тесты для сайта (https://dev.3snet.info/eventswidget/) при помощи Python и Playwright

## 📋 Тестовое покрытие

Данный тестсьют покрывают следующие аспекты:

| Test | Description |
|------|-------------|
| **Page Load** | Verifies page loads successfully with correct title |
| **Events Display** | Checks if events are visible or appropriate message shown |
| **Filter Functionality** | Tests filter/search controls if present |
| **Event Interactivity** | Verifies event items are clickable |
| **Responsive Design** | Tests on mobile, tablet, and desktop viewports |
| **Console Errors** | Ensures no JavaScript errors appear |
| **Performance** | Basic load time measurement |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 или выше
- pip (Python package manager)

### Установка и прогон

```bash
# Clone and run (Unix/Mac)
git clone https://github.com/Noiredore/events-widget-tests.git
cd events-widget-tests
pip install -r requirements.txt
playwright install
pytest

