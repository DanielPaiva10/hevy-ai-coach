import os
import requests
from dotenv import load_dotenv

load_dotenv()


class HevyClient:

    def __init__(self):
        self.api_key = os.getenv(
            "HEVY_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "HEVY_API_KEY não encontrada "
                "no arquivo .env"
            )

        self.session = requests.Session()

        self.session.headers.update({
            "api-key": self.api_key
        })

    def get_workouts(
        self,
        page=1,
        page_size=100
    ):
        url = (
            "https://api.hevyapp.com/v1/workouts"
        )

        response = self.session.get(
            url,
            params={
                "page": page,
                "pageSize": page_size
            }
        )

        response.raise_for_status()

        return response.json()

    def get_all_workouts(self):
        workouts = []

        page = 1

        while True:
            data = self.get_workouts(
                page=page,
                page_size=100
            )

            page_workouts = data.get(
                "workouts",
                []
            )

            workouts.extend(
                page_workouts
            )

            page_count = data.get(
                "page_count",
                1
            )

            if page >= page_count:
                break

            page += 1

        return workouts

    def get_routines(self):
        url = (
            "https://api.hevyapp.com/v1/routines"
        )

        response = self.session.get(url)

        if not response.ok:
            print()
            print(
                "Erro ao consultar rotinas:"
            )
            print(
                "Status:",
                response.status_code
            )
            print(
                "Resposta do Hevy:"
            )
            print(
                response.text
            )
            print()

        response.raise_for_status()

        return response.json()

    def get_all_routines(self):
        data = self.get_routines()

        if isinstance(data, dict):
            return data.get(
                "routines",
                []
            )

        if isinstance(data, list):
            return data

        return []

    def get_exercise_templates(
        self,
        page=1,
        page_size=100
    ):
        url = (
            "https://api.hevyapp.com/v1/"
            "exercise_templates"
        )

        response = self.session.get(
            url,
            params={
                "page": page,
                "pageSize": page_size
            }
        )

        response.raise_for_status()

        return response.json()

    def find_exercise_template(
        self,
        exercise_name
    ):
        search_name = (
            exercise_name
            .lower()
            .strip()
        )

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
                title = (
                    template["title"]
                    .lower()
                    .strip()
                )

                if title == search_name:
                    return template

                if title.startswith(
                    search_name
                ):
                    if best_match is None:
                        best_match = template

            if page >= page_count:
                break

            page += 1

        return best_match

    def create_routine(
        self,
        routine_data
    ):
        url = (
            "https://api.hevyapp.com/v1/"
            "routines"
        )

        response = self.session.post(
            url,
            json=routine_data
        )

        if not response.ok:
            print(
                "Erro ao criar rotina no Hevy:"
            )

            print(
                "Status:",
                response.status_code
            )

            print(
                "Resposta:",
                response.text
            )

        response.raise_for_status()

        return response.json()