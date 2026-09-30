# IMAGE ANALYZER

import os
from PIL import Image

# 1. IMAGE VALIDATION

def analyze_image(image_path):

    # Remove accidental quotation marks

    image_path = image_path.strip().strip('"').strip("'")

# Check file exists

    if not os.path.isfile(image_path):

        return {
            "status": "Failed",
            "image_valid": False,
            "image_type": None,
            "width": None,
            "height": None,
            "message": "Image file was not found."
        }

# Try opening image

    try:

        image = Image.open(image_path)

        # Check that image is readable
        image.verify()

        # Re-open after verify()
        image = Image.open(image_path)

        width, height = image.size

# Get image format

        image_type = image.format

# Return result

        return {

            "status": "Success",

            "image_valid": True,

            "image_type":
                image_type,

            "width":
                width,

            "height":
                height,

            "message":
                "Image uploaded successfully "
                "and is ready for AI analysis."
        }

    except Exception as e:

        return {

            "status": "Failed",

            "image_valid": False,

            "image_type": None,

            "width": None,

            "height": None,

            "message":
                f"Invalid or unreadable image: {e}"
        }

# 2. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("          IMAGE ANALYZER")
    print("===================================")

    image_path = input(
        "\nEnter image path: "
    ).strip()

# Analyze image

    result = analyze_image(
        image_path
    )

# DISPLAY RESULT

    print("\n===================================")
    print("         IMAGE RESULT")
    print("===================================")

    print(
        "\nStatus:",
        result["status"]
    )

    print(
        "Image Valid:",
        result["image_valid"]
    )

    print(
        "Image Type:",
        result["image_type"]
    )

    print(
        "Width:",
        result["width"]
    )

    print(
        "Height:",
        result["height"]
    )

    print(
        "Message:",
        result["message"]
    )

    print("\n===================================")