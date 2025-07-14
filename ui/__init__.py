# ui/__init__.py
"""
Wolfkit UI Package - Refactored for clean separation of concerns
Main components after Phase 3 refactoring
"""

from .app_frame import AppFrame
from .base_tab import BaseTab
from .main_workflow_tab import MainWorkflowTab
from .code_review_tab import CodeReviewTab
from .document_merge_tab import DocumentMergeTab
from .documentation_tab import DocumentationTab

# Import widgets package for convenience
from . import widgets

__all__ = [
    'AppFrame',
    'BaseTab',
    'MainWorkflowTab', 
    'CodeReviewTab',
    'DocumentMergeTab',
    'DocumentationTab',
    'widgets'
]