class TODOParser:
    def __init__(self, path):
        self.path = path
        self.todos = []
        self.read()

    def read(self):
        """
        Read To-Dos from todos.ini
        """
        try:
            with open(self.path, encoding="utf-8") as file:
                content = file.read()
                if content:
                    # 分割并清理每个待办事项
                    todos = content.split("<TODO-START-MARK>")
                    self.todos = [todo.strip() for todo in todos if todo.strip()]
        except FileNotFoundError:
            self.todos = []

    def write(self):
        """
        Write current To-Do list into todos.ini
        """
        print("正在写入文件:", self.path)  # 调试
        print("待写入的内容:", self.todos)  # 调试
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                for item in self.todos:
                    file.write(f"<TODO-START-MARK>\n{item}\n")
            print("写入完成")  # 调试
        except Exception as e:
            print(f"写入文件时出错: {str(e)}")  # 调试错误

    def add(self, text: str):
        """
        Add new To-Do into self.todos
        :param text: To-Do
        """
        self.todos.append(text.strip())
