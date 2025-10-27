from typing import List, Tuple

def format_context(results: List[Tuple[str, float]]) -> str:
	parts = []
	for text, score in results:
		parts.append(f"[score={score:.3f}]\n{text}")
	return "\n\n".join(parts)
