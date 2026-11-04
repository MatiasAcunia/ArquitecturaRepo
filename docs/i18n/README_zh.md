# Agentic SDLC — 入门指南

[v1.4 完整用户手册（八章）](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/zh/README.md) · [完整 PDF](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/output/pdf/ArquitecturaRepo_Complete_Manual_v1.4_ZH.pdf) · [v1.4 迷你指南](MINI_GUIDE_zh.md) · [FAQ](FAQ_zh.md)

现在已有[简体中文 v1.4 完整八章手册](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/zh/README.md)和独立 PDF。[旧西班牙语 v1.3 手册](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md)仍作为历史原版保留。本页面只是一份简要入门；当前操作命令请查阅 [v1.4 安装指南](../46_V1_4_PUBLIC_START_AND_SUPPORT.md)。完整版在 v1.4.0 发行之后添加到 main，不包含在原始发行 ZIP 中。

一种以代码仓库为中心、可复用的智能体软件开发架构，包含职责分工、持久状态、规划、恢复和验证机制。它不能自动完成任意软件，也不能替代产品负责人的决策。

## 在项目中安装

请选择满足需要的最小配置。先进行只读检查，不要把示例 Product State 当作真实项目状态复制。新建环境从 HOLD / UNTRUSTED_CONTEXT 开始。

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## 职责与权限

CLIENT 负责产品决策和敏感操作授权；I2 负责战略和验收；I3 在获批范围内实施、测试和恢复；I4 可选，用于有限咨询和独立审查。四类职责不意味着必须运行四个进程。

## 隐私与每月反馈

新建项目默认每月在本项目的 GitHub Actions artifacts 中生成一份最小元数据报告，用于改进 starter 结构和整理问题。报告不会自动发送给维护者，不包含代码、对话、项目名称、路径、标识符或密钥。

要彻底关闭所有报告，请在 .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json 中设置 enabled=false。删除 .github/workflows/agentic-sdlc-feedback.yml 或安装时使用 --no-feedback-workflow 只关闭定时执行，不会删除本地生成器。

## 安全与版本

**v1.4.0 已正式发布**：[带版本号的 GitHub Release 提供便携式 ZIP 和 SHA-256 校验文件](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)。安装前请核对下载文件；持续变化的 `main` 分支可能包含发布后的文档更新，不等同于发布文件。此前发布的 v1.3.0 仍可使用。新项目或尚未建立治理状态的项目请参考 [v1.4 首次安装指南](../46_V1_4_PUBLIC_START_AND_SUPPORT.md)；已有治理状态的项目须先进行 [只读检查](../32_EXISTING_GOVERNED_ATTACHMENT.md)，不能自动覆盖原有状态。便携式 CI 不能单独证明 Codex Desktop 原生执行、外部 AI 服务或真实外部操作已经通过验收。

## 语言

安装工具自动检测操作系统语言，也支持 --language zh。文档可离线阅读。GitHub 的主 README 是静态页面，请通过语言链接选择。

[v1.4 完整手册](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/v1.4/zh/README.md) · [v1.4 迷你指南](MINI_GUIDE_zh.md) · [FAQ](FAQ_zh.md) · [GitHub README](../../README.md)
