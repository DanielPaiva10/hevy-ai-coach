import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from ai.coach import Coach
from hevy.client import HevyClient
from hevy.exercise_resolver import ExerciseResolver


client = HevyClient()

resolver = ExerciseResolver(client)

coach = Coach(resolver)


student_profile = {
    "name": "Aluno Teste",
    "goal": "hipertrofia",
    "experience": "iniciante"
}


workout = coach.create_workout(student_profile)


print("Treino criado pelo Coach!")
print()
print("Título:", workout["title"])
print()

for exercise in workout["exercises"]:
    print("Exercício:", exercise["title"])
    print("ID:", exercise["exercise_template_id"])
    print("Quantidade de séries:", len(exercise["sets"]))