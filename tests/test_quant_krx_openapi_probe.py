from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROBE = REPO_ROOT / "scripts" / "quant_krx_openapi_probe.py"


class QuantKrxOpenapiProbeTest(unittest.TestCase):
    def test_dry_run_redacts_auth_header_without_env_file(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(PROBE),
                "--url",
                "https://example.invalid/svc/apis/sto/example",
                "--param",
                "basDd=20260703",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["headers"], {"AUTH_KEY": "***"})
        self.assertEqual(payload["params"], {"basDd": "20260703"})
        self.assertNotIn("KRX_AUTH_KEY", result.stdout)

    def test_missing_auth_key_fails_before_network_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env.krx"
            env_file.write_text("KRX_AUTH_KEY=\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROBE),
                    "--url",
                    "https://example.invalid/svc/apis/sto/example",
                    "--env-file",
                    str(env_file),
                    "--output",
                    str(Path(tmp) / "raw.json"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("KRX OpenAPI key is missing", result.stderr)

    def test_bad_env_line_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env.krx"
            env_file.write_text(
                textwrap.dedent(
                    """
                    # comment
                    BAD_LINE
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROBE),
                    "--url",
                    "https://example.invalid/svc/apis/sto/example",
                    "--env-file",
                    str(env_file),
                    "--output",
                    str(Path(tmp) / "raw.json"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected KEY=VALUE", result.stderr)


if __name__ == "__main__":
    unittest.main()
