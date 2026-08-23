from hevy.client import HevyClient


class ExerciseResolver:
    def __init__(self, hevy_client):
        self.hevy_client = hevy_client

    def resolve(self, exercise_name, equipment=None, muscle_group=None):
        exercises = self.get_available_exercises()

        search_name = exercise_name.lower().strip()

        if equipment:
            equipment = equipment.lower().strip()

        if muscle_group:
            muscle_group = muscle_group.lower().strip()

        candidates = []

        for exercise in exercises:
            title = exercise["title"].lower().strip()

            title_base = title.split("(")[0].strip()

            if title_base != search_name:
                continue

            candidates.append(exercise)

        if equipment:
            equipment_matches = [
                exercise
                for exercise in candidates
                if exercise["equipment"].lower() == equipment
            ]

            if equipment_matches:
                candidates = equipment_matches

        if muscle_group:
            muscle_matches = [
                exercise
                for exercise in candidates
                if exercise["primary_muscle_group"].lower() == muscle_group
            ]

            if muscle_matches:
                candidates = muscle_matches

        if not candidates:
            raise ValueError(
                f"Exercício não encontrado no Hevy: {exercise_name}"
            )

        return candidates[0]

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