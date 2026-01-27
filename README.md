# JUnit Report Generator

![PyPI - Version](https://img.shields.io/pypi/v/junit-report-generator) ![License](https://img.shields.io/pypi/l/junit-report-generator) ![Python Version](https://img.shields.io/pypi/pyversions/junit-report-generator)

**junit-report-generator** is a lightweight, zero-dependency Python tool that converts JUnit XML test reports into human-readable, static HTML dashboards.

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
pip install junit-report-generator
```

## 🛠 Usage

**Command Line Interface (CLI)**
Basic conversion (uses default template):
```bash
junit2html report.xml -o output.html
```

Using a specific template:
```bash
junit2html report.xml -o output.html --template dark
```

List available templates:
```bash
junit2html --list-templates
```

**Python Library**
You can integrate the generator directly into your Python scripts.

```python
from junit_report_generator import create_report

# Convert with a specific template
create_report(
    source="results.xml", 
    output="dashboard.html", 
    template="dark"
)

# or using a string of XML data
with open("results.xml", "r") as f:
    xml_data = f.read()
    html_content = create_report(xml_string=xml_data, template="minimal")
```

## 🎨 Available Templates
The package comes with several pre-built templates to customize your report style.

Template Name	Description	Best For
modern	(Default) A clean, colorful dashboard with charts and collapsible sections.	General use, stakeholder reports.
dark	A high-contrast dark theme version of the modern dashboard.	Late-night debugging, dark-mode lovers.
minimal	A text-heavy, high-density layout with no Javascript or charts.	Large test suites (10k+ tests), slow connections.
legacy	A simple table view similar to older Jenkins reports.	Backward compatibility.

## 📊 Example Output
The generated HTML report includes:

- Summary Cards: Total tests, passed, failed, skipped, and total duration.
- Test Cases Table: Sortable list of all test cases with status indicators.
- Failure Details: Expandable sections showing stack traces and error messages.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See LICENSE for more information.
