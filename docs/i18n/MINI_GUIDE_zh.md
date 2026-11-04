# ArquitecturaRepo — v1.4.0 迷你指南（简体中文）

本迷你指南用八个主题（00–07）简要介绍如何在自己的项目中使用 **v1.4.0**。它是面向 v1.4 的**简明实践指南**，并非旧版 v1.3 西班牙语长篇手册的完整翻译；历史手册仍保留在源代码仓库中。实际发布版本以 [v1.4.0 GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) 为准，v1.3.0 作为历史版本继续提供。

本迷你指南是 v1.4.0 发布**之后**才添加到 `main` 的，因此原有 v1.4.0 ZIP 和容器镜像**不包含此指南**。将来如需离线打包，必须使用另一个版本号发布。

## 00 · 先了解用途与边界

ArquitecturaRepo 是一套**存放在项目仓库中的开发控制层**：组织需求、决策、职责、当前状态、工程活动、证据和中断恢复。它不是自动生成应用的服务，也不是 Codex 编程模型的替代品。

- CLIENT：决定产品目标，批准敏感操作、发布与人工体验验收。
- I1：确有需要时协调多个项目；I2 Planner：规划能力、依赖与验收条件。
- I3 Controller：在已获批准的活动范围内开发、测试、集成、修复与恢复。
- I4：可选的专业人员或代理。**四类职责不代表必须运行四个代理**。

应用代码、数据库、凭据和对话可以完全保持私有。公共 starter 不需要获取这些内容。是否使用外部模型及其数据访问权限取决于另外的明确授权；安装不会自动授予权限。

## 01 · 安全安装

使用通过 CI 验证的 Python 3.12。下载 [v1.4.0 便携 ZIP](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip)，核对同时发布的 `.sha256`，解压后在**框架源码目录**打开终端。也可以检出不可变的 Git 标签 `v1.4.0`。

对于新项目，或虽有应用代码但**没有现存正式控制层**的项目，先选最小的 `SMALL`：

```bash
python "tools/scaffold_project.py" --target "../my-project" --profile SMALL --product-id MY_PROJECT --objective "Initial objective pending confirmation" --language zh --no-feedback-workflow
```

Windows PowerShell：

```powershell
python "tools\scaffold_project.py" --target "..\my-project" --profile "SMALL" --product-id "MY_PROJECT" --objective "Initial objective pending confirmation" --language "zh" --no-feedback-workflow
```

安装器会添加 `.agentic-sdlc/`，保留现有应用代码与工作流，拒绝覆盖已有的正式控制层。`--no-feedback-workflow` 只关闭定时执行，**不会禁用本地报告生成器**。如需完全禁用报告，在 `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json` 中设置 `enabled=false`。框架没有附带外部收集服务器。

然后进入**目标应用目录**运行：

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

PowerShell 中使用带引号、以 `\` 分隔的路径。初始出现 `HOLD / UNTRUSTED_CONTEXT` **是正常结果**：真实需求、代码基线和执行权限还未确认。如果项目已有 Product State、工程活动或 Controller，**不要覆盖安装**。应使用[只读的现有治理检查](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md)。目前没有通用的 v1.2/v1.3 原地自动升级。

## 02 · Planner 与项目接入

先调查真实代码、用户、数据、依赖、风险和安全限制，由 CLIENT 确认产品基线。I2 编写按**能力**划分的 charter，明确结果、边界、负责人、接口、验收标准和否定条件。不要把演示用的虚构 Product State 复制为正式状态，也不要认为安装成功就代表获得执行授权。

## 03 · 日常开发

以 Git、CURRENT 状态与可核验的证据为准，而不是仅依靠聊天记录。I3 在**同一个已授权工程活动**中管理实现、测试、调试、重试与中断恢复。普通错误不必新建活动。如果 Git、SQLite WAL、身份、执行授权或租约相互矛盾，应保持 `HOLD`。便携 CI 不等于对 Codex Desktop/Goals 原生操作或外部付费服务的认证。

## 04 · 提出修改需求

说明**可观察的结果**、背景、限制与验收方法。例如：“显示未缴纳的月费，保留历史收款记录，并使用已付款/逾期样例验证计算和界面”。I2 判断是否涉及重大战略改变，I3 负责已授权范围内的工程调整。

## 05 · 错误和恢复

- `UNTRUSTED_CONTEXT`：重新核对真实代码与需求，不得手动把状态改成通过。
- 缺少 `jsonschema`：安装目标项目的 `requirements-validation.txt`。
- `EXISTING_CONTROL_PRESERVED`：停止，改用只读检查；不能使用 `--force` 或删除旧状态。
- Git/SQLite WAL/租约信息冲突：核对证据前停止重大写入。
- 活动中断：保留日志、运行身份和产物，在**原有活动**中恢复。仅清理所有权和删除规则均已验证的文件。

公开 Issues 只应包含可复现的步骤与脱敏日志，不要公开密钥、私人路径、非公开项目名称、数据库内容或代理对话。

## 06 · 能力验收

分别检查单元测试、集成、DB/currentness、语义与泛化、真实运行、人类体验、正式发布等关卡。测试绿色或代理报告“完成”，都不等于 CLIENT 验收。将精确源码、输入、证据、负责人和结论保存到项目的权威记录。合成 CI 无法证明任意应用已达到生产级质量。

## 07 · 案例：会员俱乐部

1. CLIENT 要求会员登记、月费收取和欠费查询，并确认用户界面上的预期行为。
2. I2 检查真实数据库和权限，划定最小可用的端到端功能。
3. I3 实现登记 → 月费 → 欠费列表，并测试持久化与恢复。
4. 计费错误在**同一个**活动中修复，不为普通错误创建新活动。
5. CLIENT 实际试用后验收或退回问题，保留证据和当前决定。

## 参考和限制

[简明指南](README_zh.md) · [FAQ](FAQ_zh.md) · [主 README](../../README.md) · [v1.4 的实际支持范围](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md)。

本手册不构成生产安全认证、独立用户体验验收、原生主机集成保证，也不能证明其实际表现优于直接使用 Codex。MIT 许可不会自动覆盖第三方材料。
