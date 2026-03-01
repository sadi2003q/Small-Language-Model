# Flowchart Guide

This document provides guidelines for creating flowcharts using Mermaid syntax.

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Result 1]
    B -->|No| D[Result 2]
```

### Additional Examples

```mermaid
flowchart LR
    E[Process] --> F[Step 1]
    F --> G[Step 2]
    G --> H{Final Decision}
    H -->|Option A| I[Outcome A]
    H -->|Option B| J[Outcome B]
```

```mermaid
flowchart TB
    K[Initialization] --> L[Process Loop]
    L --> M[End]
```

## Notes
- Ensure clarity in your flowchart.
- Use descriptive names for each node.