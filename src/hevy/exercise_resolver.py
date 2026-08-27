from hevy.client import HevyClient


class ExerciseResolver:

    def __init__(self, hevy_client):
        self.hevy_client = hevy_client
        self._exercise_cache = None

    def resolve(
        self,
        exercise_name,
        equipment=None,
        muscle_group=None
    ):
        exercises = self.get_available_exercises()

        search_name = self._normalize(exercise_name)

        requested_equipment = None
        if equipment:
            requested_equipment = self._normalize(equipment)

        requested_muscle = None
        if muscle_group:
            requested_muscle = self._normalize(muscle_group)

        exact_candidates = []
        equivalent_candidates = []

        for exercise in exercises:
            title = self._normalize(exercise["title"])
            title_base = title.split("(")[0].strip()

            if title_base == search_name:
                exact_candidates.append(exercise)
                continue

            if self._is_equivalent_name(
                search_name,
                title_base
            ):
                equivalent_candidates.append(exercise)

        candidates = exact_candidates

        if not candidates:
            candidates = equivalent_candidates

        if candidates:
            candidates = self._filter_by_equipment(
                candidates,
                requested_equipment
            )

            candidates = self._filter_by_muscle(
                candidates,
                requested_muscle
            )

            if candidates:
                return self._choose_best_candidate(
                    candidates,
                    search_name,
                    requested_equipment
                )

        alternative = self._find_safe_alternative(
            exercises,
            requested_muscle,
            requested_equipment,
            search_name
        )

        if alternative:
            return alternative

        self._raise_resolution_error(
            exercise_name,
            requested_equipment,
            requested_muscle,
            exercises
        )

    def _filter_by_equipment(
        self,
        candidates,
        requested_equipment
    ):
        if not requested_equipment:
            return candidates

        matches = []

        for exercise in candidates:
            if self._equipment_matches(
                exercise["equipment"],
                requested_equipment
            ):
                matches.append(exercise)

        return matches

    def _filter_by_muscle(
        self,
        candidates,
        requested_muscle
    ):
        if not requested_muscle:
            return candidates

        matches = []

        for exercise in candidates:
            exercise_muscle = self._normalize(
                exercise["primary_muscle_group"]
            )

            if exercise_muscle == requested_muscle:
                matches.append(exercise)

        return matches

    def _find_safe_alternative(
        self,
        exercises,
        requested_muscle,
        requested_equipment,
        search_name
    ):
        if not requested_muscle:
            return None

        alternatives = []

        for exercise in exercises:
            exercise_muscle = self._normalize(
                exercise["primary_muscle_group"]
            )

            if exercise_muscle != requested_muscle:
                continue

            if requested_equipment:
                if not self._equipment_matches(
                    exercise["equipment"],
                    requested_equipment
                ):
                    continue

            alternatives.append(exercise)

        if not alternatives:
            return None

        return self._choose_best_alternative(
            alternatives,
            search_name
        )

    def _choose_best_alternative(
        self,
        candidates,
        search_name
    ):
        requested_words = set(
            search_name.split()
        )

        scored = []

        for exercise in candidates:
            title = self._normalize(
                exercise["title"]
            )

            title_base = title.split("(")[0].strip()

            score = 0

            for word in requested_words:
                if word in title_base:
                    score += 10

            if "barbell" in requested_words:
                if "barbell" in title:
                    score += 20

            if "dumbbell" in requested_words:
                if "dumbbell" in title:
                    score += 20

            if "machine" in title:
                score += 2

            scored.append(
                (score, exercise)
            )

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return scored[0][1]

    def _raise_resolution_error(
        self,
        exercise_name,
        equipment,
        muscle_group,
        exercises
    ):
        if muscle_group:
            muscle_exercises = []

            requested_muscle = self._normalize(
                muscle_group
            )

            for exercise in exercises:
                exercise_muscle = self._normalize(
                    exercise["primary_muscle_group"]
                )

                if exercise_muscle == requested_muscle:
                    muscle_exercises.append(
                        exercise["title"]
                    )

            if muscle_exercises:
                preview = ", ".join(
                    muscle_exercises[:10]
                )

                raise ValueError(
                    f"Exercício '{exercise_name}' "
                    f"não encontrado no Hevy. "
                    f"Alternativas disponíveis para "
                    f"{muscle_group}: {preview}"
                )

        raise ValueError(
            f"Exercício '{exercise_name}' "
            f"não encontrado no Hevy."
        )

    def _normalize(self, value):
        if value is None:
            return ""

        value = str(value).lower().strip()

        replacements = {
            "*": " ",
            "-": " ",
            "/": " ",
            "_": " "
        }

        for old, new in replacements.items():
            value = value.replace(old, new)

        while "  " in value:
            value = value.replace(
                "  ",
                " "
            )

        return value

    def _is_equivalent_name(
        self,
        requested_name,
        hevy_name
    ):
        requested_words = set(
            requested_name.split()
        )

        hevy_words = set(
            hevy_name.split()
        )

        aliases = {
            "barbell": {
                "barbell",
                "bar"
            },
            "dumbbell": {
                "dumbbell",
                "db"
            },
            "curl": {
                "curl"
            },
            "press": {
                "press"
            },
            "row": {
                "row"
            },
            "pulldown": {
                "pulldown",
                "pull down"
            },
            "pushdown": {
                "pushdown",
                "push down"
            },
            "extension": {
                "extension"
            },
            "squat": {
                "squat"
            },
            "deadlift": {
                "deadlift",
                "dead lift"
            },
            "thrust": {
                "thrust"
            }
        }

        for word in requested_words:

            if word in aliases:

                valid_words = aliases[word]

                if not any(
                    alias in hevy_name
                    for alias in valid_words
                ):
                    return False

            elif word not in hevy_words:
                return False

        important_words = {
            word
            for word in requested_words
            if word not in {
                "the",
                "with",
                "and"
            }
        }

        if not important_words:
            return False

        matched_words = 0

        for word in important_words:

            if word in hevy_name:
                matched_words += 1
                continue

            if word in aliases:

                if any(
                    alias in hevy_name
                    for alias in aliases[word]
                ):
                    matched_words += 1

        return (
            matched_words
            == len(important_words)
        )

    def _equipment_matches(
        self,
        available_equipment,
        requested_equipment
    ):
        available = self._normalize(
            available_equipment
        )

        requested = self._normalize(
            requested_equipment
        )

        aliases = {
            "barbell": {
                "barbell",
                "bar"
            },
            "dumbbell": {
                "dumbbell",
                "db"
            },
            "cable": {
                "cable",
                "machine"
            },
            "machine": {
                "machine",
                "cable"
            },
            "bodyweight": {
                "bodyweight",
                "body weight"
            },
            "resistance band": {
                "resistance band",
                "band"
            }
        }

        if requested in aliases:
            return (
                available
                in aliases[requested]
            )

        return available == requested

    def _choose_best_candidate(
        self,
        candidates,
        search_name,
        equipment
    ):
        if len(candidates) == 1:
            return candidates[0]

        requested_words = set(
            search_name.split()
        )

        scored_candidates = []

        for exercise in candidates:

            title = self._normalize(
                exercise["title"]
            )

            title_base = title.split(
                "("
            )[0].strip()

            score = 0

            if title_base == search_name:
                score += 100

            for word in requested_words:

                if word in title_base:
                    score += 10

            if equipment:

                if self._equipment_matches(
                    exercise["equipment"],
                    equipment
                ):
                    score += 50

            scored_candidates.append(
                (score, exercise)
            )

        scored_candidates.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return scored_candidates[0][1]

    def get_available_exercises(self):
        if self._exercise_cache is not None:
            return self._exercise_cache

        exercises = []

        page = 1

        while True:

            data = (
                self.hevy_client
                .get_exercise_templates(
                    page=page,
                    page_size=100
                )
            )

            templates = data.get(
                "exercise_templates",
                []
            )

            page_count = data.get(
                "page_count",
                1
            )

            for exercise in templates:

                exercises.append({
                    "id": exercise["id"],
                    "title": exercise["title"],
                    "type": exercise["type"],
                    "primary_muscle_group": (
                        exercise[
                            "primary_muscle_group"
                        ]
                    ),
                    "equipment": (
                        exercise["equipment"]
                    )
                })

            if page >= page_count:
                break

            page += 1

        self._exercise_cache = exercises

        return exercises