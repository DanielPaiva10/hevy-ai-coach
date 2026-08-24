import os
import requests

from dotenv import load_dotenv


load_dotenv()


class HevyClient:
    def __init__(self):
        self.api_key = os.getenv("HEVY_API_KEY")

        if not self.api_key:
            raise ValueError(
                "HEVY_API_KEY não encontrada no arquivo .env"
            )

        self.session = requests.Session()

        self.session.headers.update({
            "api-key": self.api_key
        })

    def get_workouts(self):
        url = "https://api.hevyapp.com/v1/workouts"

        response = self.session.get(url)

        response.raise_for_status()

        return response.json()

    def get_exercise_templates(self, page=1, page_size=100):
        url = "https://api.hevyapp.com/v1/exercise_templates"

        response = self.session.get(
            url,
            params={
                "page": page,
                "pageSize": page_size
            }
        )

        response.raise_for_status()

        return response.json()

    def find_exercise_template(self, exercise_name):
        search_name = exercise_name.lower().strip()

        page = 1
        best_match = None

        while True:
            data = self.get_exercise_templates(
                page=page,
                page_size=100
            )

            templates = data.get(
                "exercise_templates",
                []
            )

            page_count = data.get(
                "page_count",
                1
            )

            for template in templates:
                title = template["title"].lower().strip()

                
                if title == search_name:
                    return template

                
                if title.startswith(search_name):
                    if best_match is None:
                        best_match = template

            if page >= page_count:
                break

            page += 1

        return best_match

    def create_routine(self, routine_data):
        url = "https://api.hevyapp.com/v1/routines"

        response = self.session.post(
            url,
            json=routine_data
        )

        if not response.ok:
            print("Erro ao criar rotina no Hevy:")
            print("Status:", response.status_code)
            print("Resposta:", response.text)

        response.raise_for_status()

        return response.json()