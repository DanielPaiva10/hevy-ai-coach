class Coach:
    def __init__(self, exercise_resolver):
        self.exercise_resolver = exercise_resolver

    def generate_workout_plan(self, student_profile, exercises_data):
        plan = {
            "title": f"Treino ABC - {student_profile['name']}",
            "exercises": exercises_data
        }

        return plan

    def build_hevy_workout(self, workout_plan):
        exercises = []

        for exercise_data in workout_plan["exercises"]:
            exercise = self.exercise_resolver.resolve(
                exercise_data["name"],
                equipment=exercise_data.get("equipment"),
                muscle_group=exercise_data.get("muscle_group")
            )

            exercises.append({
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
            })

        return {
            "title": workout_plan["title"],
            "exercises": exercises
        }