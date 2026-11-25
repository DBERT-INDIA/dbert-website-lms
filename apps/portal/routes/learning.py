"""Routes for the existing Guided Learning handlers."""

from flask import Blueprint
from app import (
    api_learning_v2_concept_tree,
    api_learning_v2_reviews_due,
    api_learning_v2_session,
    api_learning_v2_turn,
)

learning_bp = Blueprint("learning", __name__)
learning_bp.add_url_rule("/api/learning/v2/session", view_func=api_learning_v2_session, methods=["POST"])
learning_bp.add_url_rule("/api/learning/v2/turn", view_func=api_learning_v2_turn, methods=["POST"])
learning_bp.add_url_rule("/api/learning/v2/reviews-due", view_func=api_learning_v2_reviews_due)
learning_bp.add_url_rule("/api/learning/v2/concept-tree/<int:course_id>", view_func=api_learning_v2_concept_tree)
