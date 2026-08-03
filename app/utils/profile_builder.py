def get_list_input(message):
    
    while True:

        value = input(message).strip()

        if value:

            return [

                item.strip()

                for item in value.split(",")

                if item.strip()

            ]

        print("Please enter at least one value.")


def get_input(message, required=True):

    while True:

        value = input(message).strip()

        if value:

            return value

        if not required:

            return ""

        print("This field is required.")


def build_candidate_profile():

    print("\n" + "=" * 70)
    print("Candidate Profile Builder")
    print("=" * 70)

    profile = {

        "name": get_input("Full Name                 : "),

        "email": get_input("Email                     : "),

        "phone": get_input("Phone Number              : "),

        "location": get_input("Location                  : "),

        "desired_role": get_input("Desired Job Role          : "),

        "education": get_input("Education                 : "),

        "experience": get_input("Experience                : "),

        "linkedin": get_input(
            "LinkedIn Profile (optional): ",
            required=False
        ),

        "github": get_input(
            "GitHub Profile (optional) : ",
            required=False
        ),

        "portfolio": get_input(
            "Portfolio (optional)      : ",
            required=False
        ),

        "skills": get_list_input(
            "\nSkills (comma separated): "
        ),

        "projects": get_list_input(
            "Projects (comma separated): "
        ),

        "services": get_list_input(
            "Services (comma separated): "
        )

    }

    return profile