# Migration Guide: OpenAI to Ollama Embeddings

## Overview
This guide helps you migrate your research agent from OpenAI embeddings to Ollama embeddings for local processing that works seamlessly with Llama 3.3:70B.

## Prerequisites

### 1. Install Ollama
```bash
# macOS
brew install ollama
brew services start ollama

# Linux/WSL
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### 2. Pull Embedding Models
```bash
# Recommended: High-quality model with large context
ollama pull nomic-embed-text

# Alternative: State-of-the-art performance (larger, slower)
ollama pull mxbai-embed-large

# For development/testing (smaller, faster)
ollama pull all-minilm
```

### 3. Install Dependencies
```bash
pip install langchain-ollama
# Note: Remove openai dependency if no longer needed
# pip uninstall openai
```

## Code Changes

### 1. Import Changes
```python
# OLD - Remove this import
# from langchain_openai import OpenAIEmbeddings

# NEW - Add this import
from langchain_ollama import OllamaEmbeddings
```

### 2. Configuration Updates
```python
# OLD - Remove these config fields
class ResearcherConfig:
    # openai_api_key: str = ""
    # embedding_model: str = "text-embedding-3-small"
    # embedding_dimensions: int = 1536

# NEW - Add these config fields
class ResearcherConfig:
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"  # or "mxbai-embed-large"
```

### 3. Embedding Initialization
```python
# OLD - Remove this initialization logic
# embedding_kwargs = {
#     "api_key": self.config.openai_api_key,
#     "model": self.config.embedding_model
# }
# if self.config.embedding_dimensions != default_dims:
#     embedding_kwargs["dimensions"] = self.config.embedding_dimensions
# self.embeddings = OpenAIEmbeddings(**embedding_kwargs)

# NEW - Use this simple initialization
ollama_base_url = getattr(self.config, 'ollama_base_url', 'http://localhost:11434')
embedding_model = getattr(self.config, 'embedding_model', 'nomic-embed-text')

# Validate supported models
supported_models = ['nomic-embed-text', 'mxbai-embed-large', 'all-minilm']
if embedding_model not in supported_models:
    logger.warning(f"Model {embedding_model} not in recommended list. Using nomic-embed-text instead.")
    embedding_model = 'nomic-embed-text'

self.embeddings = OllamaEmbeddings(
    model=embedding_model,
    base_url=ollama_base_url
)
```

## Recommended Embedding Models

### For Most Use Cases: `nomic-embed-text`
- **Size**: 137M parameters
- **Context**: 8192 tokens (large context window)
- **Performance**: Outperforms OpenAI text-embedding-ada-002
- **Speed**: Good balance of speed and quality
- **Use When**: General-purpose research, good quality requirements

### For High-Performance: `mxbai-embed-large`
- **Size**: 334M parameters
- **Performance**: State-of-the-art, outperforms OpenAI text-embedding-3-large
- **Quality**: Highest quality embeddings
- **Speed**: Slower due to larger size
- **Use When**: Maximum quality is required, processing time is less critical

### For Development: `all-minilm`
- **Size**: Smaller model
- **Speed**: Fastest processing
- **Quality**: Good for testing, lower than above models
- **Use When**: Development, testing, quick prototyping

## Performance Optimizations

### 1. Batch Size Adjustments
```python
# Reduce batch sizes for local processing
batch_size: int = 50  # Instead of 100
max_concurrent_queries: int = 2  # Instead of 3
```

### 2. Chunk Size Optimization
```python
# Optimize chunk sizes for embedding models
chunk_size: int = 800  # Slightly smaller for better quality
chunk_overlap: int = 150
```

### 3. Quality Thresholds
```python
# Adjust quality thresholds for local models
min_source_score: float = 0.4
min_content_quality_score: float = 0.5
```

## Testing Your Migration

### 1. Verify Ollama is Running
```bash
curl http://localhost:11434/api/tags
```

### 2. Test Embedding Generation
```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
test_embedding = embeddings.embed_query("This is a test query")
print(f"Embedding dimension: {len(test_embedding)}")
print(f"First 5 values: {test_embedding[:5]}")
```

### 3. Test with ChromaDB
```python
import chromadb
from langchain_ollama import OllamaEmbeddings

# Initialize
client = chromadb.Client()
collection = client.create_collection(name="test")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Test storage and retrieval
test_text = "Sample research content"
embedding = embeddings.embed_query(test_text)

collection.add(
    ids=["test1"],
    documents=[test_text],
    embeddings=[embedding]
)

# Test query
results = collection.query(
    query_embeddings=[embedding],
    n_results=1
)

print("Test successful!" if results['documents'] else "Test failed!")
```

## Benefits of Migration

### 1. **Privacy & Security**
- All embeddings generated locally
- No data sent to external APIs
- Complete control over your research data

### 2. **Cost Savings**
- No per-token costs for embeddings
- Unlimited usage once models are downloaded
- No rate limiting concerns

### 3. **Performance**
- No network latency for embedding generation
- Consistent performance regardless of API status
- Can run offline

### 4. **Compatibility**
- Perfect integration with Llama 3.3:70B
- Same vector space for consistent semantic search
- Compatible with existing ChromaDB setup

## Troubleshooting

### Common Issues and Solutions

1. **"Connection refused" error**
   ```bash
   # Ensure Ollama is running
   ollama serve
   ```

2. **Model not found**
   ```bash
   # Pull the model first
   ollama pull nomic-embed-text
   ```

3. **Slow performance**
   - Reduce batch sizes
   - Use `all-minilm` for development
   - Consider hardware upgrades (more RAM/CPU)

4. **Dimension mismatch in ChromaDB**
   - Clear existing collection if changing models
   - Models have different embedding dimensions:
     - `nomic-embed-text`: 768 dimensions
     - `mxbai-embed-large`: 1024 dimensions

## Rollback Plan

If you need to rollback to OpenAI embeddings:

1. Keep the original OpenAI configuration in comments
2. Reinstall OpenAI dependency: `pip install openai`
3. Revert the import and initialization changes
4. Update configuration to use OpenAI settings

The migration provides significant benefits while maintaining the same functionality and improving compatibility with your Llama 3.3:70B setup.