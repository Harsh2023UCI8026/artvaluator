def validate_all(data, image=None):

    if image is None:
        return False, "No image uploaded"

    if data["material_cost"] < 0:
        return False, "Material cost invalid"

    if data["time_spent"] <= 0:
        return False, "Time must be greater than 0"

    if data["detail_level"] < 0 or data["detail_level"] > 10:
        return False, "Detail must be between 0-10"

    return True, "Valid"