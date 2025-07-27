import json


def load_and_display_json(filename):
    """Load and display JSON data from a file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            print(f"\n=== {filename} ===")
            print(json.dumps(data, indent=2))
            return data
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in {filename}: {e}")
        return None


def analyze_structure(data, filename):
    """Analyze the structure of JSON data."""
    if not data:
        return

    print(f"\n--- Structure Analysis for {filename} ---")
    print(f"Top-level keys: {list(data.keys())}")

    # Check for nested objects
    nested_objects = [
        key for key, value in data.items() if isinstance(value, dict)
    ]
    if nested_objects:
        print(f"Nested objects: {nested_objects}")

    # Check for arrays
    arrays = [key for key, value in data.items() if isinstance(value, list)]
    if arrays:
        print(f"Arrays: {arrays}")


def convert_nested_to_unified(nested_data):
    """
    IMPLEMENT: Convert nested/hierarchical format to unified format
    Input: data-1.json format (nested objects)
    Output: unified format (same as nested but with format='unified')
    """
    # Create a deep copy to avoid modifying original data
    unified_data = json.loads(json.dumps(nested_data))

    # Update the metadata format to indicate it's been unified
    if 'metadata' in unified_data and isinstance(unified_data['metadata'],
                                                 dict):
        unified_data['metadata']['format'] = 'unified'

    return unified_data


def convert_flattened_to_unified(flattened_data):
    """
    IMPLEMENT: Convert flattened format to unified format
    Input: data-2.json format (flattened with prefixes)
    Output: unified format (nested structure)
    """
    unified_data = {}

    # Copy basic fields
    unified_data['message'] = flattened_data.get('message', '')
    unified_data['timestamp'] = flattened_data.get('timestamp', '')

    # Reconstruct user object from flattened fields
    unified_data['user'] = {
        'id': flattened_data.get('user_id'),
        'name': flattened_data.get('user_name', ''),
        'email': flattened_data.get('user_email', '')
    }

    # Reconstruct metadata object from flattened fields
    unified_data['metadata'] = {
        'version': flattened_data.get('metadata_version', ''),
        'format': 'unified',  # Mark as unified format
        'encoding': flattened_data.get('metadata_encoding', '')
    }

    # Convert serialized items back to objects
    unified_data['items'] = []
    if 'items' in flattened_data and isinstance(flattened_data['items'], list):
        for item_str in flattened_data['items']:
            # Parse "id:title:active" format
            parts = item_str.split(':')
            if len(parts) == 3:
                item_obj = {
                    'id': int(parts[0]),
                    'title': parts[1],
                    'active': parts[2].lower() == 'true'
                }
                unified_data['items'].append(item_obj)

    return unified_data


def test_conversions():
    """Test the conversion functions with the sample data."""
    print("\n" + "=" * 60)
    print("TESTING CONVERSION FUNCTIONS")
    print("=" * 60)

    # Load original data files
    nested_data = load_and_display_json('data-1.json')
    flattened_data = load_and_display_json('data-2.json')

    if nested_data:
        print("\n--- Converting Nested to Unified ---")
        unified_from_nested = convert_nested_to_unified(nested_data)
        print(json.dumps(unified_from_nested, indent=2))

    if flattened_data:
        print("\n--- Converting Flattened to Unified ---")
        unified_from_flattened = convert_flattened_to_unified(flattened_data)
        print(json.dumps(unified_from_flattened, indent=2))

    # Load and compare with target format
    target_data = load_and_display_json('data-result.json')

    if nested_data and target_data:
        print("\n--- Comparing Results ---")
        unified_nested = convert_nested_to_unified(nested_data)
        print(
            f"Nested->Unified matches target: {unified_nested == target_data}")

    if flattened_data and target_data:
        unified_flattened = convert_flattened_to_unified(flattened_data)
        print(
            f"Flattened->Unified matches target: {unified_flattened == target_data}"
        )


def compare_data_formats():
    """Compare the two different data formats."""
    print("Exploring two different JSON data formats...")

    # Load both files
    data1 = load_and_display_json('data-1.json')
    data2 = load_and_display_json('data-2.json')

    # Analyze structures
    analyze_structure(data1, 'data-1.json')
    analyze_structure(data2, 'data-2.json')

    print("\n--- Format Comparison ---")
    print("data-1.json uses a NESTED/HIERARCHICAL format:")
    print("  - User info is grouped in a 'user' object")
    print("  - Metadata is grouped in a 'metadata' object")
    print("  - Items contain full object structures")

    print("\ndata-2.json uses a FLATTENED format:")
    print(
        "  - User info is flattened with prefixes (user_id, user_name, etc.)")
    print("  - Metadata is flattened with prefixes (metadata_version, etc.)")
    print("  - Items are serialized as strings with delimiters")

    print("\n--- Key Differences ---")
    print("1. Nested vs Flattened structure")
    print("2. Object grouping vs prefix naming")
    print("3. Structured arrays vs serialized strings")
    print("4. Readability vs compactness trade-offs")


if __name__ == "__main__":
    compare_data_formats()
    test_conversions()
