# Azure Cognitive Search and OpenAI sample notebook

Add the following `.env` file:

```bash
AZURE_SEARCH_SERVICE = "SHORT NAME OF AZURE COG SEARCH SERVICE"
AZURE_SEARCH_INDEX = jobs
AZURE_SEARCH_KEY = "KEY TO AZURE COG SEARCH"
AZURE_SEARCH_USE_SEMANTIC_SEARCH = "false"
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = "default"
AZURE_SEARCH_TOP_K = "5"
AZURE_SEARCH_ENABLE_IN_DOMAIN = "true"
AZURE_SEARCH_CONTENT_COLUMNS = "content"
AZURE_SEARCH_FILENAME_COLUMN = "filepath"
AZURE_SEARCH_TITLE_COLUMN = "title"
AZURE_SEARCH_URL_COLUMN = "url"

# AOAI Integration Settings
AZURE_OPENAI_RESOURCE = "SHORT NAME OF OPENAI RESOURCE"
AZURE_OPENAI_MODEL = "gpt-35-turbo"
AZURE_OPENAI_KEY = "KEY FOR AZURE OPENAI"
AZURE_OPENAI_TEMPERATURE = 0
AZURE_OPENAI_TOP_P = 1.0
AZURE_OPENAI_MAX_TOKENS = 1000
AZURE_OPENAI_STOP_SEQUENCE = ""
AZURE_OPENAI_SYSTEM_MESSAGE = "You are an AI assistant that helps people find information."
AZURE_OPENAI_PREVIEW_API_VERSION = "2023-06-01-preview"
AZURE_OPENAI_STREAM = "false"
AZURE_OPENAI_MODEL_NAME = "gpt-35-turbo"
```

Sampke taken from https://github.com/microsoft/sample-app-aoai-chatGPT/blob/main/app.py. See https://learn.microsoft.com/en-us/azure/ai-services/openai/use-your-data-quickstart?tabs=command-line&pivots=programming-language-studio for more information.

Note that my Cognitive Search instance contained an index named `jobs`. It was populated with PDFs containing job descriptions. See the blog post below for more infirmation:

https://blog.baeke.info/2023/07/29/building-a-chatbot-based-on-your-documents-in-azure/

At the end of that post, there is a video as well:

https://youtu.be/gySeOggsz-w
