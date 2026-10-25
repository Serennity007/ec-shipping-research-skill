# EC 与已公布指数的比较

`scripts/compare_settlement.py` 需要两个 CSV。

期货：`contract,contract_month,price,quote_time,unit`。例如 `EC2404,2024-04,1200,2024-01-09T08:00:00+08:00,index_points`。同一合约可有多条不同时间报价，选择截止时刻最近一条；代码月份必须一致。价格为正。

指数：`index_name,period_end,published_at,value`。名称只接受文件约定 `SCFIS_EUROPE`；period_end 不晚于 published_at，以 published_at 过滤未来数据。所有时间必须带时区。表中只有值而没有公布时刻，不足以进行历史时点比较。

输出 `futures_minus_last_published_index` 及相对差值，保留统计期、公布时间、报价时间和各自年龄。它不是同步可交易基差，也不是最终结算预测。若 `index_published_after_quote=true`，这期指数在该报价时尚不可见，应使用更近报价或更早的截止时刻重新分析。

示例全为构造：截止 2024-01-09 08:00 +08，期价1200、已公布指数1000，差200/20%；1月10日才公布的1400及未来期价1600都被排除。公布日和合约只是功能样例，不模拟真实官方发布日期和真实行情。
