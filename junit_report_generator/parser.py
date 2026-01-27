"""Parser for JUnit XML reports."""

import xml.etree.ElementTree as ET
from typing import Dict, List, Any


class JUnitParser:
    """Parse JUnit XML files and extract test results."""

    def __init__(self, xml_path: str):
        """Initialize parser with XML file path.
        
        Args:
            xml_path: Path to the JUnit XML file
        """
        self.xml_path = xml_path
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    def parse(self) -> Dict[str, Any]:
        """Parse the JUnit XML and return structured data.
        
        Returns:
            Dictionary containing parsed test results
        """
        data = {
            'testsuites': [],
            'total_tests': 0,
            'total_failures': 0,
            'total_errors': 0,
            'total_skipped': 0,
            'total_time': 0.0,
        }

        # Handle both <testsuites> and single <testsuite> root elements
        if self.root.tag == 'testsuites':
            testsuites = self.root.findall('testsuite')
        elif self.root.tag == 'testsuite':
            testsuites = [self.root]
        else:
            testsuites = []

        for testsuite in testsuites:
            suite_data = self._parse_testsuite(testsuite)
            data['testsuites'].append(suite_data)
            data['total_tests'] += suite_data['tests']
            data['total_failures'] += suite_data['failures']
            data['total_errors'] += suite_data['errors']
            data['total_skipped'] += suite_data['skipped']
            data['total_time'] += suite_data['time']

        return data

    def _parse_testsuite(self, testsuite: ET.Element) -> Dict[str, Any]:
        """Parse a single test suite.
        
        Args:
            testsuite: XML element representing a test suite
            
        Returns:
            Dictionary containing test suite data
        """
        suite_data = {
            'name': testsuite.get('name', 'Unknown'),
            'tests': int(testsuite.get('tests', '0')),
            'failures': int(testsuite.get('failures', '0')),
            'errors': int(testsuite.get('errors', '0')),
            'skipped': int(testsuite.get('skipped', '0')),
            'time': float(testsuite.get('time', '0')),
            'timestamp': testsuite.get('timestamp', ''),
            'testcases': []
        }

        for testcase in testsuite.findall('testcase'):
            testcase_data = self._parse_testcase(testcase)
            suite_data['testcases'].append(testcase_data)

        return suite_data

    def _parse_testcase(self, testcase: ET.Element) -> Dict[str, Any]:
        """Parse a single test case.
        
        Args:
            testcase: XML element representing a test case
            
        Returns:
            Dictionary containing test case data
        """
        testcase_data = {
            'name': testcase.get('name', 'Unknown'),
            'classname': testcase.get('classname', ''),
            'time': float(testcase.get('time', '0')),
            'status': 'passed',
            'message': '',
            'details': ''
        }

        # Check for failure
        failure = testcase.find('failure')
        if failure is not None:
            testcase_data['status'] = 'failed'
            testcase_data['message'] = failure.get('message', '')
            testcase_data['details'] = failure.text or ''

        # Check for error
        error = testcase.find('error')
        if error is not None:
            testcase_data['status'] = 'error'
            testcase_data['message'] = error.get('message', '')
            testcase_data['details'] = error.text or ''

        # Check for skipped
        skipped = testcase.find('skipped')
        if skipped is not None:
            testcase_data['status'] = 'skipped'
            testcase_data['message'] = skipped.get('message', '')
            testcase_data['details'] = skipped.text or ''

        return testcase_data
