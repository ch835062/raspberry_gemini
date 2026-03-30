"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
        )
        pass

    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
        )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        print("使用者輸入的內容：")
        messages = body.get("messages", [])
        if messages:
            last_user_message = next(
                (m["content"] for m in reversed(messages) if m.get("role") == "user"),
                None
            )
            if last_user_message:
                print(f"使用者輸入內容: {last_user_message}")
        

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        print("模型輸出的內容：")
        messages = body.get("messages", [])
        if messages:
            last_assistant_message = next(
                (m["content"] for m in reversed(messages) if m.get("role") == "assistant"),
                None
            )
            if last_assistant_message:
                print(f"模型輸出內容: {last_assistant_message}")
        
        return body
