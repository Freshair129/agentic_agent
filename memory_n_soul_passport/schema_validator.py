import json
from pathlib import Path
from jsonschema import validate, ValidationError
from typing import Dict, Any, Optional

class MSPSchemaValidator:
    """
    Validates MSP data against strict JSON schemas.
    Enforces the 'Data Integrity Protocol' for bio-cognitive states.
    """

    def __init__(self, schema_dir: Path):
        self.schema_dir = schema_dir
        self.schemas = {}
        self._load_schemas()

    def _load_schemas(self):
        """
        Load all JSON schemas from the schema directory.
        Expects standard naming: Name_Schema.json
        """
        if not self.schema_dir.exists():
            print(f"[MSP Validator] ⚠️ Schema directory not found: {self.schema_dir}")
            return

        for schema_file in self.schema_dir.glob("*.json"):
            # Clean name: "State_Storage_Schema" -> "State_Storage_Schema"
            # (Matches file stem)
            schema_name = schema_file.stem
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    self.schemas[schema_name] = json.load(f)
            except Exception as e:
                print(f"[MSP Validator] ❌ Failed to load schema {schema_name}: {e}")

    def validate(self, data: Dict[str, Any], schema_name: str) -> bool:
        """
        Validate data against a loaded schema.
        
        Args:
            data: The dictionary data to validate.
            schema_name: The name of the schema file (without .json).
            
        Returns:
            True if valid.
            
        Raises:
            ValueError: If schema is not found.
            ValidationError: If data does not match schema.
        """
        if schema_name not in self.schemas:
            raise ValueError(f"Schema '{schema_name}' not found in registry.")

        try:
            validate(instance=data, schema=self.schemas[schema_name])
            return True
        except ValidationError as e:
            # Enhanced Error Logging
            print(f"\n[MSP Validator] ❌ Schema Violation in '{schema_name}':")
            path = " -> ".join([str(p) for p in e.path]) if e.path else "root"
            print(f"  📍 Location: {path}")
            print(f"  🛑 Error: {e.message}")
            if e.context:
                print(f"  🔎 Context: {e.context}")
                
            raise e

    def validate_safe(self, data: Dict[str, Any], schema_name: str) -> bool:
        """
        Validate data without raising exceptions (Boolean Check).
        Useful for non-critical monitoring.
        """
        try:
            return self.validate(data, schema_name)
        except (ValidationError, ValueError):
            return False
