from search_agent import SearchAgent

queries = [
    "AI software companies",
    "Machine Learning companies"
]

agent = SearchAgent()

results = agent.search(queries, max_results=5)

print()

print("=" * 80)

for company in results:

    print(company["title"])
    print(company["url"])
    print()