# 研究工作台与高级数据

## 一个命令生成一份完整研究快照

```bash
python scripts/run_research.py --config examples/workbench.json --out output
```

会创建新的 `output/run-…/`，重复运行保留之前的报告。可以从其他目录运行：把脚本、配置和输出参数换成相应绝对路径，CSV 路径仍相对配置文件解析。

| 文件 | 内容 |
|---|---|
| REPORT.html | 可直接打开的深色研究面板，含指标、价格折线、分歧、缺口、下次检查和可展开明细；无外部资源 |
| REPORT.md | 便于笔记、版本管理和分享的文字报告 |
| bundle.json | 结构计算、领域分析、高级分析、来源声明、输入哈希和生成时间 |
| inputs/ | 本次实际计算使用的 CSV 原始字节快照 |
| config.snapshot.json | 路径已改为 inputs/ 的重跑配置，摆脱原始输入位置 |
| COMPLETE.json | 只有所有输出写完才产生的完成标记；缺少时视为未完成导出 |

查看已运行的 [模拟报告](../examples/workbench/REPORT.md)、[完整 JSON](../examples/workbench/bundle.json)；下载 [HTML 文件](../examples/workbench/REPORT.html) 后在浏览器打开。GitHub 文件页展示源码，需要下载才能查看本地面板。

重跑一份冻结报告：

```bash
python scripts/run_research.py --config examples/workbench/config.snapshot.json --out output
```

## 换成自己的数据

复制 examples/workbench.json，修改 instrument、as_of、files 和 options，保持 skill 名及必需输入角色。`schema_version=1`；`data_kind` 使用 `imported_observations`；`max_bar_age_hours` 是使用者选择的陈旧阈值，周末和停市仍需按目标市场日历解释。面板工具的 `max_panel_age_days` 用日历日判断，不冒充交易日检查。

导入模式必须为每个文件角色填写来源名称和取数时间，可选真实来源链接。例如：

```json
"sources": {
  "bars": {
    "name": "实际使用的数据提供者与具体代码/合约、单位、周期",
    "retrieved_at": "2026-10-25T10:00:00+08:00",
    "url": "https://实际来源页面"
  }
}
```

上面是字段示意，使用时填实际信息；其余输入角色同样填写。历史研究还需保存当时可知版本与发布时间，下载时间不能代替公布时间。名称、哈希和来源链接记录来源声明，工具不认证它们为真。

旧的单项命令仍可用，新工作台复用相同计算函数。新的报告是结构化研究快照，不是仓位指令、收益回测或预测评分。

## 用在三种研究任务中

盘前计划：给明确数据截止时刻，记录当前背景、待确认条件、失效条件和下一次复查事件。尚未发生的观察结果留空。

事件研判：拆开事件事实、传导假设和价格反应。用同一截止时刻检查已公布数据，报告不能用后来的信息补强当时判断。

盘后复盘：从旧报告的冻结配置重跑以复核原计算，再用新输入产生新报告，逐项说明原假设是否被支持、反证或仍待观察。保留旧报告，不能用新结论覆盖旧计划。

## 欧线：绕航与需求的敏感性分析

`scripts/analyze_route_scenarios.py` 读取 `scenario,known_at,base_cycle_days,extra_cycle_days,affected_share,demand_change_fraction`。

| 字段 | 含义 |
|---|---|
| scenario | 唯一情景名称 |
| known_at | 该情景的输入假设何时已经形成，带时区；不是事件发生时间的自动证明 |
| base_cycle_days | 原完整往返周转天数，大于零 |
| extra_cycle_days | 额外完整往返天数，非负；单程估计先转换，不能重复加倍 |
| affected_share | 受影响部分占基准运力的比例，0–1，不是新闻样本中船舶的占比 |
| demand_change_fraction | 相对基准货量变化，−0.2表示减少20%，必须大于−1 |

固定船队、相同基准周转和其他条件不变时：

```text
运力比例 = (1−受影响占比) + 受影响占比 × 原周转天数 / (原周转天数+额外天数)
相对需求压力 = (1+需求变化) / 运力比例
```

例：原周期60天、额外20天、影响50%基准运力，估算运力比例87.5%，损失12.5%；货量不变时相对压力约1.1429。若货量同时下降20%，相对压力约0.9143，低于基准。**压力比不是装载率，更不是运价或 EC 涨幅。** 模型没有新船、调配、空班、利用率反应与价格弹性。

```bash
python scripts/analyze_route_scenarios.py --csv examples/route-scenarios.csv --as-of 2024-01-09T15:00:00+08:00 --data-kind synthetic --out output/route-pressure.json
```

三套附带情景均是人为假设，不是实际航路或运力损失统计。用 [UNCTAD 海运报告](https://unctad.org/system/files/official-document/rmt2025_en.pdf) 等来源核查传导机制后，还需获取具体时段的真实船队和货量证据。与现有 SCFIS 比较结果一起阅读，不能省略公布时滞和合约月份。
