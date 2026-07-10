"""
    Provides a restricted, side-effect-free evaluator for portal predicate
    expressions.

    Portal activation supports an optional predicate expression that is
    evaluated against the traced frame's namespace to decide whether tracing
    should engage.  A raw :func:`eval` of that expression is a remote-code-
    execution sink whenever the expression can be supplied by a remote caller.
    :func:`evaluate_predicate` compiles the expression only after validating
    that its syntax tree contains nothing that can call code or reach dunder
    attributes, then evaluates it with builtins stripped.
"""

import ast

from typing import Any, Dict, Optional


class UnsafeExpressionError(ValueError):
    """
        Raised when a portal predicate expression uses syntax that is not on
        the read-only allow-list (calls, subscripts, dunder access, etc.).
    """


# Only these node types may appear in a portal predicate.  The set is a
# read-only expression grammar: boolean/comparison/arithmetic operators over
# names, non-dunder attribute reads and literal containers.  Notably absent
# are ast.Call, ast.Subscript, ast.Lambda, comprehensions and ast.Starred,
# none of which are needed to express a predicate and each of which can be
# turned into code execution.
_ALLOWED_NODE_TYPES = (
    ast.Expression,
    ast.BoolOp, ast.And, ast.Or,
    ast.UnaryOp, ast.Not, ast.UAdd, ast.USub, ast.Invert,
    ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow,
    ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
    ast.Name, ast.Load,
    ast.Constant,
    ast.Attribute,
    ast.List, ast.Tuple, ast.Set,
)

_DUNDER_PREFIX = "__"


def validate_expression(*, expression: str) -> ast.Expression:
    """
        Parse and validate a portal predicate expression.

        :param expression: The predicate expression source.

        :returns: The validated ``ast.Expression`` ready to compile.
        :raises: UnsafeExpressionError
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as xcpt:
        err_msg_lines = ["Portal predicate is not a valid expression."]
        err_msg_lines.append("EXPRESSION: {!r}".format(expression))
        err_msg_lines.append("CAUSE: {}".format(xcpt))
        err_msg = "\n".join(err_msg_lines)
        raise UnsafeExpressionError(err_msg) from None

    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODE_TYPES):
            err_msg_lines = [
                "Portal predicate uses a disallowed expression element."
            ]
            err_msg_lines.append("EXPRESSION: {!r}".format(expression))
            err_msg_lines.append("ELEMENT: {}".format(type(node).__name__))
            err_msg = "\n".join(err_msg_lines)
            raise UnsafeExpressionError(err_msg)

        if isinstance(node, ast.Name):
            if node.id.startswith(_DUNDER_PREFIX):
                err_msg_lines = [
                    "Portal predicate references a dunder name."
                ]
                err_msg_lines.append("EXPRESSION: {!r}".format(expression))
                err_msg_lines.append("NAME: {}".format(node.id))
                err_msg = "\n".join(err_msg_lines)
                raise UnsafeExpressionError(err_msg)

        if isinstance(node, ast.Attribute):
            if node.attr.startswith(_DUNDER_PREFIX):
                err_msg_lines = [
                    "Portal predicate reads a dunder attribute."
                ]
                err_msg_lines.append("EXPRESSION: {!r}".format(expression))
                err_msg_lines.append("ATTRIBUTE: {}".format(node.attr))
                err_msg = "\n".join(err_msg_lines)
                raise UnsafeExpressionError(err_msg)

    rtnval = tree
    return rtnval


def evaluate_predicate(*, expression: str,
                       global_ns: Optional[Dict[str, Any]] = None,
                       local_ns: Optional[Dict[str, Any]] = None) -> bool:
    """
        Validate then evaluate a portal predicate against a frame namespace.

        The expression is evaluated with an empty ``__builtins__`` so that,
        even though it may read names from the traced frame, it cannot reach
        any builtin callable.  Combined with the no-call / no-dunder grammar
        enforced by :func:`validate_expression`, evaluation cannot execute
        code or mutate state.

        :param expression: The predicate expression source.
        :param global_ns: The frame globals to resolve names against.
        :param local_ns: The frame locals to resolve names against.

        :returns: The truthiness of the evaluated predicate.
        :raises: UnsafeExpressionError
    """
    tree = validate_expression(expression=expression)
    compiled = compile(tree, "<portal-predicate>", "eval")

    if global_ns is not None:
        safe_globals: Dict[str, Any] = dict(global_ns)
    else:
        safe_globals = {}
    safe_globals["__builtins__"] = {}

    if local_ns is not None:
        safe_locals: Dict[str, Any] = local_ns
    else:
        safe_locals = {}

    evaluated = eval(compiled, safe_globals, safe_locals)
    rtnval = bool(evaluated)
    return rtnval
