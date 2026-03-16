import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# Bug fixed: Hard range was 1-50 (narrower than Normal 1-100), making Hard
# easier than Normal. Ranges must scale with difficulty.
# ---------------------------------------------------------------------------

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range_wider_than_normal():
    # Bug fixed: Hard must be harder (wider range) than Normal, not narrower
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard range must be wider than Normal"

def test_difficulty_ranges_scale():
    # Bug fixed: ranges must increase Easy < Normal < Hard
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high


# ---------------------------------------------------------------------------
# parse_guess
# Bug fixed: no range validation — numbers outside the difficulty range
# were accepted. parse_guess now takes low and high parameters.
# ---------------------------------------------------------------------------

def test_parse_guess_valid_number():
    ok, value, err = parse_guess("10", 1, 20)
    assert ok is True
    assert value == 10
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_none():
    ok, value, err = parse_guess(None, 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc", 1, 20)
    assert ok is False
    assert value is None

def test_parse_guess_decimal_truncated():
    # Decimals should be accepted and truncated to int
    ok, value, err = parse_guess("7.9", 1, 20)
    assert ok is True
    assert value == 7

def test_parse_guess_below_range():
    # Bug fixed: numbers below the difficulty range should be rejected
    ok, value, err = parse_guess("0", 1, 20)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_above_range():
    # Bug fixed: numbers above the difficulty range should be rejected
    ok, value, err = parse_guess("21", 1, 20)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_boundary_low():
    ok, value, err = parse_guess("1", 1, 20)
    assert ok is True
    assert value == 1

def test_parse_guess_boundary_high():
    ok, value, err = parse_guess("20", 1, 20)
    assert ok is True
    assert value == 20


# ---------------------------------------------------------------------------
# check_guess
# Bug fixed: "Too High" returned "Go HIGHER!" and "Too Low" returned
# "Go LOWER!" — the hint messages were completely swapped.
# ---------------------------------------------------------------------------

def test_check_guess_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_too_high_outcome():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_check_guess_too_high_hint_says_lower():
    # Bug fixed: hint must tell the player to go LOWER, not HIGHER
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message.upper(), f"Expected 'LOWER' in hint, got: {message}"

def test_check_guess_too_low_outcome():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_too_low_hint_says_higher():
    # Bug fixed: hint must tell the player to go HIGHER, not LOWER
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message.upper(), f"Expected 'HIGHER' in hint, got: {message}"

def test_check_guess_one_apart_high():
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"

def test_check_guess_one_apart_low():
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# update_score
# Bug fixed: "Too High" on even-numbered attempts added 5 points instead
# of subtracting. Wrong guesses must always reduce the score.
# ---------------------------------------------------------------------------

def test_update_score_win_early():
    # Winning on attempt 1 should give maximum points
    score = update_score(0, "Win", 1)
    assert score > 0

def test_update_score_win_minimum_points():
    # Win score should never drop below 10 regardless of attempt number
    score = update_score(0, "Win", 100)
    assert score >= 10

def test_update_score_win_decreases_with_attempts():
    score_early = update_score(0, "Win", 1)
    score_late = update_score(0, "Win", 5)
    assert score_early > score_late

def test_update_score_too_low_subtracts():
    score = update_score(100, "Too Low", 1)
    assert score < 100

def test_update_score_too_high_odd_attempt_subtracts():
    score = update_score(100, "Too High", 1)
    assert score < 100

def test_update_score_too_high_even_attempt_subtracts():
    # Bug fixed: even-numbered "Too High" attempts incorrectly added 5 points
    score = update_score(100, "Too High", 2)
    assert score < 100, "A wrong guess must never increase the score"

def test_update_score_too_high_always_subtracts_same_amount():
    # Bug fixed: score change must be consistent regardless of attempt parity
    score_odd = update_score(100, "Too High", 1)
    score_even = update_score(100, "Too High", 2)
    assert score_odd == score_even