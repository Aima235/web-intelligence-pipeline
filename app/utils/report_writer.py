import json
import os


class ReportWriter:

    def __init__(self):

        self.output_dir = "output/rankings"

        os.makedirs(self.output_dir, exist_ok=True)

    def save(self, ranked_companies):

        path = os.path.join(
            self.output_dir,
            "ranked_companies.json"
        )

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                ranked_companies,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"\nRanking saved: {path}")