"""
ストレージ管理
プロジェクトの保存・読み込み機能
"""
import os
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .data_models import NovelProject


class ProjectStorage:
    """プロジェクトの保存・読み込みを管理"""

    def __init__(self, base_dir: str = "data/projects"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_project(self, project: NovelProject) -> bool:
        """プロジェクトを保存"""
        try:
            project.updated_at = datetime.now().isoformat()
            file_path = self._get_project_path(project.project_name)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(project.to_json())

            return True
        except Exception as e:
            print(f"プロジェクト保存エラー: {e}")
            return False

    def load_project(self, project_name: str) -> Optional[NovelProject]:
        """プロジェクトを読み込み"""
        try:
            file_path = self._get_project_path(project_name)

            if not file_path.exists():
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                json_str = f.read()

            return NovelProject.from_json(json_str)
        except Exception as e:
            print(f"プロジェクト読み込みエラー: {e}")
            return None

    def list_projects(self) -> List[str]:
        """保存されているプロジェクト一覧を取得"""
        try:
            projects = []
            for file_path in self.base_dir.glob("*.json"):
                project_name = file_path.stem
                projects.append(project_name)
            return sorted(projects)
        except Exception as e:
            print(f"プロジェクト一覧取得エラー: {e}")
            return []

    def delete_project(self, project_name: str) -> bool:
        """プロジェクトを削除"""
        try:
            file_path = self._get_project_path(project_name)

            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"プロジェクト削除エラー: {e}")
            return False

    def project_exists(self, project_name: str) -> bool:
        """プロジェクトが存在するか確認"""
        file_path = self._get_project_path(project_name)
        return file_path.exists()

    def _get_project_path(self, project_name: str) -> Path:
        """プロジェクトファイルのパスを取得"""
        # ファイル名に使えない文字を置換
        safe_name = "".join(
            c if c.isalnum() or c in (' ', '_', '-') else '_'
            for c in project_name
        )
        return self.base_dir / f"{safe_name}.json"
