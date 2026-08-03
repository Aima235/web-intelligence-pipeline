class SearchQueryGenerator:
    
    def generate(self, profile):

        queries = []

        role = profile.get("desired_role", "").strip()
        skills = profile.get("skills", [])
        services = profile.get("services", [])
        projects = profile.get("projects", [])

        # Remove duplicates while preserving order
        unique_queries = []

        def add_query(query):
            query = query.strip()
            if query and query not in unique_queries:
                unique_queries.append(query)

        # -------------------------
        # Role-Based Queries
        # -------------------------

        if role:

            add_query(f"{role} companies")

            add_query(f"{role} consulting companies")

            add_query(f"{role} service providers")

            add_query(f"{role} startups")

            add_query(f"{role} software houses")

            add_query(f"{role} agencies")

        # -------------------------
        # Skill-Based Queries
        # -------------------------

        for skill in skills:

            add_query(f"{skill} companies")

            add_query(f"{skill} consulting")

            add_query(f"{skill} solutions")

            add_query(f"{skill} software company")

            add_query(f"{skill} startups")

        # -------------------------
        # Service-Based Queries
        # -------------------------

        for service in services:

            add_query(f"{service} companies")

            add_query(f"{service} service provider")

            add_query(f"{service} agency")

            add_query(f"{service} consulting")

        # -------------------------
        # Project-Based Queries
        # -------------------------

        for project in projects:

            add_query(f"{project} company")

            add_query(f"{project} solution provider")

        # -------------------------
        # AI & Technology Companies
        # -------------------------

        add_query("Artificial Intelligence companies")

        add_query("Machine Learning companies")

        add_query("Deep Learning companies")

        add_query("Computer Vision companies")

        add_query("Natural Language Processing companies")

        add_query("Generative AI companies")

        add_query("LLM companies")

        add_query("AI automation companies")

        add_query("Data Science companies")

        add_query("Healthcare AI companies")

        add_query("FinTech AI companies")

        add_query("AI startups")

        print(f"\nGenerated {len(unique_queries)} search queries.")

        return unique_queries