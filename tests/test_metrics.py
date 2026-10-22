import math

from c4.eval.metrics import bootstrap_score_ci, percentile, score, summarize, wilson_interval


def test_score():
    assert score(6, 2, 2) == 0.7
    assert math.isnan(score(0, 0, 0))


def test_wilson_known_values():
    lo, hi = wilson_interval(50, 100)
    assert abs(lo - 0.4038) < 1e-3 and abs(hi - 0.5962) < 1e-3
    lo, hi = wilson_interval(0, 10)
    assert lo < 1e-12 and abs(hi - 0.2775) < 1e-3
    assert wilson_interval(0, 0) == (0.0, 1.0)
    lo, hi = wilson_interval(100, 100)
    assert abs(hi - 1.0) < 1e-9 and lo > 0.96


def test_bootstrap_ci_contains_score_and_is_reproducible():
    results = [1] * 60 + [0] * 10 + [-1] * 30
    lo, hi = bootstrap_score_ci(results, seed=1)
    assert lo < score(60, 10, 30) < hi
    assert (lo, hi) == bootstrap_score_ci(results, seed=1)


def test_summarize_and_percentile():
    s = summarize([1, 1, 0, -1])
    assert (s["wins"], s["draws"], s["losses"], s["n"]) == (2, 1, 1, 4)
    assert s["score"] == 0.625
    assert abs(percentile(list(range(1, 101)), 95) - 95.05) < 1e-9
