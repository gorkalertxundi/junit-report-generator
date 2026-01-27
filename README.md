# JUnit Report Generator

![PyPI - Version](https://img.shields.io/pypi/v/junit-html-report-generator) ![License](https://img.shields.io/pypi/l/junit-html-report-generator) ![Python Version](https://img.shields.io/pypi/pyversions/junit-html-report-generator)

**junit-html-report-generator** is a lightweight, zero-dependency Python tool that converts JUnit XML test reports into human-readable, static HTML dashboards.

Perfect for CI/CD pipelines, local debugging, or sharing test results with stakeholders.

## 🚀 Key Features

* **Simple Conversion:** Turn complex XML into a clean, responsive HTML file in seconds.
* **🎨 Multiple Templates:** Choose from built-in themes (Dark mode, Minimal, etc.) to suit your preferences.
* **CI/CD Ready:** Seamlessly integrates with Jenkins, GitHub Actions, GitLab CI, and CircleCI.
* **Detailed Insights:** View pass/fail rates, execution times, and capture stdout/stderr logs.
* **Dual Mode:** Use it as a CLI tool or import it as a Python library.

## 📦 Installation

Install the package via pip:

```bash
pip install junit-html-report-generator
```

## 🛠 Usage

**Command Line Interface (CLI)**
Basic conversion (uses default template):
```bash
junit-html-report-generator report.xml -o output.html
```

Using a specific template:
```bash
junit-html-report-generator report.xml -o output.html --template dark
```

Setting a custom title:
```bash
junit-html-report-generator report.xml -o output.html --template legacy --title "Nightly Run"
```

List available templates:
```bash
junit-html-report-generator --list-templates
```

**Python Library**
You can integrate the generator directly into your Python scripts.

```python
from junit_report_generator import create_report

# Convert with a specific template
create_report(
    source="results.xml", 
    output="dashboard.html", 
    template="dark",
    title="Nightly Run"
)

# or using a string of XML data
with open("results.xml", "r") as f:
    xml_data = f.read()
    html_content = create_report(xml_string=xml_data, template="minimal")
```

## 🎨 Available Templates

The package comes with several pre-built templates to customize your report style.

| Template Name | Description | Best For |
| :--- | :--- | :--- |
| **modern** | (Default) A clean, colorful dashboard with charts and collapsible sections. | General use, stakeholder reports. |
| **dark** | A high-contrast dark theme version of the modern dashboard. | Late-night debugging, dark-mode lovers. |
| **minimal** | A text-heavy, high-density layout with no Javascript or charts. | Large test suites (10k+ tests), slow connections. |
| **legacy** | A simple table view similar to older Jenkins reports. | Backward compatibility. |

### 📸 Template Previews

<table>
  <tr>
    <td width="50%" valign="top">
      <h4 align="center">Modern (Default)</h4>
      <img src="https://github.com/user-attachments/assets/34ca8100-474c-4d16-a526-b3601fffdc04" alt="Modern Report" width="100%" />
    </td>
    <td width="50%" valign="top">
      <h4 align="center">Modern Dark</h4>
      <img src="https://github.com/user-attachments/assets/29ff73b9-7e66-491f-9333-2f71c0ef35dc" alt="Dark Report" width="100%" />
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4 align="center">Minimal</h4>
      <img src="https://github.com/user-attachments/assets/8d3acc33-be63-41c7-92ce-def70d68ee89" alt="Minimal Report" width="100%" />
    </td>
    <td width="50%" valign="top">
      <h4 align="center">Legacy</h4>
      <img src="https://github.com/user-attachments/assets/f6e39403-d864-4c58-bcad-1f7c537b9189" alt="Legacy Report" width="100%" />
    </td>
  </tr>
</table>

## 📊 Example Output
The generated HTML report includes:

- Summary Cards: Total tests, passed, failed, skipped, and total duration.
- Test Cases Table: Sortable list of all test cases with status indicators.
- Failure Details: Expandable sections showing stack traces and error messages.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gorkalertxundi/junit-html-report-generator.git
   cd junit-html-report-generator
   ```

2. **Install in editable mode**
   ```bash
   pip install -e .
   ```
   This installs the package in development mode, allowing you to make changes to the source code and test them immediately without reinstalling.

3. **Verify the installation**
   ```bash
   # Check that the CLI is available
  junit-html-report-generator --list-templates
   
   # Verify templates are bundled correctly
   python -c "from junit_html_report_generator import get_available_templates; print(get_available_templates())"
   ```

### Running Tests

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
python -m unittest discover tests

# Run tests with verbose output
python -m unittest discover tests -v

# Run a specific test
python -m unittest tests.test_parser.TestJUnitParser.test_parse_single_testsuite
```

All tests should pass before submitting a pull request.

### Testing Locally

1. **Generate a test report**
   ```bash
   # Use the provided sample file
  junit-html-report-generator sample-test-results.xml -o test-report.html
   
   # Try different templates
  junit-html-report-generator sample-test-results.xml -o dark-report.html --template dark
  junit-html-report-generator sample-test-results.xml -o minimal-report.html --template minimal
   ```

2. **Test the Python API**
   ```python
   from junit_html_report_generator import create_report
   
   # Test with file
   create_report(source="sample-test-results.xml", output="api-test.html")
   
   # Test with XML string
   with open("sample-test-results.xml") as f:
       html = create_report(xml_string=f.read(), template="dark")
       print(f"Generated {len(html)} bytes of HTML")
   ```

3. **Test template bundling**
   ```bash
   # Build the package
   python -m build
   
   # Check that templates are included
   tar -tzf dist/junit-html-report-generator-*.tar.gz | grep templates
   ```

### Adding a New Template

1. Create your template file in `junit_html_report_generator/templates/yourtemplate.html`
2. Use Jinja2 syntax with these variables:
   - `{{ summary.total }}`, `{{ summary.passed }}`, `{{ summary.failed }}`, etc.
   - `{{ summary.pass_rate }}` for the percentage
   - `{% for test in test_cases %}` to iterate through tests
   - `{{ test.name }}`, `{{ test.status }}`, `{{ test.message }}`, `{{ test.output }}`
3. Test your template: `junit2html sample-test-results.xml --template yourtemplate`
4. The template will automatically appear in `--list-templates`

### Contribution Workflow

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and test thoroughly
4. Run the test suite to ensure nothing broke
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request with a clear description of your changes

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

