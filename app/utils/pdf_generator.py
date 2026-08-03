from pathlib import Path
import pdfkit
from jinja2 import Environment, FileSystemLoader


class PDFGenerator:

    def __init__(self):
        
        self.output_dir = Path("output/proposals")
        BASE_DIR = Path(__file__).resolve().parent.parent

        self.template_dir = BASE_DIR / "templates"
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.environment = Environment(
            loader=FileSystemLoader(self.template_dir)
        )

        self.config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )

    def generate(self, proposal, company, profile, filename):
        print("Template Directory:", self.template_dir.resolve())
        print("Files:", list(self.template_dir.glob("*")))
        print("Current Working Directory:", Path.cwd())
        print("Template Exists:", (self.template_dir / "proposal_template.html").exists())
        template = self.environment.get_template(
            "proposal_template.html"
        )

        html_content = template.render(
        proposal=proposal,
        company=company,
        profile=profile
)

        output_path = self.output_dir / f"{filename}.pdf"

        pdfkit.from_string(
            html_content,
            str(output_path),
            configuration=self.config
        )

        return output_path