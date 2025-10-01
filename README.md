flowchart TD
  subgraph User
    A[User Query\n(e.g. "Find AI engineer jobs")]
  end

  subgraph Agent_Process
    direction TB
    B[Prompt Template\n(query + tool descriptions)]
    C[LLM (Reasoning)\nreturns: {action, action_input}]
    D[Output Parser / Engine\nextracts tool name & input]
    E[Tool Execution\n(e.g. Search LinkedIn)]
    F[Tool Result / Observation\n(URLs, descriptions)]
    G[Scratchpad / History\nholds actions & observations]
    H[LLM (Reasoning - 2nd pass)\nreceives history + observation]
    I[Final Answer (text)]
    J[Output Parser\n(convert to JSON / Pydantic)]
    K[Structured Object\n(program-ready)]
  end

  A --> B
  B --> C
  C --> D
  D --> E
  E --> F
  F --> G
  G --> H
  H --> I
  I --> J
  J --> K

  %% Notes / adornments
  classDef tool fill:#f3f4f6,stroke:#333,stroke-width:1px;
  class E,F,D,G tool
  click E "https://example.com" "Tool = external integration (placeholder)"