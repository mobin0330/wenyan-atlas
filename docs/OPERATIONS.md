# 运行、内容维护与回滚

## 本地预览

从仓库根目录运行 `python3.12 server.py --port 9381`，浏览器访问 http://127.0.0.1:9381。预览绑定回环地址，每次使用临时三篇样例库。按 Ctrl-C 退出。核心领域测试可独立运行。

```sh
python3.12 -m unittest discover -s tests -p test_atlas.py -v
```

## 私有试用与完整测试

Python 3.12 依赖见 `requirements.lock`。从维护者取得共享 `security-service` 源码，先按其 `QUICKSTART.md` 校验 SDK 并完成站点注册。仓库交接时使用共享模块 1.2.2 做回归。通过工作区布局或 `PYTHONPATH` 导入 SDK。

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
export SECURITY_SERVICE_DIR='/absolute/path/to/security-service'
export PYTHONPATH="$SECURITY_SERVICE_DIR"
.venv/bin/python "$SECURITY_SERVICE_DIR/verify_sdk.py"
.venv/bin/python -m unittest discover -s tests -v
```

浏览器回归需要 Playwright 与 Chromium。运行 `tests/browser_03.py` 时用含项目根目录及共享 SDK 的 Python 搜索路径。该脚本使用隔离库和模拟网关，演练阅读、教材溯源和背诵记录。

私有试用库可从仓库数据重建。

```sh
mkdir -p .local
.venv/bin/python manage.py --db .local/trial-v4.sqlite import data/trial.json
.venv/bin/python manage.py --db .local/trial-v4.sqlite import data/contextual-gu.json
.venv/bin/python manage.py --db .local/trial-v4.sqlite check
```

`asgi_app.py` 的 `GateConfig` 保存线上域名及凭据文件路径。换域名部署时按共享 SDK 要求配置目标 HTTPS origin 和新注册的服务端凭据。当前配置使用 `.local/security-client.json`。认证错误应由共享 SDK 拒绝请求。

```sh
.venv/bin/python -m uvicorn asgi_app:app --host 127.0.0.1 --port 9382 --no-proxy-headers
```

Mac mini 现有入口为 https://wyw.ericmo.top/。Cloudflare Tunnel 转发至回环端口 9382。用户级 LaunchAgent 标签为 `top.ericmo.wenyan-atlas`，登录后启动。Home 项目列表配置在独立的 `home-portal` 项目内。更新时只重载本项目。

```sh
launchctl print "gui/$(id -u)/top.ericmo.wenyan-atlas"
launchctl kickstart -k "gui/$(id -u)/top.ericmo.wenyan-atlas"
```

## 内容维护和恢复

`manage.py queue` 导出待审核内容。通过 `manage.py review` 录入真实审核者与证据。编辑以新版本保留旧记录，涉及教材版次、归属、原文、义项、实例和题目的状态分别审核。导入流程按数据摘要去重，冲突须处理后重试。

```sh
.venv/bin/python manage.py --db .local/trial-v4.sqlite backup /absolute/path/new-backup.sqlite
```

升级前先备份数据库。恢复时将备份复制到新路径，校验完整性和学习记录后再切换服务，保留原库以便回退。数据库迁移文件按编号追加。安全模块统一在共享项目维护。
