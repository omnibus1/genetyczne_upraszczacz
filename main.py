import sys
from antlr4 import *
from dist.MyGrammerLexer import MyGrammerLexer
from dist.MyGrammerParser import MyGrammerParser
from dist.MyGrammerVisitor import MyGrammerVisitor
import math
start_index = {}

def simple_equation(ctx):
    try:
        first_is_simple = not (ctx.parentCtx.children[1].binary_operator() or ctx.parentCtx.children[1].unary_operator())
    except:
        first_is_simple = True
    try:
        second_is_simple = not (ctx.parentCtx.children[3].binary_operator() or ctx.parentCtx.children[3].unary_operator())
    except:
        second_is_simple = True
    return first_is_simple, second_is_simple

class MyVisitor(MyGrammerVisitor):
    output = ""
    node_index = {}

    # Visit a parse tree produced by MyGrammerParser#expr.
    def visitExpr(self, ctx: MyGrammerParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MyGrammerParser#binary_operator.
    def visitBinary_operator(self, ctx: MyGrammerParser.Binary_operatorContext):
        first_simple, second_simple= simple_equation(ctx)

        if first_simple and second_simple:
            first_float = ctx.parentCtx.children[1].floatVal()
            second_float = ctx.parentCtx.children[3].floatVal()
            if first_float and second_float:
                self.output += "<"+str(eval(ctx.parentCtx.getText()[1:-1]))+">"
            else:
                self.output += ctx.parentCtx.getText()[1:-1]

        elif first_simple:
            self.output += ctx.parentCtx.children[1].getText()
            self.output += ctx.getText()
            self.visitChildren(ctx)

        elif second_simple:
            self.output += ctx.getText()
            self.output += ctx.parentCtx.children[3].getText()

        else:
            self.output += ctx.getText()
        self.visitChildren(ctx)

    # Visit a parse tree produced by MyGrammerParser#mul.
    def visitMul(self, ctx: MyGrammerParser.MulContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MyGrammerParser#div.
    def visitDiv(self, ctx: MyGrammerParser.DivContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MyGrammerParser#add.
    def visitAdd(self, ctx: MyGrammerParser.AddContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MyGrammerParser#sub.
    def visitSub(self, ctx: MyGrammerParser.SubContext):
        return self.visitChildren(ctx)

    def visitLeft_quote(self, ctx: MyGrammerParser.Left_quoteContext):
        self.output += "("
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyGrammerParser#right_quote.
    def visitRight_quote(self, ctx:MyGrammerParser.Right_quoteContext):
        self.output += ")"
        return self.visitChildren(ctx)

    def visitUnary_operator(self, ctx:MyGrammerParser.Unary_operatorContext):
        is_simple = ctx.parentCtx.children[2].floatVal()
        if is_simple:
            new_str = ctx.parentCtx.getText()
            new_str = new_str.replace("sin", "math.sin")
            new_str = new_str.replace("cos", "math.cos")
            val = eval(new_str)
            self.output += str(val)
        else:
            self.output += ctx.getText()
        return self.visitChildren(ctx)

    def format_output(self):
        output = self.output
        output = output.replace("()", "")
        output = output.replace("(<", "")
        output = output.replace(">)", "")
        return output

def simplify_expression(input):
    first_input = input
    while True:
        data = InputStream(input)
        lexer = MyGrammerLexer(data)
        stream = CommonTokenStream(lexer)
        parser = MyGrammerParser(stream)
        tree = parser.expr()
        visitor = MyVisitor()
        visitor.visit(tree)
        output = visitor.format_output()

        if input == output or not (output.startswith("(") or output.startswith("sin") or output.startswith("cos")):
            break
        else:
            input = output
    print_resoult(first_input, output)


def print_resoult(input, output):
    print("")
    print("======================")
    print(input)
    print("simplified:")
    print(output)
    print("======================")
    print("")

def clear_output(output):
    output = output.replace("()", "")
    output = output.replace("(<", "")
    output = output.replace(">)", "")
    return output



if __name__ == "__main__":
    expressions = ["((23.23 + 23.23) * (23.23 + 23.23))", "(2.3 + (5.2 * 7.9))",
               "((x + sin(-2.4763086688067935)) * ((2.97151104188705 - -1.1257548419538699) + 4.652445575363105))",
               "(sin((-2.4775196572508182 + x)) / (-1.6237642236659875 - cos(-3.4938004711671966)))",
               "sin((-0.306859997011931 - (((-2.3821427944606812 + -1.7833046777651074) + x) - ((cos(-1.5897997954111842) + 3.2029468875337326) * -4.4121197626020585))))",
               "(((-0.929245997242532 - -4.680245561991513) - y) + ((x * (y * (cos(cos(-0.2442091796174095)) - -2.6045385326887494))) + ((4.998852989377303 + -2.1386102966371645) + ((y / -0.170011289176478) + (sin((1.6075499483970574 * 1.3191283846939719)) - (2.358931544040037 * (cos((-3.7996972567437948 + -2.6045385326887494)) / 4.921371229966848)))))))",
               "((y * ((x - (0.563971634568178 * -0.7416155736624566)) + (-4.685658952617697 / sin(0.7155405036803373)))) - 0.5308676453408987)",
               "(x + ((cos(cos((x / 1.8117144633694409))) - ((2.410672697661198 + -3.9000910582893464) + x)) / ((sin(2.3849853583153946) - -1.4061987700463776) - (((((-2.605152686901512 / ((-3.139224077009705 / -3.3500370990936403) - ((((-4.975854936568684 - (x * 4.164872313505155)) + 2.285898019261003) * x) / -0.1437289661597969))) * 4.0871452025855834) * 0.7616841220875292) * ((sin(sin((x + -2.9233128301074296))) * -2.177315126458895) - -3.6847677475453997)) * (cos((2.3849853583153946 * (((sin((4.0871452025855834 + x)) * sin(1.8117144633694409)) - -4.975854936568684) + cos(sin(-1.6375130497393786))))) - 0.9791566354074792)))))",
               "((((x - cos((1.4570583116493507 - -3.4032203898749245))) - cos(1.3489252569666688)) / ((x / ((1.3489252569666688 * ((x / (((-4.526374642893137 * -4.1370067352066355) - cos(-3.5463565698384625)) - -3.092900536104973)) + 4.703177241551652)) * cos(sin((-3.092900536104973 * cos(0.5018234456553383)))))) + sin(2.0314999924815673))) - sin(((4.068691623727389 * 4.487940256652186) + -1.433274740104328)))"
            
               ]

    for expression in expressions:
        simplify_expression(expression)
