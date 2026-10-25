# 欧线 EC 研究 Skill

把航线事件、有效运力、船司报价与已公布结算运价指数放到一条时间轴，判断叙事是否真正传导到 EC 合约。

作者：[Serennity007](https://github.com/Serennity007) · [四类研究导航](https://github.com/Serennity007/market-research-skills) · [完整 Skill](SKILL.md) · MIT

## 能做什么

1. 确认 EC 合约月，区分期价、SCFIS 欧洲航线、SCFI 欧洲航线与船司报价；不要交叉替代。
2. 拆解事件如何影响上海—欧洲航线：红海/苏伊士通行、绕航时间、有效运力、班次和货量；原油运输航路不是集运欧线的直接替代。
3. 比较已公布运价与期价时读取 `references/domain-data.md`，按 published_at 截断，而非按统计期末日期假设当时已经可见。
4. 同时观察合约月差和多周期结构，检查预期是否已被交易。最终结算按目标合约最新交易所规则另算，不能用最后一期指数直接代替。
5. 输出情景、失效条件和下一次运价/航线信息检查点；对事后回忆保留证据等级，不把高确信度写成确定收益。

这是可单独使用的研究 Skill：指令、参考、示例和计算脚本都在本仓库内，不依赖其他三个项目。离线脚本使用 Python 3.10+ 标准库，无 API Key。

## 快速体验

```bash
git clone https://github.com/Serennity007/ec-shipping-research-skill.git
cd ec-shipping-research-skill
python scripts/analyze_structure.py --csv examples/bars.csv --instrument EC_SYNTHETIC --timeframe H4 --as-of 2024-01-09T00:00:00+00:00 --data-kind synthetic --support 100 --out output/structure.json
python scripts/compare_settlement.py --futures examples/futures.csv --index examples/settlement-index.csv --contract EC2404 --as-of 2024-01-09T08:00:00+08:00 --data-kind synthetic --out output/ec.json
python -m unittest discover -s tests -v
```

输出保存在 `output/`。重复运行请换文件名；脚本拒绝覆盖输入和已有结果。

先看 [输入样例](examples/bars.csv)、[结构计算输出](examples/structure-output.json) 和 [数据约定](references/data-contract.md)。K 线例子是 2024 年时间标签的构造数据，统一使用虚构标的名；归档时间不代表 2024 年曾经做过此分析。末端收复支撑但均线方向仍有分歧，示范如何保留冲突证据。

[领域工具数据规范](references/domain-data.md) · [领域计算输出](examples/domain-output.json)

## 作为 Skill 使用

把本仓库完整复制到使用工具支持的技能目录，保留文件夹名 `ec-shipping-research-skill`。例如 Codex 的用户技能目录为 `~/.codex/skills/ec-shipping-research-skill`；有图形界面或其他代理时按其技能目录约定安装。

```text
使用 $ec-shipping-research-skill，标的是……，截止时间是……，数据来自……。
请核查证据与时效，给出有条件的研究结论、失效条件及复盘检查点。
```

需要当前行情时，使用者提供带来源和时间的文件，或由其已授权的数据工具获取。此仓库不内置行情订阅、账户接入和自动下单。

## 证据与验证范围

计算测试覆盖时间截止、输入校验、指标/领域算术和命令行文件保护。`examples/` 全部是 **synthetic 模拟样例**，用于验证功能；没有宣称真实行情测试、纸面账户收益或实盘盈利。作者的历史观点与证据等级见 [方法说明](references/method.md)。

共同 K 线引擎从作者 [选股与量化技能合集](https://github.com/Serennity007/awesome-stock-quant-skills/tree/67156b0aa4860894a8cdbc66b797db535531fe59/my-skills/gold-cross-asset-research) 的已收盘数据分析器适配而来。各仓库随带自身代码与测试，互不需要联网导入。

[研究与复盘记录模板](references/report-template.md) · [官方来源](references/sources.md)

本地验证（2026-10-25）：**18 项测试通过**，Skill 入口通过结构校验。[从输出到研究结论的模拟记录](examples/research-note.md) 展示保留分歧和留空未知结果的写法。
