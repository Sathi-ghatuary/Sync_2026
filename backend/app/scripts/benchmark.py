"""
Benchmark script for title verification latency and concurrency behavior.

Usage:
  python -m app.scripts.benchmark
  python -m app.scripts.benchmark --requests 200 --workers 20 --target-ms 2000
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from fastapi.testclient import TestClient

from ..main import app


SAMPLE_TITLES = [
    "Morning Herald",
    "Dawn Chronicle",
    "Pratidin Sandhya",
    "Hindu Indian Express",
    "Crime Watch Daily",
    "The India News Bulletin",
    "National Business Chronicle",
    "Sunrise Dispatch",
    "Weekly Samachar Digest",
    "Digital Bharat Times",
]


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, int(round((p / 100.0) * (len(ordered) - 1)))))
    return ordered[idx]


def run_request(client: TestClient, title: str) -> tuple[float, int]:
    start = time.perf_counter()
    resp = client.post("/verify", json={"title": title})
    elapsed_ms = (time.perf_counter() - start) * 1000
    return elapsed_ms, resp.status_code


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark /verify API endpoint")
    parser.add_argument("--requests", type=int, default=100, help="Total requests to run")
    parser.add_argument("--workers", type=int, default=10, help="Concurrent worker threads")
    parser.add_argument("--target-ms", type=float, default=2000.0, help="Latency target in milliseconds")
    parser.add_argument("--warmup", type=int, default=5, help="Warmup requests (excluded from metrics)")
    args = parser.parse_args()

    latencies: List[float] = []
    failed = 0
    started = time.perf_counter()

    with TestClient(app) as client:
        # Warmup phase to remove model initialization skew.
        for _ in range(max(0, args.warmup)):
            _ = run_request(client, random.choice(SAMPLE_TITLES))

        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = []
            for _ in range(args.requests):
                title = random.choice(SAMPLE_TITLES)
                futures.append(pool.submit(run_request, client, title))

            for fut in as_completed(futures):
                ms, status = fut.result()
                latencies.append(ms)
                if status != 200:
                    failed += 1

    wall_ms = (time.perf_counter() - started) * 1000
    avg = statistics.mean(latencies) if latencies else 0.0
    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    max_v = max(latencies) if latencies else 0.0

    print("=== Benchmark Result ===")
    print(f"Requests: {args.requests}")
    print(f"Workers: {args.workers}")
    print(f"Failures: {failed}")
    print(f"Wall Time (ms): {wall_ms:.2f}")
    print(f"Avg (ms): {avg:.2f}")
    print(f"P50 (ms): {p50:.2f}")
    print(f"P95 (ms): {p95:.2f}")
    print(f"Max (ms): {max_v:.2f}")
    print(f"Target (ms): {args.target_ms:.2f}")
    print(f"Target Met (P95 <= target): {p95 <= args.target_ms}")


if __name__ == "__main__":
    main()
