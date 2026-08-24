from typing import Optional


class WorkoutValidator:
    REQUIRED_STUDENT_FIELDS = [
        "name",
        "age",
        "sex",
        "height_cm",
        "weight_kg",
        "goal",
        "experience_level",
        "weekly_frequency",
        "session_duration_minutes",
    ]

    def validate(self, workout_data):
        if not isinstance(workout_data, dict):
            raise ValueError("Os dados do treino devem ser um dicionário.")

        if "student" not in workout_data:
            raise ValueError("Campo 'student' não encontrado.")

        if "program" not in workout_data:
            raise ValueError("Campo 'program' não encontrado.")

        self._validate_student(workout_data["student"])
        self._validate_program(workout_data["program"])

        return True

    def _validate_student(self, student):
        if not isinstance(student, dict):
            raise ValueError("'student' deve ser um dicionário.")

        for field in self.REQUIRED_STUDENT_FIELDS:
            if field not in student:
                raise ValueError(
                    f"Campo obrigatório do aluno não encontrado: {field}"
                )

        if not isinstance(student["age"], (int, float)):
            raise ValueError("'age' deve ser um número.")

        if not isinstance(student["height_cm"], (int, float)):
            raise ValueError("'height_cm' deve ser um número.")

        if not isinstance(student["weight_kg"], (int, float)):
            raise ValueError("'weight_kg' deve ser um número.")

        if not isinstance(student["weekly_frequency"], int):
            raise ValueError("'weekly_frequency' deve ser um número inteiro.")

        if not isinstance(student["session_duration_minutes"], int):
            raise ValueError(
                "'session_duration_minutes' deve ser um número inteiro."
            )

    def _validate_program(self, program):
        if not isinstance(program, dict):
            raise ValueError("'program' deve ser um dicionário.")

        if "title" not in program:
            raise ValueError("Campo 'title' não encontrado no programa.")

        if "workouts" not in program:
            raise ValueError("Campo 'workouts' não encontrado no programa.")

        if not isinstance(program["workouts"], list):
            raise ValueError("'workouts' deve ser uma lista.")

        if len(program["workouts"]) == 0:
            raise ValueError("O programa precisa ter pelo menos um treino.")

        for workout in program["workouts"]:
            self._validate_workout(workout)

    def _validate_workout(self, workout):
        if "name" not in workout:
            raise ValueError("Treino sem nome.")

        if "exercises" not in workout:
            raise ValueError(
                f"O treino '{workout['name']}' não possui exercícios."
            )

        if not isinstance(workout["exercises"], list):
            raise ValueError(
                f"'exercises' do treino '{workout['name']}' deve ser uma lista."
            )

        if len(workout["exercises"]) == 0:
            raise ValueError(
                f"O treino '{workout['name']}' precisa ter pelo menos um exercício."
            )

        for exercise in workout["exercises"]:
            self._validate_exercise(exercise)

    def _validate_exercise(self, exercise):
        required_fields = [
            "name",
            "equipment",
            "muscle_group",
            "sets",
            "reps",
        ]

        for field in required_fields:
            if field not in exercise:
                raise ValueError(
                    f"Campo obrigatório do exercício não encontrado: {field}"
                )

        if not isinstance(exercise["sets"], int):
            raise ValueError("'sets' deve ser um número inteiro.")

        if exercise["sets"] <= 0:
            raise ValueError("'sets' deve ser maior que zero.")

        reps = exercise["reps"]

        if isinstance(reps, dict):
            if "min" not in reps or "max" not in reps:
                raise ValueError(
                    "'reps' deve possuir 'min' e 'max'."
                )

            if reps["min"] <= 0 or reps["max"] <= 0:
                raise ValueError(
                    "A quantidade de repetições deve ser maior que zero."
                )

            if reps["min"] > reps["max"]:
                raise ValueError(
                    "'reps.min' não pode ser maior que 'reps.max'."
                )

        elif not isinstance(reps, int):
            raise ValueError(
                "'reps' deve ser um número inteiro ou um intervalo."
            )

        if "weight_kg" in exercise and exercise["weight_kg"] is not None:
            if not isinstance(exercise["weight_kg"], (int, float)):
                raise ValueError("'weight_kg' deve ser um número.")

        if "rest_seconds" in exercise and exercise["rest_seconds"] is not None:
            if not isinstance(exercise["rest_seconds"], (int, float)):
                raise ValueError("'rest_seconds' deve ser um número.")

        if "tempo" in exercise and exercise["tempo"] is not None:
            if not isinstance(exercise["tempo"], str):
                raise ValueError("'tempo' deve ser um texto.")