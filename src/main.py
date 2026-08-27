import sys
import os

sys.path.append(
    os.path.dirname(__file__)
)

from hevy.client import HevyClient
from hevy.exercise_resolver import ExerciseResolver
from ai.coach import Coach
from models.workout import WorkoutValidator
from models.student import Student


# ========================================
# CRIAR ALUNO
# ========================================

def create_student():

    return Student(
        name="Aluno Teste",
        age=15,
        sex="male",
        height_cm=164,
        weight_kg=52,
        goal="hipertrofia",
        experience_level="iniciante",
        experience_years=0,
        weekly_frequency=3,
        session_duration_minutes=60,
        priority_muscle_groups=[],
        movement_limitations=[],
        injuries_or_restrictions=[],
        excluded_exercises=[],
        available_equipment=[
            "machine",
            "barbell",
            "cable"
        ],
        recent_training_history={},
        preferences=[]
    )


def main():

    # ========================================
    # DADOS DO ALUNO
    # ========================================

    student = create_student()

    # ========================================
    # CONEXÃO COM HEVY
    # ========================================

    print("================================")
    print("HEVY AI COACH")
    print("================================")
    print()

    print("Conectando ao Hevy...")

    hevy = HevyClient()

    print(
        "Conexão com o Hevy estabelecida!"
    )

    print()

    resolver = ExerciseResolver(
        hevy
    )

    coach = Coach(
        resolver
    )

    # ========================================
    # GERAR PLANO
    # ========================================

    print("================================")
    print("Gerando rotina personalizada")
    print("================================")
    print()

    workout_plan = (
        coach.generate_workout_plan(
            student
        )
    )

    print(
        "Aluno:",
        student.name
    )

    print(
        "Objetivo:",
        student.goal
    )

    print(
        "Nível:",
        student.experience_level
    )

    print(
        "Frequência semanal:",
        student.weekly_frequency,
        "dias"
    )

    print()

    # ========================================
    # MOSTRAR ESTRUTURA
    # ========================================

    print("================================")
    print("Estrutura escolhida pelo Coach")
    print("================================")
    print()

    print(
        "Título:",
        workout_plan["title"]
    )

    print(
        "Divisão:",
        workout_plan["split"]
    )

    print()

    # ========================================
    # MOSTRAR DIVISÃO
    # ========================================

    print("Divisão dos exercícios:")
    print()

    for workout in workout_plan["workouts"]:

        print(
            f"Treino {workout['name']}:"
        )

        for exercise in workout["exercises"]:

            print(
                f"- {exercise['name']} "
                f"({exercise['muscle_group']})"
            )

        print()

    # ========================================
    # PREPARAR DADOS PARA VALIDAÇÃO
    # ========================================

    workouts_data = []

    for workout in workout_plan["workouts"]:

        exercises_data = []

        for exercise in workout["exercises"]:

            exercises_data.append({
                "name": exercise["name"],
                "equipment": exercise.get(
                    "equipment"
                ),
                "muscle_group": exercise.get(
                    "muscle_group"
                ),
                "sets": exercise["sets"],
                "reps": exercise["reps"],
                "weight_kg": exercise.get(
                    "weight_kg",
                    0
                ),
                "rest_seconds": exercise.get(
                    "rest_seconds"
                ),
                "tempo": exercise.get(
                    "tempo"
                )
            })

        workouts_data.append({
            "name": workout["name"],
            "exercises": exercises_data
        })

    workout_data = {
        "student": {
            "name": student.name,
            "age": student.age,
            "sex": student.sex,
            "height_cm": student.height_cm,
            "weight_kg": student.weight_kg,
            "goal": student.goal,
            "experience_level": (
                student.experience_level
            ),
            "weekly_frequency": (
                student.weekly_frequency
            ),
            "session_duration_minutes": (
                student.session_duration_minutes
            ),
            "priority_muscle_groups": (
                student.priority_muscle_groups
            ),
            "movement_limitations": (
                student.movement_limitations
            ),
            "injuries_or_restrictions": (
                student.injuries_or_restrictions
            ),
            "excluded_exercises": (
                student.excluded_exercises
            ),
            "available_equipment": (
                student.available_equipment
            ),
            "recent_training_history": (
                student.recent_training_history
            ),
            "preferences": (
                student.preferences
            )
        },
        "program": {
            "title": workout_plan["title"],
            "workouts": workouts_data
        }
    }

    # ========================================
    # VALIDAR
    # ========================================

    print(
        "Validando dados do treino..."
    )

    validator = WorkoutValidator()

    validator.validate(
        workout_data
    )

    print(
        "Validação aprovada!"
    )

    print()

    # ========================================
    # MOSTRAR PLANO COMPLETO
    # ========================================

    print("================================")
    print("Plano de treino criado")
    print("================================")
    print()

    for workout in workout_plan["workouts"]:

        print(
            f"Treino {workout['name']}"
        )

        print()

        for exercise in workout["exercises"]:

            reps = exercise["reps"]

            if isinstance(
                reps,
                dict
            ):

                reps_text = (
                    f"{reps['min']}-"
                    f"{reps['max']}"
                )

            else:

                reps_text = str(
                    reps
                )

            print(
                f"Exercício: "
                f"{exercise['name']}"
            )

            print(
                f"Músculo: "
                f"{exercise['muscle_group']}"
            )

            print(
                f"Séries: "
                f"{exercise['sets']}"
            )

            print(
                f"Repetições: "
                f"{reps_text}"
            )

            print(
                f"Carga inicial: "
                f"{exercise.get('weight_kg', 0)} kg"
            )

            print()

    # ========================================
    # CONFIRMAÇÃO PARA ENVIAR AO HEVY
    # ========================================

    print("================================")
    print("Enviar rotina para o Hevy?")
    print("================================")
    print()

    print(
        "Digite 'sim' para confirmar "
        "ou 'não' para cancelar."
    )

    print()

    resposta = input("> ").strip().lower()

    if resposta not in [
        "sim",
        "s"
    ]:

        print()

        print(
            "Rotina não enviada ao Hevy."
        )

        print(
            "O plano foi criado "
            "e validado com sucesso."
        )

        return

    print()

    # ========================================
    # CONSTRUIR ROTINA PARA O HEVY
    # ========================================

    print(
        "Montando rotina para o Hevy..."
    )

    print()

    hevy_workout = (
        coach.build_hevy_workout(
            workout_plan
        )
    )

    print(
        "Rotina montada com sucesso!"
    )

    print()

    # ========================================
    # ENVIAR ROTINA
    # ========================================

    print(
        "Enviando rotina para o Hevy..."
    )

    print()

    routine_data = {
        "routine": {
            "title": hevy_workout["title"],
            "folder_id": None,
            "notes": (
                "Rotina criada pelo "
                "Hevy AI Coach."
            ),
            "exercises": (
                hevy_workout["exercises"]
            )
        }
    }

    print(
        f"Criando rotina: "
        f"{hevy_workout['title']}"
    )

    created_routine = (
        hevy.create_routine(
            routine_data
        )
    )

    print(
        "Rotina criada com sucesso!"
    )

    print()

    # ========================================
    # PEGAR DADOS DA ROTINA CRIADA
    # ========================================

    routine_list = created_routine.get(
        "routine",
        []
    )

    if routine_list:

        created_id = routine_list[0].get(
            "id"
        )

        created_title = routine_list[0].get(
            "title"
        )

        print(
            "ID da rotina:",
            created_id
        )

        print(
            "Título da rotina:",
            created_title
        )

    else:

        print(
            "Rotina criada, mas o Hevy "
            "não retornou os dados da rotina."
        )

    print()

    # ========================================
    # FINALIZAÇÃO
    # ========================================

    print("================================")
    print("PROCESSO CONCLUÍDO")
    print("================================")
    print()

    print(
        "A rotina foi criada pelo Coach,"
    )

    print(
        "validada e enviada para o Hevy."
    )

    print()

    print(
        "O Hevy agora será responsável "
        "pelo acompanhamento da evolução "
        "do aluno."
    )


if __name__ == "__main__":
    main()
