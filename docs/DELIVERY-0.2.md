# 0.2 试用交付 · 2026-11-05

用户明确授权扩充小学高年级及初中四年内容并部署 wyw.ericmo.top，无需追加常规批准。

## 当前线上状态

- https://wyw.ericmo.top → mac-tunnel → 127.0.0.1:9382 → Uvicorn ASGI。
- 独立用户 LaunchAgent：~/Library/LaunchAgents/top.ericmo.wenyan-atlas.plist。RunAtLoad/KeepAlive 仅用于这个新项目的持续访问。
- 直接导入 shared_email_auth.asgi.EmailAuthMiddleware。专用客户端由官方 register_client.py 注册；未发送邮件。
- 公网首页200、样式200、脚本200、未登录学习API401；HTTP客户端默认Python UA会被既有CF规则1010拦截，正常浏览器UA可用，没有关闭CF安全策略。
- 现有17条Tunnel路由保留，仅新增wyw的精确hostname和专用CNAME。备份位于.local/deploy-backup。未修改现有项目源码或认证模块。

## 内容与功能

数据46条篇目记录，其中两个历史片段不在试用目录；用户可见44单元。覆盖五个试用范围，各单元均有字词定位。共有46个用法、130个语境实例、121道候选题。原始篇目中的不同用法已按语义合并，避免同一种用法按文章各建一份。

来源包括古文观止MIT古代正文、孟子/论语古文原文CC0候选及自行整理的古籍学习选文；未导入现代教材译注、插画或现代翻译训练集。来源说明与本地快照摘要保留。第三方教材链接索引只用于定位官方站点，未拿它代替逐册官方目录核验；部分官方电子教材路径返回403，未绕过。

当前年级是阅读推荐，非教材归属结论。全部试用知识保留pending并提示复核，不自动将数据批准为教材标准。“古文全文/完整学习选文可读”与“对应现行教材已核验”必须分别验收。

## 测试

- 33项领域/HTTP/ASGI测试通过，含真实SDK的未登录/错误来源拒绝、五个范围均有内容、试用答题服务端记录、正式模式不泄漏待审内容。
- 原版35项浏览器检查与7项焦点/主题检查通过；界面复核F1–F4已解决，记录在.impeccable/review/finish-review.md。
- 扩充版隔离认证浏览器测试使用仅存在于loopback测试进程的FakeGateway；不会替换线上门禁。结果见trial-browser-results.json。
- 真实公网未登录边界见public-verification.json。未自动触发真实OTP，不冒称用户真实登录已验收。

## 数据库与回滚

线上使用.local/trial-v4.sqlite。旧trial.sqlite/trial-v3.sqlite以及deploy-backup保留；迁移复制已有preferences与learning_records。试验生成器需要先expand_corpus.py再annotate_trial.py，正式导入新库校验后再切换，不原地覆盖已审核内容。

备份使用manage.py --db .local/trial-v4.sqlite backup <新文件>。回滚时先备份当前学习记录，改asgi_app.py数据库路径到旧库，并kickstart本项目；不能忽略新旧题目/用法版本差异而盲目回滚。CF入口可保留，无需改其他路由。

## 仍未完成的验收

这轮交付扩大了实际测试规模，并非全量正式教材交付。逐册目录、人审、整句解释、独立学生档案、严格迁移测验与学习效果实验仍未完成。当前可以评审阅读→对照→辨析→记录的流程，不能宣称已经证明学习有效或现行教材覆盖完整。
