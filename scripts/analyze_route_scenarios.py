#!/usr/bin/env python3
"""Estimate a fixed-fleet round-trip capacity sensitivity, without estimating freight or EC prices."""
import argparse
from pathlib import Path
from market_io import timestamp, number, records, provenance, emit, kind


def analyze(raw, as_of, data_kind):
    cutoff=timestamp(as_of)
    results,seen,excluded=[],set(),0
    for row in records(raw,['scenario','known_at','base_cycle_days','extra_cycle_days','affected_share','demand_change_fraction']):
        known=timestamp(row['known_at'])
        if known>cutoff:
            excluded+=1
            continue
        name=row['scenario'].strip()
        if not name or name in seen:
            raise ValueError('scenario names must be nonempty and unique')
        seen.add(name)
        base=number(row['base_cycle_days'],positive=True)
        extra=number(row['extra_cycle_days'])
        share=number(row['affected_share'])
        demand=number(row['demand_change_fraction'])
        if extra<0 or not 0<=share<=1 or demand<=-1:
            raise ValueError('extra days >=0, affected share in [0,1], demand change >-1 required')
        capacity=(1-share)+share*base/(base+extra)
        pressure=(1+demand)/capacity
        results.append({'scenario':name,'known_at':known.isoformat(),'base_cycle_days':base,'extra_cycle_days':extra,
                        'affected_share':share,'demand_change_fraction':demand,'effective_capacity_fraction':capacity,
                        'capacity_loss_fraction':1-capacity,'demand_per_capacity_relative':pressure,
                        'pressure_vs_baseline':'higher' if pressure>1 else 'lower' if pressure<1 else 'unchanged'})
    if not results:
        raise ValueError('no available scenarios at cutoff')
    return {'schema_version':1,'data_kind':kind(data_kind),'as_of_utc':cutoff.isoformat(),
            'scenarios':results,'excluded_future_scenarios':excluded,'source_sha256':provenance(raw),
            'model':'capacity=(1-share)+share*base_cycle/(base_cycle+extra_cycle); pressure=(1+demand_change)/capacity',
            'scope':'User-assumed sensitivity, not observed capacity loss, freight elasticity or EC return.',
            'limitations':['Affected share refers to baseline capacity, not the percentage of ships in a news sample',
                           'Assumes a fixed fleet, unchanged vessel capacity and baseline utilization, no redeployment or new deliveries',
                           'extra_cycle_days is additional ROUND-TRIP cycle time; do not double-count a one-way estimate',
                           'No estimated relationship from capacity pressure to freight rates or futures prices']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv',type=Path,required=True)
    parser.add_argument('--as-of',required=True)
    parser.add_argument('--data-kind',choices=('synthetic','imported_observations'),required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        emit(analyze(args.csv.read_bytes(),args.as_of,args.data_kind),args.out,[args.csv])
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2,f'ERROR: {exc}\n')
    print('Saved fixed-fleet route scenarios; no freight price prediction.')


if __name__=='__main__':
    main()
