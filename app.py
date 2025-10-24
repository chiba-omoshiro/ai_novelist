"""
AI小説家 - メインアプリケーション
ローカルで動作するStreamlitアプリ
"""
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

from modules.data_models import NovelProject
from modules.storage import ProjectStorage
from modules.ai_client import AIClient

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="AI小説家",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# セッション状態の初期化
if 'storage' not in st.session_state:
    st.session_state.storage = ProjectStorage()

if 'ai_client' not in st.session_state:
    st.session_state.ai_client = AIClient()

if 'current_project' not in st.session_state:
    st.session_state.current_project = None

if 'project_name' not in st.session_state:
    st.session_state.project_name = ""


def save_current_project():
    """現在のプロジェクトを保存"""
    if st.session_state.current_project:
        st.session_state.storage.save_project(st.session_state.current_project)


def load_project(project_name: str):
    """プロジェクトを読み込み"""
    project = st.session_state.storage.load_project(project_name)
    if project:
        st.session_state.current_project = project
        st.session_state.project_name = project_name
        return True
    return False


def create_new_project(project_name: str):
    """新規プロジェクトを作成"""
    st.session_state.current_project = NovelProject(project_name=project_name)
    st.session_state.project_name = project_name
    save_current_project()


# メインUI
st.title("📚 AI小説家")
st.markdown("AIと一緒に小説を創作するアプリケーション")

# サイドバー - プロジェクト管理
with st.sidebar:
    st.header("プロジェクト管理")

    # API キーの確認
    st.subheader("API設定")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if google_api_key:
        st.success("✓ Google API キー設定済み")
    else:
        st.warning("⚠ Google API キーが未設定")

    if anthropic_api_key:
        st.success("✓ Anthropic API キー設定済み")
    else:
        st.warning("⚠ Anthropic API キーが未設定")

    st.divider()

    # プロジェクト選択
    project_mode = st.radio(
        "モードを選択",
        ["新規プロジェクト", "既存プロジェクトを開く"],
        key="project_mode"
    )

    if project_mode == "新規プロジェクト":
        new_project_name = st.text_input(
            "プロジェクト名",
            placeholder="例: 異世界冒険譚"
        )

        if st.button("プロジェクトを作成", type="primary", use_container_width=True):
            if new_project_name:
                if st.session_state.storage.project_exists(new_project_name):
                    st.error("同名のプロジェクトが既に存在します")
                else:
                    create_new_project(new_project_name)
                    st.success(f"プロジェクト '{new_project_name}' を作成しました")
                    st.rerun()
            else:
                st.error("プロジェクト名を入力してください")

    else:  # 既存プロジェクトを開く
        projects = st.session_state.storage.list_projects()

        if projects:
            selected_project = st.selectbox(
                "プロジェクトを選択",
                projects,
                key="selected_project"
            )

            if st.button("プロジェクトを開く", type="primary", use_container_width=True):
                if load_project(selected_project):
                    st.success(f"プロジェクト '{selected_project}' を開きました")
                    st.rerun()
                else:
                    st.error("プロジェクトの読み込みに失敗しました")

            # プロジェクト削除
            if st.button("プロジェクトを削除", use_container_width=True):
                if st.session_state.storage.delete_project(selected_project):
                    st.success(f"プロジェクト '{selected_project}' を削除しました")
                    if st.session_state.project_name == selected_project:
                        st.session_state.current_project = None
                        st.session_state.project_name = ""
                    st.rerun()
        else:
            st.info("保存されているプロジェクトはありません")

    # 現在のプロジェクト情報
    if st.session_state.current_project:
        st.divider()
        st.subheader("現在のプロジェクト")
        st.write(f"**{st.session_state.project_name}**")

        # 進捗状況
        progress = []
        if st.session_state.current_project.idea_fragments:
            progress.append("✓ アイデア選択")
        if st.session_state.current_project.settings:
            progress.append("✓ 設定決定")
        if st.session_state.current_project.plots:
            progress.append("✓ プロット作成")
        if st.session_state.current_project.characters:
            progress.append("✓ 登場人物")
        if st.session_state.current_project.writing_config:
            progress.append("✓ 執筆設定")
        if st.session_state.current_project.novel_text:
            progress.append("✓ 本文執筆")

        if progress:
            st.write("進捗:")
            for p in progress:
                st.write(p)

        if st.button("プロジェクトを保存", use_container_width=True):
            save_current_project()
            st.success("保存しました")

# メインコンテンツ
if st.session_state.current_project:
    st.success(f"現在のプロジェクト: **{st.session_state.project_name}**")

    st.markdown("""
    ### 📝 作成ステップ

    左のサイドバーから各ステップのページに移動して、小説を作成していきましょう。

    1. **アイデア選択** - AIが提示するフレーズから選んでアイデアを膨らませる
    2. **設定決定** - 物語の基本設定を決める
    3. **プロット作成** - 物語の流れを組み立てる
    4. **登場人物** - キャラクターを作成する
    5. **執筆設定** - 長さ、文体、雰囲気を指定する
    6. **本文執筆** - AIに小説を書いてもらう

    各ステップで複数のバージョンを保存でき、前のステップに戻って変更することもできます。
    """)

    # ナビゲーションボタン
    st.markdown("### 🚀 次のステップへ")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("1. アイデア選択 →", use_container_width=True):
            st.switch_page("pages/1_アイデア選択.py")

    with col2:
        if st.button("2. 設定決定 →", use_container_width=True):
            st.switch_page("pages/2_設定決定.py")

    with col3:
        if st.button("3. プロット作成 →", use_container_width=True):
            st.switch_page("pages/3_プロット作成.py")

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("4. 登場人物 →", use_container_width=True):
            st.switch_page("pages/4_登場人物.py")

    with col5:
        if st.button("5. 執筆設定 →", use_container_width=True):
            st.switch_page("pages/5_執筆設定.py")

    with col6:
        if st.button("6. 本文執筆 →", use_container_width=True):
            st.switch_page("pages/6_本文執筆.py")

else:
    st.info("👈 左のサイドバーから新規プロジェクトを作成するか、既存のプロジェクトを開いてください")

    st.markdown("""
    ### AI小説家の使い方

    1. **APIキーの設定**
        - `.env` ファイルを作成して、以下のAPIキーを設定してください
        - `GOOGLE_API_KEY`: Google Gemini API
        - `ANTHROPIC_API_KEY`: Anthropic Claude API

    2. **プロジェクトの作成**
        - サイドバーから「新規プロジェクト」を選び、プロジェクト名を入力

    3. **小説の作成**
        - 6つのステップを順番に進めていきます
        - 各ステップで複数のバリエーションを試すことができます
        - 前のステップに戻って変更することも可能です

    4. **プロジェクトの保存**
        - 作業内容は自動的に保存されます
        - 複数のプロジェクトを管理できます
    """)
