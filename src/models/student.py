class Student:
    def __init__(
        self,
        name,
        age,
        sex,
        height_cm,
        weight_kg,
        goal,
        experience_level,
        experience_years,
        weekly_frequency,
        session_duration_minutes,
        priority_muscle_groups=None,
        movement_limitations=None,
        injuries_or_restrictions=None,
        excluded_exercises=None,
        available_equipment=None,
        recent_training_history=None,
        preferences=None
    ):
        self.name = name
        self.age = age
        self.sex = sex
        self.height_cm = height_cm
        self.weight_kg = weight_kg

        self.goal = goal
        self.experience_level = experience_level
        self.experience_years = experience_years

        self.weekly_frequency = weekly_frequency
        self.session_duration_minutes = session_duration_minutes

        self.priority_muscle_groups = (
            priority_muscle_groups or []
        )

        self.movement_limitations = (
            movement_limitations or []
        )

        self.injuries_or_restrictions = (
            injuries_or_restrictions or []
        )

        self.excluded_exercises = (
            excluded_exercises or []
        )

        self.available_equipment = (
            available_equipment or []
        )

        self.recent_training_history = (
            recent_training_history or []
        )

        self.preferences = preferences or {}

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "goal": self.goal,
            "experience_level": self.experience_level,
            "experience_years": self.experience_years,
            "weekly_frequency": self.weekly_frequency,
            "session_duration_minutes": (
                self.session_duration_minutes
            ),
            "priority_muscle_groups": (
                self.priority_muscle_groups
            ),
            "movement_limitations": (
                self.movement_limitations
            ),
            "injuries_or_restrictions": (
                self.injuries_or_restrictions
            ),
            "excluded_exercises": (
                self.excluded_exercises
            ),
            "available_equipment": (
                self.available_equipment
            ),
            "recent_training_history": (
                self.recent_training_history
            ),
            "preferences": self.preferences
        }