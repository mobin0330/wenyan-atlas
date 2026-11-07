# 进度入口修复 · 2026-11-05

问题：给用户的报告URL是受保护API，未登录直接打开只得到401提示。

修复：新增登录后站内 `#work-status`，通过公共 SharedEmailAuth.request 读取 `/api/work-status`。首页“先看使用手册”可进入，手册顶部有“查看教材整理进度”，桌面导航名为“使用手册与整理进度”。当前状态明确为15:19的静态快照、未运行后台教材整理、网站运行中；不冒充实时监控。公共登录与安全策略原样保留。

验证：真实SDK+隔离假网关下，未登录首页显示公共登录页、进度API401；390/1440浏览器完成首页→手册→进度→返回，6行工作底账正常，未见JS错误或整页横溢。截图与记录在 `.impeccable/review/progress-entry/` 与 `docs/progress-entry-check.json`。未发送真实邮件。

公网主页200且为公共登录页，新版app.js可读，进度API未登录401，邮件服务available=true、SDK1.1.0；结果 `docs/progress-entry-public.json`。专用服务已重载。独立finish review为ship，仅覆盖该入口；设计检查确认未改token与CSS。未声称通过实际生产邮箱登录或核准教材数值。

回滚备份：`.local/backups/progress-entry/`。本轮未修改公共SDK、凭据或学习记录。后续任务状态更新时，应同步 `data/work-status.json`、`docs/WORK-STATUS.md` 和手册中的时间说明。
