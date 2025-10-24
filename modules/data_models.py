"""
データモデル定義
小説プロジェクトの各ステップのデータ構造を定義
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime
import json


@dataclass
class IdeaFragment:
    """アイデアの断片"""
    text: str
    selected: bool = False
    category: Optional[str] = None


@dataclass
class Setting:
    """設定（ステップ2）"""
    text: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Plot:
    """プロット（ステップ3）"""
    text: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Character:
    """登場人物（ステップ4）"""
    name: str
    personality: str
    background: Optional[str] = None
    role: Optional[str] = None


@dataclass
class WritingConfig:
    """執筆設定（ステップ5）"""
    length: str  # "短編", "中編", "長編"
    style: str  # "文学的", "ライトノベル風", "エッセイ風" など
    tone: str  # "明るい", "暗い", "ミステリアス" など
    ai_model: str = "haiku3.5"  # "haiku3.5", "sonnet4.5", "gemini2.5pro"


@dataclass
class NovelProject:
    """小説プロジェクト全体"""
    project_name: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # 各ステップのデータ
    idea_fragments: List[IdeaFragment] = field(default_factory=list)
    expanded_ideas: List[str] = field(default_factory=list)
    settings: List[Setting] = field(default_factory=list)
    selected_setting_index: Optional[int] = None
    plots: List[Plot] = field(default_factory=list)
    selected_plot_index: Optional[int] = None
    characters: List[Character] = field(default_factory=list)
    writing_config: Optional[WritingConfig] = None
    novel_text: str = ""

    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'NovelProject':
        """辞書からインスタンスを作成"""
        # ネストされたデータクラスを復元
        if 'idea_fragments' in data:
            data['idea_fragments'] = [
                IdeaFragment(**item) for item in data['idea_fragments']
            ]
        if 'settings' in data:
            data['settings'] = [
                Setting(**item) for item in data['settings']
            ]
        if 'plots' in data:
            data['plots'] = [
                Plot(**item) for item in data['plots']
            ]
        if 'characters' in data:
            data['characters'] = [
                Character(**item) for item in data['characters']
            ]
        if 'writing_config' in data and data['writing_config']:
            data['writing_config'] = WritingConfig(**data['writing_config'])

        return cls(**data)

    def to_json(self) -> str:
        """JSON文字列に変換"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'NovelProject':
        """JSON文字列からインスタンスを作成"""
        data = json.loads(json_str)
        return cls.from_dict(data)
