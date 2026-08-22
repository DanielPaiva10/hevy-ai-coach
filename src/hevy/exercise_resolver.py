from hevy.client import HevyClient


class ExerciseResolver:
    def __init__(self, hevy_client):
        self.hevy_client = hevy_client

    def resolve(self, exercise_name):
        exercise = self.hevy_client.find_exercise_template(
            exercise_name
        )

        if exercise is None:
            raise ValueError(
                f"Exercício não encontrado no Hevy: {exercise_name}"
            )

        return {
            "id": exercise["id"],
            "title": exercise["title"],
            "type": exercise["type"],
            "primary_muscle_group": exercise["primary_muscle_group"],
            "equipment": exercise["equipment"]
        }

    def get_available_exercises(self):
        exercises = []

        page = 1

        while True:
            data = self.hevy_client.get_exercise_templates(
                page=page,
                page_size=100
            )

            templates = data.get("exercise_templates", [])
            page_count = data.get("page_count", 1)

            for exercise in templates:
                exercises.append({
                    "id": exercise["id"],
                    "title": exercise["title"],
                    "type": exercise["type"],
                    "primary_muscle_group": exercise["primary_muscle_group"],
                    "equipment": exercise["equipment"]
                })

            if page >= page_count:
                break

            page += 1

        return exercises