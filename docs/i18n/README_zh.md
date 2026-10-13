# Agentic SDLC — 入门指南

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

关闭方法：在 .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json 中设置 enabled=false，删除 .github/workflows/agentic-sdlc-feedback.yml，或安装时加 --no-feedback-workflow。

## 安全与版本

稳定版本为 1.1.0。1.2 仍处于候选阶段：Codex Desktop Goal、Gemini、外部操作及多项目任务需要真实环境验证。CI 通过不等于产品验收。

## 语言

安装工具自动检测操作系统语言，也支持 --language zh。文档可离线阅读。GitHub 的主 README 是静态页面，请通过语言链接选择。

[FAQ](FAQ_zh.md) · [GitHub README](../../README.md)
