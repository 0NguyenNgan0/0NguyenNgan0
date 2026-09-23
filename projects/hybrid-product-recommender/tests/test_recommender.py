"""Behavioral checks for leakage boundaries, ranking contracts, and ALS solves."""
from datetime import timedelta
import unittest

import numpy as np

from recommender.data import CUTOFF, Event, Product, make_synthetic_data, temporal_split
from recommender.evaluate import evaluate, ranking_metrics
from recommender.model import METHODS, HybridRecommender, implicit_als


class RecommenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.events = make_synthetic_data()
        cls.train, cls.test = temporal_split(cls.events)
        cls.model = HybridRecommender().fit(cls.catalog, cls.train)

    def test_global_time_boundary_and_deduplication(self):
        exact = Event("boundary_user", "demo_item_000", "view", CUTOFF)
        train, test = temporal_split(self.events + [exact, exact])
        self.assertTrue(all(e.timestamp < CUTOFF for e in train))
        self.assertTrue(all(e.timestamp >= CUTOFF for e in test))
        self.assertEqual(test.count(exact), 1)
        self.assertFalse(set(train) & set(test))

    def test_synthetic_data_is_repeatable(self):
        self.assertEqual(make_synthetic_data(), (self.catalog, self.events))
        self.assertNotEqual(make_synthetic_data(17)[1], self.events)

    def test_routes_and_common_cold_start_fallback(self):
        self.assertEqual(self.model.route("demo_user_000"), "hybrid")
        self.assertEqual(self.model.route("demo_user_060"), "content")
        self.assertEqual(self.model.route("unseen_user"), "popularity")
        popular = self.model.recommend("unseen_user", method="popularity")
        for method in METHODS:
            self.assertEqual(self.model.recommend("unseen_user", method=method), popular)
        self.assertEqual(self.model.recommend("demo_user_060", method="hybrid"),
                         self.model.recommend("demo_user_060", method="content"))

    def test_all_methods_exclude_seen_and_obey_top_k(self):
        for method in METHODS:
            for user in ["demo_user_000", "demo_user_060", "unseen_user"]:
                recs = self.model.recommend(user, 10, method)
                self.assertEqual(len(recs), 10)
                self.assertEqual(len(set(recs)), 10)
                self.assertFalse(set(recs) & self.model.seen(user))
                self.assertTrue(set(recs) <= set(self.model.item_ids))
        all_remaining = self.model.recommend("demo_user_000", 1000)
        self.assertEqual(len(all_remaining), len(self.catalog) - len(self.model.seen("demo_user_000")))

    def test_als_objective_decreases_and_zero_history_item_has_zero_factors(self):
        r = np.array([[3, 0, 1, 0], [0, 4, 1, 0], [2, 0, 2, 0]], dtype=float)
        x, y, losses = implicit_als(r, factors=3, iterations=10)
        self.assertTrue(np.isfinite(x @ y.T).all())
        self.assertTrue(np.all(np.diff(losses) <= 1e-8))
        self.assertLess(losses[-1], losses[0])
        np.testing.assert_allclose(y[3], 0, atol=1e-10)

    def test_content_can_retrieve_item_without_training_interactions(self):
        catalog = [Product("a", "audio", "alpha"), Product("b", "audio", "alpha"),
                   Product("c", "camera", "beta")]
        train = [Event("u", "a", "view", CUTOFF - timedelta(days=1))]
        model = HybridRecommender().fit(catalog, train)
        self.assertEqual(model.recommend("u", 1, "content"), ["b"])

    def test_metric_hand_calculation_and_short_list_penalty(self):
        metrics = ranking_metrics(["a", "x", "b"], {"a", "b", "c"}, 3)
        self.assertAlmostEqual(metrics["precision_at_k"], 2 / 3)
        self.assertAlmostEqual(metrics["recall_at_k"], 2 / 3)
        self.assertAlmostEqual(metrics["ndcg_at_k"], 1.5 / (1 + 1 / np.log2(3) + 0.5))
        self.assertEqual(ranking_metrics(["a"], {"a"}, 10)["precision_at_k"], 0.1)

    def test_evaluation_uses_argument_and_rejects_temporal_overlap(self):
        report = evaluate(self.model, self.test)
        self.assertEqual(report["users_in_holdout"], 80)
        self.assertEqual(report["cohort_counts"], {"warm": 60, "sparse": 10, "new": 10})
        subset = [e for e in self.test if e.user_id == "demo_user_070"]
        self.assertEqual(evaluate(self.model, subset)["evaluated_users"], 1)
        with self.assertRaises(ValueError):
            evaluate(self.model, self.test + [self.train[0]])

    def test_evaluation_excludes_repeat_consumption_and_counts_skips(self):
        user = "demo_user_000"
        seen = sorted(self.model.seen(user))[0]
        repeat = Event(user, seen, "purchase", CUTOFF + timedelta(days=1))
        report = evaluate(self.model, [repeat] + [e for e in self.test if e.user_id == "demo_user_070"])
        self.assertEqual(report["users_in_holdout"], 2)
        self.assertEqual(report["evaluated_users"], 1)
        self.assertEqual(report["skipped_no_novel_items"], 1)

    def test_invalid_inputs_fail_visibly(self):
        with self.assertRaises(ValueError):
            self.model.recommend("u", 0)
        with self.assertRaises(ValueError):
            self.model.recommend("u", method="typo")
        with self.assertRaises(ValueError):
            HybridRecommender().fit(self.catalog, [])
        with self.assertRaises(ValueError):
            HybridRecommender().fit(self.catalog, [Event("u", "missing", "view", CUTOFF)])
        with self.assertRaises(ValueError):
            evaluate(self.model, [])


if __name__ == "__main__":
    unittest.main()
