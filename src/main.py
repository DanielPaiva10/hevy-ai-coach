import sys
import os

sys.path.append(os.path.dirname(__file__))

from hevy.client import HevyClient
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

    coach = Coach()
    hevy = HevyClient()

    workout = coach.create_workout(student_profile)

    routine_data = {
        "routine": {
            "title": workout["title"],
            "folder_id": None,
            "notes": "Rotina criada pelo Hevy AI Coach.",
            "exercises": workout["exercises"]
        }
    }

    created_routine = hevy.create_routine(routine_data)

    print("Rotina criada com sucesso!")
    print(created_routine)


if __name__ == "__main__":
    main()