from datetime import datetime

def date_convert(date_str):
    # !Raw date string must be in ISO 8601 format
    try:
        # Parse the date string into a datetime object if '%Y-%m-%dT%H:%M:%S.%fZ' is the format string
        parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Format and return the date in a more readable way (e.g., "October 8, 2024, 10:13 AM")
        return parsed_date.strftime("%B %d, %Y, %I:%M %p")

    except Exception as e:
        print(f"❌ Exception occurred while converting date to readable format: {e}")
        return date_str

