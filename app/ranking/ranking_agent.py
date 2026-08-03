class RankingAgent:
    """
    Sort companies according to match score.
    """

    def __init__(self):
        pass

    def rank(self, companies):

        ranked = sorted(
            companies,
            key=lambda company: company.get("match_score", 0),
            reverse=True
        )

        return ranked