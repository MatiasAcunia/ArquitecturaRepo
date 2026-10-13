# Agentic SDLC FAQ (zh)

[ZH guide](README_zh.md) · [Main README](../../README.md)

### 1. Agentic SDLC 是什么？

一个用于组织智能体软件开发的可复用架构，并非能够自动生成任意应用的软件。

### 2. 如何开始？

先检查或 fork 仓库，进行只读发现，选择最小配置并按安装提示操作。新的 scaffold 以 HOLD 状态启动。

### 3. 能用于已有仓库吗？

可以。首先核实真实代码、数据及权限。不要随意覆盖应用文件，也不要把示例状态当作真实状态。

### 4. 四类职责需要四个模型吗？

不需要。CLIENT、Planner I2、Campaign Lead I3 和 I4 专家是职责边界，并非固定进程数量。

### 5. 谁批准敏感操作？

产品目标、主观验收、发布、费用及敏感数据的授权仍由 CLIENT 控制。I3 不得擅自推断许可。

### 6. Goals 和 Codex Desktop 已自动集成了吗？

尚未。v1.2 有可选 Goal/Plan 检查代码，但每次调用的真实主机集成仍需物理测试。

### 7. Gemini 默认启用或收费吗？

不会。只有经过明确启用以及凭据、配额、隐私检查后才允许使用 I4；默认不上传私有代码。

### 8. 它会重启或删除我的 Codex 会话吗？

starter 本身不会。Codex Daily Control 2.0.2 是独立参考；v1.2 的主机适配器尚未完成验收。

### 9. 默认启用什么反馈？

每月在项目自己的 GitHub Actions artifacts 中保存一次少量元数据，帮助改进 starter，但不会自动向外部发送。

### 10. 哪些信息不会收集？

代码、对话、项目或仓库名称、路径、密钥、个人标识符、需求正文、SHA 和任意自由文本。

### 11. 如何切换语言或关闭反馈？

使用 --language auto|en|es|pt|fr|de|it|ja|zh。关闭反馈可设置 enabled=false 或使用 --no-feedback-workflow。GitHub 的 README 是静态的。

### 12. 哪些功能通过测试，如何报告问题？

1.1 为稳定版；1.2 仍需独立真实环境验证。请在 GitHub Issue 中提交可复现步骤和脱敏日志。原创材料采用 MIT 许可证。

---

[ZH guide](README_zh.md)
