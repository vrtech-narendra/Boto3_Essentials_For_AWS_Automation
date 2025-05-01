import argparse
import sys 
try: 
    import boto3
except ModuleNotFoundError :
    print("Please Install boto3 Module First and Retry")
    sys.exit(1)

def classify_methods(service_name):
    crud_patterns = {
        "Create": ("create_", "put_", "allocate_", "add_"),
        "Read": ("get_", "describe_", "list_", "fetch_"),
        "Update": ("update_", "modify_"),
        "Delete": ("delete_", "remove_", "terminate_", "revoke_")
    }

    client = boto3.client(service_name, 'us-east-1')
    methods = [m for m in dir(client) if callable(getattr(client, m)) and not m.startswith('_')]

    crud_methods = {key: [] for key in crud_patterns}
    crud_methods["Other"] = []

    for method in methods:
        matched = False
        for category, prefixes in crud_patterns.items():
            if any(method.startswith(prefix) for prefix in prefixes):
                crud_methods[category].append(method)
                matched = True
                break
        if not matched:
            crud_methods["Other"].append(method)

    return crud_methods

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Required Methods from client ")
    parser.add_argument('-s', '--serviceName', required=True)
    parser.add_argument('-m', '--methodType', required=True, choices=['create','read','update', 'delete'])
    args = parser.parse_args()
    service=args.serviceName
    methodType=args.methodType                           
    try:
        classified = classify_methods(service)
        for category, methods in classified.items():
            if category.lower() not in [ methodType, "other"]:
                continue
            print(f"\n{category} Methods:")
            for method in methods:
                print(f" - {method}")
    except Exception as e:
        print(f"Error: {e}")
