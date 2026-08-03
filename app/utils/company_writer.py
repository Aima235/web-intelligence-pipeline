import json
import os


class CompanyWriter:

    def save(self, companies):

        os.makedirs("app/output", exist_ok=True)

        with open(
            "app/output/companies.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                [company.model_dump() for company in companies],
                f,
                indent=4,
                ensure_ascii=False
            )

        return "app/output/companies.json"