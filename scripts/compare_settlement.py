#!/usr/bin/env python3
"""Compare EC quotes with the latest SCFIS Europe observation published by the cutoff."""
import argparse
from datetime import date
from pathlib import Path
import re

from market_io import timestamp, number, records, provenance, emit, kind


def analyze(futures_raw, index_raw, contract, as_of, data_kind):
    cutoff = timestamp(as_of)
    contract = contract.upper()
    match = re.fullmatch(r"EC(\d{2})(\d{2})", contract)
    if not match:
        raise ValueError("contract must identify an EC YYMM month")
    delivery = f"20{match[1]}-{match[2]}"
    date.fromisoformat(delivery + "-01")
    quotes = records(futures_raw, ["contract", "contract_month", "price", "quote_time", "unit"])
    candidates, quote_seen, excluded_quotes = [], set(), 0
    for row in quotes:
        if row["contract"].upper() != contract:
            continue
        observed = timestamp(row["quote_time"])
        if observed > cutoff:
            excluded_quotes += 1
            continue
        if row["contract_month"] != delivery or row["unit"] != "index_points":
            raise ValueError("contract month or EC quote units do not match")
        if observed in quote_seen:
            raise ValueError("duplicate EC quote timestamp")
        quote_seen.add(observed)
        candidates.append((observed, number(row["price"], positive=True)))
    observations = records(index_raw, ["index_name", "period_end", "published_at", "value"])
    available, seen, excluded_publications = [], set(), 0
    for row in observations:
        if row["index_name"] != "SCFIS_EUROPE":
            raise ValueError("SCFI or another route cannot be substituted for SCFIS_EUROPE")
        period, published = timestamp(row["period_end"]), timestamp(row["published_at"])
        if period > published:
            raise ValueError("index period cannot end after its publication")
        if published > cutoff:
            excluded_publications += 1
            continue
        if published in seen:
            raise ValueError("duplicate index publication timestamp")
        seen.add(published)
        available.append((published, period, number(row["value"], positive=True)))
    if not candidates or not available:
        raise ValueError("no EC quote and published SCFIS observation available at cutoff")
    quote_time, price = max(candidates)
    published, period, value = max(available)
    return {"schema_version": 1, "data_kind": kind(data_kind), "contract": contract,
            "contract_month": delivery, "as_of_utc": cutoff.isoformat(), "quote_time": quote_time.isoformat(),
            "futures_price": price, "index_name": "SCFIS_EUROPE", "index_period_end": period.isoformat(),
            "index_published_at": published.isoformat(), "last_published_index": value,
            "futures_minus_last_published_index": price - value,
            "difference_ratio": price / value - 1, "publication_age_seconds": (cutoff - published).total_seconds(),
            "quote_age_seconds": (cutoff - quote_time).total_seconds(),
            "index_published_after_quote": published > quote_time,
            "excluded_future_quotes": excluded_quotes, "excluded_future_publications": excluded_publications,
            "source_sha256": {"futures": provenance(futures_raw), "index": provenance(index_raw)},
            "scope": "Difference from a lagged published index, not a guaranteed basis trade or final settlement-price forecast.",
            "limitations": ["No final cash-settlement calculation; verify exchange rules for the specific contract",
                            "Shipping news, carrier quotes and SCFI are not SCFIS settlement observations",
                            "Quote and publication timestamps can differ; do not present this as a synchronous tradable spread"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--futures", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--data-kind", required=True, choices=("synthetic", "imported_observations"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(args.futures.read_bytes(), args.index.read_bytes(), args.contract, args.as_of, args.data_kind)
        emit(result, args.out, [args.futures, args.index])
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(f"Saved {result['contract']} versus published SCFIS / {result['data_kind']}.")


if __name__ == "__main__":
    main()
