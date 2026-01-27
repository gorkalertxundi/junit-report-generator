"""Command-line interface for junit-report-generator."""

import argparse
import sys
import os
from junit_report_generator.parser import JUnitParser
from junit_report_generator.generator import ReportGenerator, list_templates


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='junit-report-generator',
        description='Transform JUnit XML reports into clean, standalone HTML reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate a basic HTML report
  junit-report-generator junit-results.xml report.html

  # Use a modern template
  junit-report-generator junit-results.xml report.html --template modern

  # List available templates
  junit-report-generator --list-templates
        '''
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Path to JUnit XML file'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Path to output HTML file'
    )
    
    parser.add_argument(
        '-t', '--template',
        default='basic',
        choices=['basic', 'modern', 'detailed'],
        help='HTML template to use (default: basic)'
    )
    
    parser.add_argument(
        '--list-templates',
        action='store_true',
        help='List available templates and exit'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle --list-templates
    if args.list_templates:
        templates = list_templates()
        print("Available templates:")
        for template in templates:
            print(f"  - {template}")
        return 0
    
    # Validate required arguments
    if not args.input or not args.output:
        parser.error("Both input and output arguments are required (unless using --list-templates)")
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1
    
    try:
        # Parse JUnit XML
        print(f"Parsing JUnit XML from '{args.input}'...")
        junit_parser = JUnitParser(args.input)
        data = junit_parser.parse()
        
        # Generate HTML report
        print(f"Generating HTML report using '{args.template}' template...")
        generator = ReportGenerator(args.template)
        generator.generate(data, args.output)
        
        print(f"✓ Report generated successfully: '{args.output}'")
        print(f"  Total tests: {data['total_tests']}")
        print(f"  Passed: {data['total_tests'] - data['total_failures'] - data['total_errors'] - data['total_skipped']}")
        print(f"  Failed: {data['total_failures']}")
        print(f"  Errors: {data['total_errors']}")
        print(f"  Skipped: {data['total_skipped']}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
