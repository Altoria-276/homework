from typing import List
from openai import OpenAI, embeddings
from langchain_openai import OpenAIEmbeddings


def query_translation(question: str, n: int = 3) -> List[str]:
    """
    将问题翻译成 n 个相关子问题
    Args:
        question (str): 问题
        n (int, optional): 分解个数. Defaults to 3.

    Returns:
        List[str]: 子问题列表
    """
    client = OpenAI(
        api_key="sk-629cf0c60810492fbac2cd0630e8d259",  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )

    template = f"""您是一个有用的助手，可以生成与输入问题相关的多个子问题。
    目标是将输入分解为一组可以单独获得答案的子问题/子问题。
    生成与以下内容相关的多个搜索查询:{question}
    0utput ({n} queries):"""

    completion = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": template,
            },
        ],
    )
    result = completion.choices[0].message.content.split("\n")

    print("Query Translation")
    for answer in result:
        print(answer)

    return result


if __name__ == "__main__":
    query_translation("天津有什么美食适合作为和女朋友一起吃的晚餐。", n=5)
    query_translation("天津有什么适合和女朋友一起去逛的地方", n=5)
