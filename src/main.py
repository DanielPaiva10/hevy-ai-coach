import sys
import os

sys.path.append(os.path.dirname(__file__))

from hevy.client import HevyClient
from hevy.exercise_resolver import ExerciseResolver
from ai.coach import Coach
from models.workout import WorkoutValidator


def main():
    workout_data = {
        "student": {
            "name": "Aluno Teste",
            "age": 20,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 75,
            "goal": "hipertrofia",
            "experience_level": "iniciante",
            "experience_years": 1,
            "weekly_frequency": 3,
            "session_duration_minutes": 60,
            "priority_muscle_groups": [],
            "movement_limitations": [],
            "injuries_or_restrictions": [],
            "excluded_exercises": [],
            "available_equipment": [
                "machine",
                "barbell"
            ],
            "preferences": [],
            "recent_training_history": {}
        },

        "program": {
            "title": "Treino ABC - Aluno Teste",

            "workouts": [
                {
                    "name": "A",

                    "exercises": [
                        {
                            "name": "Leg Extension",
                            "equipment": "machine",
                            "muscle_group": "quadriceps",
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
                            "name": "Squat",
                            "equipment": "barbell",
                            "muscle_group": "quadriceps",
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
                            "name": "Romanian Deadlift",
                            "equipment": "barbell",
                            "muscle_group": "hamstrings",
                            "sets": 3,
                            "reps": {
                                "min": 8,
                                "max": 10
                            },
                            "weight_kg": 40,
                            "rest_seconds": 120,
                            "tempo": "2-0-2-0"
                        }
                    ]
                }
            ]
        }
    }

    print("Validando dados do treino...")

    validator = WorkoutValidator()
    validator.validate(workout_data)

    print("Validação aprovada!")
    print()

    student_profile = workout_data["student"]

    exercises_data = workout_data["program"]["workouts"][0]["exercises"]

    hevy = HevyClient()
    resolver = ExerciseResolver(hevy)
    coach = Coach(resolver)

    workout_plan = coach.generate_workout_plan(
        student_profile,
        exercises_data
    )

    hevy_workout = coach.build_hevy_workout(
        workout_plan
    )

    print("Plano de treino criado!")
    print()

    print("Título:", hevy_workout["title"])
    print()

    for exercise in hevy_workout["exercises"]:
        print("ID:", exercise["exercise_template_id"])
        print("Séries:", len(exercise["sets"]))
        print("Repetições:", exercise["sets"][0]["reps"])
        print("Carga:", exercise["sets"][0]["weight_kg"], "kg")
        print()

    routine_data = {
        "routine": {
            "title": hevy_workout["title"],
            "folder_id": None,
            "notes": "Rotina criada pelo Hevy AI Coach.",
            "exercises": hevy_workout["exercises"]
        }
    }

    print("Enviando rotina para o Hevy...")

    created_routine = hevy.create_routine(routine_data)

    print("Rotina criada com sucesso no Hevy!")
    print(created_routine)


if __name__ == "__main__":
    main()