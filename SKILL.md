---
name: ec-shipping-research-skill
description: 研究集运指数（欧线）期货 EC 的航路扰动、有效运力、运价与 SCFIS 欧洲航线指数，核对合约月份和信息公布时间；不把新闻报价当成结算价或保证上涨。
license: MIT
metadata:
  author: Serennity007
  version: "2.0.0"
---

# 欧线 EC 研究 Skill

把航线事件、有效运力、船司报价与已公布结算运价指数放到一条时间轴，判断叙事是否真正传导到 EC 合约。

## 工作方式

1. 确认 EC 合约月，区分期价、SCFIS 欧洲航线、SCFI 欧洲航线与船司报价；不要交叉替代。
2. 拆解事件如何影响上海—欧洲航线：红海/苏伊士通行、绕航时间、有效运力、班次和货量；原油运输航路不是集运欧线的直接替代。
3. 比较已公布运价与期价时读取 `references/domain-data.md`，按 published_at 截断，而非按统计期末日期假设当时已经可见。
4. 同时观察合约月差和多周期结构，检查预期是否已被交易。最终结算按目标合约最新交易所规则另算，不能用最后一期指数直接代替。
5. 输出情景、失效条件和下一次运价/航线信息检查点；对事后回忆保留证据等级，不把高确信度写成确定收益。

## 按任务读取

- 解释驱动、拆解情景或审核观点时，读 [研究方法](references/method.md)。
- 导入数据或解释指标时，读 [文件与时间契约](references/data-contract.md)。
- 运行领域工具前读 [领域数据与计算](references/domain-data.md)。
- 写研究报告和复盘时，读 [记录字段](references/report-template.md)。
- 核查外部口径时，使用 [官方来源入口](references/sources.md)，记录实际访问日期。

## 研究工作台

完整研究时先读 [工作台与高级数据](references/workbench.md)。使用者给了数据就核对来源、口径和截止时间，运行本地报告；只有问题没有当前数据时，给缺口清单和情景框架。

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

报告同时输出 HTML、Markdown、JSON，冻结输入并提供可重跑配置。保留陈旧数据、证据冲突、样本缺失和未就绪指标；不把工具生成的报告视为人工核验结论。若讨论当日计划，区分观察条件、确认条件、失效条件和下次检查事件；复盘追加记录，不改写原计划。

## 单项离线计算

在仓库根目录运行；其他目录运行时将脚本、输入和输出替换成对应绝对路径。

```bash
python scripts/analyze_structure.py --csv examples/bars.csv --instrument EC_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00+00:00 --data-kind synthetic --support 100 --out output/structure.json
```

附带数据全部为构造样例。更换真实数据后使用 `--data-kind imported_observations` 并填写来源，不因为标签变化而宣称实测收益。未提供当前数据时可以给研究框架和明确缺口，不能编造即时行情。

保留当时可知信息；未公布数据、未来 K 线不能进入历史结论。工具只做描述计算，不提供已验证的胜率、收益或自动执行。

<!-- futures-desk-v3 -->
## Versioned bilingual desk / 双语研究工作台

For historical vintages, explicit daily sessions, comparable basis/spreads, seasonal evidence and fee/margin stress, read [the input contract](docs/desk-data-contract.md) and [the chain playbook](references/research-playbook.md).

```bash
python scripts/run_desk.py run --config examples/desk-demo/ec-shipping/config.json --out output --lang en
```

Both English and Chinese reports are generated. Read [the capacity model](docs/desk-risk-model.md) when sizing or stress is requested. Use `verify` and `replay` subcommands for the desk. The existing `run_research.py` command remains supported; new legacy bundles now hash every artifact and verify snapshots on reload. For old committed demonstrations, only the previously recorded input hashes can be verified with `scripts/legacy_bundle_integrity.py`; their original files remain unchanged.
