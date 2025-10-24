"""
ステップ2: 設定決定
膨らませたアイデアから物語の基本設定を決める
"""
import streamlit as st
from modules.data_models import Setting

st.set_page_config(page_title="設定決定", page_icon="⚙️", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
ai_client = st.session_state.ai_client
storage = st.session_state.storage

st.title("⚙️ ステップ2: 設定決定")
st.markdown("膨らませたアイデアを基に、物語の基本設定を作成します。")

# 膨らませたアイデアがあるか確認
if not project.expanded_ideas:
    st.warning("ステップ1でアイデアを膨らませてください")
    if st.button("← ステップ1に戻る"):
        st.switch_page("pages/1_アイデア選択.py")
    st.stop()

# アイデアを選択
st.subheader("基にするアイデアを選択")
selected_idea_index = st.selectbox(
    "アイデアのバージョンを選択",
    range(len(project.expanded_ideas)),
    format_func=lambda x: f"バージョン {x+1}"
)

selected_idea = project.expanded_ideas[selected_idea_index]

with st.expander("選択したアイデアを表示"):
    st.write(selected_idea)

st.divider()

# 設定の生成
st.subheader("設定を生成")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("設定を生成", type="primary", use_container_width=True):
        with st.spinner("AIが設定を生成中..."):
            setting_text = ai_client.generate_setting(selected_idea)

            # 設定を追加
            new_setting = Setting(text=setting_text)
            project.settings.append(new_setting)
            storage.save_project(project)
            st.success("設定を生成しました")
            st.rerun()

# 手動で設定を追加
with st.expander("手動で設定を入力"):
    manual_setting = st.text_area(
        "設定を入力",
        placeholder="例: 一人の青年が不思議な老人と出会い鍵を託される",
        height=100
    )
    if st.button("手動設定を追加"):
        if manual_setting.strip():
            new_setting = Setting(text=manual_setting.strip())
            project.settings.append(new_setting)
            storage.save_project(project)
            st.success("設定を追加しました")
            st.rerun()
        else:
            st.error("設定を入力してください")

st.divider()

# 生成された設定を表示＆選択
if project.settings:
    st.subheader("生成された設定（複数保存可能）")

    for i, setting in enumerate(project.settings):
        with st.container(border=True):
            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                st.markdown(f"**設定 {i+1}**")
                st.write(setting.text)

                # この設定を選択
                is_selected = (project.selected_setting_index == i)
                if st.checkbox("この設定を使用", value=is_selected, key=f"select_setting_{i}"):
                    project.selected_setting_index = i
                    storage.save_project(project)

            with col2:
                if st.button("編集", key=f"edit_setting_{i}"):
                    st.session_state[f"editing_setting_{i}"] = True

            with col3:
                if st.button("削除", key=f"delete_setting_{i}"):
                    project.settings.pop(i)
                    if project.selected_setting_index == i:
                        project.selected_setting_index = None
                    elif project.selected_setting_index and project.selected_setting_index > i:
                        project.selected_setting_index -= 1
                    storage.save_project(project)
                    st.rerun()

            # 編集モード
            if st.session_state.get(f"editing_setting_{i}", False):
                edited_text = st.text_area(
                    "設定を編集",
                    value=setting.text,
                    key=f"edit_text_{i}",
                    height=100
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("保存", key=f"save_edit_{i}"):
                        project.settings[i].text = edited_text
                        storage.save_project(project)
                        st.session_state[f"editing_setting_{i}"] = False
                        st.rerun()
                with col_b:
                    if st.button("キャンセル", key=f"cancel_edit_{i}"):
                        st.session_state[f"editing_setting_{i}"] = False
                        st.rerun()

    # 選択状態の表示
    if project.selected_setting_index is not None:
        st.success(f"設定 {project.selected_setting_index + 1} を使用します")

# ナビゲーション
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← ステップ1に戻る"):
        st.switch_page("pages/1_アイデア選択.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
with col3:
    if st.button("次のステップへ →", type="primary"):
        if project.selected_setting_index is not None:
            st.switch_page("pages/3_プロット作成.py")
        else:
            st.error("使用する設定を選択してください")
