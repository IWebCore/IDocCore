
from bs4 import BeautifulSoup
from googletrans import Translator

def translate_html(input_file, output_file):
    # 读取HTML文件
    with open(input_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # 初始化翻译器
    translator = Translator()
    
    # 翻译所有可见文本节点
    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style'] and element.strip():
            try:
                translated = translator.translate(element, dest='en').text
                element.replace_with(translated)
            except:
                continue
    
    # 保存翻译后的文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

# 使用示例
translate_html('index.html', 'index_en.html')
