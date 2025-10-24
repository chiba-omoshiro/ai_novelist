"""
ステップ1: アイデア選択
AIが提示するフレーズから選んでアイデアを膨らませる
"""
import streamlit as st
from modules.data_models import IdeaFragment

st.set_page_config(page_title="アイデア選択", page_icon="💡", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    st.info("メインページに戻ってプロジェクトを作成または選択してください")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
ai_client = st.session_state.ai_client
storage = st.session_state.storage

st.title("💡 ステップ1: アイデア選択")
st.markdown("AIが提示するフレーズや断片から、興味深いものを選んでアイデアを膨らませましょう。")

# タブで機能を分ける
tab1, tab2 = st.tabs(["アイデア断片の生成", "選択したアイデアを膨らませる"])

with tab1:
    st.subheader("アイデア断片を生成")

    col1, col2 = st.columns([3, 1])
    with col1:
        fragment_count = st.slider("生成する断片の数", 10, 30, 20)
    with col2:
        if st.button("生成", type="primary", use_container_width=True):
            with st.spinner("AIがアイデアを生成中..."):
                fragments = ai_client.generate_idea_fragments(fragment_count)

                # IdeaFragmentオブジェクトに変換
                project.idea_fragments = [
                    IdeaFragment(text=f, selected=False)
                    for f in fragments
                ]
                storage.save_project(project)
                st.success(f"{len(fragments)}個のアイデア断片を生成しました")
                st.rerun()

    # 生成されたフレーズを表示＆選択
    if project.idea_fragments:
        st.markdown("### 生成されたアイデア断片")
        st.markdown("興味深いものにチェックを入れてください（複数選択可）")

        # チェックボックスで選択
        for i, fragment in enumerate(project.idea_fragments):
            key = f"fragment_{i}"
            checked = st.checkbox(
                fragment.text,
                value=fragment.selected,
                key=key
            )
            project.idea_fragments[i].selected = checked

        # 選択を保存
        if st.button("選択を保存", use_container_width=True):
            storage.save_project(project)
            st.success("選択を保存しました")
            selected_count = sum(1 for f in project.idea_fragments if f.selected)
            st.info(f"{selected_count}個のアイデアを選択中")

with tab2:
    st.subheader("選択したアイデアを膨らませる")

    selected_fragments = [f for f in project.idea_fragments if f.selected]

    if not selected_fragments:
        st.warning("まず「アイデア断片の生成」タブでアイデアを選択してください")
    else:
        st.markdown(f"**選択中のアイデア: {len(selected_fragments)}個**")

        # 選択されたフレーズを表示
        with st.expander("選択したアイデア断片を表示"):
            for fragment in selected_fragments:
                st.write(f"- {fragment.text}")

        if st.button("アイデアを膨らませる", type="primary", use_container_width=True):
            with st.spinner("AIがアイデアを膨らませています..."):
                selected_texts = [f.text for f in selected_fragments]
                expanded_idea = ai_client.expand_ideas(selected_texts)

                # 膨らませたアイデアをリストに追加
                if expanded_idea not in project.expanded_ideas:
                    project.expanded_ideas.append(expanded_idea)
                    storage.save_project(project)
                    st.success("アイデアを膨らませました")
                    st.rerun()

        # 膨らませたアイデアを表示
        if project.expanded_ideas:
            st.markdown("### 膨らませたアイデア（複数保存可能）")

            for i, idea in enumerate(project.expanded_ideas):
                with st.container(border=True):
                    st.markdown(f"**バージョン {i+1}**")
                    st.write(idea)

                    col1, col2 = st.columns([5, 1])
                    with col2:
                        if st.button("削除", key=f"delete_idea_{i}"):
                            project.expanded_ideas.pop(i)
                            storage.save_project(project)
                            st.rerun()

# ナビゲーション
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← メインページに戻る"):
        st.switch_page("app.py")
with col2:
    if st.button("次のステップへ →", type="primary"):
        if project.expanded_ideas:
            st.switch_page("pages/2_設定決定.py")
        else:
            st.error("まずアイデアを膨らませてください")
