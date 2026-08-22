from hevy.exercise_resolver import ExerciseResolver


class Coach:
    def __init__(self, exercise_resolver):
        self.exercise_resolver = exercise_resolver

    def create_workout(self, student_profile):
        exercise = self.exercise_resolver.resolve("Leg Extension")

        workout = {
            "title": f"Treino ABC - {student_profile['name']}",
            "exercises": [
                {
                    "exercise_template_id": exercise["id"],
                    "title": exercise["title"],
                    "sets": [
                        {
                            "type": "normal",
                            "weight_kg": 0,
                            "reps": 10,
                            "distance_meters": None,
                            "duration_seconds": None,
                            "custom_metric": None
                        },
                        {
                            "type": "normal",
                            "weight_kg": 0,
                            "reps": 10,
                            "distance_meters": None,
                            "duration_seconds": None,
                            "custom_metric": None
                        },
                        {
                            "type": "normal",
                            "weight_kg": 0,
                            "reps": 10,
                            "distance_meters": None,
                            "duration_seconds": None,
                            "custom_metric": None
                        }
                    ]
                }
            ]
        }

        return workout