import pandas as pd
import argparse
import json

def load_schema(schema_path):
    with open(schema_path, 'r') as f:
        return json.load(f)

def validate_schema(df, schema):
    errors = []

    # Check required columns
    for col in schema['required_columns']:
        if col not in df.columns:
            errors.append(f"Missing required column: {col}")

    # Check dtypes
    for col, expected_type in schema['columns'].items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                errors.append(f"Column {col}: expected {expected_type}, found {actual_type}")

    return errors

def check_nulls(df, schema):
    errors = []
    for col in schema['no_nulls']:
        if df[col].isnull().any():
            errors.append(f"Null values found in column: {col}")
    return errors

def check_constraints(df, schema):
    errors = []
    for col, constraints in schema.get("value_constraints", {}).items():
        if "min" in constraints and (df[col] < constraints["min"]).any():
            errors.append(f"Column {col} has values below {constraints['min']}")
        if "max" in constraints and (df[col] > constraints["max"]).any():
            errors.append(f"Column {col} has values above {constraints['max']}")
    return errors

def main():
    parser = argparse.ArgumentParser(description="Data Validation Toolkit")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--schema", required=True, help="Path to schema JSON")
    args = parser.parse_args()

    df = pd.read_csv(args.file)
    schema = load_schema(args.schema)

    errors = []
    errors += validate_schema(df, schema)
    errors += check_nulls(df, schema)
    errors += check_constraints(df, schema)

    if errors:
        print("\n🚨 Validation Errors Found:")
        for e in errors:
            print(f"- {e}")
    else:
        print("✅ All checks passed.")

if __name__ == "__main__":
    main()