# README.md

# Events Widget Page Tests

Automated tests for the [Events Widget page](https://dev.3snet.info/eventswidget/) using Playwright with Python.

## 📋 Test Coverage

The test suite covers the following aspects:

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
- Python 3.8 or higher
- pip (Python package manager)

### One-line Setup & Run

```bash
# Clone and run (Unix/Mac)
git clone https://github.com/Noiredore/events-widget-tests.git
cd events-widget-tests
pip install -r requirements.txt
playwright install
pytest
