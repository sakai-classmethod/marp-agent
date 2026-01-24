# borderテーマ導入の問題整理

## 目標
Marpテーマを `default + invert` から `border`（コミュニティテーマ）に変更する

## 実施した変更

### 1. ファイル追加・修正（完了）

| ファイル | 変更内容 | 状態 |
|---------|---------|------|
| `src/themes/border.css` | カスタムテーマCSS新規作成 | ✅ |
| `amplify/agent/runtime/border.css` | PDF生成用テーマCSS | ✅ |
| `src/components/SlidePreview.tsx` | Marp Coreにテーマ登録 | ✅ |
| `amplify/agent/runtime/agent.py` | システムプロンプト `theme: border` に変更 | ✅ |
| `src/hooks/useAgentCore.ts` | モック実装のテーマ更新 | ✅ |
| `docs/KNOWLEDGE.md` | borderテーマの説明追加 | ✅ |
| `docs/PLAN.md` | ディレクトリ構成更新 | ✅ |
| `tests/e2e-test.md` | テスト項目追加 | ✅ |

### 2. ビルド確認（完了）
```
npm run build → 成功
```

## 現在の問題

### 問題1: sandboxデプロイが反映されない

**症状**:
- agent.pyの変更（`theme: border`）がランタイムに反映されていない
- 生成されるスライドは依然として `theme: default` + `class: invert`

**原因候補**:
1. sandboxのHotswapが正しく動作していない
2. 複数のsandboxプロセスが競合している
3. ランタイムのコンテナイメージが更新されていない

### 問題2: 複数のsandboxプロセス競合

**症状**:
```
[ERROR] [MultipleSandboxInstancesError] Multiple sandbox instances detected.
```

**現状**:
- 4つのampxプロセスが同時に動作中
- sandbox deleteを実行したが、別のプロセスが残っている

## 必要なアクション

### Step 1: 環境クリーンアップ
1. すべてのampxプロセスを停止
2. `.amplify/artifacts/` をクリア
3. sandbox deleteで完全削除

### Step 2: sandbox再起動
1. Docker起動確認
2. `npx ampx sandbox` を1つだけ起動
3. デプロイ完了まで待機（約5-10分）

### Step 3: テスト実行
1. devサーバー起動
2. ブラウザでスライド生成
3. borderテーマ（グレー枠線＋グラデーション背景）の適用確認
4. スクリーンショットを `tests/screenshots/` に保存

## 技術的な補足

### borderテーマの特徴
- 背景: グレーのグラデーション（`#f7f7f7` → `#d3d3d3`）
- 枠線: 濃いグレー（`#303030`）の太枠線
- アウトライン: 白

### 旧テーマ（default + invert）の特徴
- 背景: ダークブルー/ネイビー
- テキスト: 白

### 確認コマンド
```bash
# ampxプロセス確認
ps aux | grep "ampx" | grep -v grep | grep -v "Code Helper"

# sandbox削除
npx ampx sandbox delete --yes

# sandbox起動
TAVILY_API_KEY=$(grep TAVILY_API_KEY .env | cut -d= -f2) npx ampx sandbox

# CloudFormation状態確認
aws cloudformation describe-stacks \
  --stack-name amplify-marpagent-minorun365-sandbox-c233fd7ea3 \
  --query "Stacks[0].{Status:StackStatus,LastUpdated:LastUpdatedTime}"
```

## 次のステップ

みのるんに確認:
1. すべてのampxプロセスを停止してよいか
2. sandbox deleteで環境を完全にクリアしてよいか
3. 上記完了後、新しくsandboxを起動してテストを実行
