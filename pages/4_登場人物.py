"""
ステップ4: 登場人物
キャラクターを作成する
"""
import streamlit as st
from modules.data_models import Character

st.set_page_config(page_title="登場人物", page_icon="👥", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
ai_client = st.session_state.ai_client
storage = st.session_state.storage

st.title("👥 ステップ4: 登場人物")
st.markdown("物語のキャラクターを作成します。")

# 設定とプロットが選択されているか確認
if project.selected_setting_index is None or project.selected_plot_index is None:
    st.warning("ステップ2とステップ3を完了してください")
    if st.button("← ステップ3に戻る"):
        st.switch_page("pages/3_プロット作成.py")
    st.stop()

selected_setting = project.settings[project.selected_setting_index]
selected_plot = project.plots[project.selected_plot_index]

# 選択された設定とプロットを表示
with st.expander("使用する設定とプロットを表示"):
    st.markdown("**設定**")
    st.write(selected_setting.text)
    st.markdown("**プロット**")
    st.write(selected_plot.text)

st.divider()

# キャラクターの生成
st.subheader("キャラクターを生成")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    character_count = st.number_input("生成する人数", min_value=1, max_value=10, value=3)
with col3:
    if st.button("キャラクター生成", type="primary", use_container_width=True):
        with st.spinner("AIがキャラクターを生成中..."):
            characters = ai_client.generate_characters(
                selected_setting.text,
                selected_plot.text,
                character_count
            )

            # キャラクターを追加
            for char_data in characters:
                new_character = Character(
                    name=char_data.get("name", "名前なし"),
                    personality=char_data.get("personality", ""),
                    background=char_data.get("background", ""),
                    role=char_data.get("role", "")
                )
                project.characters.append(new_character)

            storage.save_project(project)
            st.success(f"{len(characters)}人のキャラクターを生成しました")
            st.rerun()

# 手動でキャラクターを追加
with st.expander("手動でキャラクターを追加"):
    col1, col2 = st.columns(2)
    with col1:
        manual_name = st.text_input("名前")
        manual_role = st.text_input("役割", placeholder="例: 主人公、ライバル、メンター")
    with col2:
        manual_personality = st.text_area("性格", height=100)
        manual_background = st.text_area("背景", height=100)

    if st.button("キャラクターを追加"):
        if manual_name.strip() and manual_personality.strip():
            new_character = Character(
                name=manual_name.strip(),
                personality=manual_personality.strip(),
                background=manual_background.strip() if manual_background else None,
                role=manual_role.strip() if manual_role else None
            )
            project.characters.append(new_character)
            storage.save_project(project)
            st.success(f"キャラクター '{manual_name}' を追加しました")
            st.rerun()
        else:
            st.error("名前と性格は必須です")

st.divider()

# 登録されたキャラクターを表示
if project.characters:
    st.subheader(f"登録されたキャラクター（{len(project.characters)}人）")

    for i, character in enumerate(project.characters):
        with st.container(border=True):
            col1, col2, col3 = st.columns([5, 1, 1])

            with col1:
                st.markdown(f"### {character.name}")
                if character.role:
                    st.caption(f"役割: {character.role}")
                st.markdown("**性格**")
                st.write(character.personality)
                if character.background:
                    st.markdown("**背景**")
                    st.write(character.background)

            with col2:
                if st.button("編集", key=f"edit_char_{i}"):
                    st.session_state[f"editing_char_{i}"] = True

            with col3:
                if st.button("削除", key=f"delete_char_{i}"):
                    project.characters.pop(i)
                    storage.save_project(project)
                    st.rerun()

            # 編集モード
            if st.session_state.get(f"editing_char_{i}", False):
                st.markdown("---")
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    edited_name = st.text_input("名前", value=character.name, key=f"edit_name_{i}")
                    edited_role = st.text_input("役割", value=character.role or "", key=f"edit_role_{i}")
                with edit_col2:
                    edited_personality = st.text_area("性格", value=character.personality, key=f"edit_personality_{i}", height=100)
                    edited_background = st.text_area("背景", value=character.background or "", key=f"edit_background_{i}", height=100)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("保存", key=f"save_edit_{i}"):
                        project.characters[i].name = edited_name
                        project.characters[i].role = edited_role if edited_role else None
                        project.characters[i].personality = edited_personality
                        project.characters[i].background = edited_background if edited_background else None
                        storage.save_project(project)
                        st.session_state[f"editing_char_{i}"] = False
                        st.rerun()
                with col_b:
                    if st.button("キャンセル", key=f"cancel_edit_{i}"):
                        st.session_state[f"editing_char_{i}"] = False
                        st.rerun()
else:
    st.info("まだキャラクターが登録されていません。上のボタンからキャラクターを生成してください。")

# ナビゲーション
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← ステップ3に戻る"):
        st.switch_page("pages/3_プロット作成.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
with col3:
    if st.button("次のステップへ →", type="primary"):
        if project.characters:
            st.switch_page("pages/5_執筆設定.py")
        else:
            st.error("少なくとも1人のキャラクターを作成してください")
