# paper-summarizer
Post summaries of papers to discord channel (summarized by GPT-API)

## Prerequisites
- Python 3.x

```bash
pip install openai requests scholarly 
```

## Usage
### API Keys
Set the environment variables or set them directly in `batch.py`.

```python 
# batch.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

# ... or set your API key directly as follows 
# ex. 
# OPENAI_API_KEY = "YOUR_API_KEY"
```

| Environment Variable | Description |
|----------------------|-------------|
|`OPENAI_API_KEY`       |Your OpenAI API key.|
|`DISCORD_BOT_TOKEN`    |Your Discord bot token.|
|`DISCORD_CHANNEL_ID`   |The channel ID to post the paper.|

### Search Keywords
You can customize the search keywords by editing `search_keywords.txt`.  
Each line is a keyword. The search will be performed for each line.

```python 
# examples
deep learning
machine learning 

# You can also use AND / OR operator
transformer OR attention
```

## Customization
### Optional Environment Variables
| Environment Variable | Description |
|----------------------|-------------|
|`DISCORD_NOTIFIEE`   |The user name to be notified on finish (if at least one new paper is there).|

### Search Optimization
You can customize the search & summarization size by editing `batch.py` directly.

```python
SEARCH_LIMIT = 10
BATCH_SIZE = 10
```

| Variable | Description |
|----------|-------------|
|`SEARCH_LIMIT`|The maximum number of papers to search.|
|`BATCH_SIZE`|The number of papers to summarize at once.|
