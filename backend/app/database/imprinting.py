"""Template Imprinting Protocol validation and utilities."""

import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ImprintingValidationResult:
    """Result of Template Imprinting Protocol validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    token_count: int
    adherence_score: float


class TemplateImprintingValidator:
    """Validates Template Imprinting Protocol structures."""
    
    # Token patterns from the protocol specification
    FILL_PATTERN = re.compile(r'\{FILL:\s*([^}]+)\}')
    ENUM_PATTERN = re.compile(r'\{ENUM:\s*([^}]+)\}')
    REF_PATTERN = re.compile(r'@\{REF:\s*([^}]+)\}')
    AUTO_PATTERN = re.compile(r'@auto_([a-z_]+)')
    
    MAX_HEADLINE_LENGTH = 200
    OPTIMAL_TOKEN_RANGE = (50, 200)
    
    def validate_template_mode(self, template_mode: Dict[str, Any]) -> List[str]:
        """Validate the template_mode block.
        
        Args:
            template_mode: Template mode configuration
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Required fields
        required_fields = ['level', 'headline']
        for field in required_fields:
            if field not in template_mode:
                errors.append(f"template_mode missing required field: {field}")
        
        # Validate level
        if 'level' in template_mode:
            valid_levels = ['fatal', 'warning', 'info']
            if template_mode['level'] not in valid_levels:
                errors.append(f"Invalid level '{template_mode['level']}'. Must be one of: {valid_levels}")
        
        # Validate headline length
        if 'headline' in template_mode:
            headline = template_mode['headline']
            if len(headline) > self.MAX_HEADLINE_LENGTH:
                errors.append(f"Headline too long ({len(headline)} chars). Max: {self.MAX_HEADLINE_LENGTH}")
            if len(headline.strip()) == 0:
                errors.append("Headline cannot be empty")
        
        return errors
    
    def validate_template_structure(self, template_structure: Dict[str, Any]) -> List[str]:
        """Validate the template structure.
        
        Args:
            template_structure: Template structure configuration
            
        Returns:
            List of validation errors
        """
        errors = []
        
        if not template_structure:
            errors.append("Template structure cannot be empty")
            return errors
        
        # Validate each field in the template
        for path, value_spec in template_structure.items():
            if not isinstance(path, str):
                errors.append(f"Template path must be string, got {type(path)}")
                continue
            
            # Validate path format (dot notation, arrays)
            if not self._is_valid_path(path):
                errors.append(f"Invalid template path: {path}")
            
            # Validate value specification
            if isinstance(value_spec, str):
                spec_errors = self._validate_value_spec(value_spec)
                errors.extend([f"Path '{path}': {error}" for error in spec_errors])
        
        return errors
    
    def _is_valid_path(self, path: str) -> bool:
        """Check if a template path is valid dot notation."""
        # Allow: field.subfield, array[0], array[*], field.array[*].subfield
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*|\[\*?\]|\[\d+\])*$'
        return bool(re.match(pattern, path))
    
    def _validate_value_spec(self, value_spec: str) -> List[str]:
        """Validate a value specification string."""
        errors = []
        
        # Check for recognized patterns
        fill_match = self.FILL_PATTERN.search(value_spec)
        enum_match = self.ENUM_PATTERN.search(value_spec)
        ref_match = self.REF_PATTERN.search(value_spec)
        auto_match = self.AUTO_PATTERN.search(value_spec)
        
        if fill_match:
            description = fill_match.group(1).strip()
            if not description:
                errors.append("FILL description cannot be empty")
        elif enum_match:
            enum_values = enum_match.group(1).strip()
            if not enum_values:
                errors.append("ENUM values cannot be empty")
            else:
                # Validate enum format: value1|value2|value3
                values = [v.strip() for v in enum_values.split('|')]
                if len(values) < 2:
                    errors.append("ENUM must have at least 2 options")
                for value in values:
                    if not value:
                        errors.append("ENUM values cannot be empty")
        elif ref_match:
            ref_type = ref_match.group(1).strip()
            if not ref_type:
                errors.append("REF type cannot be empty")
        elif auto_match:
            auto_action = auto_match.group(1)
            valid_auto_actions = ['balance', 'calculate', 'generate', 'validate']
            if auto_action not in valid_auto_actions:
                errors.append(f"Unknown auto action: {auto_action}")
        else:
            # Not a template pattern - should be a literal value
            pass
        
        return errors
    
    def calculate_token_count(self, template_mode: Dict[str, Any], 
                            template_structure: Dict[str, Any]) -> int:
        """Calculate approximate token count for imprinting."""
        # Rough token estimation: 1 token ≈ 4 characters
        content = json.dumps({"template_mode": template_mode, "template": template_structure})
        return len(content) // 4
    
    def calculate_adherence_score(self, template_mode: Dict[str, Any],
                                template_structure: Dict[str, Any]) -> float:
        """Calculate adherence score based on Template Imprinting Protocol best practices."""
        score = 1.0
        
        # Check template_mode quality
        if 'level' not in template_mode:
            score -= 0.2
        elif template_mode['level'] != 'fatal':
            score -= 0.1
        
        if 'headline' not in template_mode:
            score -= 0.3
        else:
            headline_len = len(template_mode['headline'])
            if headline_len > self.MAX_HEADLINE_LENGTH:
                score -= 0.2
            elif headline_len < 20:
                score -= 0.1
        
        # Check template structure quality
        if not template_structure:
            score -= 0.5
        else:
            # Prefer inline enums and specific patterns
            pattern_count = 0
            total_fields = len(template_structure)
            
            for value_spec in template_structure.values():
                if isinstance(value_spec, str):
                    if (self.ENUM_PATTERN.search(value_spec) or 
                        self.FILL_PATTERN.search(value_spec) or
                        self.REF_PATTERN.search(value_spec)):
                        pattern_count += 1
            
            if total_fields > 0:
                pattern_ratio = pattern_count / total_fields
                score *= pattern_ratio
        
        return max(0.0, min(1.0, score))
    
    def validate_imprinting_template(self, template_mode: Dict[str, Any],
                                   template_structure: Dict[str, Any],
                                   example_filled: Optional[Dict[str, Any]] = None) -> ImprintingValidationResult:
        """Validate a complete Template Imprinting Protocol template.
        
        Args:
            template_mode: Behavioral configuration
            template_structure: Template structure
            example_filled: Optional example
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Validate template_mode
        mode_errors = self.validate_template_mode(template_mode)
        errors.extend(mode_errors)
        
        # Validate template_structure
        structure_errors = self.validate_template_structure(template_structure)
        errors.extend(structure_errors)
        
        # Calculate metrics
        token_count = self.calculate_token_count(template_mode, template_structure)
        adherence_score = self.calculate_adherence_score(template_mode, template_structure)
        
        # Check token count
        if token_count < self.OPTIMAL_TOKEN_RANGE[0]:
            warnings.append(f"Token count ({token_count}) below optimal range {self.OPTIMAL_TOKEN_RANGE}")
        elif token_count > self.OPTIMAL_TOKEN_RANGE[1]:
            warnings.append(f"Token count ({token_count}) above optimal range {self.OPTIMAL_TOKEN_RANGE}")
        
        # Validate example if provided
        if example_filled:
            example_errors = self._validate_example_structure(template_structure, example_filled)
            errors.extend(example_errors)
        
        return ImprintingValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            token_count=token_count,
            adherence_score=adherence_score
        )
    
    def _validate_example_structure(self, template_structure: Dict[str, Any],
                                  example: Dict[str, Any]) -> List[str]:
        """Validate that example matches template structure."""
        errors = []
        
        # Check that example fields match template paths
        template_paths = set(template_structure.keys())
        
        def extract_paths_from_example(obj: Any, prefix: str = "") -> set:
            """Extract dot-notation paths from example object."""
            paths = set()
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{prefix}.{key}" if prefix else key
                    paths.add(current_path)
                    if isinstance(value, (dict, list)):
                        paths.update(extract_paths_from_example(value, current_path))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{prefix}[{i}]"
                    if isinstance(item, (dict, list)):
                        paths.update(extract_paths_from_example(item, current_path))
            return paths
        
        example_paths = extract_paths_from_example(example)
        
        # Check for missing template paths in example
        missing_paths = template_paths - example_paths
        if missing_paths:
            errors.append(f"Example missing template paths: {missing_paths}")
        
        return errors


# Global validator instance
imprinting_validator = TemplateImprintingValidator()