from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-629cf0c60810492fbac2cd0630e8d259",  # 替换为您的API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 替换为您的base_url
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

def answer_question_based_on_summary(summary, question):
    """
    根据文档总结回答问题
    :param summary: 文档总结
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
    
    # # 第二步：根据总结回答问题
    # answer = answer_question_based_on_summary(summary, question)
    
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

if __name__ == '__main__':
    # 文档文件路径列表
    file_paths = ['计网定义.txt', '网安定义.txt', '网络分层.txt','物联网.txt','云计算.txt']
    
    # 加载文档
    documents = load_documents(file_paths)
    
    # 示例问题
    question = "网络安全领域包含什么问题"
    
    # 生成模板问题
    template_question = generate_template_question(question)
    file_token = '' 
    # 遍历所有文档并回答问题
    for doc_index, document in documents.items():
        answer = search_document(document, template_question) 
        file_token += str(doc_index-1) + ':'+ answer +"   " 
    # print(file_token) 
    template_answer = answer_question_based_on_summary(file_token, question) 
    print("对于问题："+question+"\n帮您在以下文档寻找:"+file_paths[int(template_answer)]) 
