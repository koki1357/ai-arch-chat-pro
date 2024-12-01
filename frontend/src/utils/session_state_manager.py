import streamlit as st
from datetime import datetime
from typing import Any


class SessionStateManager:
    @staticmethod
    def initialize_states():
        """Initialize all session states"""
        states = {
            'current_system_description': "",
            'search_results': [],
            'chat_history': [],
            'selected_system': None,
            'last_update': datetime.utcnow()
        }

        for key, default_value in states.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def get_state(key: str) -> Any:
        """Get value from session state"""
        return st.session_state.get(key)

    @staticmethod
    def set_state(key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value
        st.session_state.last_update = datetime.utcnow()

    @staticmethod
    def add_chat_message(role: str, content: str):
        """Add new message to chat history"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })

    @staticmethod
    def clear_chat_history():
        """Clear chat history"""
        st.session_state.chat_history = []
