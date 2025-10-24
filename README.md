# AI小説家

AIと一緒に小説を創作するStreamlitアプリケーション

## 概要

「AI小説家」は、AIの力を借りて小説を執筆するためのローカルWebアプリケーションです。アイデア出しから本文執筆まで、6つのステップで小説を完成させることができます。

## 主な機能

1. **アイデア選択** - AIが提示する多数のフレーズから選択してアイデアを膨らませる
2. **設定決定** - 物語の基本設定を作成（複数バージョン保存可能）
3. **プロット作成** - 発端から結末までの物語の流れを組み立てる
4. **登場人物** - キャラクターの性格や背景を設定
5. **執筆設定** - 長さ、文体、読後感を指定
6. **本文執筆** - チャットAI用のプロンプトを生成（推奨）または直接API経由で執筆

### 特徴

- **プロンプト生成機能**（推奨）
  - チャットAI（Claude.ai、ChatGPT、Gemini）で使える完璧なプロンプトを生成
  - トークン制限なしで長編小説も自由に執筆可能
  - コストを気にせず何度でも試せる
  - 対話しながら内容を調整・修正できる

- **ローカル環境で動作**
  - データはすべてローカルに保存
  - プライバシー保護

- **柔軟なプロジェクト管理**
  - 複数のプロジェクトを管理可能
  - 各ステップで複数のバリエーションを保存
  - 前のステップに戻って変更可能

- **AI統合**
  - アイデア出し: Google Gemini 2.5 Flash
  - プロンプト生成: Claude、ChatGPT、Gemini向けに最適化
  - 直接執筆（オプション）: Claude 3.5 Haiku / Claude Sonnet 4.5 / Gemini 2.5 Pro

## セットアップ

### クイックスタート（自動セットアップ）

セットアップスクリプトを使えば、簡単にセットアップできます：

**Mac/Linux:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

その後、`.env` ファイルにAPIキーを設定してください。

### 手動セットアップ

#### 1. 仮想環境の作成と有効化

**重要**: 複数のPythonプロジェクトがある場合は仮想環境を使用することを強く推奨します。

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化（Mac/Linux）
source venv/bin/activate

# 仮想環境を有効化（Windows）
venv\Scripts\activate
```

仮想環境が有効化されると、ターミナルのプロンプトに `(venv)` が表示されます。

### 2. 依存関係のインストール

仮想環境を有効化した状態で、以下のコマンドを実行します：

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example` を `.env` にコピーして、APIキーを設定します：

```bash
cp .env.example .env
```

`.env` ファイルを編集して、以下のAPIキーを設定してください：

```
# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Anthropic Claude API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### APIキーの取得方法

- **Google Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey) でAPIキーを取得
- **Anthropic Claude API**: [Anthropic Console](https://console.anthropic.com/) でAPIキーを取得

### 4. アプリケーションの起動

#### 起動スクリプトを使う（推奨）

**Mac/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

#### 手動で起動

仮想環境を有効化した状態で、以下のコマンドを実行します：

```bash
# 仮想環境の有効化（Mac/Linux）
source venv/bin/activate

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# アプリケーションの起動
streamlit run app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます（通常は http://localhost:8501 ）。

### 5. 作業終了後

アプリケーションを終了したら、仮想環境を無効化できます：

```bash
deactivate
```

次回起動時は、再度仮想環境を有効化してから `streamlit run app.py` を実行してください。

## 使い方

### 基本的な流れ

1. **プロジェクトの作成**
   - サイドバーから「新規プロジェクト」を選択
   - プロジェクト名を入力して作成

2. **小説の設定作成（ステップ1-5）**
   - ステップ1から順番に進めていきます
   - 各ステップで複数のバージョンを試すことができます
   - 気に入らない場合は前のステップに戻って変更可能

3. **プロンプト生成（ステップ6・推奨）**
   - チャットAI（Claude.ai、ChatGPT、Gemini）を選択
   - 「プロンプトを生成」ボタンをクリック
   - 生成されたプロンプトをコピー
   - 選択したチャットAIに貼り付けて小説を執筆

4. **プロジェクトの保存**
   - 作業内容は自動的に保存されます
   - サイドバーの「プロジェクトを保存」ボタンでも保存可能

5. **プロンプトのエクスポート**
   - プロンプトをテキストファイルとしてダウンロード
   - プロジェクト全体をJSONでエクスポートも可能

### プロンプト生成のメリット

- **長編小説も自由に**: API制限がないため、何万文字でも執筆可能
- **コスト削減**: 無料プランのチャットAIでも使える
- **対話的な修正**: チャットで「続きを書いて」「この部分を詳しく」など指示可能
- **高品質**: 最新のチャットAIモデルを自由に選択可能

## プロジェクト構造

```
ai_novelist/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 依存関係
├── .env.example               # 環境変数テンプレート
├── .gitignore                 # Git除外設定
├── README.md                  # このファイル
├── data/                      # プロジェクトデータ保存用
│   └── projects/
├── modules/                   # バックエンドモジュール
│   ├── __init__.py
│   ├── ai_client.py           # AI API連携
│   ├── data_models.py         # データモデル
│   └── storage.py             # ストレージ管理
└── pages/                     # Streamlitページ
    ├── 1_アイデア選択.py
    ├── 2_設定決定.py
    ├── 3_プロット作成.py
    ├── 4_登場人物.py
    ├── 5_執筆設定.py
    └── 6_本文執筆.py
```

## 使用技術

- **フレームワーク**: Streamlit
- **AI API**:
  - Google Generative AI (Gemini)
  - Anthropic API (Claude)
- **データ保存**: JSON（ローカルファイル）

## GitHub連携

このプロジェクトはGitHubでバージョン管理を行うことを推奨します。

```bash
# Git初期化
git init

# ファイルを追加
git add .

# 最初のコミット
git commit -m "Initial commit: AI Novelist application"

# GitHubリポジトリに接続
git remote add origin https://github.com/your-username/ai_novelist.git

# プッシュ
git push -u origin main
```

## 注意事項

- APIキーは `.env` ファイルに保存され、Gitにコミットされません
- 生成されたプロジェクトデータは `data/projects/` に保存されます
- AIの生成結果は毎回異なる場合があります
- 長編小説の生成には時間がかかる場合があります

## ライセンス

MIT License

## 作者

Created with Claude Code
