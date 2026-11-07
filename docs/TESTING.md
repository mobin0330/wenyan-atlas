# 测试与交付验收

日期：2026-11-04。测试结论只覆盖本轮小样例产品试验，不能代替教材审核、儿童试用、真实设备或公网部署验收。

## 数据和接口

```sh
python3.12 -m unittest discover -s tests -v
node --check static/app.js
python3.12 manage.py check
```

29 项通过（20 领域 + 9 HTTP）。覆盖：迁移重复运行、导入去重、事务回滚、偏移与外键一致、同词多义、审核层层拦截、五项范围与真实年级过滤、scope 切换保留记录、图节点上限、题目不预泄答案、提示与首答记录、浏览不计掌握、审批审计、拒绝覆盖、SQLite 备份恢复、接口/路径白名单、限流、预览不能打开私库、真实 SDK 错误 Host/未登录拒绝。

范围筛选使用隔离测试库里的明确 TEST ONLY 元数据验证；没有把测试年级写入正式数据。

## 浏览器端

使用本机已存在的 Playwright 测试环境，无新增运行依赖：

```sh
/Users/doudou_files/claude/wuhanmetro/venv/bin/python tests/browser_check.py
```

需先启动本地 9381 预览。27 项检查通过，见 browser-results.json。覆盖 1440 桌面、390 手机、768 平板；默认范围/至少一项/刷新恢复、图缩放、用法选择、原文精确定位与返回、文字替代、搜索/无结果、提示与答题反馈、学习证据、正式空目录、18 个待核验册位、深色主题、响应式无横向溢出。JavaScript/CSP 错误 0。

截图在 `.impeccable/review/`；深色截图等待主题过渡结束后采集，避免把切换中间帧当作最终配色。独立设计复核及最终修复结论另见该目录 finish-review.md。

## 公共认证固定验收

遵循 security-service/QUICKSTART.md：

- `verify_sdk.py`：1.0.0 / 14 个 runtime 文件校验通过。
- `python3.12 -m unittest test_shared_sdk test_security -v`：17 项通过。
- `../speech-service/.venv/bin/python test_http.py`：PASS，模拟投递，没有发送真实邮件。
- AgentFlow `PYTHONPATH=src python3.12 -m unittest tests.console.test_console -v`：18 项通过。
- AgentFlow `node --test tests/console/test_web.cjs`：5 项通过。

公共模块未修改，没有为此项目复制登录资源。成功路径在公共 SDK 的隔离测试中验证；新项目未配置真实域名/邮件凭据，不能宣称真实登录已验收。

## 基础性能样本

同机 loopback、暖服务、单客户端连续 20 次图谱请求，3 篇/15 实例数据：中位 2.81 ms，P95 5.46 ms，图谱响应 3451 字节，服务 RSS 约 35.5 MiB。浏览器首屏的本机样例加载量级约 80 ms。详见 performance-results.json / browser-results.json。

这些结果不是压力测试，不能外推大数据/远程/真实手机网络。bootstrap 尚未做大语料分页，正式扩容前必须完成。

## 验收差距

已完成可运行/可测试的学习关系试验。尚未满足正式阶段 0 退出条件：18 册版权页和目录、篇目总量、授权情况、人工学科审核。已发布教材篇目 0，覆盖率不可计算。

尚未满足完整阶段 1：真实教材目录与独立学习者记录、写入式审核后台、经过核验的正式教材题库、全量数据分页、真实 iOS Safari/Android 设备与辅助技术验收、ASGI 公网生产部署。

当前不能声称 AI 质量达标，因为没有启用 AI；不能声称记忆效果改善，因为没有进行学习实验；不能声称完整 PWA，因为无离线服务工作线程。

## 0.2追加验收

新内容46条记录/44可见单元、46用法、130实例、121候选题。领域/HTTP/ASGI合计33项通过；焦点专测增加到7项，包括同地图切换用法保留焦点。真实公网首页200，未登录学习API401。详见DELIVERY-0.2.md。旧29项、三篇数据和未部署描述为0.1测试基线。
