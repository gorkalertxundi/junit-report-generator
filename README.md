# junit-report-generator

Transform JUnit XML reports into clean, standalone HTML reports. Perfect for visualizing test results, analyzing failures, and sharing test summaries via CI/CD pipelines without external dependencies.

## Features

- 🎨 **Multiple Templates**: Choose from basic, modern, or detailed HTML templates
- 📊 **Rich Test Reporting**: Displays test suites, test cases, failures, errors, and skipped tests
- 🚀 **Zero Dependencies**: Standalone tool with no external runtime dependencies
- 📦 **Easy Installation**: Install via pip from PyPI
- 🔧 **CLI Interface**: Simple command-line interface for quick report generation
- 💯 **Pure Python**: Works with Python 3.7+

## Installation

```bash
pip install junit-report-generator
```

## Usage

### Basic Usage

Generate a basic HTML report from a JUnit XML file:

```bash
junit-report-generator junit-results.xml report.html
```

### Using Different Templates

Choose from three built-in templates: `basic`, `modern`, or `detailed`:

```bash
# Use the modern template
junit-report-generator junit-results.xml report.html --template modern

# Use the detailed template
junit-report-generator junit-results.xml report.html --template detailed
```

### List Available Templates

```bash
junit-report-generator --list-templates
```

### Command-Line Options

```
usage: junit-report-generator [-h] [-t {basic,modern,detailed}] [--list-templates] [--version] [input] [output]

Transform JUnit XML reports into clean, standalone HTML reports

positional arguments:
  input                 Path to JUnit XML file
  output                Path to output HTML file

options:
  -h, --help            show this help message and exit
  -t {basic,modern,detailed}, --template {basic,modern,detailed}
                        HTML template to use (default: basic)
  --list-templates      List available templates and exit
  --version             show program's version number and exit
```

## Templates

### Basic Template
A clean and simple report with essential information.

![Basic Template](https://github.com/user-attachments/assets/d447b207-c9aa-460c-bc17-b3551e14a794)

### Modern Template
A modern, gradient-based design with enhanced visual appeal.

![Modern Template](https://github.com/user-attachments/assets/1696e18c-d38b-4309-88d9-8f61a38d3c2e)

### Detailed Template
Comprehensive view with statistics and detailed test information.

![Detailed Template](https://github.com/user-attachments/assets/273ae333-2e9f-41af-9287-2aae41c6ae5f)

## Example

```bash
# Generate a modern HTML report from pytest JUnit XML output
pytest --junitxml=test-results.xml
junit-report-generator test-results.xml test-report.html --template modern
```

## JUnit XML Format

This tool supports standard JUnit XML format. Here's a simple example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
    <testsuite name="MyTests" tests="3" failures="1" errors="0" skipped="0" time="1.234">
        <testcase name="test_success" classname="tests.MyTests" time="0.456"/>
        <testcase name="test_failure" classname="tests.MyTests" time="0.123">
            <failure message="AssertionError: Expected True">
                Traceback information here...
            </failure>
        </testcase>
        <testcase name="test_skipped" classname="tests.MyTests" time="0.001">
            <skipped message="Not implemented yet"/>
        </testcase>
    </testsuite>
</testsuites>
```

## Integration with Testing Frameworks

### pytest

```bash
pytest --junitxml=junit.xml
junit-report-generator junit.xml report.html
```

### unittest (Python)

```python
import xmlrunner

# In your test runner
runner = xmlrunner.XMLTestRunner(output='test-reports')
runner.run(test_suite)
```

Then generate the report:

```bash
junit-report-generator test-reports/TEST-*.xml report.html
```

### Maven (Java)

Maven Surefire automatically generates JUnit XML reports:

```bash
mvn test
junit-report-generator target/surefire-reports/*.xml report.html
```

### Gradle (Java)

```bash
gradle test
junit-report-generator build/test-results/test/*.xml report.html
```

## Development

### Setup

```bash
git clone https://github.com/gorkalertxundi/junit-report-generator.git
cd junit-report-generator
pip install -e .
```

### Running Tests

```bash
# Test with the example file
python -m junit_report_generator.cli examples/sample-junit.xml output.html
```

### Building for PyPI

```bash
pip install build
python -m build
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Similar Tools

- **junit2html**: Another popular tool for converting JUnit XML to HTML
- **allure**: Comprehensive test reporting framework

## Why junit-report-generator?

- ✅ No external dependencies
- ✅ Multiple modern templates
- ✅ Simple and fast
- ✅ Easy to integrate into CI/CD pipelines
- ✅ Active maintenance

## Support

- GitHub Issues: https://github.com/gorkalertxundi/junit-report-generator/issues
- PyPI: https://pypi.org/project/junit-report-generator/
