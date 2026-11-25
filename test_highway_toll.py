# Name: Pranaav Prabhakaran
# SRN : PES1UG24AM387
# Lab 6: Code and Branch Coverage - Highway Toll Calculator
#
# This test suite exercises every function, line and branch in
# highway_toll.py, targeting 100% statement and branch coverage.

import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ---------------------------------------------------------------------------
# toll_for
# ---------------------------------------------------------------------------

def test_invalid_axle_count_raises():
    # axles < 2 -> ValueError branch
    with pytest.raises(ValueError):
        toll_for(1, False, False)


def test_two_axle_base_toll():
    # axles in BASE_TOLL, no peak, no fastag
    assert toll_for(2, False, False) == 100


def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150


def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250


def test_five_axle_uses_flat_base():
    # axles not in BASE_TOLL -> base = 400 (else branch)
    assert toll_for(5, False, False) == 400


def test_peak_surcharge_applied():
    # is_peak True branch: 100 * 1.25
    assert toll_for(2, True, False) == 125.0


def test_fastag_discount_two_axle():
    # has_fastag True and axles == 2 -> 100 * 0.9
    assert toll_for(2, False, True) == 90.0


def test_fastag_discount_non_two_axle():
    # has_fastag True and axles != 2 -> 150 * 0.95
    assert toll_for(3, False, True) == 142.5


def test_peak_and_fastag_combined_two_axle():
    # both peak and fastag on a 2-axle vehicle: 100 * 1.25 * 0.9
    assert toll_for(2, True, True) == 112.5


def test_peak_and_fastag_combined_multi_axle():
    # both peak and fastag on a 5-axle vehicle: 400 * 1.25 * 0.95
    assert toll_for(5, True, True) == 475.0


# ---------------------------------------------------------------------------
# toll_charge
# ---------------------------------------------------------------------------

def test_ambulance_is_exempt():
    # vehicle in EXEMPT -> returns 0
    assert toll_charge("ambulance", 2, False, False) == 0


def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 4, True, True) == 0


def test_non_exempt_vehicle_delegates_to_toll_for():
    # vehicle not in EXEMPT -> delegates to toll_for
    assert toll_charge("car", 2, False, False) == 100


# ---------------------------------------------------------------------------
# pass_advice
# ---------------------------------------------------------------------------

def test_pass_advice_buy_pass():
    # total cost > pass_price -> "buy_pass"
    trips = [(False, False), (False, False), (False, False)]  # 100 * 3 = 300
    assert pass_advice(trips, 2, 250) == "buy_pass"


def test_pass_advice_either_when_equal():
    # total cost == pass_price -> "either"
    trips = [(False, False), (False, False)]  # 100 * 2 = 200
    assert pass_advice(trips, 2, 200) == "either"


def test_pass_advice_pay_per_trip():
    # total cost < pass_price -> "pay_per_trip"
    trips = [(False, False)]  # 100
    assert pass_advice(trips, 2, 250) == "pay_per_trip"


def test_pass_advice_empty_trips():
    # no trips -> cost 0, which is < any positive pass_price
    assert pass_advice([], 2, 100) == "pay_per_trip"
