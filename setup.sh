#!/bin/bash
# AI小説家 セットアップスクリプト（Mac/Linux用）

echo "🚀 AI小説家のセットアップを開始します..."
echo ""

# 仮想環境の作成
if [ ! -d "venv" ]; then
    echo "📦 仮想環境を作成中..."
    python3 -m venv venv
    echo "✓ 仮想環境を作成しました"
else
    echo "✓ 仮想環境は既に存在します"
fi

echo ""

# 仮想環境の有効化
echo "🔧 仮想環境を有効化中..."
source venv/bin/activate

# 依存関係のインストール
echo "📚 依存関係をインストール中..."
pip install -r requirements.txt

echo ""
echo "✅ セットアップが完了しました！"
echo ""

# .envファイルのチェック
if [ ! -f ".env" ]; then
    echo "⚠️  .envファイルが見つかりません"
    echo "📝 .env.exampleをコピーして.envを作成してください："
    echo "   cp .env.example .env"
    echo ""
    echo "その後、.envファイルを編集してAPIキーを設定してください。"
    echo ""
else
    echo "✓ .envファイルが存在します"
    echo ""
fi

echo "🎉 アプリケーションを起動するには："
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "作業終了後は 'deactivate' で仮想環境を無効化できます。"
