# DEPARTMENT ROUTING ENGINE

# 1. DEPARTMENT MAPPING

DEPARTMENT_MAPPING = {

    "Water Supply": {
        "department": "Water Supply Department",
        "team": "Water Supply Team",
        "office_type": "Municipal Water Department"
    },

    "Electricity": {
        "department": "Electricity Department",
        "team": "Electricity Maintenance Team",
        "office_type": "Electricity Service Department"
    },

    "Street Light": {
        "department": "Municipal Street Light Department",
        "team": "Street Light Maintenance Team",
        "office_type": "Municipal Corporation"
    },

    "Road": {
        "department": "Road Department",
        "team": "Road Maintenance Team",
        "office_type": "PWD / Municipal Road Department"
    },

    "Healthcare": {
        "department": "Health Department",
        "team": "Healthcare Services Team",
        "office_type": "District Health Department"
    },

    "Sanitation": {
        "department": "Sanitation Department",
        "team": "Sanitation Maintenance Team",
        "office_type": "Municipal Corporation"
    },

    "Drainage": {
        "department": "Drainage Department",
        "team": "Drainage Maintenance Team",
        "office_type": "Municipal Corporation"
    },

    "Environment": {
        "department": "Environment Department",
        "team": "Environmental Services Team",
        "office_type": "Municipal / Environmental Department"
    }
}

# 2. ROUTING FUNCTION

def route_complaint(
    category,
    city=None,
    district=None,
    area=None
    ):

    # Check category

    if category is None:

        return {
            "routing_status": "Failed",
            "department": None,
            "team": None,
            "office_type": None,
            "city": city,
            "district": district,
            "area": area,
            "routing_reason": (
                "Complaint category is not available."
            )
        }

# Find department

    routing_info = DEPARTMENT_MAPPING.get(
        category
    )

# Unknown category

    if routing_info is None:

        return {
            "routing_status": "Failed",
            "department": "General Grievance Department",
            "team": "General Complaint Handling Team",
            "office_type": "District Grievance Office",
            "city": city,
            "district": district,
            "area": area,
            "routing_reason": (
                "Category was not recognized, "
                "so complaint is routed to "
                "the general grievance department."
            )
        }

# Successful routing

    return {

        "routing_status": "Success",

        "department":
            routing_info["department"],

        "team":
            routing_info["team"],

        "office_type":
            routing_info["office_type"],

        "city":
            city,

        "district":
            district,

        "area":
            area,

        "routing_reason": (
            f"Complaint categorized as "
            f"{category} and routed to the "
            f"{routing_info['department']}."
        )
    }

# 3. TEST PROGRAM

if __name__ == "__main__":

    print("\n===================================")
    print("       DEPARTMENT ROUTING ENGINE")
    print("===================================")

    category = input(
        "\nEnter category: "
    ).strip()

    city = input(
        "Enter city: "
    ).strip()

    district = input(
        "Enter district: "
    ).strip()

    area = input(
        "Enter area: "
    ).strip()

    result = route_complaint(
        category,
        city,
        district,
        area
    )

    print("\n===================================")
    print("          ROUTING RESULT")
    print("===================================")

    print(
        "\nRouting Status:",
        result["routing_status"]
    )

    print(
        "Department:",
        result["department"]
    )

    print(
        "Team:",
        result["team"]
    )

    print(
        "Office Type:",
        result["office_type"]
    )

    print(
        "City:",
        result["city"]
    )

    print(
        "District:",
        result["district"]
    )

    print(
        "Area:",
        result["area"]
    )

    print(
        "Routing Reason:",
        result["routing_reason"]
    )

    print("\n===================================")
