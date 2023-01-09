from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
from pandas import DataFrame
from smart.calc.predictor import SmartGoalPredictor

from smart.model.smart_objects import SmartGoal
from mpt.single_sums import get_future_sum_with_payments, get_future_value_sum_with_present_value


def test_smart_goal_predictor_success():
    periods = 30
    timely = datetime.now() + relativedelta(years=periods)

    present_value = 100000.00
    payment_amount = 20000.00
    interest_rate = 0.07
    compounding = 1

    future_value_sum = get_future_value_sum_with_present_value(present_value,
                                                               interest_rate,
                                                               periods,
                                                               compounding)

    future_sum_with_payments = get_future_sum_with_payments(payment_amount,
                                                            interest_rate,
                                                            periods,
                                                            compounding)

    measurable = future_value_sum + future_sum_with_payments

    retirement_population = load_csv("data/retirement_population.csv")
    retirement_sample = load_csv("data/successful_retirement_sample.csv")

    goal = SmartGoal(column="investment",
                     specific="dollars",
                     measurable=measurable,
                     achievable=retirement_population,
                     realistic=retirement_sample,
                     timely=timely)

    predictor = SmartGoalPredictor(goal=goal,
                                   std_deviation=1,
                                   target=1000000)

    success_probability = predictor.success_probability()

    assert (success_probability >= 1)

    assert (predictor.is_success())


def test_smart_goal_predictor_failure():
    periods = 30
    timely = datetime.now() + relativedelta(years=periods)

    present_value = 100000.00
    payment_amount = 2000.00
    interest_rate = 0.07
    compounding = 1

    future_value_sum = get_future_value_sum_with_present_value(present_value,
                                                               interest_rate,
                                                               periods,
                                                               compounding)

    future_sum_with_payments = get_future_sum_with_payments(payment_amount,
                                                            interest_rate,
                                                            periods,
                                                            compounding)

    measurable = future_value_sum + future_sum_with_payments

    retirement_population = load_csv("data/retirement_population.csv")
    retirement_sample = load_csv("data/unsuccessful_retirement_sample.csv")

    goal = SmartGoal(column="investment",
                     specific="dollars",
                     measurable=measurable,
                     achievable=retirement_sample,
                     realistic=retirement_population,
                     timely=timely)

    predictor = SmartGoalPredictor(goal=goal,
                                   target=1000000,
                                   std_deviation=1)

    success_probability = predictor.success_probability()

    assert (success_probability == 0.55)

    assert (not predictor.is_success())


def load_csv(file_name: str) -> DataFrame:
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, file_name)

    return pd.read_csv(path)
