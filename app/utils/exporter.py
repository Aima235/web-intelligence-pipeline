import json
import os

from schemas.output_schema import create_output_schema

class Exporter:

    def __init__(self, output_dir="output/json"):

        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, company):

        schema = create_output_schema()

        if hasattr(company, "integration_data"):
            schema.update(company.integration_data)

        filename = (
            company.company_name
            .lower()
            .replace(" ", "_")
            .replace("/", "_")
        )

        output_path = os.path.join(
            self.output_dir,
            f"{filename}.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                schema,
                file,
                indent=4,
                ensure_ascii=False
            )

        return output_path