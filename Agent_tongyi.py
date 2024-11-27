from openai import OpenAI
import os

def get_response():
    client = OpenAI(
        api_key="sk-629cf0c60810492fbac2cd0630e8d259", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '请编写一个Python函数 find_prime_numbers，该函数接受一个整数 n 作为参数，并返回一个包含所有小于 n 的质数（素数）的列表。质数是指仅能被1和其自身整除的正整数，如2, 3, 5, 7等。'}],
        )
    print(completion.model_dump_json())

if __name__ == '__main__':
    get_response()