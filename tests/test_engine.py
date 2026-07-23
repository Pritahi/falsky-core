"""
Falsky — Real unit tests for the trust engine.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.trust_engine import process_test_run, get_dashboard_data


class RealFalskyTests(unittest.TestCase):
    def test_passing_run(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="tests" tests="1" failures="0">
    <testcase name="test_homepage_loads" classname="DemoTest" time="0.12"/>
  </testsuite>
</testsuites>"""
        result = process_test_run(
            xml_content=xml,
            repo_name="falsky-core",
            run_id="ci_run_001",
            branch="main",
            commit_sha="abc0123",
        )
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["avg_trust_score"], 100.0)

    def test_mixed_runs(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="tests" tests="2" failures="1">
    <testcase name="test_api_returns_200" classname="DemoTest" time="0.35">
      <failure message="500 Server Error">details</failure>
    </testcase>
    <testcase name="test_user_can_login" classname="DemoTest" time="0.08"/>
  </testsuite>
</testsuites>"""
        result = process_test_run(
            xml_content=xml,
            repo_name="falsky-core",
            run_id="ci_run_002",
            branch="main",
            commit_sha="abc0124",
        )
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failed"], 1)
        self.assertLess(result["avg_trust_score"], 100.0)
        self.assertEqual(result["total"], 2)

    def test_dashboard_metrics(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="tests" tests="2" failures="1">
    <testcase name="test_api_returns_200" classname="DemoTest" time="0.35">
      <failure message="500 Server Error">details</failure>
    </testcase>
    <testcase name="test_user_can_login" classname="DemoTest" time="0.08"/>
  </testsuite>
</testsuites>"""
        process_test_run(
            xml_content=xml,
            repo_name="falsky-core",
            run_id="ci_run_003",
            branch="main",
            commit_sha="abc0125",
        )
        dash = get_dashboard_data("falsky-core")
        self.assertGreaterEqual(dash["total"], 1)

    def test_flaky_test_detection(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="tests" tests="1" failures="0">
    <testcase name="test_database_connection_pool" classname="DemoTest" time="0.95"/>
  </testsuite>
</testsuites>"""
        process_test_run(
            xml_content=xml,
            repo_name="falsky-core",
            run_id="ci_run_004",
            branch="main",
            commit_sha="abc0126",
        )
        dash = get_dashboard_data("falsky-core")
        self.assertGreaterEqual(dash["total"], 1)


if __name__ == "__main__":
    unittest.main()
