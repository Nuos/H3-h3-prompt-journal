"""Validate only the JSON Schema vocabulary used by this self-contained package.

This is not a general JSON Schema implementation. Unknown keywords fail closed.
"""
import json
import math
import re


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def validate(value, schema, root, path=""):
    supported = {"$schema", "$id", "$defs", "$ref", "title", "description", "oneOf", "const", "enum",
                 "type", "properties", "required", "additionalProperties", "propertyNames", "items",
                 "minItems", "uniqueItems", "minLength", "pattern", "minimum", "exclusiveMinimum"}
    errors = [(path, "Unsupported schema keyword " + key) for key in sorted(set(schema) - supported)]
    if errors:
        return errors
    if "$ref" in schema:
        name = schema["$ref"].removeprefix("#/$defs/")
        if name not in root["$defs"] or not schema["$ref"].startswith("#/$defs/"):
            return [(path, "Unresolvable local schema reference")]
        return validate(value, root["$defs"][name], root, path)
    if "oneOf" in schema:
        matches = [validate(value, child, root, path) for child in schema["oneOf"]]
        if sum(not item for item in matches) != 1:
            return [(path, "Value must match exactly one declared shape")]
    if "const" in schema and canonical(value) != canonical(schema["const"]):
        errors.append((path, "Expected constant " + repr(schema["const"])))
    if "enum" in schema and not any(canonical(value) == canonical(x) for x in schema["enum"]):
        errors.append((path, "Value is outside the declared enumeration"))
    types = {
        "object": lambda x: isinstance(x, dict), "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str), "integer": lambda x: type(x) is int,
        "number": lambda x: type(x) in (int, float) and math.isfinite(x),
        "boolean": lambda x: type(x) is bool, "null": lambda x: x is None,
    }
    if "type" in schema and (schema["type"] not in types or not types[schema["type"]](value)):
        return errors + [(path, "Expected " + str(schema["type"]))]
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append((path + "/" + key, "Required field is missing"))
        for key, child in value.items():
            pointer = path + "/" + key.replace("~", "~0").replace("/", "~1")
            if "propertyNames" in schema:
                errors += validate(key, schema["propertyNames"], root, pointer)
            if key in props:
                errors += validate(child, props[key], root, pointer)
            elif schema.get("additionalProperties") is False:
                errors.append((pointer, "Undeclared field"))
            elif isinstance(schema.get("additionalProperties"), dict):
                errors += validate(child, schema["additionalProperties"], root, pointer)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append((path, "Too few entries"))
        if schema.get("uniqueItems") and len({canonical(x) for x in value}) != len(value):
            errors.append((path, "Duplicate entries"))
        for i, child in enumerate(value):
            errors += validate(child, schema.get("items", {}), root, path + "/" + str(i))
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0) or (schema.get("minLength", 0) and not value.strip()):
            errors.append((path, "Empty or blank text; retain unknown information outside an accepted declaration"))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append((path, "Text does not match the public format"))
    if type(value) in (int, float):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append((path, "Below minimum"))
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append((path, "Must exceed the declared minimum"))
    return errors
