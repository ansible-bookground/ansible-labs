from typing import Union, Any
from ansiblelint.rules import AnsibleLintRule

class DeprecatedVariableRule(AnsibleLintRule):
    """Deprecated variable declarations."""

    id = 'EXAMPLE001'
    description = 'Check for lines that have old style ${var} ' + \
                  'declarations'
    tags = { 'deprecations' }

    def match(self, line: str) -> Union[bool, str]:
        return '${' in line
