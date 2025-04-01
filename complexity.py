import ast
import json

# -------------------------------------------------------------------
# 1. Extract a simplified representation of the loop iterable.
#
#    For time-complexity, a constant literal (or container) will be "c" meaning constant.
# -------------------------------------------------------------------
def extract_iterable(iter_node):
    """
    Simplify the loop's iterable according to these rules:
    
    1. If iter_node is a literal constant or container (string, list, tuple, set, dict):
         -> return "c" (i.e. constant)
         
    2. If iter_node is a Call:
         a. If the call is to range(...):
              - If all arguments are constant, return "c"
              - Else, for the first nonconstant argument:
                    * If it is a Name, return "len(<name>)"
                    * If it is a call to len(...) with a Name argument, return "len(<name>)"
                    * Otherwise, return "len(other)"
         b. If the call is to len(...):
              - If its sole argument is a Name, return "len(<name>)"
              - Else, return "len(other)"
         c. For any other function call, return "len(other)"
    
    3. If iter_node is a Name:
         -> return "len(<name>)"
    
    4. Otherwise, return "len(other)"
    """
    # Case 1: Literals or containers are constant
    if isinstance(iter_node, (ast.Constant, ast.List, ast.Tuple, ast.Set, ast.Dict)):
        return "c"
    
    # Case 2: Function calls
    if isinstance(iter_node, ast.Call):
        if isinstance(iter_node.func, ast.Name):
            fname = iter_node.func.id
            if fname == "range":
                # If all range arguments are constant:
                if all(isinstance(arg, ast.Constant) for arg in iter_node.args):
                    return "c"
                else:
                    # Look for the first nonconstant argument.
                    for arg in iter_node.args:
                        if not isinstance(arg, ast.Constant):
                            if isinstance(arg, ast.Name):
                                return f"len({arg.id})"
                            # Check if the argument is a call to len(...) with a Name argument.
                            elif (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and 
                                  arg.func.id == "len" and arg.args and isinstance(arg.args[0], ast.Name)):
                                return f"len({arg.args[0].id})"
                            else:
                                return "len(other)"
                    return "len(other)"
            elif fname == "len":
                if iter_node.args and isinstance(iter_node.args[0], ast.Name):
                    return f"len({iter_node.args[0].id})"
                else:
                    return "len(other)"
            else:
                return "len(other)"
        else:
            return "len(other)"
    
    # Case 3: A variable reference
    if isinstance(iter_node, ast.Name):
         return f"len({iter_node.id})"
    
    # Case 4: Fallback
    return "len(other)"


# -------------------------------------------------------------------
# 2. Build a hierarchical loop tree.
# -------------------------------------------------------------------
class LoopNode:
    """
    A node in the loop tree.
    
    Attributes:
      - node: The original AST node (For or While) or a string ("Global Root")
      - loop_type: "For", "While", or None (if global/root)
      - iterable: The simplified iteration factor (only for For loops)
      - children: List of nested LoopNode objects.
    """
    def __init__(self, node, loop_type=None, iterable=None):
        self.node = node
        self.loop_type = loop_type    # "For", "While", or None for root
        self.iterable = iterable      # Only applicable for For loops
        self.children = []

def loop_to_dict(loop_node):
    """Convert the LoopNode tree recursively to a dict for JSON output."""
    if loop_node.loop_type is None:
        d = {"node": "Global Root", "children": []}
    else:
        d = {
            "node": loop_node.loop_type,
            "iterable": loop_node.iterable,
            "children": []
        }
    d["children"] = [loop_to_dict(child) for child in loop_node.children]
    return d

class LoopTreeVisitor(ast.NodeVisitor):
    """
    An AST visitor that builds a hierarchical tree of loops.
    
    Sibling loops in the same block become siblings in the tree;
    loops nested inside another loop become children.
    """
    def __init__(self):
        self.root = LoopNode("Global Root")
        self.loop_stack = [self.root]

    def visit_For(self, node):
        iterable = extract_iterable(node.iter)
        new_loop = LoopNode(node, loop_type="For", iterable=iterable)
        self.loop_stack[-1].children.append(new_loop)
        self.loop_stack.append(new_loop)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)
        self.loop_stack.pop()

    def visit_While(self, node):
        new_loop = LoopNode(node, loop_type="While", iterable=None)
        self.loop_stack[-1].children.append(new_loop)
        self.loop_stack.append(new_loop)
        for stmt in node.body:
            self.visit(stmt)
        for stmt in node.orelse:
            self.visit(stmt)
        self.loop_stack.pop()
    
    def generic_visit(self, node):
        super().generic_visit(node)


# -------------------------------------------------------------------
# 3. Compute the symbolic time complexity from the loop tree.
#
#    This version simplifies away redundant multiplications or additions with "1".
# -------------------------------------------------------------------
def compute_complexity(node):
    """
    Recursively compute a symbolic time complexity expression.
    Simplify away redundant multiplications or additions with "1".
    
    - For the global root, we sum the complexities of its children.
    - For a For loop:
         Let factor be its iteration factor (if "c", treat as "1").
         If there are nested loops, multiply the outer factor by the sum
         of the inner complexities; if there are none, assume cost "1".
         Then, if one part is "1", return just the other.
    - For a While loop, we denote its cost as unknown ("?").
    """
    if node.loop_type is None:
        # Global root: sum costs of children and drop redundant "1" if others exist.
        costs = [compute_complexity(child) for child in node.children]
        non_ones = [c for c in costs if c != "1"]
        if non_ones:
            return " + ".join(non_ones)
        else:
            return "1"

    if node.loop_type == "For":
        factor = node.iterable
        factor_expr = "1" if factor == "c" else factor
        inner = " + ".join(compute_complexity(child) for child in node.children) if node.children else "1"
        
        # Simplify away multiplication by 1.
        if inner == "1":
            return factor_expr
        if factor_expr == "1":
            return inner
        return f"{factor_expr}*({inner})"

    if node.loop_type == "While":
        inner = " + ".join(compute_complexity(child) for child in node.children) if node.children else "1"
        return "?" if inner == "1" else f"?*({inner})"

    return "1"  # Fallback


# -------------------------------------------------------------------
# 4. Put it all together and simulate with sample code.
# -------------------------------------------------------------------
code = """
for i in range(1,n):
    for j in ['a', 'b', 'c']:
        print(i, j)
for i in num:
    print(1)
"""

# Parse the code into an AST.
tree = ast.parse(code)
visitor = LoopTreeVisitor()
visitor.visit(tree)

def print_loop_tree(node, indent=0):
    spacing = " " * indent
    if node.loop_type is None:
        print(spacing + "Global Root")
    elif node.loop_type == "For":
        print(spacing + f"For (iterable: {node.iterable})")
    elif node.loop_type == "While":
        print(spacing + "While")
    for child in node.children:
        print_loop_tree(child, indent + 4)

print("Tree structure:")
print_loop_tree(visitor.root)

tree_json = json.dumps(loop_to_dict(visitor.root), indent=4)
print("\nJSON representation:")
print(tree_json)

# Compute and print the time complexity expression.
time_complexity = compute_complexity(visitor.root)
print("\nEstimated Time Complexity Expression:")
print(time_complexity)