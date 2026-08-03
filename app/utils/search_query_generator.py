class SearchQueryGenerator:
    
    def generate(self, profile):

        unique_queries = []

        def add_query(query):
            query = query.strip()
            if query and query not in unique_queries:
                unique_queries.append(query)

        role = profile.get("desired_role", "")

        skills = profile.get("skills", [])

        services = profile.get("services", [])

        projects = profile.get("projects", [])

        industries = profile.get("target_industries", [])

        keywords = profile.get("search_keywords", [])

        # --------------------------------------------------
        # Role Based Queries
        # --------------------------------------------------

        if role:

            add_query(f"{role} companies")

            add_query(f"{role} software companies")

            add_query(f"{role} consulting companies")

            add_query(f"{role} startups")

            add_query(f"{role} agencies")

            add_query(f"{role} technology companies")

            add_query(f"{role} AI companies")

        # --------------------------------------------------
        # Skill Based Queries
        # --------------------------------------------------

        for skill in skills:

            add_query(f"{skill} companies")

            add_query(f"{skill} software company")

            add_query(f"{skill} consulting")

            add_query(f"{skill} service provider")

            add_query(f"{skill} startups")

        # --------------------------------------------------
        # Service Based Queries
        # --------------------------------------------------

        for service in services:

            add_query(f"{service} companies")

            add_query(f"{service} consulting companies")

            add_query(f"{service} service provider")

            add_query(f"{service} software company")

        # --------------------------------------------------
        # Project Based Queries
        # --------------------------------------------------

        for project in projects:

            add_query(f"{project} companies")

            add_query(f"{project} solution provider")

            add_query(f"{project} technology company")

        # --------------------------------------------------
        # Industry Based Queries
        # --------------------------------------------------

        for industry in industries:

            add_query(f"{industry} AI companies")

            add_query(f"{industry} software companies")

            add_query(f"{industry} technology companies")

        # --------------------------------------------------
        # AI Generated Keywords
        # --------------------------------------------------

        for keyword in keywords:

            add_query(f"{keyword} companies")

            add_query(f"{keyword} consulting")

            add_query(f"{keyword} startups")

        # --------------------------------------------------
        # Generic AI Queries
        # --------------------------------------------------

        generic_queries = [

            "Artificial Intelligence companies",

            "Machine Learning companies",

            "Deep Learning companies",

            "Computer Vision companies",

            "Natural Language Processing companies",

            "LLM companies",

            "Generative AI companies",

            "AI Automation companies",

            "Data Science companies",

            "Healthcare AI companies",

            "Retail AI companies",

            "FinTech AI companies",

            "AI startups",

            "AI software houses",

            "AI consulting firms"

        ]

        for query in generic_queries:
            add_query(query)

        print(f"\nGenerated {len(unique_queries)} search queries.")

        return unique_queries