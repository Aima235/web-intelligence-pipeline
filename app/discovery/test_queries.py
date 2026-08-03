from search_queries import SearchQueryGenerator

profile = {
    "skills": [
        "Python",
        "FastAPI",
        "LangChain",
        "Machine Learning",
        "LLMs"
    ]
}

generator = SearchQueryGenerator()

queries = generator.generate(profile)

for i, query in enumerate(queries, start=1):
    print(f"{i}. {query}")