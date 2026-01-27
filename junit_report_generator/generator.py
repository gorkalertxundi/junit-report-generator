"""HTML report generator using simple template rendering."""

import os
import html
from datetime import datetime
from typing import Dict, Any, List


class ReportGenerator:
    """Generate HTML reports from parsed JUnit data."""

    def __init__(self, template_name: str = "basic"):
        """Initialize report generator with template.
        
        Args:
            template_name: Name of the template to use (basic, modern, or detailed)
        """
        self.template_name = template_name
        self.template_path = self._get_template_path(template_name)

    def _get_template_path(self, template_name: str) -> str:
        """Get the full path to the template file.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Full path to the template file
        """
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        template_file = f"{template_name}.html"
        return os.path.join(templates_dir, template_file)

    def generate(self, data: Dict[str, Any], output_path: str) -> None:
        """Generate HTML report from parsed data.
        
        Args:
            data: Parsed JUnit test data
            output_path: Path where the HTML report will be saved
        """
        # Read template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Calculate additional metrics
        total_passed = (data['total_tests'] - data['total_failures'] - 
                       data['total_errors'] - data['total_skipped'])
        
        success_rate = 0
        if data['total_tests'] > 0:
            success_rate = round((total_passed / data['total_tests']) * 100, 1)

        # Prepare context
        context = {
            'total_tests': data['total_tests'],
            'total_passed': total_passed,
            'total_failures': data['total_failures'],
            'total_errors': data['total_errors'],
            'total_skipped': data['total_skipped'],
            'total_failed_and_errors': data['total_failures'] + data['total_errors'],
            'total_testsuites': len(data['testsuites']),
            'total_time': round(data['total_time'], 2),
            'testsuites': data['testsuites'],
            'success_rate': success_rate,
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Render template
        html_content = self._render_template(template, context)

        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _render_template(self, template: str, context: Dict[str, Any]) -> str:
        """Simple template rendering using manual parsing.
        
        Args:
            template: Template string
            context: Context dictionary with values
            
        Returns:
            Rendered HTML string
        """
        result = template
        
        # Replace simple variables first
        for key, value in context.items():
            if not isinstance(value, (list, dict)):
                placeholder = "{{ " + key + " }}"
                result = result.replace(placeholder, str(value))
        
        # Handle for loops manually
        result = self._process_loops(result, context)
        
        return result

    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process for loops in template."""
        result = []
        i = 0
        
        while i < len(template):
            # Look for {% for
            if template[i:i+7] == '{% for ':
                # Find the end of the for tag
                end_tag = template.find(' %}', i)
                if end_tag == -1:
                    result.append(template[i])
                    i += 1
                    continue
                
                # Parse the for statement
                for_statement = template[i+7:end_tag].strip()
                parts = for_statement.split(' in ')
                if len(parts) != 2:
                    result.append(template[i])
                    i += 1
                    continue
                
                item_name = parts[0].strip()
                list_name = parts[1].strip()
                
                # Find the matching {% endfor %}
                loop_start = end_tag + 3
                depth = 1
                j = loop_start
                
                while j < len(template) and depth > 0:
                    if template[j:j+7] == '{% for ':
                        depth += 1
                        j += 7
                    elif template[j:j+12] == '{% endfor %}':
                        depth -= 1
                        if depth == 0:
                            break
                        j += 12
                    else:
                        j += 1
                
                if depth != 0:
                    result.append(template[i])
                    i += 1
                    continue
                
                loop_content = template[loop_start:j]
                
                # Process the loop
                if list_name in context and isinstance(context[list_name], list):
                    for item in context[list_name]:
                        rendered_item = self._render_item(loop_content, item_name, item, context)
                        result.append(rendered_item)
                
                i = j + 12  # Skip past {% endfor %}
            else:
                result.append(template[i])
                i += 1
        
        return ''.join(result)

    def _render_item(self, content: str, item_name: str, item: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Render a single item in a loop."""
        result = content
        
        if isinstance(item, dict):
            # Replace all item.property references
            for key, value in item.items():
                # Handle different formats
                placeholder1 = "{{ " + item_name + "." + key + " }}"
                placeholder2 = "{{ " + item_name + "." + key + "|upper }}"
                placeholder3 = "{{ " + item_name + "." + key + "|length }}"
                
                # Escape HTML by default
                str_value = html.escape(str(value)) if value else ''
                
                result = result.replace(placeholder1, str_value)
                result = result.replace(placeholder2, str_value.upper())
                result = result.replace(placeholder3, str(len(value)) if hasattr(value, '__len__') else '0')
        
        # Handle nested loops
        result = self._process_loops(result, {**context, item_name: item})
        
        # Handle if statements
        result = self._process_ifs(result, {**context, item_name: item})
        
        return result

    def _process_ifs(self, template: str, context: Dict[str, Any]) -> str:
        """Process if statements in template."""
        result = []
        i = 0
        
        while i < len(template):
            # Look for {% if
            if template[i:i+6] == '{% if ':
                # Find the end of the if tag
                end_tag = template.find(' %}', i)
                if end_tag == -1:
                    result.append(template[i])
                    i += 1
                    continue
                
                # Parse the if statement
                condition = template[i+6:end_tag].strip()
                
                # Find the matching {% endif %}
                content_start = end_tag + 3
                depth = 1
                j = content_start
                
                while j < len(template) and depth > 0:
                    if template[j:j+6] == '{% if ':
                        depth += 1
                        j += 6
                    elif template[j:j+11] == '{% endif %}':
                        depth -= 1
                        if depth == 0:
                            break
                        j += 11
                    else:
                        j += 1
                
                if depth != 0:
                    result.append(template[i])
                    i += 1
                    continue
                
                if_content = template[content_start:j]
                
                # Evaluate condition
                condition_value = self._eval_condition(condition, context)
                
                if condition_value:
                    result.append(if_content)
                
                i = j + 11  # Skip past {% endif %}
            else:
                result.append(template[i])
                i += 1
        
        return ''.join(result)

    def _eval_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple condition."""
        # Simple evaluation - just check if the variable exists and is truthy
        parts = condition.split('.')
        value = context
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return False
        
        # Check if truthy
        return bool(value)


def list_templates() -> List[str]:
    """List available templates.
    
    Returns:
        List of available template names
    """
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    templates = []
    
    if os.path.exists(templates_dir):
        for filename in os.listdir(templates_dir):
            if filename.endswith('.html'):
                templates.append(filename[:-5])  # Remove .html extension
    
    return sorted(templates)
