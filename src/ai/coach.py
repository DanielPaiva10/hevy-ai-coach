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

            if exercise is None:
                raise ValueError(
                    f"Exercício não encontrado: {exercise_data['name']}"
                )

            sets = self._build_sets(exercise_data)

            exercises.append({
                "exercise_template_id": exercise["id"],
                "sets": sets
            })

        return {
            "title": workout_plan["title"],
            "exercises": exercises
        }

    def _build_sets(self, exercise_data):
        number_of_sets = exercise_data["sets"]
        reps = exercise_data["reps"]
        weight_kg = exercise_data.get("weight_kg", 0)

        if isinstance(reps, dict):
            reps_value = reps["max"]
        else:
            reps_value = reps

        sets = []

        for _ in range(number_of_sets):
            sets.append({
                "type": "normal",
                "weight_kg": weight_kg,
                "reps": reps_value,
                "distance_meters": None,
                "duration_seconds": None,
                "custom_metric": None
            })

        return sets