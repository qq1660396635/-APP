#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64

# --- 任务一：定义加密函数 ---
def encrypt_text(raw_text):
    """
    对原始文本进行“加密”：Base64编码后，每4字符一组倒序拼接。
    """
    # 1. 将原始文本进行 Base64 编码
    # b64encode 需要 bytes 类型输入，所以先编码为 utf-8
    # 结果也是 bytes，再解码回字符串
    b64_bytes = base64.b64encode(raw_text.encode('utf-8'))
    b64_string = b64_bytes.decode('utf-8')

    # 2. 将 Base64 字符串每 4 个字符为一组进行分割
    groups = [b64_string[i:i+4] for i in range(0, len(b64_string), 4)]

    # 3. 将分组列表倒序，然后拼接成一个“乱码”字符串
    shuffled_string = "".join(reversed(groups))

    return shuffled_string

# --- 任务二：定义解密函数 ---
def decrypt_text(shuffled_text):
    """
    对“加密”后的文本进行解密：将分组倒序恢复，然后Base64解码。
    """
    # 1. 将“乱码”字符串每 4 个字符为一组进行分割
    groups = [shuffled_text[i:i+4] for i in range(0, len(shuffled_text), 4)]

    # 2. 将分组列表再次倒序（恢复为原始 Base64 顺序），然后拼接
    b64_string = "".join(reversed(groups))

    # 3. 将恢复的 Base64 字符串进行解码
    # b64decode 需要 bytes 类型输入，解码后结果也是 bytes
    try:
        raw_bytes = base64.b64decode(b64_string.encode('utf-8'))
        raw_text = raw_bytes.decode('utf-8')
        return raw_text
    except (base64.binascii.Error, UnicodeDecodeError):
        return "❌ 解密失败：输入的内容可能不是有效的加密字符串。"

# --- 任务三：主程序交互逻辑 ---
if __name__ == "__main__":
    # 1. 提示用户所用的“加密”方法
    print("--- 文本加/解密工具 ---")
    print("【加密方法说明】")
    print("1. 对原文进行 Base64 编码。")
    print("2. 将编码后的字符串每 4 个字符分为一组。")
    print("3. 将所有分组进行倒序排列，然后拼接成最终结果。\n")

    # 2. 让用户选择操作模式
    choice = input("请选择操作 (1: 加密, 2: 解密): ")

    # 3. 根据用户选择执行相应操作并输出结果
    if choice == "1":
        # --- 加密流程 ---
        print("\n--- 加密模式 ---")
        raw_input = input("请输入要加密的原始内容:\n")
        encrypted_result = encrypt_text(raw_input)
        print("\n--- 加密结果 ---")
        print(encrypted_result)

    elif choice == "2":
        # --- 解密流程 ---
        print("\n--- 解密模式 ---")
        enc_input = input("请输入要解密的乱码内容:\n")
        decrypted_result = decrypt_text(enc_input)
        print("\n--- 解密原文 ---")
        print(decrypted_result)

    else:
        # --- 无效输入处理 ---
        print("\n❌ 无效的选择，请输入 1 或 2。")

