from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
        api_key="sk-629cf0c60810492fbac2cd0630e8d259",  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )

def summarize_document(document):
    """
    使用大模型总结文档内容
    :param document: 文档内容
    :return: 文档总结
    """
    response = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'请总结以下文档内容：\n{document}'}
        ]
    )
    return response.choices[0].message.content

def file_routing(folders, question):
    """
    根据文档总结回答问题
    :param summary: 文档总结或文档名
    :param question: 用户问题
    :return: 回答内容
    """
    response = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'根据以下文档列表总结寻找和问题最接近的文档，你只需要输出列表中对应的文档名：\n{folders}\n问题：{question}'}
        ]
    )
    print("document processing")
    return response.choices[0].message.content

def answer_question_based_on_summary(summary, question):
    """
    根据文档总结回答问题
    :param summary: 文档总结或文档名
    :param question: 用户问题
    :return: 回答内容
    """
    response = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'根据以下文档总结寻找和问题最接近的文档，你只需要输出文档编号：\n{summary}\n问题：{question}'}
        ]
    )
    print("document processing")
    return response.choices[0].message.content

def search_document(document, question):
    """
    搜索文档并回答问题
    :param document: 文档内容
    :param question: 用户问题
    :return: 回答内容
    """
    # 第一步：总结文档
    summary = summarize_document(document)
    
    return summary

def read_document(file_path):
    """
    读取文档内容
    :param file_path: 文档文件路径
    :return: 文档内容
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        document = file.read()
    return document

def load_documents(file_paths):
    """
    加载多个文档并存储在字典中，每个文档分配一个唯一的序号
    :param file_paths: 文档文件路径列表
    :return: 文档字典，键为序号，值为文档内容
    """
    documents = {}
    for idx, file_path in enumerate(file_paths, start=1):
        documents[idx] = read_document(os.path.join('files',file_path))
    return documents

def generate_template_question(question):
    """
    生成模板问题
    :param question: 用户问题
    :return: 模板问题
    """
    return f"请根据以下文档总结回答问题：\n{question}"

def generate_template_answer(answer, doc_index):
    """
    生成模板回答
    :param answer: 回答内容
    :param doc_index: 文档序号
    :return: 模板回答
    """
    return f"回答：{answer}\n对应的文档序号：{doc_index}"

from typing import List
from openai import OpenAI, embeddings

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
    result = completion.choices[0].message.content.split(" ")

    print("Query Translation")
    # for answer in result:
    #     # print(answer)

    return result
# 假设 load_documents 函数
def load_documents_from_folder(directory_path,folder_name):
    file_paths = []
    
    # 构建文件夹的完整路径
    folder_path = os.path.join(directory_path, folder_name)
    documents = {}
    idx = 0
    for idx, file_path in enumerate(file_paths, start=1):
        documents[idx] = read_document(os.path.join('files',file_path))
    # 获取文件夹中的所有文件
    try:
        # 获取该目录下的所有文件和文件夹
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # 遍历文件列表，读取文件内容
        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            file_paths.append(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    documents[idx] = read_document(file_path) # 将文件内容添加到 documents 列表
            except Exception as e:
                print(f"加载文件 {file_path} 时发生错误: {e}")
            idx += 1
        
    except FileNotFoundError:
        print(f"文件夹 {folder_name} 未找到")
    except Exception as e:
        print(f"读取文件夹时发生错误: {e}")
    
    return file_paths, documents
def get_folder_names(directory):
    return [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

if __name__ == '__main__':
    print("这是一个专注于计算机系统结构的智能体，专注于数字逻辑、计算机组成原理、计算机系统结构、操作系统、编译原理、计算机网络的知识\n")

    # 示例问题
    question = input("请输入您的问题: ")

    # 文档存放路径
    directory_path = "文档"  

    folders = get_folder_names(directory_path)
    folder_name = file_routing(folders, question)
    # 加载文档
    file_paths, documents = load_documents_from_folder(directory_path,folder_name)

    # 
    question_translated = query_translation(question, n=5)
    
    # 生成模板问题
    template_question = generate_template_question(question_translated)
    file_token = '' 
    # 遍历所有文档并回答问题
    for doc_index, document in documents.items():
        answer = search_document(document, template_question) 
        file_token += str(doc_index) + ':'+ answer +"   " 
    template_answer = answer_question_based_on_summary(file_token, question) 
    # print("对于问题："+question+"\n帮您在以下文档寻找:"+file_paths[int(template_answer)]) 

    content_selected = read_document(file_paths[int(template_answer)])

    final_template = f"""这是您需要回答的问题:
    \\n ---\\n {question} \in --- \\n
    以下是任何可用的背景问题:
    \\n ---\\n {question_translated} \\n ---\\n
    以下是与该问题相关的其他背景:
    ---\\n {content_selected} \\n --- \\n
    使用上述上下文和任何背景问题只需回答问题:\\n{question}"""
    response = client.chat.completions.create(
        model="qwen-coder-turbo",
        messages=[
            {'role': 'system', 'content': 'You are an expert on computer system.'},
            {'role': 'user', 'content': final_template}
        ]
    )
    print("\n对于您的问题，回答是：\n"+response.choices[0].message.content)
