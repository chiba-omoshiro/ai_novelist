"""
ステップ6: 本文執筆
AIに小説を書いてもらう
"""
import streamlit as st

st.set_page_config(page_title="本文執筆", page_icon="📝", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
ai_client = st.session_state.ai_client
storage = st.session_state.storage

st.title("📝 ステップ6: 本文執筆")
st.markdown("これまでの設定を基に、AIが小説を執筆します。")

# 執筆設定が完了しているか確認
if not project.writing_config:
    st.warning("ステップ5で執筆設定を完了してください")
    if st.button("← ステップ5に戻る"):
        st.switch_page("pages/5_執筆設定.py")
    st.stop()

# 必要な情報を取得
selected_setting = project.settings[project.selected_setting_index]
selected_plot = project.plots[project.selected_plot_index]
characters = project.characters
writing_config = project.writing_config

# 設定の確認
with st.expander("執筆に使用する設定を確認"):
    st.markdown("### 設定")
    st.write(selected_setting.text)

    st.markdown("### プロット")
    st.write(selected_plot.text)

    st.markdown(f"### キャラクター ({len(characters)}人)")
    for char in characters:
        st.write(f"**{char.name}** ({char.role or '役割なし'}): {char.personality}")

    st.markdown("### 執筆設定")
    st.write(f"- 長さ: {writing_config.length}")
    st.write(f"- 文体: {writing_config.style}")
    st.write(f"- 雰囲気: {writing_config.tone}")
    st.write(f"- AIモデル: {writing_config.ai_model}")

st.divider()

# 執筆ボタン
st.subheader("小説を執筆")

if st.button("AIに執筆してもらう", type="primary", use_container_width=True):
    with st.spinner(f"AIが小説を執筆中... ({writing_config.ai_model} を使用)"):
        # キャラクター情報を辞書に変換
        characters_data = [
            {
                "name": char.name,
                "role": char.role,
                "personality": char.personality,
                "background": char.background
            }
            for char in characters
        ]

        # 小説を執筆
        novel_text = ai_client.write_novel(
            setting=selected_setting.text,
            plot=selected_plot.text,
            characters=characters_data,
            length=writing_config.length,
            style=writing_config.style,
            tone=writing_config.tone,
            model=writing_config.ai_model
        )

        # 小説を保存
        project.novel_text = novel_text
        storage.save_project(project)

        st.success("小説の執筆が完了しました！")
        st.rerun()

st.divider()

# 執筆された小説を表示
if project.novel_text:
    st.subheader("執筆された小説")

    # 文字数をカウント
    char_count = len(project.novel_text)
    st.caption(f"文字数: {char_count:,}文字")

    # 小説本文を表示
    with st.container(border=True):
        st.markdown(project.novel_text)

    # 編集機能
    with st.expander("小説を編集"):
        edited_text = st.text_area(
            "本文を編集",
            value=project.novel_text,
            height=400,
            key="edit_novel"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("変更を保存", type="primary"):
                project.novel_text = edited_text
                storage.save_project(project)
                st.success("変更を保存しました")
                st.rerun()
        with col2:
            if st.button("元に戻す"):
                st.rerun()

    # ダウンロード機能
    st.divider()
    st.subheader("エクスポート")

    col1, col2 = st.columns(2)

    with col1:
        # テキストファイルとしてダウンロード
        st.download_button(
            label="📄 テキストファイルとしてダウンロード",
            data=project.novel_text,
            file_name=f"{project.project_name}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        # プロジェクト全体をJSONでエクスポート
        st.download_button(
            label="📦 プロジェクトをエクスポート (JSON)",
            data=project.to_json(),
            file_name=f"{project.project_name}_project.json",
            mime="application/json",
            use_container_width=True
        )

    # 再執筆
    st.divider()
    if st.button("🔄 最初から執筆し直す", use_container_width=True):
        if st.session_state.get("confirm_rewrite", False):
            project.novel_text = ""
            storage.save_project(project)
            st.session_state["confirm_rewrite"] = False
            st.success("本文をクリアしました。上のボタンから再度執筆してください。")
            st.rerun()
        else:
            st.session_state["confirm_rewrite"] = True
            st.warning("もう一度クリックすると本文が削除されます")

else:
    st.info("まだ小説が執筆されていません。上のボタンから執筆を開始してください。")

# ナビゲーション
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← ステップ5に戻る"):
        st.switch_page("pages/5_執筆設定.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
