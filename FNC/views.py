from django.shortcuts import render
from django.http import HttpResponse
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
import pygraphviz as pgv

# Create your views here.
listOfSyb = {
    '&': '∧',
    '|': '∨',
    '>': '→',
    '=': '↔',
    '!': '¬'
}
formals = {}
def change(input_text, dict):
    new_input = []
    for i in input_text:
        if i in dict:
            new_input += dict[i]
        else:
            new_input += i
    return new_input
def update_dict_and_exp(Exp, dict, count, start, end):
    dict.update({count: "".join(Exp[start:end])})
    return Exp[:start] + [count] + Exp[end:], count + 1

def find_priority(Exp):
    i = 0
    count = 0
    dict = {}
    while i < len(Exp):
        if Exp[i] == '(':
            j = i
            while Exp[j] != ')':
                if Exp[j] == '∧' or Exp[j] == '∨':
                    if Exp[j - 2] == '¬' and Exp[j + 1] == '¬':
                        Exp, count = update_dict_and_exp(Exp, dict, count, j - 2, j + 3)
                    elif Exp[j - 2] == '¬':
                        Exp, count = update_dict_and_exp(Exp, dict, count, j - 2, j + 2)
                    elif Exp[j + 1] == '¬':
                        Exp, count = update_dict_and_exp(Exp, dict, count, j - 1, j + 3)
                    else:
                        Exp, count = update_dict_and_exp(Exp, dict, count, j - 1, j + 2)
                    j -= 1
                j += 1
            i = j
        elif Exp[i] == '∧' or Exp[i] == '∨':
            if Exp[i - 1] != ')' and Exp[i + 1] != '(':
                if Exp[i - 2] == '¬' and Exp[i + 1] == '¬':
                    Exp, count = update_dict_and_exp(Exp, dict, count, i - 2, i + 3)
                elif Exp[i - 2] == '¬':
                    Exp, count = update_dict_and_exp(Exp, dict, count, i - 2, i + 2)
                elif Exp[i + 1] == '¬':
                    Exp, count = update_dict_and_exp(Exp, dict, count, i - 1, i + 3)
                else:
                    Exp, count = update_dict_and_exp(Exp, dict, count, i - 1, i + 2)
        i += 1
    return dict, Exp


def EliminateImp(Exp):
    i = 0
    while i < len(Exp):
        if Exp[i] == '→':
            Exp[i] = '∨'
            if Exp[i - 1] == ')':
                j = i
                while Exp[j] != '(':
                    j -= 1
                Exp.insert(j, '¬')
            else:
                Exp.insert(i - 1, '¬')
        i += 1
    return Exp

def EliminateEqui(Exp):
    i = 0
    rightSide = []
    leftSide = []
    while i < len(Exp):
        if Exp[i] == '↔':
            leftSide = Exp[:i]
            rightSide = Exp[i + 1:]
            Exp = ['('] + leftSide + ['→'] + rightSide + [')'] + ['∧'] + ['('] + rightSide + ['→'] + leftSide + [')']
        i += 1
    return Exp

def EnterNegation(Exp):
    count = 0
    i = 0
    while i < len(Exp):
        if Exp[i] == '¬':
            Exp.pop(i)
            count += 1
        elif Exp[i] == '∧':
            Exp[i] = '∨'
            count += 1
        elif Exp[i] == '∨':
            Exp[i] = '∧'
            count += 1
        else:
            Exp.insert(i, '¬')
            i += 1
            count += 2
        i += 1
    return ['('] + Exp + [')'], count + 2


def EliminateNegation(Exp, dict):
    i = 0
    skip = 0
    while i < len(Exp):
        if Exp[i] == '¬' and Exp[i + 1] == '¬':
            Exp.pop(i)
            Exp.pop(i)
        elif Exp[i] == '¬' and Exp[i + 1] == '(':
            j = i
            Exp.pop(i)
            while Exp[j] != ')':
                if Exp[j] == '∧':
                    Exp[j] = '∨'
                elif Exp[j] == '∨':
                    Exp[j] = '∧'
                elif Exp[j] == '¬' and Exp[j + 1] != '¬':
                    Exp.pop(j)
                    j -= 1
                elif Exp[j] == '¬' and Exp[j + 1] == '¬':
                    Exp.pop(j)
                elif str(Exp[j]).isdigit():
                    Exp[j + 1:j + 1], skip = EnterNegation(list(dict[Exp[j]]))
                    Exp.pop(j)
                    j += skip - 1
                j += 1
            i = j
        elif str(Exp[i]).isdigit() and Exp[i - 1] == '¬':
            Exp[i - 1:i + 1], skip = EnterNegation(list(dict[Exp[i]]))
            i += skip - 2
        elif str(Exp[i]).isdigit() and Exp[i - 1] != '¬':
            skip = len(list(dict[Exp[i]])) + 2
            Exp[i:i + 1] = ['('] + list(dict[Exp[i]]) + [')']
            i += skip - 2
        i += 1
    return Exp


def EliminateBracet(Exp):
    i = 0
    Num_Or = 0
    Num_And = 0
    openBracet = 0
    closeBracet = 0
    bracetIndex = 0
    while (i < len(Exp)):
        if Exp[i] == '(':
            openBracet += 1
            if openBracet >= 2:
                bracetIndex = i
        elif Exp[i] == '∧' and openBracet >= 1:
            Num_And += 1
        elif Exp[i] == '∨' and openBracet >= 1:
            Num_Or += 1
        elif Exp[i] == ')':
            closeBracet += 1
            if closeBracet >= 2 and openBracet == closeBracet:
                if Num_And > 0 and Num_Or == 0 or Num_And == 0 and Num_Or > 0:
                    Exp.pop(i)
                    Exp.pop(bracetIndex)
                    openBracet = 0
                    closeBracet = 0
                    Num_And = 0
                    Num_Or = 0
                else:
                    openBracet = 0
                    closeBracet = 0
                    Num_And = 0
                    Num_Or = 0
        i += 1
    return Exp


def Make_clause(Exp):
    i = 0
    start = 0
    end = 0
    or_Exp = []
    and_Exp = []
    NumBracet = 0
    inBracet = False
    switch = False
    while i < len(Exp):
        if Exp[i] == '(':
            if NumBracet == 0:
                if start != 0 and switch != True:
                    start = i
            NumBracet += 1
            inBracet = True
        elif Exp[i] == ')':
            NumBracet -= 1
            if NumBracet == 0:
                inBracet = False
                if switch == True and len(and_Exp) > 0 and len(or_Exp) > 0:
                    end = i + 1
                    statment = []
                    for j in range(len(and_Exp)):
                        statment += ['('] + list(and_Exp[j])
                        for k in range(len(or_Exp)):
                            statment += ['∨'] + list(or_Exp[k])
                        statment += [')']
                        if j < len(and_Exp) - 1:
                            statment += ['∧']
                    Exp[start:end] = statment
                    i = len(statment) - 1
                    switch = False
        elif Exp[i] == '∧' and inBracet == True:
            switch = True
        elif Exp[i] == '∨' and inBracet == False:
            switch = True
        elif Exp[i] == '¬' and inBracet == True and Exp[i + 2] == '∨' or Exp[i] == '¬' and inBracet == True and Exp[
            i - 1] == '∨':
            or_Exp.append("".join(Exp[i:i + 2]))
        elif Exp[i - 1] != '¬' and inBracet == True and Exp[i + 1] == '∨' or Exp[i - 1] != '¬' and inBracet == True and \
                Exp[i - 1] == '∨':
            or_Exp.append(Exp[i])
        elif Exp[i] == '¬' and inBracet == True and Exp[i + 2] == '∧' or Exp[i] == '¬' and inBracet == True and Exp[
            i - 1] == '∧':
            and_Exp.append("".join(Exp[i:i + 2]))
        elif Exp[i - 1] != '¬' and inBracet == True and Exp[i + 1] == '∧' or Exp[i - 1] != '¬' and inBracet == True and \
                Exp[i - 1] == '∧':
            and_Exp.append(Exp[i])
        i += 1
    return Exp


def Semplification(Exp):
    i = 0
    start = 0
    end = 0
    List = []
    inBracet = False
    while i < len(Exp):
        if Exp[i] == '(':
            start = i + 1
            inBracet = True
        elif Exp[i] == ')':
            end = i
            inBracet = False
            j = 0
            statment = []
            while j < len(List):
                statment += list(List[j])
                if j < len(List) - 1:
                    statment += ['∨']
                j += 1
            Exp[start:end] = statment
            if len(statment) != end - start:
                i = i - end + start + len(statment)
            List.clear()
        elif Exp[i] == '¬' and inBracet == True and "".join(Exp[i:i + 2]) not in List:
            if "".join(Exp[i + 1:i + 2]) not in List:
                List.append("".join(Exp[i:i + 2]))
            else:
                List.remove("".join(Exp[i + 1:i + 2]))
        elif Exp[i - 1] != '¬' and Exp[i] not in ['∨', '∧', '¬'] and inBracet == True and "".join(Exp[i]) not in List:
            if '¬' + "".join(Exp[i]) not in List:
                List.append("".join(Exp[i]))
            else:
                List.remove('¬' + "".join(Exp[i]))
        i += 1
    return Exp


def tree(Exp):
    i = 0
    stack = {}
    woc = {}
    wop = []
    Node_List = []
    inBracet = 0
    while i < len(Exp):
        if Exp[i] == '(':
            inBracet += 1
        elif Exp[i] == ')':
            if stack:
                last_key, last_value = next(reversed(stack.items()))
                j = 0
                while j < len(wop):
                    if inBracet in wop[j].keys():
                        list(wop[j].values())[0].parent = last_value
                        wop.pop(j)
                        j-=1
                    j+=1
                stack.popitem()
                if wop:
                    last_key1, last_value1 = list(wop[-1].items())[-1]
                    last_value.parent = last_value1
                else:
                    wop.append({inBracet: last_value})
            elif woc:
                last_key, last_value = list(wop[-1].items())[-1]
                last_key1, last_value1 = next(reversed(woc.items()))
                last_value.parent = last_value1
                woc.popitem()
                wop.pop(-1)
            inBracet -= 1
        elif Exp[i] == '¬':
            node = Node('¬')
            Node_List.append(node)
            woc.update({inBracet: node})
            if Exp[i-1] == '∧' or Exp[i-1] == '∨':
                last_key, last_value = list(wop[-1].items())[-1]
                node.parent = last_value
            else:
                wop.append({inBracet: node})
        elif Exp[i].isalpha():
            if woc:
                last_key, last_value = next(reversed(woc.items()))
            else:
                last_key, last_value = -1 , Node("none")
            if last_value.name == '¬' and last_key == inBracet:
                node = Node(Exp[i], parent=last_value)
                Node_List.append(node)
                woc.popitem()
            else:
                node = Node(Exp[i])
                wop.append({inBracet: node})
        elif Exp[i] == '∨' or Exp[i] == '∧':
            last_key, last_value = list(wop[-1].items())[-1]
            node = Node(Exp[i], children=[last_value])
            Node_List.append(node)
            wop.pop(-1)
            wop.append({inBracet: node})
            if Exp[i+1].isalpha():
                node = Node(Exp[i+1], parent=node) # the node is defined before !!!
                Node_List.pop(-1)
                Node_List.append(node)
                i+=1
            elif Exp[i+1] == '(':
                woc.update({inBracet: node})
                inBracet += 1
                i += 1
        elif Exp[i] == '→' or Exp[i] == '↔':
            node = Node(Exp[i])
            stack.update({inBracet: node})
        i+=1
    if len(wop) > 1:
        last_key, last_value = next(reversed(stack.items()))
        j = 0
        while j < len(wop):
            if inBracet in wop[j].keys():
                list(wop[j].values())[0].parent = last_value
                wop.pop(j)
                j -= 1
            j += 1
        wop.append({inBracet: last_value})
    return list(wop[-1].values())[-1]

def tree2(Exp):
    i = 0
    stack = []
    andLogic = Node('∧')
    while i < len(Exp):
        if Exp[i] == '(':
            orLogic = Node('∨')
        elif Exp[i] == ')':
            orLogic.parent = andLogic
        elif Exp[i] == '¬':
            node = Node('¬', parent=orLogic)
            stack.append(node)
        elif Exp[i].isalpha():
            if Exp[i-1] == '¬':
                node = Node(Exp[i], parent=stack.pop())
            else:
                node = Node(Exp[i], parent=orLogic)
        i+=1
    return andLogic

def FNC(request):
    context = {}
    if request.method == 'POST':
        logic_phrase = list(str(request.POST.get('logic_phrase')))
        logic_phrase_converted = change(logic_phrase, listOfSyb)
        context.update({'converted_phrase': "".join(logic_phrase_converted)})
        dict, logic1 = find_priority(logic_phrase_converted)
        logic2 = EliminateEqui(logic1)
        logic3 = EliminateImp(logic2)
        eliminated_equi_imp = EliminateNegation(logic3, dict)
        context.update({'Eliminated_equi_imp': "".join(eliminated_equi_imp)})
        logic4 = EliminateBracet(eliminated_equi_imp)
        fnc_form_clausal = Make_clause(logic4)
        context.update({'form_clausal': "".join(fnc_form_clausal)})
        logic_phrase_final = Semplification(fnc_form_clausal)
        context.update({'final_phrase': "".join(logic_phrase_final)})
    return render(request, 'main.html', context)

def make_graph(root):
    A = pgv.AGraph(directed=True, encoding='UTF-8')
    for idx, node in enumerate(PreOrderIter(root)):
        node_name = f"{node.name}{idx}"
        A.add_node(node_name)
        if node.name == '∨':
            A.get_node(node_name).attr['label'] = 'v'
        elif node.name == '∧':
            A.get_node(node_name).attr['label'] = '^'
        else:
            A.get_node(node_name).attr['label'] = node.name
        if node.parent:
            parent_idx = next(i for i, n in enumerate(PreOrderIter(root)) if n == node.parent)
            parent_name = f"{node.parent.name}{parent_idx}"
            A.add_edge(parent_name, node_name)
    return A

def show_graph(request, logic_phrase_type, logic_phrase):
    # Convert the logic phrase to a list
    logic_phrase = list(logic_phrase)

    # Generate the tree based on the logic phrase type
    if logic_phrase_type in ['converted_phrase', 'Eliminated_equi_imp']:
        root = tree(logic_phrase)
    elif logic_phrase_type in ['form_clausal', 'final_phrase']:
        root = tree2(logic_phrase)

    # Generate the graph
    A = make_graph(root)

    # Save the graph as a PNG image
    A.layout(prog='dot')
    A.draw('graph.png')

    # Return the image as a response
    with open('graph.png', 'rb') as f:
        return HttpResponse(f.read(), content_type="image/png")
