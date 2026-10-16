# エージェント継続ブリッジ — Agent Continuity Bridge 0.2.1

## 目的

ArquitecturaRepo は開発の権限、計画、受け入れ判定を管理します。この任意プラグインは、外部の継続管理コントローラーとの接続を独立した境界として提供します。AIモデルでも別のキャンペーン管理者でもありません。ポータブルな中核機能は、このプラグインなしで動作します。

## 現在確認できる機能

別途入手した Codex Daily Control 3.1 の ZIP を実行せずに検査します。安全なパス、ファイル一覧、全 SHA-256、バージョン、設定の整合性を確認し、既存プロジェクトにパッケージのハッシュだけを登録・再検証・解除します。個人設定、認証情報、Goal ID、会話データは同梱しません。

## 必要条件と接続

Python 3.10 以上、.agentic-sdlc を持つ既存の ArquitecturaRepo プロジェクト、別途入手した 3.1 ZIP が必要です。コントローラー自体のネイティブ動作には Windows、PowerShell 5.1、互換性のある Codex Desktop、別途設定した Git、SQLite、必要に応じて Drive/rclone が必要です。ブリッジはこれらをインストールしません。

## 安全性と制限

3.1 はリリース候補であり、Windows/Codex 実機の承認試験は未完了です。ネイティブな終了、Desktop の引き継ぎ、クォータ復帰、リモート配信は無効／未検証です。

## CLI

```bash
python "bridge.py" inspect --package "CONTROLLER_3_1.zip"
python "bridge.py" install --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" status --project "MY_PROJECT" --package "CONTROLLER_3_1.zip"
python "bridge.py" uninstall --project "MY_PROJECT"
```


既存プロジェクトへの導入: `python install_into_project.py --project "PROJECT"`。CLI は `.agentic-sdlc/extensions/agent-continuity-bridge/pluginctl.py` に配置されます。削除 (`--remove`) の前にコントローラー登録を解除してください。ネイティブ操作は行いません。
