from datetime import datetime
import os


class Logger:

    def __init__(self):

        os.makedirs("output/logs", exist_ok=True)

        self.run_log = "output/logs/run.log"
        self.error_log = "output/logs/errors.log"

    def log(self, message):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(
            self.run_log,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(f"[{timestamp}] {message}\n")

    def error(self, website, error):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(
            self.error_log,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(
                f"[{timestamp}] {website}\n"
                f"Error: {error}\n\n"
            )