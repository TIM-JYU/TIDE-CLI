def json_to_key_value_pairs(json_data: dict):
    """
    Convert json to key value pairs
    """
    return {
        course["course_name"]: course["course_id"] for course in json_data["courses"]
    }
