from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage


class SparkAIWrapper:
    def __init__(self):
        # 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        self.SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
        # 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
        self.SPARKAI_APP_ID = '25ae9c0c'
        self.SPARKAI_API_SECRET = 'ZGUwNjc4YTczYWJlMzc1Zjg1NTc0MDA3'
        self.SPARKAI_API_KEY = '986ca405621d9c3b2dca009e35692c52'
        # 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
        self.SPARKAI_DOMAIN = '4.0Ultra'

        self.spark = ChatSparkLLM(
            spark_api_url=self.SPARKAI_URL,
            spark_app_id=self.SPARKAI_APP_ID,
            spark_api_key=self.SPARKAI_API_KEY,
            spark_api_secret=self.SPARKAI_API_SECRET,
            spark_llm_domain=self.SPARKAI_DOMAIN,
            streaming=False,
        )

    def send_message_with_context(self, content, context_messages=None):
        """
        发送带有上下文的消息给星火认知大模型并获取响应

        :param content: 当前要发送的新消息内容
        :param context_messages: 包含上下文的消息列表，每个元素是一个ChatMessage对象，
                                 格式如 [ChatMessage(role="user", content="之前的问题"),
                                        ChatMessage(role="assistant", content="之前的回答"),...]
                                 如果为None，则只发送当前消息，不带上上下文
        """

        if context_messages is None:
            context_messages = []

        messages = []
        # 先添加系统设置消息（如果有），假设这里没有系统设置消息，如有需求可后续添加
        # system_message = ChatMessage(role="system", content="这里可设置系统相关要求，如扮演角色等")
        # messages.append(system_message)

        # 添加上下文消息
        messages.extend(context_messages)

        # 添加当前要发送的消息
        messages.append(ChatMessage(
            role="user",
            content=content
        ))

        handler = ChunkPrintHandler()
        response = self.spark.generate([messages], callbacks=[handler])
        return response