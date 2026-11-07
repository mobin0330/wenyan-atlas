# 实施方案与决策记录

## 运行结构

浏览器原生 ES modules/CSS/SVG → 同源业务 API → Atlas 领域模块 → SQLite。

Python 3.12 的标准库即可运行样例，不需要 Node 构建、不安装模型、不新增微服务。私有模式直接导入工作区 shared_email_auth.http.EmailHTTPMixin 与 EmailGate，前端调用真实 `/auth/http.js`。没有复制登录页、Cookie、来源验证或认证接口。SDK 版本检查为 1.0.0。

SQLite 适合此阶段低并发与本机持久化；事务、外键、约束保护导入。官方 [sqlite3 文档](https://docs.python.org/3.12/library/sqlite3.html)提供在线 backup 方法，本项目采用该方法避免只拷贝 WAL 主文件造成不完整备份。

标准库 HTTP 是本地试验载体。Python 官方[明确不建议将 http.server 用作生产服务器](https://docs.python.org/3.12/library/http.server.html)。因此本轮不把它暴露为公开生产服务、不建立 Tunnel、不安装自启动。正式上线前迁移传输层到 ASGI/FastAPI + 成熟 server，直接复用公共 ASGI 认证适配器；Atlas 领域和 SQLite 结构保持独立。

## 为什么偏离参考技术栈

- 目标首先是学习流程与数据可靠性，不是大型前端工程。原生界面足以承担七个小页面，零前端运行时依赖。
- 现有认证唯一标准是 Python SDK；使用 Python 服务能直接接入，避免在 Next.js 中复制认证逻辑。
- 关系数据已存在结构化表，局部 SVG 不需要额外图库。没有使用全库物理布局；“词→用法→原句”的方向是有语义的。
- 暂不接 AI Provider，因为没有已审核检索库时接模型不能增加知识可靠性。候选数据生成与发布必须隔离。

## 表与约束

- sources：URL、版本、权利说明、整理方式。
- textbook_editions / volumes / memberships：学制、版次、使用学年、真实年级、上下册、单元、分类、页码与归属证据。
- works / sentences：篇目、顺序、显示文本、底本文字、候选解释、审核状态。
- lexemes / senses / occurrences：字词、用法、读音/词类、本句位置和解释。
- questions：候选选项、答案、依据、提示、版本、审核状态。获取题目不返回答案；提交后由服务端判断。
- content_reviews / imports / schema_migrations：审核审计、导入去重、迁移版本。
- learning_records：类型 read/discrimination/recitation/dictation；题目、义项、篇目、提示、答对与时间独立保存。
- preferences：学习范围。
- coverage_slots：18 个目标核验槽位，不能当作已确认教材。

首版用 typed relational tables 替代全能 knowledge_nodes/edges；图的边实时由已审核外键投影，减少双写漂移。尚未建人物事件、通假专表、媒体表、知识追踪模型；遇到真实数据再加迁移。

## API 与隔离

GET /api/bootstrap?mode=sample|published&scopes=小学,六年级
GET /api/graph?lexeme=zhi&sense=zhi-of
GET /api/records
POST /api/attempt {question_id,choice,hinted}
POST /api/preferences {scopes}
POST /api/read {work_id}
GET /api/health

图最多 1 词 + 8 用法 + 12 原文实例，不一次画全库；前端默认折叠非选中例句。当前 bootstrap 面向小样例会载入当前语料，尚不是大数据分页 API。扩至数百篇前改成目录分页 + 单篇接口 + FTS5 检索，不能以目前小样例性能推断大规模性能。

公开样例预览只绑定 127.0.0.1，每次启动用独立临时库，不能 --db 指向私有库；只返回可公开的原典候选，尝试记录在浏览器。私有模式缺少 HTTPS origin/凭据立即失败；所有 /api/ 由真实 SDK 拦截；无凭据不回退预览。静态资源采用固定白名单，不能读项目或数据库文件。业务请求限流 240 次/分钟/进程，适合本机试验，不宣称分布式生产限流。

首版私有 profile 固定 household，这表示一个受门禁保护的家庭空间，**不是多用户授权模型**。多个孩子使用前应增加学习者选择、隔离、导出/删除，不把门禁会话当学生身份。

## 可解释的学习状态

浏览只记已读。答题按题目/日首次保存，重做可练习但不能刷高证据。提示答对不是独立掌握。跨两日、两篇、三道不同题且最近三次独立答对，才显示“已有迁移证据”；其余为尚未练习/初步理解/借助提示完成/待巩固。按最新证据建议 1/3/7 天复习，到期覆盖显示待复习。这是产品假设，非科学定标。

时间当前存 UTC，日去重以 UTC 日期；中国本地午夜附近可能与日历感知不同。正式版应配置学习者时区再扩展，不在本轮伪称完整个性化复习系统。当前每种用法的题目还很少，很多状态门槛自然不会达到，这是诚实行为。

## 分阶段任务与退出条件

阶段 0（已做技术试验，内容关口未关闭）：来源调查、样例 JSON、模式、去重与审核管道。退出：取得至少一组目标版教材归属和人审释义，能复核每条记录。

阶段 1a（本轮）：可运行局部地图、原文定位、五项范围、搜索、辨析、浏览器积累、正式发布隔离、测试与文档。先供产品评审。

阶段 1b：合格编辑批准代表性篇目；真实教材选择与目录；审核写入界面和角色授权；独立学生档案；分页检索；实际 iOS/Android 测试；ASGI 部署与真实门禁验收。退出：学生能在真实目标教材中完成“读→比→练→复习”。

阶段 2：内容库优先扩充；盲评 AI 候选准确率后引入受约束抽取和提示；非叙事文章用论证/空间结构，不强制故事卡；分段背诵可先做确定性隐藏。

阶段 3：独立评估 ASR/OCR 的不确定性、人改结果与音图数据保留；多端记录、离线包与撤回；效果验证达标后再考虑视频。
