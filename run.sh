#!/bin/bash
# AI小説家 起動スクリプト（Mac/Linux用）

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "❌ 仮想環境が見つかりません"
    echo "まず setup.sh を実行してセットアップを完了してください："
    echo "   ./setup.sh"
    exit 1
fi

# .envファイルの確認
if [ ! -f ".env" ]; then
    echo "⚠️  .envファイルが見つかりません"
    echo "📝 APIキーを設定してください："
    echo "   cp .env.example .env"
    echo "その後、.envファイルを編集してAPIキーを設定してください。"
    echo ""
    read -p "続行しますか？ (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        exit 1
    fi
fi

# 仮想環境の有効化
echo "🔧 仮想環境を有効化中..."
source venv/bin/activate

# アプリケーションの起動
echo "🚀 AI小説家を起動しています..."
echo ""
streamlit run app.py
