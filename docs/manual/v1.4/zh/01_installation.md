# 01 — 安装和初始配置

ArquitecturaRepo · v1.4 完整用户手册 · 简体中文

> 这一章介绍如何识别正确的发行物、在正确的应用仓库中创建控制层、选择合适配置，以及理解为什么初次安装后的 HOLD 状态是安全的。请以[官方 v1.4 安装说明](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)为实际操作的依据。

## 本章内容

1. 准备工具与权限
2. 区分 starter、fork 和应用
3. 安装前的只读检查
4. 六种配置的选择
5. 生成 .agentic-sdlc 控制层
6. 安装后的检查
7. 已有治理状态的项目
8. 常见故障与安全处理

## 1. 准备开发环境

下列示例使用 Windows 和 PowerShell。需要能够访问 Git 仓库、运行 Python、在目标应用目录中拥有适当的文件权限。v1.4 的便携式持续集成测试使用 Python 3.12，但不要求某家专有云服务、商业 IDE 或特定 AI 模型。你可以选择自己的编辑器及合法的代码托管方式。

先查看当前终端环境：

    & "python" --version
    & "py" --version
    & "git" --version
    Get-Location

如果某个命令不存在，先检查安装位置、PATH 和终端会话。不要为了让检查通过而修改应用的 Product State。工具的可用性与产品需求的正确性是两回事。如果需要 Python 验证依赖，使用仓库提供的 requirements 文件安装，避免从不可信来源运行未知脚本。

使用编程代理之前，请确认其当前工作目录、可修改的文件范围、正在使用的 Git 分支以及是否有尚未提交的改动。即使代理已登录 GitHub，也不能据此推定它被授权操作生产数据库、创建付费资源或发布代码。相关授权要明确指向具体目标。

## 2. 三个容易混淆的位置

第一个位置是 ArquitecturaRepo 本身：里面存放公开协议、模板、配置、工具、测试和文档。第二个位置是你可能维护的 fork：它用于修改 starter 的通用规则，而不是应用产品。第三个位置是实际要开发的项目，例如 club-app：它拥有自己的代码、数据库以及安装后形成的 .agentic-sdlc/ 目录。

例如，一个清楚的本地目录安排是：

    C:\Proyectos\
        ArquitecturaRepo\
        club-app\

通常从第一个目录运行生成器，把控制层写到第二个应用目录。不要打开 starter 本身，误以为正在开发俱乐部应用；也不要把 starter 自带的示例 Product State 当作真实会员需求。示例中的提交、测试、负责人和业务数据都是合成内容。

对于可复现安装，建议获取[版本化的 v1.4.0 Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)。它包含固定的 ZIP、SHA-256 校验与文件清单。验证下载文件后再使用。随着 main 分支持续更新，本手册这类后来增加的资料可能存在于源码树，但不属于原先 v1.4.0 ZIP 的内容。记录你使用的确切发行版本，而不只写“最新”。

## 3. 安装前进行只读检查

先进入实际应用的目录，查看原有代码、工作流、配置、数据库迁移与未提交改动。检查是否存在 .agentic-sdlc/。如果已经存在，那么这个项目可能已经有正式的状态、活动中的执行任务、授权记录或恢复依据，不能直接覆盖。

对于已有治理状态的应用，应该走[已有项目的只读接入预检](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)，而不是重复生成。尤其不要把 v1.2 或 v1.3 状态想当然地升级成 v1.4。迁移涉及旧决定、新格式和实际产品的数据，需要另行确认兼容性。

在新项目中，也先明确要解决的用户问题、保存哪些数据、希望部署在哪里，以及第一版明确不做什么。不知道的事项保留为未决。安装工具不知道你的产品细节，不能在生成时凭空替你确定。

如果一个目录已经包含大量应用文件，不需要为了配合教程而删除它们。这个 starter 的控制层应当附着于真实产品，而不是要求把真实产品重建成某个演示项目。

## 4. 按风险选择配置

配置定义位于[profiles/profiles.json](../../../../profiles/profiles.json)。应根据项目风险和实际运作方式选择，而不是根据想同时运行多少个代理来决定。

| 配置 | 适用特征 |
| --- | --- |
| SMALL | 简单、边界清楚，暂时没有复杂持久状态的产品 |
| STATEFUL | 持久数据、用户、备份、迁移与状态一致性重要 |
| ARTIFACT_HEAVY | 大量生成产物、存储成本、来源或版权重要 |
| MULTI_WORKSTREAM | 多个工作流共同组成同一最终产品 |
| MULTI_PRODUCT | 多个不同产品共享策略、人员或基础设施 |
| HIGH_CONSEQUENCE | 隐私、安全、金钱或不可逆操作可能造成重大影响 |

对于学习用的小脚本，SMALL 通常足够。包含会员资料和会费历史的俱乐部应用可考虑 STATEFUL。配置越高并不代表产品越高级；增加不必要的管理流程可能延误真正的功能交付。选定配置后记录原因，在发现真实需求变化时调整。

任何配置都不能替代对生产环境的检查。名称为 STATEFUL 不代表数据库备份已实施；名称为 HIGH_CONSEQUENCE 也不代表安全审查已完成。所需证据取决于实际产品。

## 5. 为全新项目生成控制层

确认目标后，从 starter 的根目录执行以下 PowerShell 示例。命令是演示，不应对尚未检查的实际目录直接照搬：

    & "python" "tools\scaffold_project.py" --target "..\mi-proyecto" --profile "SMALL" --product-id "MI_PROYECTO" --objective "Initial objective, awaiting confirmation" --language "en" --no-feedback-workflow

虚构俱乐部的示例如下：

    & "python" "tools\scaffold_project.py" --target "..\club-app" --profile "STATEFUL" --product-id "CLUB_MANAGER" --objective "Member and dues management for a club" --language "en" --no-feedback-workflow

将路径、标识和目标替换为你已经核对的实际值。这里的 --language en 是生成器的语言参数示例，不代表本手册的语言设置；如果安装脚本支持所需语言，可以按实际命令帮助进行选择。不要推测未测试的参数行为。

生成器创建的是目标项目内的 .agentic-sdlc/ 控制层，不是将应用功能自动实现。它应保护现有的规范控制层，拒绝普通的覆盖尝试。生成后看到 HOLD / UNTRUSTED_CONTEXT 是合理的：新的结构尚不知道真实代码、需求、所有者与当前执行状态。

可选的 --with-runtime 添加参考执行控制机制，但不会安装外部 LLM、启动原生 Codex Desktop 工作或替你批准某项任务。--no-feedback-workflow 关闭可选的定期反馈调度；本地元数据报告生成器是否启用由另外的配置控制。这里区分机制、权限和实际操作，避免误解。

## 6. 生成成功后进行验证

在实际应用的目录里，安装声明的验证依赖并运行状态、发现和恢复检查：

    & "python" -m pip install -r ".agentic-sdlc\requirements-validation.txt"
    & "python" ".agentic-sdlc\tools\project_status.py" --control-root ".agentic-sdlc"
    & "python" ".agentic-sdlc\tools\discover_project.py" --project-root "."
    & "python" ".agentic-sdlc\tools\reconstruct_context.py" --root ".agentic-sdlc"

第一个脚本报告控制层状态；第二个检查实际项目中的文件与相关元数据；第三个尝试在没有旧聊天的情况下恢复现有文脉。重建检查显示 HOLD 不一定意味着工具有 bug，也可能表示项目还没有完成正式接入。

确认管理目录位于预定目标、原有应用文件没有被覆盖、错误或未知信息可以从文件中读取。仅仅验证 JSON 格式与文件存在，并不能证明注册页面可以打开、数据库不会丢数据或用户能完成任务。

这一阶段的准确结果是“控制层已创建并检查”，不是“产品已采用”或“能力已验收”。接下来的正式接入需要调查真实代码、用户意图、产品状态和授权关系。

## 7. 已治理项目必须保留历史

如果 .agentic-sdlc/ 已存在，先确定它是否包含当前 Product State、批准的能力、执行租约、数据库引用、验证产物或恢复记录。覆盖或删除可能破坏未来唯一可用的恢复路径。

正确路线是查看[已有治理项目接入说明](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)、核对[版本升级限制](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)，必要时在只读模式建立兼容性报告。不要把新生成的空模板直接替换已经运行的治理状态，也不要把“重新安装一次”当作解决验证失败的默认办法。

对旧项目进行任何迁移，都必须先确认迁移的范围、当前的数据与代码、需要保留的历史、回滚方式以及是否获得适当授权。只有真正可追踪的证据能够支持迁移后状态的可靠性。

## 8. 常见问题与安全动作

| 看到的现象 | 可能意味着 | 应做的事 |
| --- | --- | --- |
| Python 命令不存在 | 本地环境未正确设置 | 检查安装和 PATH |
| 找不到 .agentic-sdlc/ | 目标路径错误或生成失败 | 核对命令日志和工作目录 |
| jsonschema 缺失 | 验证依赖尚未安装 | 安装声明的 requirements |
| 出现 HOLD | 还缺真实项目的可信基准 | 继续调查与正式接入 |
| 提示已有控制层 | 项目可能已被治理 | 转入只读接入预检 |
| Git 显示陌生改动 | 可能存在其他人的工作 | 识别所有者、保留改动 |
| 管理测试通过但应用无法使用 | 管理机制与物理功能不同 | 启动应用并检查用户旅程 |
| 外部账户没有权限 | 服务登录或授权不正确 | 核对范围，不泄露令牌 |

失败时记录原始错误、目标目录、工具版本和采取的动作。不要抹除日志、编造通过结果、强制清理整份仓库。正常的安装问题可以在原位置诊断与修复；治理范围和数据一致性问题需要更谨慎的处理。

**下一章：** 02 — Planner 如何发现真实产品并完成正式接入。

## 来源与适用范围

- [公开安装和支持矩阵](../../../46_V1_4_PUBLIC_START_AND_SUPPORT.md)
- [v1.4 发行说明](../../../47_V1_4_RELEASE_NOTES_AND_UPGRADE.md)
- [首次 fork 与启动](../../../01_FORK_AND_BOOTSTRAP.md)
- [项目接入与交接](../../../16_TRANSFER_ADOPTION.md)
- [已有治理项目的只读预检](../../../32_EXISTING_GOVERNED_ATTACHMENT.md)
- [验证机制](../../../10_EXECUTABLE_VALIDATION.md)
- [实际生成器代码](../../../../tools/scaffold_project.py)

本章所有产品名称与命令参数仅用于说明，并非真实部署成功的证明。
