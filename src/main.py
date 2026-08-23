import sys
import os

sys.path.append(os.path.dirname(__file__))

from hevy.client import HevyClient
from hevy.exercise_resolver import ExerciseResolver
from ai.coach import Coach


def main():
    student_profile = {
        "name": "Aluno Teste",
        "age": 20,
        "height": 175,
        "goal": "hipertrofia",
        "experience": "iniciante",
        "restrictions": []
    }

    hevy = HevyClient()

    resolver = ExerciseResolver(hevy)

    coach = Coach(resolver)

    exercises_data = [
        {
            "name": "Leg Extension",
            "equipment": "machine",
            "muscle_group": "quadriceps"
        },
        {
            "name": "Squat",
            "equipment": "barbell",
            "muscle_group": "quadriceps"
        },
        {
            "name": "Romanian Deadlift",
            "equipment": "barbell",
            "muscle_group": "hamstrings"
        }
    ]

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
        print("Exercício:", exercise["title"])
        print("ID:", exercise["exercise_template_id"])
        print("Séries:", len(exercise["sets"]))
        print()


if __name__ == "__main__":
    main()