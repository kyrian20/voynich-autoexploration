"""Offline regression checks for the bounded Gemini review response validator."""
import unittest

from scripts.validate_gemini_review import validate


def valid_response():
    return {
        "limitations": ["No translation"] * 5,
        "competing_hypotheses": [
            {"name": f"hypothesis-{i}", "prediction": "testable prediction",
             "falsifier": "specific disconfirming observation"} for i in range(3)
        ],
        "proposed_design": {
            "unit_of_analysis": "folio", "sampling_frame": "documented subset",
            "strata": "section", "holdout": "disjoint folios",
            "test_statistic": "paired contrast", "negative_controls": ["permutation"],
            "parser_validation": "independent IVTFF reader",
            "multiple_testing": "predefined family", "stopping_rule": "fixed analysis"
        },
        "pre_registration": {
            "primary_outcome": "directional contrast",
            "decision_rule": "needs_data", "failure_conditions": ["parser mismatch"]
        },
        "required_inputs": ["source hashes"], "unresolved_questions": ["section mapping"]
    }


class GeminiReviewSchemaTests(unittest.TestCase):
    def test_valid_proposal_is_structurally_accepted(self):
        self.assertEqual(validate(valid_response()), [])

    def test_rejects_non_object(self):
        self.assertTrue(validate(["not a proposal"]))

    def test_rejects_missing_sections(self):
        response = valid_response()
        del response["pre_registration"]
        self.assertTrue(validate(response))

    def test_rejects_too_few_hypotheses(self):
        response = valid_response()
        response["competing_hypotheses"] = response["competing_hypotheses"][:2]
        self.assertTrue(validate(response))

    def test_rejects_missing_falsifier(self):
        response = valid_response()
        del response["competing_hypotheses"][0]["falsifier"]
        self.assertTrue(validate(response))

    def test_rejects_empty_required_input(self):
        response = valid_response()
        response["required_inputs"] = [""]
        self.assertTrue(validate(response))

    def test_rejects_unexpected_fields(self):
        response = valid_response()
        response["scientifically_validated"] = True
        self.assertTrue(validate(response))


if __name__ == "__main__":
    unittest.main()
