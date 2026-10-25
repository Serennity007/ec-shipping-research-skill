# Europe container freight / 欧线集运 EC

Use the user's requested instrument, window and language. Do not invent a current contract, data subscription, margin schedule or market observation.

## Evidence to establish before interpretation

Record the dated contract, exchange, quote unit/currency, relevant delivery or index definition, cutoff with offset, observation/publication/availability times, and original source. On a roll, keep both contracts and their overlap explicit; do not splice the move into a return.

## Chain-specific hypotheses and failure conditions

- Identify the exact published settlement-index series, covered route and release time. A spot booking quotation is not a settlement-index observation.
- Compare futures points with the matching index definition and settlement window. A point premium is descriptive, not a cash-and-carry opportunity.
- A rerouting scenario changes voyage duration and effective capacity only under stated fleet, speed, idle-time and demand assumptions; do not equate delay with lost cargo.
- Separate announced blank sailings, realized sailings, booking demand and realized load factors. Avoid adding overlapping capacity reductions.
- Falsify a disruption-led premium if effective capacity recovers or bookings weaken while futures remain elevated. Verify the latest official settlement rules separately.

## Representative evidence series

- `settlement_index`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `effective_capacity`: declare source coverage, native units, publication cadence and revision policy before comparing values.
- `load_factor`: declare source coverage, native units, publication cadence and revision policy before comparing values.

A missing series is a gap, not zero. Explain which claim it would support or contradict. Use `fundamentals.metric` names that distinguish region, grade and coverage; the engine does not infer these from a short label.

## Practical research delivery

1. Preserve the supplied files and source claims; state whether the evidence is synthetic, retrieved now or an archived vintage.
2. Run `scripts/run_desk.py` for daily observations, vintages, comparable basis/curve, declared processing recipes and hypothetical capacity. Use existing specialist commands where their native macro, breadth, route or curve inputs fit better.
3. Read the quality gates before interpreting numbers. Reject unit/identity contradictions. Describe unavailable calculations rather than hiding them.
4. Write the observed facts first, then the proposed transmission mechanism, the strongest contrary evidence, and the next publication/event that can falsify it. Cite the original source for substantive imported claims.
5. If the user requests a setup, retain their declared trigger, confirmation, invalidation and time limit; do not manufacture historical signals after seeing future data. Separate a scenario from a forecast.
6. If capacity is requested, require the user's budget and effective rule schedule; report stress beyond the stop plan and the model's single-position scope. Do not select risk parameters for the user.

## Next checks

- Verify the index provider's publication calendar and observed release vintage.
- Map contract expiry and the applicable settlement observation window from official notices.
- Test rerouting and demand jointly; retain the original fleet denominator.

## 中文研究要点

- 核对具体结算指数、航线覆盖与发布时间；即期订舱报价不是结算指数观测。
- 期货点数须匹配指数定义与结算窗口；点数升水只是描述，不能解释为现货持有套利机会。
- 绕航只在船队、航速、停泊与需求假设下改变航程和有效运力；延误不等于货量消失。
- 宣布停航、实际开航、订舱需求和实际装载率分开；重叠运力削减不重复相加。
- 运力恢复或订舱转弱而期价仍高时，应检验并证伪扰动溢价叙事；另查最新官方结算规则。

- 核验指数机构的发布日历与实际公布版本。
- 根据官方通知核对合约到期及适用的结算观察窗口。
- 联合检验绕航和需求变化，保留原始船队分母。

## Review exercises

- A user supplies a continuous contract and asks for a roll-period return: obtain dated contracts/overlap or label the result unavailable; do not reinterpret the continuous code as a deliverable contract.
- An inventory revision was published after the report cutoff: exclude that vintage and retain the previously available observation; show the exclusion count.
- A large calculated premium has asynchronous quotes or different tax/quality scope: block the comparison and identify the precise input needed.
- A user asks for the 'best trade' with no current data: supply conditional research questions and evidence gaps; do not invent a current market or implied confidence score.
- A simulated loss budget fits twelve lots but an adverse gap exceeds it: report both values and state why the stop cannot guarantee that budget.
