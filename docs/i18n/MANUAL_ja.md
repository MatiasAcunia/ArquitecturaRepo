# ArquitecturaRepo — v1.4.0 実践マニュアル（日本語）

このガイドは **v1.4.0** を自分のプロジェクトで使うための 8 章（00〜07）です。旧スペイン語版 v1.3 の全文翻訳ではなく、**v1.4 向けに新たにまとめた実践ガイド**です。旧版の詳細マニュアルはソースリポジトリに保存されています。配布の正本は変更できない [v1.4.0 GitHub Release](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0) で、v1.3.0 も旧版として残っています。

このマニュアルは v1.4.0 公開**後**に `main` に追加されました。公開済みの変更できない v1.4.0 ZIP／コンテナには**含まれていません**。オフライン配布には、別バージョンとしての将来のリリースが必要です。

## 00 · 目的と制限を知る

ArquitecturaRepo は、要件・意思決定・担当・現行状態・開発キャンペーン・根拠・中断からの復帰を **リポジトリ内** で管理する仕組みです。アプリの自動生成サービスでも Codex の代替モデルでもありません。

- CLIENT：製品の目的、機密性の高い操作、公開、実際の使いやすさを決定・承認します。
- I1：必要な場合だけ複数プロジェクトを調整します。
- I2 Planner：製品と依存関係を調べ、実装すべき能力と受入基準を定義します。
- I3 Controller：承認済みキャンペーン内で実装・テスト・統合・修正・復旧を担当します。
- I4：必要時のみ専門作業を担当します。**4 つの役割に 4 つのエージェントは不要**です。

アプリのソース、DB、秘密鍵、会話を公開する必要はありません。外部 AI に何を渡すかは、別途許可するツールやサービス次第です。このフレームワークを導入しても外部アクセス権は付与されません。

## 01 · 安全なインストール

CI で確認されている Python 3.12 を使用します。[v1.4.0 のポータブル ZIP](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/download/v1.4.0/ArquitecturaRepo-v1.4.0-portable.zip) を入手し、同時公開の `.sha256` と照合して展開します。**展開したフレームワークのディレクトリ**で端末を開いてください。固定 Git タグ `v1.4.0` の使用も可能です。

新規プロジェクト、または既存コードはあるが **正式な制御レイヤーがない** プロジェクトには、最小の `SMALL` を使います。

```bash
python "tools/scaffold_project.py" --target "../my-project" --profile SMALL --product-id MY_PROJECT --objective "Initial objective pending confirmation" --language ja --no-feedback-workflow
```

Windows PowerShell：

```powershell
python "tools\scaffold_project.py" --target "..\my-project" --profile "SMALL" --product-id "MY_PROJECT" --objective "Initial objective pending confirmation" --language "ja" --no-feedback-workflow
```

インストーラーは `.agentic-sdlc/` を追加しますが、既存のアプリコードやワークフローを上書きせず、既存の正規制御レイヤーの置換を拒否します。`--no-feedback-workflow` は月次実行の予定だけを削除し、**ローカルのレポート生成機能は残ります**。すべて停止するには `.agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json` の `enabled=false` を設定してください。外部送信先は同梱されていません。

次に **導入先プロジェクトのディレクトリ**で実行します。

```bash
python -m pip install -r ".agentic-sdlc/requirements-validation.txt"
python ".agentic-sdlc/tools/project_status.py" --control-root ".agentic-sdlc"
python ".agentic-sdlc/tools/discover_project.py" --project-root "."
python ".agentic-sdlc/tools/reconstruct_context.py" --root ".agentic-sdlc"
```

PowerShell のパスは引用符付きで `\` を使います。最初に `HOLD / UNTRUSTED_CONTEXT` と表示されても **正常** です。実際の要件、ソース、権限はまだ承認されていません。既に Product State、キャンペーン、Controller がある場合は **上書きしないでください**。[既存管理プロジェクト向け読み取り専用チェック](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/32_EXISTING_GOVERNED_ATTACHMENT.md) を使います。v1.2/v1.3 からの汎用自動移行はありません。

## 02 · Planner と導入判断

実際のコード・利用者・DB・セキュリティ・依存関係・要件を調査し、CLIENT が製品の前提を確認します。I2 は **能力単位** で、目標・範囲・責任者・インターフェース・受入条件・不合格条件を定義します。サンプルの架空 Product State を実際の状態としてコピーしたり、インストール成功を実行許可と見なしたりしてはいけません。

## 03 · 日々の作業

古いチャットより、Git・CURRENT 状態・実証された根拠を優先します。I3 は承認された **同じキャンペーン** で実装、テスト、デバッグ、再試行、復旧を行います。普通のバグごとに新キャンペーンを作りません。Git、SQLite WAL、ID、実行権限、リースが食い違う場合は `HOLD` にします。ポータブル CI は Codex Desktop/Goals のネイティブ操作や外部サービスを保証しません。

## 04 · 変更の依頼

期待する**観察可能な結果**、制約、受入テストを伝えます。例：「会費の未払い月を表示し、過去の入金記録を壊さず、支払済み・遅延ケースのテストと画面で確認する」。I2 は戦略上の影響を判断し、I3 は承認範囲内の修正を担当します。

## 05 · エラーと復旧

- `UNTRUSTED_CONTEXT`：ソースと要件を確認します。状態を手で書き換えて成功扱いにしません。
- `jsonschema` がない：導入先の `requirements-validation.txt` をインストールします。
- `EXISTING_CONTROL_PRESERVED`：停止し、読み取り専用ルートへ。`--force` や既存状態の削除は不可。
- Git/SQLite WAL/リースの矛盾：証拠が一致するまで重要な書き込みを停止します。
- 中断：ジャーナル、実行 ID、成果物を保全し、元のキャンペーンで復旧します。所有者が確認できないファイルを消さないでください。

公開 Issue には再現手順と伏せ字処理済みログのみ。秘密鍵、個人パス、非公開プロジェクト名、DB、会話を掲載しないでください。

## 06 · 能力の受入

単体・統合・DB/currentness・意味/一般化・物理実行・人間の評価・公開の各ゲートを **別々** に扱います。テスト成功やエージェントの「完了」は CLIENT の承認ではありません。正確なソース、証拠、担当、判断を正規記録に残します。合成 CI は実アプリの本番品質を証明しません。

## 07 · 会員クラブの例

1. CLIENT が会員登録、月会費、未納一覧を依頼し、期待する動作を確認します。
2. I2 が実 DB・アクセス権を調査して最小の実用機能を定義します。
3. I3 が登録 → 会費 → 未納照会を実装し、DB と復旧を試験します。
4. 計算バグは **同じ** キャンペーンで修正します。
5. CLIENT が画面を実際に操作して承認または差し戻しし、根拠を保存します。

## 参考情報と限界

[短いガイド](README_ja.md) · [FAQ](FAQ_ja.md) · [ルート README](../../README.md) · [v1.4 の実証範囲](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/v1.4.0/docs/46_V1_4_PUBLIC_START_AND_SUPPORT.md)。

この文書は本番セキュリティ認証、第三者の使いやすさ検証、ネイティブホスト保証、Codex 直接利用より優れているという実測結果ではありません。MIT ライセンスは第三者の素材に自動適用されません。
