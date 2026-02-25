"""Pure-function workflow engine for processing decision-tree workflows."""

from typing import Any


def get_node(workflow_def: dict, node_id: str) -> dict | None:
    """Get a node from the workflow definition by ID."""
    return workflow_def.get("nodes", {}).get(node_id)


def get_root_node_id(workflow_def: dict) -> str:
    """Get the root node ID from the workflow definition."""
    return workflow_def.get("root_node_id", "")


def is_terminal(node: dict) -> bool:
    """Check if a node is a terminal (finding) node."""
    return node.get("type") == "terminal"


def resolve_next_node(workflow_def: dict, node_id: str, answer: Any) -> str | None:
    """Given a node and an answer, resolve the next node ID.

    For 'select' inputs: match the answer value to an option's next_node_id.
    For 'group' inputs: evaluate next_node_rules conditions.
    For other inputs: use the node's direct next_node_id.
    """
    node = get_node(workflow_def, node_id)
    if not node or is_terminal(node):
        return None

    input_type = node.get("input_type", "text")

    if input_type == "select":
        for option in node.get("options", []):
            if option.get("value") == answer:
                return option.get("next_node_id")
        return None

    if input_type == "group":
        # answer is a dict of field values; evaluate next_node_rules
        rules = node.get("next_node_rules", [])
        for rule in rules:
            condition = rule.get("condition", {})
            field = condition.get("field")
            op = condition.get("op")
            value = condition.get("value")

            if field and isinstance(answer, dict):
                actual = answer.get(field)
                if op == "eq" and actual == value:
                    return rule.get("next_node_id")
                if op == "neq" and actual != value:
                    return rule.get("next_node_id")

        # If no rule matched, use default_next_node_id or last rule's fallback
        return node.get("default_next_node_id")

    # For text/textarea/date/number: direct next_node_id
    return node.get("next_node_id")


def get_terminal_finding(node: dict) -> dict:
    """Extract the finding information from a terminal node."""
    return {
        "finding_type": node.get("finding_type", "observation"),
        "title": node.get("title", ""),
        "recommendation": node.get("recommendation", ""),
    }


def build_breadcrumb_trail(
    workflow_def: dict, answers: dict
) -> list[dict]:
    """Build an ordered trail of answered questions for display.

    Returns a list of dicts: [{"node_id": ..., "prompt": ..., "answer_display": ...}, ...]
    """
    trail = []
    current_id = get_root_node_id(workflow_def)

    while current_id:
        node = get_node(workflow_def, current_id)
        if not node or is_terminal(node):
            break

        if current_id not in answers:
            break

        answer = answers[current_id]
        answer_display = _format_answer_display(node, answer)

        trail.append({
            "node_id": current_id,
            "prompt": node.get("prompt", ""),
            "answer_display": answer_display,
        })

        next_id = resolve_next_node(workflow_def, current_id, answer)
        current_id = next_id

    return trail


def get_current_node_id(workflow_def: dict, answers: dict) -> str:
    """Walk the workflow using existing answers to find the current unanswered node."""
    current_id = get_root_node_id(workflow_def)

    while current_id:
        node = get_node(workflow_def, current_id)
        if not node or is_terminal(node):
            return current_id

        if current_id not in answers:
            return current_id

        next_id = resolve_next_node(workflow_def, current_id, answers[current_id])
        if not next_id:
            return current_id
        current_id = next_id

    return current_id


def _format_answer_display(node: dict, answer: Any) -> str:
    """Format an answer for human-readable display."""
    input_type = node.get("input_type", "text")

    if input_type == "select":
        for option in node.get("options", []):
            if option.get("value") == answer:
                return option.get("label", answer)
        return str(answer)

    if input_type == "group" and isinstance(answer, dict):
        parts = []
        for field_def in node.get("fields", []):
            name = field_def.get("name")
            label = field_def.get("label", name)
            val = answer.get(name, "")
            if val:
                # For select fields within groups, resolve the label
                if field_def.get("input_type") == "select":
                    for opt in field_def.get("options", []):
                        if opt.get("value") == val:
                            val = opt.get("label", val)
                            break
                parts.append(f"{label}: {val}")
        return "; ".join(parts) if parts else str(answer)

    return str(answer)
