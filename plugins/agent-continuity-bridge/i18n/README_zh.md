# 智能体连续性桥接插件 — Agent Continuity Bridge 0.2.1

## 存在目的

ArquitecturaRepo 负责软件工程的权限、计划和验收。本可选插件提供与独立版本的外部智能体连续性控制器之间的隔离接口。它不是 AI 模型，也不是第二个项目负责人。可移植核心无需此插件即可运行。

## 目前可验证的功能

离线检查单独提供的 Codex Daily Control 3.1 ZIP：核对安全路径、文件清单、全部 SHA-256、版本及配置一致性；在现有项目中仅登记软件包摘要，并支持重新核验与安全移除。不会分发私人配置、凭据、Goal 标识或对话数据。

## 依赖与连接

需要 Python 3.10 或更高版本、已安装 .agentic-sdlc 控制层的 ArquitecturaRepo 项目，以及单独获取的 3.1 ZIP。如需运行原生控制器，还需要 Windows、PowerShell 5.1、兼容的 Codex Desktop，以及单独配置的 Git、SQLite 和可选的 Drive/rclone。本桥接插件不会安装这些组件。

## 安全与限制

3.1 仍是尚未通过 Windows/Codex 实机验证的发布候选版本。原生关闭、Desktop 控制权移交、配额重启和远程交付在本插件中保持禁用／未验证。

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


安装到已有项目：`python install_into_project.py --project "PROJECT"`。CLI 位于 `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py`。执行 `--remove` 前请先取消控制器注册。不执行原生控制器操作。
