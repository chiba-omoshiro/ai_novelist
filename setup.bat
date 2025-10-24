@echo off
REM AI小説家 セットアップスクリプト（Windows用）

echo 🚀 AI小説家のセットアップを開始します...
echo.

REM 仮想環境の作成
if not exist "venv" (
    echo 📦 仮想環境を作成中...
    python -m venv venv
    echo ✓ 仮想環境を作成しました
) else (
    echo ✓ 仮想環境は既に存在します
)

echo.

REM 仮想環境の有効化
echo 🔧 仮想環境を有効化中...
call venv\Scripts\activate

REM 依存関係のインストール
echo 📚 依存関係をインストール中...
pip install -r requirements.txt

echo.
echo ✅ セットアップが完了しました！
echo.

REM .envファイルのチェック
if not exist ".env" (
    echo ⚠️  .envファイルが見つかりません
    echo 📝 .env.exampleをコピーして.envを作成してください：
    echo    copy .env.example .env
    echo.
    echo その後、.envファイルを編集してAPIキーを設定してください。
    echo.
) else (
    echo ✓ .envファイルが存在します
    echo.
)

echo 🎉 アプリケーションを起動するには：
echo    venv\Scripts\activate
echo    streamlit run app.py
echo.
echo 作業終了後は 'deactivate' で仮想環境を無効化できます。

pause
