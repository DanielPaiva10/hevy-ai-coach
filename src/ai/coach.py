class Coach:

    def __init__(self, exercise_resolver):
        self.exercise_resolver = exercise_resolver

    # ============================================================
    # GERAÇÃO PRINCIPAL DO PLANO
    # ============================================================

    def generate_workout_plan(self, student):

        self._validate_student_input(student)

        workout_structure = self._determine_structure(
            student
        )

        workouts = self._build_workouts(
            student,
            workout_structure
        )

        plan = {
            "title": workout_structure["title"],
            "split": workout_structure["split"],
            "workouts": workouts
        }

        return plan

    # ============================================================
    # VALIDAÇÃO BÁSICA DO ALUNO
    # ============================================================

    def _validate_student_input(self, student):

        required_fields = [
            "name",
            "age",
            "height_cm",
            "weight_kg",
            "goal",
            "experience_level",
            "weekly_frequency",
            "session_duration_minutes"
        ]

        for field in required_fields:

            if not hasattr(student, field):
                raise ValueError(
                    f"Aluno não possui o campo obrigatório: {field}"
                )

        if student.weekly_frequency < 1:
            raise ValueError(
                "A frequência semanal deve ser maior que zero."
            )

        if student.weekly_frequency > 7:
            raise ValueError(
                "A frequência semanal não pode ser maior que 7."
            )

        if student.session_duration_minutes <= 0:
            raise ValueError(
                "A duração da sessão deve ser maior que zero."
            )

        if student.weight_kg <= 0:
            raise ValueError(
                "O peso do aluno deve ser maior que zero."
            )

    # ============================================================
    # DEFINIÇÃO DA ESTRUTURA SEMANAL
    # ============================================================

    def _determine_structure(self, student):

        frequency = student.weekly_frequency
        level = student.experience_level.lower().strip()
        goal = student.goal.lower().strip()

        if goal == "hipertrofia":

            if level == "iniciante":

                if frequency <= 2:
                    return {
                        "title": (
                            f"Treino Full Body - "
                            f"{student.name}"
                        ),
                        "split": "full_body"
                    }

                if frequency == 3:
                    return {
                        "title": (
                            f"Treino ABC - "
                            f"{student.name}"
                        ),
                        "split": "abc"
                    }

                return {
                    "title": (
                        f"Treino ABCD - "
                        f"{student.name}"
                    ),
                    "split": "abcd"
                }

            if level == "intermediário":

                if frequency <= 3:
                    return {
                        "title": (
                            f"Treino ABC - "
                            f"{student.name}"
                        ),
                        "split": "abc"
                    }

                if frequency == 4:
                    return {
                        "title": (
                            f"Treino ABCD - "
                            f"{student.name}"
                        ),
                        "split": "abcd"
                    }

                return {
                    "title": (
                        f"Treino ABCDE - "
                        f"{student.name}"
                    ),
                    "split": "abcde"
                }

            if level == "avançado":

                if frequency <= 4:
                    return {
                        "title": (
                            f"Treino ABCD - "
                            f"{student.name}"
                        ),
                        "split": "abcd"
                    }

                return {
                    "title": (
                        f"Treino ABCDE - "
                        f"{student.name}"
                    ),
                    "split": "abcde"
                }

        raise ValueError(
            "Combinação de objetivo e nível "
            "não suportada: "
            f"{student.goal} / "
            f"{student.experience_level}"
        )

    # ============================================================
    # CONSTRUÇÃO DOS TREINOS
    # ============================================================

    def _build_workouts(
        self,
        student,
        workout_structure
    ):

        split = workout_structure["split"]

        exercises = self._get_exercise_library()

        exercises = self._filter_exercises(
            exercises,
            student
        )

        exercises = self._adapt_exercises_to_student(
            exercises,
            student
        )

        if split == "full_body":

            return [
                {
                    "name": "A",
                    "exercises": self._select_full_body(
                        exercises,
                        student
                    )
                }
            ]

        if split == "abc":

            return [
                {
                    "name": "A",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "chest",
                            "shoulders",
                            "triceps"
                        ],
                        student
                    )
                },
                {
                    "name": "B",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "lats",
                            "upper_back",
                            "biceps"
                        ],
                        student
                    )
                },
                {
                    "name": "C",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "quadriceps",
                            "hamstrings",
                            "glutes"
                        ],
                        student
                    )
                }
            ]

        if split == "abcd":

            return [
                {
                    "name": "A",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "chest",
                            "triceps"
                        ],
                        student
                    )
                },
                {
                    "name": "B",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "lats",
                            "upper_back",
                            "biceps"
                        ],
                        student
                    )
                },
                {
                    "name": "C",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "quadriceps"
                        ],
                        student
                    )
                },
                {
                    "name": "D",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "hamstrings",
                            "glutes",
                            "shoulders"
                        ],
                        student
                    )
                }
            ]

        if split == "abcde":

            return [
                {
                    "name": "A",
                    "exercises": self._select_day(
                        exercises,
                        ["chest"],
                        student
                    )
                },
                {
                    "name": "B",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "lats",
                            "upper_back"
                        ],
                        student
                    )
                },
                {
                    "name": "C",
                    "exercises": self._select_day(
                        exercises,
                        ["shoulders"],
                        student
                    )
                },
                {
                    "name": "D",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "quadriceps",
                            "hamstrings"
                        ],
                        student
                    )
                },
                {
                    "name": "E",
                    "exercises": self._select_day(
                        exercises,
                        [
                            "biceps",
                            "triceps",
                            "glutes"
                        ],
                        student
                    )
                }
            ]

        raise ValueError(
            f"Divisão não suportada: {split}"
        )

    # ============================================================
    # BIBLIOTECA DE EXERCÍCIOS
    # ============================================================

    def _get_exercise_library(self):

        return [

            {
                "name": "Bench Press",
                "equipment": "barbell",
                "muscle_group": "chest",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 40,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Incline Bench Press",
                "equipment": "barbell",
                "muscle_group": "chest",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 30,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Chest Fly",
                "equipment": "machine",
                "muscle_group": "chest",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 20,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Shoulder Press",
                "equipment": "machine",
                "muscle_group": "shoulders",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 20,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Lateral Raise",
                "equipment": "dumbbell",
                "muscle_group": "shoulders",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 8,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Triceps Pushdown",
                "equipment": None,
                "muscle_group": "triceps",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 20,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Overhead Triceps Extension",
                "equipment": "cable",
                "muscle_group": "triceps",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 15,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Lat Pulldown",
                "equipment": None,
                "muscle_group": "lats",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 30,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Seated Row",
                "equipment": "machine",
                "muscle_group": "upper_back",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 30,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Lat Pulldown - Close Grip",
                "equipment": None,
                "muscle_group": "lats",
                "category": "compound",
                "sets": 2,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 30,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Barbell Curl",
                "equipment": "barbell",
                "muscle_group": "biceps",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 20,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Hammer Curl",
                "equipment": "dumbbell",
                "muscle_group": "biceps",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 10,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Squat",
                "equipment": "barbell",
                "muscle_group": "quadriceps",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 10
                },
                "weight_kg": 40,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Leg Extension",
                "equipment": "machine",
                "muscle_group": "quadriceps",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 20,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Leg Press",
                "equipment": "machine",
                "muscle_group": "quadriceps",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 80,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Romanian Deadlift",
                "equipment": "barbell",
                "muscle_group": "hamstrings",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 10
                },
                "weight_kg": 40,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Leg Curl",
                "equipment": "machine",
                "muscle_group": "hamstrings",
                "category": "isolation",
                "sets": 2,
                "reps": {
                    "min": 10,
                    "max": 15
                },
                "weight_kg": 20,
                "rest_seconds": 90,
                "tempo": "2-0-2-0"
            },

            {
                "name": "Hip Thrust",
                "equipment": "barbell",
                "muscle_group": "glutes",
                "category": "compound",
                "sets": 3,
                "reps": {
                    "min": 8,
                    "max": 12
                },
                "weight_kg": 40,
                "rest_seconds": 120,
                "tempo": "2-0-2-0"
            }
        ]

    # ============================================================
    # FILTRO DE EXERCÍCIOS
    # ============================================================

    def _filter_exercises(
        self,
        exercises,
        student
    ):

        excluded = [
            exercise.lower().strip()
            for exercise in getattr(
                student,
                "excluded_exercises",
                []
            )
        ]

        limitations = [
            limitation.lower().strip()
            for limitation in getattr(
                student,
                "movement_limitations",
                []
            )
        ]

        restrictions = [
            restriction.lower().strip()
            for restriction in getattr(
                student,
                "injuries_or_restrictions",
                []
            )
        ]

        available_equipment = [
            equipment.lower().strip()
            for equipment in getattr(
                student,
                "available_equipment",
                []
            )
        ]

        filtered = []

        for original in exercises:

            exercise = original.copy()

            exercise_name = (
                exercise["name"]
                .lower()
                .strip()
            )

            if exercise_name in excluded:
                continue

            blocked = False

            for limitation in limitations:

                if limitation in exercise_name:
                    blocked = True
                    break

            if blocked:
                continue

            for restriction in restrictions:

                if restriction in exercise_name:
                    blocked = True
                    break

            if blocked:
                continue

            required_equipment = exercise.get(
                "equipment"
            )

            if (
                required_equipment is not None
                and available_equipment
                and required_equipment.lower()
                not in available_equipment
            ):
                continue

            filtered.append(exercise)

        return filtered

    # ============================================================
    # ADAPTAÇÕES DE ACORDO COM O PERFIL
    # ============================================================

    def _adapt_exercises_to_student(
        self,
        exercises,
        student
    ):

        level = (
            student.experience_level
            .lower()
            .strip()
        )

        adapted = []

        for original in exercises:

            exercise = original.copy()

            exercise["reps"] = original["reps"].copy()

            if level == "iniciante":

                exercise["sets"] = min(
                    exercise["sets"],
                    3
                )

                if exercise["category"] == "isolation":
                    exercise["sets"] = min(
                        exercise["sets"],
                        2
                    )

                exercise["rest_seconds"] = max(
                    exercise["rest_seconds"],
                    90
                )

                exercise["tempo"] = "2-0-2-0"

            elif level == "intermediário":

                exercise["rest_seconds"] = max(
                    exercise["rest_seconds"],
                    90
                )

            elif level == "avançado":

                exercise["rest_seconds"] = max(
                    exercise["rest_seconds"],
                    90
                )

            else:
                raise ValueError(
                    f"Nível de experiência não suportado: "
                    f"{student.experience_level}"
                )

            adapted.append(exercise)

        return adapted

    # ============================================================
    # SELEÇÃO DE UM DIA
    # ============================================================

    def _select_day(
        self,
        exercises,
        muscle_groups,
        student
    ):

        selected = []

        priority_groups = [
            group.lower().strip()
            for group in getattr(
                student,
                "priority_muscle_groups",
                []
            )
        ]

        ordered_groups = sorted(
            muscle_groups,
            key=lambda group: (
                0
                if group in priority_groups
                else 1
            )
        )

        for muscle_group in ordered_groups:

            group_exercises = [
                exercise
                for exercise in exercises
                if exercise["muscle_group"]
                == muscle_group
            ]

            if not group_exercises:
                continue

            compounds = [
                exercise
                for exercise in group_exercises
                if exercise["category"]
                == "compound"
            ]

            isolations = [
                exercise
                for exercise in group_exercises
                if exercise["category"]
                == "isolation"
            ]

            if compounds:
                selected.append(
                    compounds[0]
                )

            if isolations:
                selected.append(
                    isolations[0]
                )

            if (
                muscle_group
                in [
                    "chest",
                    "lats",
                    "upper_back",
                    "quadriceps",
                    "hamstrings",
                    "glutes"
                ]
                and len(selected) < 5
                and len(compounds) > 1
            ):

                second_compound = compounds[1]

                if second_compound not in selected:
                    selected.append(
                        second_compound
                    )

        level = (
            student.experience_level
            .lower()
            .strip()
        )

        if level == "iniciante":
            maximum = 5
        else:
            maximum = 6

        return selected[:maximum]

    # ============================================================
    # FULL BODY
    # ============================================================

    def _select_full_body(
        self,
        exercises,
        student
    ):

        target_groups = [
            "quadriceps",
            "hamstrings",
            "chest",
            "lats",
            "shoulders"
        ]

        selected = []

        for muscle_group in target_groups:

            candidates = [
                exercise
                for exercise in exercises
                if (
                    exercise["muscle_group"]
                    == muscle_group
                    and exercise["category"]
                    == "compound"
                )
            ]

            if candidates:
                selected.append(
                    candidates[0]
                )

        if (
            student.experience_level
            .lower()
            .strip()
            == "iniciante"
        ):
            return selected[:5]

        return selected[:6]

    # ============================================================
    # CONSTRUÇÃO DA ROTINA PARA O HEVY
    # ============================================================

    def build_hevy_workout(
        self,
        workout_plan
    ):

        if not isinstance(workout_plan, dict):
            raise ValueError(
                "workout_plan deve ser um dicionário."
            )

        if "title" not in workout_plan:
            raise ValueError(
                "Workout plan não possui 'title'."
            )

        if "workouts" not in workout_plan:
            raise ValueError(
                "Workout plan não possui 'workouts'."
            )

        exercises = []

        for workout in workout_plan["workouts"]:

            for exercise_data in workout["exercises"]:

                requested_equipment = (
                    exercise_data.get("equipment")
                )

                exercise = (
                    self.exercise_resolver.resolve(
                        exercise_data["name"],
                        equipment=requested_equipment,
                        muscle_group=exercise_data.get(
                            "muscle_group"
                        )
                    )
                )

                if exercise is None:
                    raise ValueError(
                        "Exercício não encontrado: "
                        f"{exercise_data['name']}"
                    )

                reps = exercise_data["reps"]

                if isinstance(reps, dict):
                    reps_value = reps["max"]
                else:
                    reps_value = reps

                sets = []

                for _ in range(
                    exercise_data["sets"]
                ):

                    sets.append({
                        "type": "normal",
                        "weight_kg": exercise_data.get(
                            "weight_kg",
                            0
                        ),
                        "reps": reps_value,
                        "distance_meters": None,
                        "duration_seconds": None,
                        "custom_metric": None
                    })

                exercises.append({
                    "exercise_template_id": (
                        exercise["id"]
                    ),
                    "sets": sets
                })

        return {
            "title": workout_plan["title"],
            "exercises": exercises
        }