# Agentic SDLC — はじめに

[v1.4 ミニガイド](MINI_GUIDE_ja.md) · [FAQ](FAQ_ja.md)

[全8章の詳細マニュアル](https://github.com/MatiasAcunia/ArquitecturaRepo/blob/main/docs/manual/ES/README.md)は**ソースリポジトリ内でスペイン語のみ**提供される**旧 v1.3 版**です。インストール先にはコピーされません。このページは v1.4 の短い入門であり、全文翻訳ではありません。最新の操作手順は[v1.4 インストールガイド](../46_V1_4_PUBLIC_START_AND_SUPPORT.md)を参照してください。

エージェントを使ったソフトウェア開発向けの、リポジトリを中心とした再利用可能なアーキテクチャです。役割分担、永続的な状態、計画、復旧、検証を提供します。あらゆるアプリを自動で完成させるものではなく、製品責任者の判断も代行しません。

## プロジェクトへの導入

必要最小限のプロファイルを選んでください。最初は読み取り専用で調査し、サンプルの Product State を実際のプロジェクトへコピーしないでください。新規環境は HOLD / UNTRUSTED_CONTEXT から始まります。

```bash
python tools/scaffold_project.py --target "../my-project" --profile SMALL --product-id EXAMPLE --language auto
```

## 役割と権限

CLIENT は製品方針と機密操作の承認、I2 は戦略と受入れ、I3 は承認された範囲での実装と復旧を担当します。I4 は限定的な支援と独立した検証のためのオプションです。四つの役割が四つのプロセスを意味するわけではありません。

## プライバシーと月次フィードバック

新しい構成では、プロジェクト自身の GitHub Actions に月一回、最小限のメタデータレポートを保存する設定が既定で有効です。構造の改善と問題の分類に役立ちますが、保守者に自動送信されません。コード、会話、プロジェクト名、パス、識別子、認証情報は含みません。

すべてのレポートを停止するには .agentic-sdlc/feedback/ARCHITECTURE_FEEDBACK_CONFIG.json で enabled=false を設定します。.github/workflows/agentic-sdlc-feedback.yml の削除や --no-feedback-workflow は定期実行だけを停止し、ローカル生成機能は残ります。

## 安全性とバージョン

**v1.4.0 は公開済みです**。[バージョン付き GitHub Release にポータブル ZIP と SHA-256 チェックサム](https://github.com/MatiasAcunia/ArquitecturaRepo/releases/tag/v1.4.0)があります。インストール前にダウンロードしたファイルを検証してください。変更される `main` ブランチには公開後の文書修正が含まれる場合があり、リリース成果物そのものではありません。以前の v1.3.0 リリースも引き続き利用できます。新規または既存の統治状態がないプロジェクトには [v1.4 初回導入ガイド](../46_V1_4_PUBLIC_START_AND_SUPPORT.md) を、すでに統治状態があるプロジェクトには [読み取り専用の事前確認](../32_EXISTING_GOVERNED_ATTACHMENT.md) を使用し、状態を自動で上書きしないでください。ポータブル CI だけでは Codex Desktop のネイティブ実行、外部 AI プロバイダー、実際の外部操作を認証できません。

## 言語

導入ツールは OS の言語を検出し、--language ja で明示指定もできます。資料はオフラインで読めます。GitHub の README は静的なので、言語リンクから選択してください。

[v1.4 ミニガイド](MINI_GUIDE_ja.md) · [FAQ](FAQ_ja.md) · [GitHub README](../../README.md)
