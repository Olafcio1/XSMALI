from smali.parser.misc.Statement import MethodBody

def handle_method_body(self, body: MethodBody) -> None:
    self.tab(1)

    for stmt in body:
        if stmt["type"] == "define-locals":
            self.write("let")

            for i in range(stmt["value"]):
                self.write(" v%d," % i)

            self.unwrite(1)
            self.write(";\n")
        elif stmt["type"] == "return-void":
            self.write("return void;\n")

    self.tab(-1)
