import re

def detect_clauses(text):
    """
    Split text into clauses based on numbered headers (e.g., '1.', '2.1', 'Section X').
    Returns: List of clause strings.
    """
    if not text:
        return []
    
    lines = text.split("\n")
    clauses = []
    current_clause = ""
    clause_start = False
    
    clause_pattern = re.compile(r"^(?:\d+\.|\d+\.\d+|Section \d+|[IVX]+\.)\s+")
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if clause_pattern.match(line):
            if current_clause:
                clauses.append(current_clause.strip())
            current_clause = line
            clause_start = True
        elif clause_start:
            current_clause += " " + line
    
    if current_clause:
        clauses.append(current_clause.strip())
    
    return clauses