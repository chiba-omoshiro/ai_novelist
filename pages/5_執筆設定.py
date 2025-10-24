"""
ステップ5: 執筆設定
長さ、文体、雰囲気を指定する
"""
import streamlit as st
from modules.data_models import WritingConfig

st.set_page_config(page_title="執筆設定", page_icon="✍️", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
storage = st.session_state.storage

st.title("✍️ ステップ5: 執筆設定")
st.markdown("小説の長さ、文体、雰囲気を設定します。")

# キャラクターが作成されているか確認
if not project.characters:
    st.warning("ステップ4でキャラクターを作成してください")
    if st.button("← ステップ4に戻る"):
        st.switch_page("pages/4_登場人物.py")
    st.stop()

st.divider()

# 既存の設定がある場合は表示
if project.writing_config:
    st.info("現在の設定が読み込まれています。変更する場合は下記のフォームを編集してください。")
    default_length = project.writing_config.length
    default_style = project.writing_config.style
    default_tone = project.writing_config.tone
    default_model = project.writing_config.ai_model
else:
    default_length = "短編"
    default_style = "文学的"
    default_tone = "明るい"
    default_model = "haiku3.5"

# 設定フォーム
st.subheader("執筆設定")

col1, col2 = st.columns(2)

with col1:
    # 長さ
    length = st.selectbox(
        "長さ",
        ["短編", "中編", "長編"],
        index=["短編", "中編", "長編"].index(default_length)
    )
    st.caption("短編: 2000-3000文字、中編: 5000-8000文字、長編: 10000文字以上")

    # 文体
    style = st.selectbox(
        "文体",
        ["文学的", "ライトノベル風", "エッセイ風", "児童文学風", "ミステリー風", "SF風"],
        index=["文学的", "ライトノベル風", "エッセイ風", "児童文学風", "ミステリー風", "SF風"].index(default_style) if default_style in ["文学的", "ライトノベル風", "エッセイ風", "児童文学風", "ミステリー風", "SF風"] else 0
    )

with col2:
    # 雰囲気・読後感
    tone = st.selectbox(
        "雰囲気・読後感",
        ["明るい", "暗い", "ミステリアス", "感動的", "コミカル", "緊張感のある", "ノスタルジック"],
        index=["明るい", "暗い", "ミステリアス", "感動的", "コミカル", "緊張感のある", "ノスタルジック"].index(default_tone) if default_tone in ["明るい", "暗い", "ミステリアス", "感動的", "コミカル", "緊張感のある", "ノスタルジック"] else 0
    )

    # 使用するAIモデル
    ai_model = st.selectbox(
        "使用するAIモデル（執筆用）",
        ["haiku3.5", "sonnet4.5", "gemini2.5pro"],
        index=["haiku3.5", "sonnet4.5", "gemini2.5pro"].index(default_model),
        format_func=lambda x: {
            "haiku3.5": "Claude 3.5 Haiku (高速・コスト効率)",
            "sonnet4.5": "Claude Sonnet 4.5 (高品質)",
            "gemini2.5pro": "Gemini 2.5 Pro (思考型・高品質)"
        }[x]
    )

st.divider()

# カスタム文体・雰囲気
with st.expander("カスタム設定（オプション）"):
    st.markdown("選択肢にない文体や雰囲気を指定したい場合は、ここに入力してください。")

    custom_style = st.text_input("カスタム文体", placeholder="例: 時代小説風、詩的な")
    custom_tone = st.text_input("カスタム雰囲気", placeholder="例: 哲学的な、幻想的な")

    if custom_style:
        style = custom_style
    if custom_tone:
        tone = custom_tone

st.divider()

# 設定の確認と保存
st.subheader("設定の確認")

config_summary = f"""
- **長さ**: {length}
- **文体**: {style}
- **雰囲気・読後感**: {tone}
- **AIモデル**: {ai_model}
"""

st.markdown(config_summary)

if st.button("この設定で執筆する", type="primary", use_container_width=True):
    # 設定を保存
    project.writing_config = WritingConfig(
        length=length,
        style=style,
        tone=tone,
        ai_model=ai_model
    )
    storage.save_project(project)
    st.success("執筆設定を保存しました")
    st.info("次のステップで本文を執筆します")

# ナビゲーション
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← ステップ4に戻る"):
        st.switch_page("pages/4_登場人物.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
with col3:
    if st.button("本文執筆へ →", type="primary"):
        if project.writing_config:
            st.switch_page("pages/6_本文執筆.py")
        else:
            st.error("まず設定を保存してください")
