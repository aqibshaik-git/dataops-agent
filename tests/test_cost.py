import pytest

from dataops_agent.config import Pricing
from dataops_agent.cost import call_cost

HAIKU = Pricing(
    input_per_mtok=0.10,
    output_per_mtok=0.50,
    long_context_threshold=100_000,
    long_input_per_mtok=0.50,
    long_output_per_mtok=2.50,
)


def test_one_million_each_way_costs_input_plus_output_rate():
    assert call_cost(1_000_000, 0, Pricing(3.0, 15.0)) == pytest.approx(3.0)
    assert call_cost(0, 1_000_000, Pricing(3.0, 15.0)) == pytest.approx(15.0)


def test_small_call_is_fractions_of_a_cent():
    # 500 in, 300 out: 500*0.10/1e6 + 300*0.50/1e6
    assert call_cost(500, 300, HAIKU) == pytest.approx(0.0002)


def test_at_threshold_uses_normal_rates():
    assert call_cost(100_000, 0, HAIKU) == pytest.approx(0.01)


def test_over_threshold_uses_long_rates_for_input_and_output():
    assert call_cost(100_001, 1_000, HAIKU) == pytest.approx(100_001 * 0.50 / 1e6 + 1_000 * 2.50 / 1e6)


def test_negative_tokens_rejected():
    with pytest.raises(ValueError):
        call_cost(-1, 0, HAIKU)
