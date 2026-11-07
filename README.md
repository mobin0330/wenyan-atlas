# 文言星图

面向小学和上海五四学制初中学生的文言文学习工具。学生可以从课文原句出发，比较同一个词在不同篇目中的用法，再做辨析和自主背诵。

当前交付是 **0.3 可交互学习原型**。学生教材目录包含六上 1 篇、七上 7 篇。《曹冲称象》已登记在研究清单，仍待接入学生库。18 册教材入口与 52 个研究观察条目用于后续内容建设。已确认采用各册最新正式出版修订版。实际进度见[产品评审](docs/PRODUCT-REALITY-REVIEW.md)。

## 本地启动

使用 Python 3.12，从仓库根目录启动三篇样例的本机预览。

```sh
python3.12 server.py --port 9381
```

浏览器打开 http://127.0.0.1:9381。预览自动生成临时样例库。按 Ctrl-C 退出。图谱、原文和候选题可直接试用。私有试用版使用另外的 ASGI 入口和共享安全模块，详见[运行与部署](docs/OPERATIONS.md)。

```sh
python3.12 -m unittest discover -s tests -p test_atlas.py -v
```

## 交接资料

| 文档 | 内容 |
|---|---|
| [PRD](docs/PRD.md) | 产品目标、需求、分阶段验收 |
| [接手指南](docs/HANDOFF.md) | 当前实现、关键入口、优先任务 |
| [运行与部署](docs/OPERATIONS.md) | 本地测试、私有部署、备份恢复 |
| [实际进度评审](docs/PRODUCT-REALITY-REVIEW.md) | 学生端实际覆盖、技术与内容缺口 |
| [教材与词义溯源](docs/LEXICAL-PROVENANCE.md) | 内容编辑规则 |
| [教材研究报告](docs/TEXTBOOK-RESEARCH.md) | 18 册来源、版本差异及篇目观察 |
| [资料权利说明](data/ATTRIBUTION.md) | 古籍、上游许可证及候选内容 |
| [使用手册](docs/STUDENT-MANUAL.md) | 阅读、查词、图谱、背诵 |
| [架构](docs/ARCHITECTURE.md) · [设计](DESIGN.md) | 工程结构与设计规则 |

`docs/DELIVERY-*`、`docs/TESTING.md` 保存历史批次记录。当前状态和部署步骤以上表对应文档为准。
