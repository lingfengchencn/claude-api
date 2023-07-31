# Claude 2 API（非官方）

该项目提供了一个非官方API，可以让用户访问和与Claude AI交互，并尝试使用相同的实验。

这个Python包通过cookie的值返回[Claude 2](https://claude.ai/)的响应。

**请谨慎使用并负责任地使用这个包。**

该项目逆向工程了Claude的推理过程。使用cookie里面的`sessionKey`，您可以向Claude 2提问并获得答案。请注意，Claude 2 API不是免费的服务，而是为了帮助开发人员测试某些功能而提供的工具，因为Anthropic的Claude 2免费API的开发和发布存在延迟。它采用了轻量级结构，可以轻松适应官方API的出现。因此，我强烈不建议将其用于任何其他目的。如果您有正式的[Claude-2 API](https://www.anthropic.com/index/claude-2)访问权限，请用对应的官方代码替换提供的响应。

<br>

## 安装

要使用 Claude 2 非官方 API，您可以使用 pip 安装、克隆 GitHub 存储库或直接下载 Python 文件。

终端：

    pip install claude2-api
    
或者

克隆存储库：

    git clone https://github.com/Nipun1212/Claude_api.git


<br>

## 身份验证
> **警告** 不要暴露 `sessionKey` cookie 
1. 访问 https://claude.ai/
2. F12 进入控制台
3. 网络: organizations → 请求标头 → 复制 Cookie 的全部值。

请注意，虽然我出于方便将 `sessionKey` 值称为 API 密钥，但它并不是官方提供的 API 密钥。
Cookie 值会经常更改。如果出现错误，请再次验证该值。大多数错误是由于输入了无效的 cookie 值导致的。

<br>

## 用法

导入claude api，并获取conversation:

```python
    from claude import Claude
    session_key = 'sk-ant-sid01-...'

    proxies = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087'
    }

    claude = Claude(session_key=session_key,
                    proxies=proxies,  # default None
                    model='claude-2.0',  # default 'claude-2.0'
                    timezone='Asia/Shanghai')  # default os timezone
    conversation = claude.get_conversation("7e...-.-.-.-1b2...8")

```


## Send Message

发送消息、文件，并获取claude 返回的结果。（文件目前仅支持文本）

```python
    # append message or file
    result = conversation.append_message(message='tell me about this file',
                                         file_list=['../LICENSE'])
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

创建一个新的会话:

```python
    import uuid
    claude = Claude(session_key, proxies)
    conversation = claude.new_conversation(uuid.uuid4().hex)
```

<br>

## 免责声明

本项目提供了 Claude AI 的非官方 API，与 Claude AI 或 Anthropic 无关并且未得到它们的认可。使用时请自行承担风险。

如需了解如何使用 Claude AI，请参考官方文档[https://claude.ai/docs]。


> **警告** 重要提示
  使用 BardAPI 包所涉及的所有法律责任由用户自行承担。这个 Python 包仅为开发者方便访问 Google Bard 而设计，用户需要负责管理数据并适当地使用这个包。有关更多信息，请参阅 Google Bard 官方文档。

> **警告** 注意事项
这个 Python 包不是 Google 官方包或 API 服务，它也没有与 Google 相关联，而是使用了 Google 帐户 cookie。这意味着过度或商业化的使用可能会导致您的 Google 帐户受到限制。这个包是为了支持开发者在出现官方 Google 包延迟时进行功能测试而创建的。但是，它不应该被滥用。请谨慎使用，并参考 Readme 获取更多信息。