"""Math evaluation tool utilities."""

from __future__ import annotations

from langchain_core.tools import Tool


import ast

def _safe_eval(expression: str) -> str:
    """Safely evaluate a math expression using ast.literal_eval."""
    try:
        node = ast.parse(expression, mode='eval')
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.USub
        )

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Num):  # For Python <3.8
                return node.n
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                elif isinstance(node.op, ast.Sub):
                    return left - right
                elif isinstance(node.op, ast.Mult):
                    return left * right
                elif isinstance(node.op, ast.Div):
                    return left / right
                elif isinstance(node.op, ast.Pow):
                    return left ** right
                elif isinstance(node.op, ast.Mod):
                    return left % right
                else:
                    raise ValueError("Unsupported operator")
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                if isinstance(node.op, ast.USub):
                    return -operand
                else:
                    raise ValueError("Unsupported unary operator")
            else:
                raise ValueError(f"Unsupported expression: {type(node).__name__}")

        # Check for only allowed nodes
        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                raise ValueError(f"Disallowed expression: {type(n).__name__}")

        result = _eval(node)
    except Exception as exc:  # pragma: no cover - error path
        return f"Error: {exc}"
    return str(result)


def get_math_tool() -> Tool:
    """Return a simple calculator tool."""
    return Tool.from_function(
        func=_safe_eval,
        name="calculator",
        description="Evaluate a math expression.",
    )
