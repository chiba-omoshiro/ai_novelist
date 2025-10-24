@echo off
REM AI小説家 起動スクリプト（Windows用）

REM 仮想環境の確認
if not exist "venv" (
    echo ❌ 仮想環境が見つかりません
    echo まず setup.bat を実行してセットアップを完了してください：
    echo    setup.bat
    pause
    exit /b 1
)

REM .envファイルの確認
if not exist ".env" (
    echo ⚠️  .envファイルが見つかりません
    echo 📝 APIキーを設定してください：
    echo    copy .env.example .env
    echo その後、.envファイルを編集してAPIキーを設定してください。
    echo.
    set /p confirm="続行しますか？ (y/N): "
    if /i not "%confirm%"=="y" exit /b 1
)

REM 仮想環境の有効化
echo 🔧 仮想環境を有効化中...
call venv\Scripts\activate

REM アプリケーションの起動
echo 🚀 AI小説家を起動しています...
echo.
streamlit run app.py
