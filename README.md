# paper-summarizer
Post summaries of papers to discord channel (summarized by OpenAI API)

### Sample output
<img src="https://user-images.githubusercontent.com/57845734/236689178-25ed2ecc-97b3-4317-bf18-9b868ea4df34.png" width="800">
(The default summarification language is Japanese / デフォルトでは日本語でのサマリになります)

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

### Prompt & model
You can change prompt & model by editing `batch.py` directly.
```python
def ask_gpt_to_summarize(abstract: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # model
        messages=[
            {"role": "assistant", "content": abstract},
            {
                "role": "user",
                "content": "この文章を400字以内の日本語で要約してください。", # prompt to ask the summarization
            },
        ],
    )
    return response.choices[0].message.content
```

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

# Steps to introduce 
1. Create discord app & configure
2. Generate & copy OpenAI API token
3. Copy discord channel id
4. Set environment variables

## 1. Create discord app
see https://gist.github.com/t407o/ab8d7874350bd4c60bad8522196f185b

## 2. Copy OpenAI API token
see https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/

## 3. Copy discord Channel ID
see https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-

## 4. Set environmental variables
Now that you have all of `OPENAI_API_KEY`, `DISCORD_BOT_TOKEN` and `DISCORD_CHANNEL_ID`, set it to environment variables!  
After that you can run the script... *Congrats*!!
```shell
python batch.py
```
**NOTE**: you should set at least 1 search keyword in `search_keywords.txt` to execute it correctly

## (Optional) Scheduling
Scheduling the execution is the main use case of this script. 
- Windows - use windows scheduler (FYI https://datatofish.com/python-script-windows-scheduler/)
- Mac, Linux - use cron (FYI https://ostechnix.com/a-beginners-guide-to-cron-jobs/)
