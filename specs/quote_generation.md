# Quote Generation Specification

## Goals
The quoting agent must:
1. Extract key insights from the conversation or provided content.
2. Produce concise, well‑formatted block quotes using Markdown.
3. Attribute sources accurately with inline citations.
4. Follow the designated **tone**: professional, neutral, and helpful.

## Output Structure
`markdown
> "Quote text"  
> — *Source Title*, Author (Year)

**Analysis:** Brief commentary (1‑2 sentences)
`

## Rules
| ID | Rule | Pattern |
|----|------|---------|
| R1 | Must wrap quote in `>` | `^>` |
| R2 | Must include em‑dash attribution line | `—` |
| R3 | Must provide **Analysis** section | `\\*\\*Analysis:` |

## Evaluation Checks
Each rule above maps to a regex pattern used by `spec_guard` for grading.
