from numbers import Real

from smart.model.smart_objects import SmartGoal


class SmartGoalPredictor:
    def __init__(self,
                 goal: SmartGoal,
                 std_deviation: 3,
                 target: Real,
                 success_factor=0.70):
        self.goal = goal
        self.target = target
        self.std_deviation = std_deviation
        self.success_factor = success_factor

    def achievability(self) -> int:
        return len(self.goal.achievable[self.goal.achievable[self.goal.column] >= self.target]) / len(self.goal.achievable)

    def realistically(self) -> int:
        return len(self.goal.realistic[self.goal.realistic[self.goal.column] > self.target]) / len(self.goal.realistic)

    def success_probability(self) -> float:
        if self.goal.measurable >= self.target:
            return 1

        achievability = self.achievability()
        realistically = self.realistically()

        return (achievability + realistically) / 2

    def is_success(self):
        return self.success_probability() >= self.success_factor
