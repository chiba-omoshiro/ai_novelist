"""
AI API連携モジュール
Gemini と Claude API を使用したテキスト生成
"""
import os
from typing import Optional
import google.generativeai as genai
from anthropic import Anthropic


class AIClient:
    """AI API クライアント"""

    def __init__(self):
        # API キーの読み込み
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # Gemini の初期化
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.gemini_flash = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.gemini_pro = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')

        # Claude の初期化
        if self.anthropic_api_key:
            self.anthropic = Anthropic(api_key=self.anthropic_api_key)

    def generate_idea_fragments(self, count: int = 20) -> list[str]:
        """アイデアの断片を生成（Gemini Flash使用）"""
        if not self.google_api_key:
            return ["APIキーが設定されていません"]

        prompt = f"""
小説のアイデアとなる魅力的なフレーズや断片を{count}個生成してください。
以下のカテゴリーからバランスよく選んでください：

- 設定（舞台、世界観）
- キャラクター要素（人物の特徴、職業、性格）
- 出来事（事件、遭遇、発見）
- テーマ（愛、冒険、成長、裏切り、など）
- 物（アイテム、遺物、武器、書物）
- 雰囲気（ミステリアス、ノスタルジック、緊張感）

各フレーズは1-2行程度で、創造力を刺激する具体的で印象的なものにしてください。
番号付きリストで出力してください。
"""

        try:
            response = self.gemini_flash.generate_content(prompt)
            # レスポンスを行ごとに分割して、各アイデアを抽出
            lines = response.text.strip().split('\n')
            fragments = []
            for line in lines:
                line = line.strip()
                if line and any(line.startswith(f"{i}.") for i in range(1, count + 1)):
                    # 番号を削除
                    fragment = line.split('.', 1)[1].strip()
                    fragments.append(fragment)

            return fragments if fragments else [response.text]
        except Exception as e:
            return [f"エラー: {str(e)}"]

    def expand_ideas(self, selected_fragments: list[str]) -> str:
        """選択された断片からアイデアを膨らませる（Gemini Flash使用）"""
        if not self.google_api_key:
            return "APIキーが設定されていません"

        fragments_text = "\n".join(f"- {f}" for f in selected_fragments)
        prompt = f"""
以下のアイデアの断片を組み合わせて、小説の核となる魅力的なコンセプトを3-4段落で説明してください：

{fragments_text}

これらの要素を自然に組み合わせ、独創的で面白い物語の方向性を提示してください。
"""

        try:
            response = self.gemini_flash.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"エラー: {str(e)}"

    def generate_setting(self, idea_text: str) -> str:
        """設定を生成（Gemini Flash使用）"""
        if not self.google_api_key:
            return "APIキーが設定されていません"

        prompt = f"""
以下のアイデアに基づいて、小説の基本設定を2-3文で簡潔に書いてください：

{idea_text}

設定には以下を含めてください：
- 主人公の基本情報
- 物語の始まりとなる状況や出来事
- 舞台となる世界や時代（必要に応じて）
"""

        try:
            response = self.gemini_flash.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"エラー: {str(e)}"

    def generate_plot(self, setting: str) -> str:
        """プロットを生成（Gemini Flash使用）"""
        if not self.google_api_key:
            return "APIキーが設定されていません"

        prompt = f"""
以下の設定に基づいて、小説のプロットを作成してください：

{setting}

プロットには以下の要素を含めてください：
1. 発端（物語の始まり）
2. 展開（事件や困難の発生）
3. クライマックス（最大の山場）
4. 結末（物語の締めくくり）

各要素を2-3文で説明してください。
"""

        try:
            response = self.gemini_flash.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"エラー: {str(e)}"

    def generate_characters(self, setting: str, plot: str, count: int = 3) -> list[dict]:
        """登場人物を生成（Gemini Flash使用）"""
        if not self.google_api_key:
            return [{"name": "エラー", "personality": "APIキーが設定されていません"}]

        prompt = f"""
以下の設定とプロットに基づいて、主要な登場人物を{count}人作成してください：

【設定】
{setting}

【プロット】
{plot}

各キャラクターについて以下の情報をJSON形式で出力してください：
- name: 名前
- role: 役割（主人公、ライバル、メンター、など）
- personality: 性格（2-3文）
- background: 背景（簡単な経歴や動機）

JSON配列形式で出力してください。
"""

        try:
            response = self.gemini_flash.generate_content(prompt)
            # JSONパースを試みる（簡易的な実装）
            import json
            import re

            # JSON部分を抽出
            text = response.text
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                characters = json.loads(json_match.group())
                return characters
            else:
                # JSONが見つからない場合はテキストを返す
                return [{"name": "生成失敗", "personality": text}]
        except Exception as e:
            return [{"name": "エラー", "personality": str(e)}]

    def generate_novel_prompt(
        self,
        setting: str,
        plot: str,
        characters: list[dict],
        length: str,
        style: str,
        tone: str,
        ai_platform: str = "claude"
    ) -> str:
        """チャットAI用の小説執筆プロンプトを生成"""

        characters_text = "\n".join(
            f"- **{c.get('name', '名前なし')}** ({c.get('role', '役割不明')})\n"
            f"  - 性格: {c.get('personality', '')}\n"
            f"  - 背景: {c.get('background', '不明')}"
            for c in characters
        )

        length_guide = {
            "短編": "2000-3000文字程度",
            "中編": "5000-8000文字程度",
            "長編": "10000文字以上"
        }

        # プラットフォーム別の推奨事項
        platform_notes = {
            "claude": "# Claude用プロンプト\n\n長文生成に優れています。必要に応じて「続きを書いて」と指示してください。",
            "chatgpt": "# ChatGPT用プロンプト\n\n長文の場合は複数回に分けて生成を依頼してください。",
            "gemini": "# Gemini用プロンプト\n\n長文生成が可能です。プロンプトをそのまま貼り付けて使用してください。"
        }

        prompt = f"""{platform_notes.get(ai_platform, '')}

あなたはプロの小説家です。以下の設定に基づいて、魅力的な小説を執筆してください。

## 📖 基本設定

{setting}

## 📋 プロット（物語の流れ）

{plot}

## 👥 登場人物

{characters_text}

## ✍️ 執筆指示（必ず守ってください）

### 分量
{length}（目安: {length_guide.get(length, '')}）

### 文体
{style}で書いてください。

### 雰囲気・読後感
{tone}雰囲気の作品にしてください。

## 📝 執筆のポイント

1. **心理描写**: 登場人物の内面を丁寧に描写してください
2. **情景描写**: 五感を使った描写で読者を物語の世界に引き込んでください
3. **プロット遵守**: 上記のプロットに沿いつつも、自然な展開を心がけてください
4. **文体の統一**: 指定された文体「{style}」を最後まで維持してください
5. **雰囲気の維持**: 「{tone}」という読後感を意識して執筆してください
6. **完成度**: 途中で終わらせず、起承転結のある完結した作品にしてください

---

それでは、上記の設定に基づいて小説を執筆してください。
"""

        return prompt

    def write_novel(
        self,
        setting: str,
        plot: str,
        characters: list[dict],
        length: str,
        style: str,
        tone: str,
        model: str = "haiku3.5"
    ) -> str:
        """小説本文を執筆"""

        # モデルに応じて適切なAPIを使用
        if model == "gemini2.5pro":
            return self._write_with_gemini(setting, plot, characters, length, style, tone)
        else:
            return self._write_with_claude(setting, plot, characters, length, style, tone, model)

    def _write_with_gemini(
        self,
        setting: str,
        plot: str,
        characters: list[dict],
        length: str,
        style: str,
        tone: str
    ) -> str:
        """Gemini Pro で小説を執筆"""
        if not self.google_api_key:
            return "APIキーが設定されていません"

        characters_text = "\n".join(
            f"- {c.get('name', '名前なし')}: {c.get('personality', '')}"
            for c in characters
        )

        length_guide = {
            "短編": "2000-3000文字程度",
            "中編": "5000-8000文字程度",
            "長編": "10000文字以上"
        }

        prompt = f"""
以下の要素に基づいて、小説を執筆してください：

【設定】
{setting}

【プロット】
{plot}

【登場人物】
{characters_text}

【執筆指示】
- 長さ: {length}（{length_guide.get(length, '')}）
- 文体: {style}
- 雰囲気・読後感: {tone}

物語を魅力的に描写し、読者を引き込む小説を書いてください。
"""

        try:
            response = self.gemini_pro.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"エラー: {str(e)}"

    def _write_with_claude(
        self,
        setting: str,
        plot: str,
        characters: list[dict],
        length: str,
        style: str,
        tone: str,
        model: str
    ) -> str:
        """Claude で小説を執筆"""
        if not self.anthropic_api_key:
            return "APIキーが設定されていません"

        characters_text = "\n".join(
            f"- {c.get('name', '名前なし')}: {c.get('personality', '')}"
            for c in characters
        )

        length_guide = {
            "短編": "2000-3000文字程度",
            "中編": "5000-8000文字程度",
            "長編": "10000文字以上"
        }

        prompt = f"""
以下の要素に基づいて、小説を執筆してください：

【設定】
{setting}

【プロット】
{plot}

【登場人物】
{characters_text}

【執筆指示】
- 長さ: {length}（{length_guide.get(length, '')}）
- 文体: {style}
- 雰囲気・読後感: {tone}

物語を魅力的に描写し、読者を引き込む小説を書いてください。
"""

        # モデル名の変換と最大トークン数の設定
        model_map = {
            "haiku3.5": "claude-3-5-haiku-20241022",
            "sonnet4.5": "claude-sonnet-4-20250514"
        }

        # モデルごとの最大トークン数
        max_tokens_map = {
            "haiku3.5": 8192,
            "sonnet4.5": 8192
        }

        try:
            response = self.anthropic.messages.create(
                model=model_map.get(model, "claude-3-5-haiku-20241022"),
                max_tokens=max_tokens_map.get(model, 8192),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"エラー: {str(e)}"
