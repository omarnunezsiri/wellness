"""
AI-powered task celebration and motivation system.

This module provides AI-generated motivational responses for task completion
using Google's Gemini API. It focuses specifically on task-related celebrations
with a warm, autumn-themed personality.
"""

from html import escape

from google import genai
from google.genai import types


class TaskAI:
    """
    AI client for generating task-related motivational responses.

    This class provides AI-powered celebratory messages when users complete tasks,
    maintaining a warm, encouraging, autumn-themed personality. It uses Google's
    Gemini API to generate personalized responses while ensuring input sanitization
    for security.

    Attributes:
        client: Google Gemini AI client instance
        config: AI generation configuration with autumn-themed personality
        model: Gemini model identifier for text generation
    """

    def __init__(self, api_key: str):
        """Initialize the TaskAI client with Gemini API configuration."""
        self.client = genai.Client(api_key=api_key)

        self.config = types.GenerateContentConfig(
            system_instruction="""You are a warm, encouraging wellness companion with a cozy autumn vibe.
            When a user completes a task, respond with genuine celebration and motivation. Keep responses:
            - Sweet and supportive (like a caring friend by a fireplace)
            - Motivational but not overwhelming
            - Cozy and comforting in tone with autumn warmth
            - 1 sentence max
            - Focus on their progress and self-care
            - Use warm, gentle language but also casual and friendly
            - Be genuinely excited about their accomplishment
            - Make it feel personal and heartfelt
            - Use autumn-themed emojis: 🍂 🧡 🌟 🍯 ✨ 🌙 🕯️ 🌻 ☕ 🥧
            - Channel the feeling of golden hour, cozy sweaters, and warm drinks""",
            temperature=0.8,
            max_output_tokens=40,
            candidate_count=1,
            top_p=0.8,
            top_k=20,
            response_mime_type="text/plain",
            presence_penalty=0.1,
            frequency_penalty=0.1,
        )

        self.model = "gemini-2.0-flash-001"

    def celebrate_task_completion(self, completed_task: str) -> str:
        """Generate a celebratory message for completing a task."""
        safe_task = escape(completed_task.strip()) if completed_task else ""

        if not safe_task:
            return "Great job completing your task! You're taking wonderful care of yourself. 🌟"

        prompt = f"Completed task: {safe_task}\n\nCelebrate this accomplishment:"

        try:
            response = self.client.models.generate_content(model=self.model, contents=prompt, config=self.config)
            return response.text.strip() if response.text else self._get_fallback_message(safe_task)

        except Exception as e:
            print(f"TaskAI service error: {type(e).__name__}")
            return self._get_fallback_message(safe_task)

    def _get_fallback_message(self, task: str) -> str:
        return f"Beautiful work completing '{task}'! You're taking such good care of yourself. 🌟"
