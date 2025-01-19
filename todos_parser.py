import os

class TODOParser:
    def __init__(self, path):
        self.path = os.path.abspath(path)  # 转换为绝对路径
        self.todos = []  # 列表中的每一项都是 {"text": str, "done": bool} 的字典
        self.read()

    def read(self):
        """
        Read To-Dos from todos.ini
        Format:
        <TODO-START-MARK>
        text
        <STATUS>done/undone</STATUS>
        """
        try:
            print("\n=== 开始读取待办事项文件 ===")
            print(f"文件路径: {self.path}")
            
            if not os.path.exists(self.path):
                print(f"文件不存在，将在写入时创建: {self.path}")
                self.todos = []
                return

            with open(self.path, encoding="utf-8") as file:
                content = file.read()
                print(f"读取到的文件内容:\n{content}")
                print(f"文件内容长度: {len(content)} 字节")
                
                if content:
                    # 分割并清理每个待办事项
                    todos = content.split("<TODO-START-MARK>")
                    print(f"分割后的项目数量: {len(todos)}")
                    for i, item in enumerate(todos):
                        print(f"项目 {i}: '{item}'")
                    
                    # 过滤掉空字符串并清理每个待办事项
                    self.todos = []
                    for todo in todos:
                        todo = todo.strip()
                        if todo:  # 只添加非空的待办事项
                            # 解析待办事项的文本和状态
                            lines = todo.split("\n")
                            text = lines[0].strip()
                            done = False
                            for line in lines[1:]:
                                if line.strip() == "<STATUS>done</STATUS>":
                                    done = True
                                    break
                            print(f"处理待办事项: '{text}' (完成: {done})")
                            self.todos.append({"text": text, "done": done})
                    
                    print(f"成功读取 {len(self.todos)} 个待办事项:")
                    for i, todo in enumerate(self.todos, 1):
                        status = "已完成" if todo["done"] else "未完成"
                        print(f"  {i}. {todo['text']} ({status})")
                else:
                    print("文件为空")
                    self.todos = []
            
            print("=== 读取完成 ===\n")
            
        except Exception as e:
            import traceback
            print(f"读取文件出错:")
            print(traceback.format_exc())
            self.todos = []

    def write(self):
        """
        Write current To-Do list into todos.ini
        """
        print("\n=== 开始写入待办事项 ===")
        print(f"文件路径: {self.path}")
        print(f"待写入的内容: {self.todos}")
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            
            # 写入文件
            with open(self.path, "w", encoding="utf-8") as file:
                # 如果没有待办事项，清空文件
                if not self.todos:
                    print("没有待办事项，清空文件")
                    file.write("")
                    return
                
                # 写入所有待办事项
                for todo in self.todos:
                    text = todo["text"]
                    done = todo["done"]
                    if text and text.strip():  # 只写入非空的待办事项
                        status = "<STATUS>done</STATUS>" if done else "<STATUS>undone</STATUS>"
                        content = f"<TODO-START-MARK>\n{text.strip()}\n{status}\n"
                        file.write(content)
                        print(f"写入内容: {content!r}")
            
            # 验证写入
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"验证文件内容:\n{content}")
                print(f"文件大小: {len(content)} 字节")
            
            print("=== 写入完成 ===\n")
        except Exception as e:
            print(f"写入文件时出错: {str(e)}")
            raise  # 重新抛出异常，让上层知道发生了错误

    def add(self, text: str):
        """
        Add new To-Do into self.todos
        :param text: To-Do text
        """
        self.todos.append({"text": text.strip(), "done": False})  # 新添加的待办事项默认未完成

    def set_done(self, index: int, done: bool):
        """
        Set the done status of a todo item
        :param index: Index of the todo item
        :param done: New done status
        """
        if 0 <= index < len(self.todos):
            self.todos[index]["done"] = done
