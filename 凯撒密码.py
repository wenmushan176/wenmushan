def caesar_cipher(text, shift, encrypt=True):
    # 初始化一个空字符串用于存储结果文本
    result = ""

    # 确保位移量在1到25之间
    shift = shift % 26

    # 遍历输入的每一个字符
    for char in text:
        # 检查字符是否为字母
        if char.isalpha():
            # 计算实际的位移量
            mount = shift if encrypt else -shift

            # 将字符的Unicode码加上位移量
            code = ord(char) + mount

            # 处理小写字母的情况
            if char.islower():
                # 如果超出'z'的Unicode码，循环回到'a'
                if code > ord('z'):
                    code -= 26
                # 如果位移后小于'a'的Unicode码，循环到'z'
                elif code < ord('a'):
                    code += 26
            # 处理大写字母的情况
            elif char.isupper():
                # 如果超出'Z'的Unicode码，循环回到'A'
                if code > ord('Z'):
                    code -= 26
                # 如果位移后小于'A'的Unicode码，循环到'Z'
                elif code < ord('A'):
                    code += 26

            # 将加密或解密后的字符添加到结果字符串中
            result += chr(code)
        else:
            # 非字母字符（如空格、标点符号）保持不变，直接添加到结果字符串中
            result += char

    # 返回加密或解密后的文本
    return result

# 用户输入文本和密钥
message = input("请输入要加密或解密的文本: ")  # 原始消息
shift = int(input("请输入密钥 (1-25): "))  # 位移量

# 用户选择加密或解密
action = input("请选择操作 (加密: e, 解密: d): ").lower()

# 根据用户选择调用加密或解密函数
if action == 'e':
    processed_message = caesar_cipher(message, shift, encrypt=True)
    print(f"加密后: {processed_message}")
elif action == 'd':
    processed_message = caesar_cipher(message, shift, encrypt=False)
    print(f"解密后: {processed_message}")
else:
    print("无效的操作选择。")