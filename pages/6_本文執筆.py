"""
ステップ6: 本文執筆
チャットAI用のプロンプトを生成
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
st.markdown("設定をまとめて、チャットAI用のプロンプトを生成します。")

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

st.divider()

# タブで機能を分ける
tab1, tab2 = st.tabs(["💬 プロンプト生成（推奨）", "🤖 API経由で執筆（制限あり）"])

with tab1:
    st.subheader("チャットAI用プロンプトを生成")

    st.info("""
    **推奨**: このプロンプトをClaude.ai、ChatGPT、Geminiなどのチャットに貼り付けて使用してください。

    - トークン数の制限がないため、長編小説も自由に生成できます
    - 対話しながら内容を調整・修正できます
    - コストを気にせず何度でも試せます
    """)

    # AIプラットフォーム選択
    ai_platform = st.selectbox(
        "使用するチャットAI",
        ["claude", "chatgpt", "gemini"],
        format_func=lambda x: {
            "claude": "Claude (Claude.ai)",
            "chatgpt": "ChatGPT (OpenAI)",
            "gemini": "Gemini (Google)"
        }[x]
    )

    st.markdown("### 生成されたプロンプト")

    # プロンプト生成
    if 'generated_prompt' not in st.session_state:
        st.session_state.generated_prompt = None

    if st.button("📝 プロンプトを生成", type="primary", use_container_width=True):
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

        # プロンプト生成
        prompt = ai_client.generate_novel_prompt(
            setting=selected_setting.text,
            plot=selected_plot.text,
            characters=characters_data,
            length=writing_config.length,
            style=writing_config.style,
            tone=writing_config.tone,
            ai_platform=ai_platform
        )

        st.session_state.generated_prompt = prompt
        st.success("プロンプトを生成しました！")

    # 生成されたプロンプトを表示
    if st.session_state.generated_prompt:
        # プロンプトをテキストエリアに表示（コピーしやすいように）
        prompt_text = st.text_area(
            "プロンプト（このテキストをコピーしてチャットAIに貼り付けてください）",
            value=st.session_state.generated_prompt,
            height=400,
            key="prompt_display"
        )

        # 文字数表示
        st.caption(f"文字数: {len(st.session_state.generated_prompt):,}文字")

        col1, col2, col3 = st.columns(3)

        with col1:
            # ダウンロードボタン
            st.download_button(
                label="📄 プロンプトをダウンロード",
                data=st.session_state.generated_prompt,
                file_name=f"{project.project_name}_prompt.txt",
                mime="text/plain",
                use_container_width=True
            )

        with col2:
            # プロジェクトに保存
            if st.button("💾 プロジェクトに保存", use_container_width=True):
                project.novel_text = f"[生成プロンプト]\n\n{st.session_state.generated_prompt}"
                storage.save_project(project)
                st.success("プロンプトをプロジェクトに保存しました")

        with col3:
            # クリア
            if st.button("🗑️ クリア", use_container_width=True):
                st.session_state.generated_prompt = None
                st.rerun()

        st.divider()

        # 使い方ガイド
        with st.expander("📖 使い方ガイド"):
            platform_guides = {
                "claude": """
### Claude.ai での使い方

1. [Claude.ai](https://claude.ai) にアクセス
2. 新しいチャットを開始
3. 上記のプロンプトをコピー＆ペースト
4. 送信して小説を生成
5. 「続きを書いて」と指示すれば続きを書いてくれます
6. 修正が必要な場合は「〇〇の部分をもっと詳しく」などと指示
""",
                "chatgpt": """
### ChatGPT での使い方

1. [ChatGPT](https://chat.openai.com) にアクセス
2. 新しいチャットを開始
3. 上記のプロンプトをコピー＆ペースト
4. 送信して小説を生成
5. 長編の場合は「続きを書いて」と複数回指示
6. GPT-4以上のモデル推奨（長文生成に優れています）
""",
                "gemini": """
### Gemini での使い方

1. [Gemini](https://gemini.google.com) にアクセス
2. 新しいチャットを開始
3. 上記のプロンプトをコピー＆ペースト
4. 送信して小説を生成
5. 長文生成に優れているため、一度に多くのテキストを生成できます
6. 修正が必要な場合は追加で指示を出してください
"""
            }
            st.markdown(platform_guides.get(ai_platform, ""))

with tab2:
    st.subheader("API経由で執筆（上級者向け）")

    st.warning("""
    **注意**: API経由での執筆には以下の制限があります：

    - Claude Haiku: 最大8,192トークン（約4,000-6,000文字程度）
    - コストが発生します
    - 長編小説には不向きです

    **推奨**: 「プロンプト生成」タブを使用してください。
    """)

    if st.button("🤖 API経由で執筆する", use_container_width=True):
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

    # 執筆された小説を表示
    if project.novel_text and not project.novel_text.startswith("[生成プロンプト]"):
        st.markdown("---")
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

# ナビゲーション
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("← ステップ5に戻る"):
        st.switch_page("pages/5_執筆設定.py")
with col2:
    if st.button("メインページに戻る"):
        st.switch_page("app.py")
