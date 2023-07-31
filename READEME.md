# Claude 2 API ( Unofficial )

This project provides an unofficial API for Claude 2 from Anthropic, allowing users to access and interact with Claude AI and trying out experiments with the same.

The python package that returns response of [Claude 2](https://claude.ai/) through value of cookie.


**Please exercise caution and use this package responsibly.**

Using `sessionKey` cookie, you can ask questions and get answers from Claude 2. Please note that the claude 2 api is not a free service, but rather a tool provided to assist developers with testing certain functionalities due to the delayed development and release of Anthropic's Claude 2 free API. It has been designed with a lightweight structure that can easily adapt to the emergence of an official API. Therefore, I strongly discourage using it for any other purposes. If you have access to official [Claude-2 API](https://www.anthropic.com/index/claude-2), replace the provided response with the corresponding official code.

<br>

## Installation

To use the Claude 2 Unofficial API, you can either pip install or clone the GitHub repository or directly download the Python file.

Clone the repository:
```
    git clone https://github.com/Nipun1212/Claude_api.git

    pip install .

```


<br>

## Authentication
> **Warning** Do not expose the `sessionKey` cookie 
1. Visit https://claude.ai/
2. F12 for console
3. Network: organizations → Request Headers → Copy the whole value of Cookie.

Note that while I referred to `sessionKey` value as an API key for convenience, it is not an officially provided API key. 
Cookie value subject to frequent changes. Verify the value again if an error occurs. Most errors occur when an invalid cookie value is entered.

<br>

## Usage


Import the Claude AI module in your Python script:

```python
    from claude import Claude
    session_key = 'sk-ant-sid01-...'

    proxies = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087'
    }

    claude = Claude(session_key=session_key,
                    proxies=proxies,  # default None
                    model='claude-2',  # default 'claude-2'
                    timezone='Asia/Shanghai')  # default os timezone
    conversation = claude.get_conversation("7e...-.-.-.-1b2...8")

```


## Send Message

To send a message to Claude, you can use the get_answer method. It finds your most recent conversation, and if it doesn't exist, it automatically creates a new conversation, and uses it to chat with the model.

```python
    # append message or file
    result = conversation.append_message(message='tell me about this file',
                                         file_list=['../LICENSE'])
    # print(result)
    for chunks in result.stream_chunks():
        # chunks：
        # {
        #     'completion': '..',
        #     'stop_reason': null,
        #     'model': 'claude-2.0',
        #     'stop': null,
        #     'log_id': '44e18c18ee9fce1d5db0b816d4bfb890212ad96646caa507f307bc6f4e3c3629',
        #     'message_limit': {"type":"within_limit"}
        # }
        print(chunks['completion'])
```

## Create New Chat

To create a new chat conversation , you can use the create_new_conversation method:

```python
    claude = Claude(session_key, proxies)
    conversation = claude.new_conversation("333...-.-.-.-333...")

```

<br>


## Disclaimer

This project provides an unofficial API for Claude AI and is not affiliated with or endorsed by Claude AI or Anthropic. Use it at your own risk.

Please refer to the official Claude AI documentation[https://claude.ai/docs] for more information on how to use Claude AI.

## Reference 
[1] https://github.com/KoushikNavuluri/Claude-API <br>
            
> **Warning** Important Notice
  The user assumes all legal responsibilities associated with using the BardAPI package. This Python package merely facilitates easy access to Google Bard for developers. Users are solely responsible for managing data and using the package appropriately. For further information, please consult the Google Bard Official Document.
    
> **Warning** Caution
This Python package is not an official Google package or API service. It is not affiliated with Google and uses Google account cookies, which means that excessive or commercial usage may result in restrictions on your Google account. The package was created to support developers in testing functionalities due to delays in the official Google package. However, it should not be misused or abused. Please be cautious and refer to the Readme for more information.
  
<br><br>
  
*Copyright (c) 2023 Nipun Bhatia *<br>

