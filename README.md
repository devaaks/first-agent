# First Agent 🤖

A modular AI-powered agent built with LangChain and Claude that uses the ReAct (Reasoning + Acting) framework to search and retrieve structured information from the web.

## 🌟 Features

- **ReAct Agent Framework**: Implements the ReAct pattern for reasoning and action
- **Structured Output**: Returns responses in a validated Pydantic schema format
- **Web Search Integration**: Uses Tavily Search for real-time web information retrieval
- **Claude 3.5 Sonnet**: Powered by Anthropic's latest language model
- **Modular Architecture**: Clean, object-oriented design with separate concerns
- **Configurable**: Easy configuration management for different use cases
- **Type-Safe**: Full type hints and Pydantic validation

## 📋 Prerequisites

- Python 3.12 or higher
- UV package manager (recommended) or pip
- Anthropic API key
- Tavily API key

## 🚀 Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/devaaks/first-agent.git
cd job-search-agent

# Install dependencies with UV
uv sync
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/devaaks/first-agent.git
cd job-search-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the project root with your API keys:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 💻 Usage

### Basic Example

Run the main script:

```bash
python new-main.py
```

### Custom Implementation

```python
from new_main import JobSearchAgent, JobSearchAgentConfig, ResultProcessor

# Create custom configuration
config = JobSearchAgentConfig(
    model_name="claude-3-5-sonnet-latest",
    temperature=0.0,
    max_tokens=512,
    verbose=True  # Enable verbose mode for debugging
)

# Initialize the agent
agent = JobSearchAgent(config)

# Execute a search
query = "Find the top 3 Python libraries for data science"
result = agent.search(query)

# Process and display results
ResultProcessor.display_result(result)
```

## 📁 Project Structure

```
job-search-agent/
├── main.py              # Original implementation
├── new-main.py          # Modular, production-ready implementation
├── prompt.py            # Custom ReAct prompt templates
├── schema.py            # Pydantic schemas for structured output
├── pyproject.toml       # Project dependencies and metadata
├── uv.lock             # UV lock file
├── .env                # Environment variables (not in repo)
└── README.md           # This file
```

## 🏗️ Architecture

### Core Components

1. **JobSearchAgentConfig**: Configuration class for agent settings
2. **JobSearchAgent**: Main agent class that orchestrates the search process
3. **ResultProcessor**: Utility class for parsing and displaying results
4. **AgentResponse Schema**: Pydantic model for structured output validation

### Flow

```
User Query → JobSearchAgent → ReAct Agent → Tool (Tavily) → Structured Response
```

## 🔧 Customization

### Adding New Tools

Edit the `_create_tools` method in `JobSearchAgent`:

```python
def _create_tools(self) -> List[Any]:
    return [
        TavilySearch(),
        # Add your custom tools here
    ]
```

### Modifying Output Schema

Edit `schema.py` to define your custom response structure:

```python
class AgentResponse(BaseModel):
    answer: str = Field(description="The agent's answer")
    sources: List[Source] = Field(description="Sources used")
    # Add custom fields here
```

### Customizing Prompts

Modify `prompt.py` to adjust the ReAct prompt template for your specific use case.

## 🛠️ Development

### Code Formatting

```bash
# Format code with black
black .

# Sort imports with isort
isort .
```

### Running in Verbose Mode

Set `verbose=True` in the configuration to see detailed agent reasoning:

```python
config = JobSearchAgentConfig(verbose=True)
```

## 📦 Dependencies

- **langchain**: Framework for building LLM applications
- **langchain-anthropic**: Anthropic integration for LangChain
- **langchain-tavily**: Tavily search integration
- **anthropic**: Official Anthropic API client
- **pydantic**: Data validation using Python type hints
- **python-dotenv**: Environment variable management
- **black**: Code formatter
- **isort**: Import sorter

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Examples

### Example 1: Sports Information

```python
agent = create_default_agent()
result = agent.search("Search for top 3 indian players in ICC ODI batting rankings")
ResultProcessor.display_result(result)
```

### Example 2: Technology Research

```python
agent = create_default_agent()
result = agent.search("What are the latest advancements in AI in 2025?")
ResultProcessor.display_result(result)
```

## 🐛 Troubleshooting

### API Key Issues

Ensure your `.env` file is in the project root and contains valid API keys.

### Import Errors

Make sure all dependencies are installed:
```bash
uv sync  # or pip install -r requirements.txt
```

### Verbose Debugging

Enable verbose mode to see the agent's reasoning process:
```python
config = JobSearchAgentConfig(verbose=True)
```

## 📄 License

MIT License

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Search capabilities by [Tavily](https://tavily.com/)

---

**Note**: This project is a demonstration of the ReAct agent pattern and can be adapted for various information retrieval tasks beyond job searching.
