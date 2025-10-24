"""
ステップ3: プロット作成
物語の流れを組み立てる
"""
import streamlit as st
from modules.data_models import Plot

st.set_page_config(page_title="プロット作成", page_icon="📋", layout="wide")

# セッション状態の確認
if 'current_project' not in st.session_state or st.session_state.current_project is None:
    st.error("プロジェクトが選択されていません")
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
    st.stop()

project = st.session_state.current_project
ai_client = st.session_state.ai_client
storage = st.session_state.storage

st.title("📋 ステップ3: プロット作成")
st.markdown("設定を基に、物語の流れを作成します。")

# 設定が選択されているか確認
if project.selected_setting_index is None or not project.settings:
    st.warning("ステップ2で設定を選択してください")
    if st.button("← ステップ2に戻る"):
        st.switch_page("pages/2_設定決定.py")
    st.stop()

selected_setting = project.settings[project.selected_setting_index]

# 選択された設定を表示
st.subheader("使用する設定")
with st.expander("設定を表示"):
    st.write(selected_setting.text)

st.divider()

# プロットの生成
st.subheader("プロットを生成")

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("プロットを生成", type="primary", use_container_width=True):
        with st.spinner("AIがプロットを生成中..."):
            plot_text = ai_client.generate_plot(selected_setting.text)

            # プロットを追加
            new_plot = Plot(text=plot_text)
            project.plots.append(new_plot)
            storage.save_project(project)
            st.success("プロットを生成しました")
            st.rerun()

# 手動でプロットを追加
with st.expander("手動でプロットを入力"):
    manual_plot = st.text_area(
        "プロットを入力",
        placeholder="発端、展開、クライマックス、結末を記述してください",
        height=200
    )
    if st.button("手動プロットを追加"):
        if manual_plot.strip():
            new_plot = Plot(text=manual_plot.strip())
            project.plots.append(new_plot)
            storage.save_project(project)
            st.success("プロットを追加しました")
            st.rerun()
        else:
            st.error("プロットを入力してください")

st.divider()

# 生成されたプロットを表示＆選択
if project.plots:
    st.subheader("生成されたプロット（複数保存可能）")

    for i, plot in enumerate(project.plots):
        with st.container(border=True):
            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                st.markdown(f"**プロット {i+1}**")
                st.write(plot.text)

                # このプロットを選択
                is_selected = (project.selected_plot_index == i)
                if st.checkbox("このプロットを使用", value=is_selected, key=f"select_plot_{i}"):
                    project.selected_plot_index = i
                    storage.save_project(project)

            with col2:
                if st.button("編集", key=f"edit_plot_{i}"):
                    st.session_state[f"editing_plot_{i}"] = True

            with col3:
                if st.button("削除", key=f"delete_plot_{i}"):
                    project.plots.pop(i)
                    if project.selected_plot_index == i:
                        project.selected_plot_index = None
                    elif project.selected_plot_index and project.selected_plot_index > i:
                        project.selected_plot_index -= 1
                    storage.save_project(project)
                    st.rerun()

            # 編集モード
            if st.session_state.get(f"editing_plot_{i}", False):
                edited_text = st.text_area(
                    "プロットを編集",
                    value=plot.text,
                    key=f"edit_text_{i}",
                    height=200
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("保存", key=f"save_edit_{i}"):
                        project.plots[i].text = edited_text
                        storage.save_project(project)
                        st.session_state[f"editing_plot_{i}"] = False
                        st.rerun()
                with col_b:
                    if st.button("キャンセル", key=f"cancel_edit_{i}"):
                        st.session_state[f"editing_plot_{i}"] = False
                        st.rerun()

    # 選択状態の表示
    if project.selected_plot_index is not None:
        st.success(f"プロット {project.selected_plot_index + 1} を使用します")

# ナビゲーション
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← ステップ2に戻る"):
        st.switch_page("pages/2_設定決定.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
with col3:
    if st.button("次のステップへ →", type="primary"):
        if project.selected_plot_index is not None:
            st.switch_page("pages/4_登場人物.py")
        else:
            st.error("使用するプロットを選択してください")
