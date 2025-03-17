import sys
import copy


# finding indexes of U and L as if template indexes is sorted 0 to row*column-1
# instead of column and row usage
def find_searchlist(temp):
    all_items = []
    searching_list = []
    for i in temp:
        all_items.extend(i)
    for j in range(len(all_items)):
        if all_items[j] == "U" or all_items[j] == "L":
            searching_list.append(j)
    return searching_list


def restriction_index(constrain):  # get a constraint line as a argument then return indexes haven't no constraint(-1)
    indexes = []
    for j in range(len(constrain)):
        if int(constrain[j]) != -1:
            indexes.append(j)
    return indexes


# return lengths of row and column of template
def calculate_len(template):
    return [len(template),len(template[0])]


# reverse columns and rows (columns will be row,rows will be column)
def create_column_list(template, lengths):
    new_column_temp = []
    for i in range(lengths[1]):
        new_row = []
        for j in range(lengths[0]):
            new_row += template[j][i]
        new_column_temp.append(new_row)
    return new_column_temp


# it finds direction of neighbours according to state of row or column
def find_direction(row_or_column, len_list):
    if row_or_column == 0:
        return [0, 1]
    elif row_or_column == len_list-1:
        return [-1, 0]
    else:
        return [-1,0,1]


# It checks whether it is the same as its neighbor
def neighbor_check(row, column, temp, possible, lengths):
    if possible != "N":
        for i in find_direction(row, lengths[0]):
            if i == 0:
                for a in find_direction(column, lengths[1]):
                    if a != 0 and temp[row+i][column + a] == possible:
                        return False
            else:
                if temp[row+i][column] == possible:
                    return False
    return True


# assume that template has index 0 to row*column-1 instead of row and column.
# Then it converts number to row and column index
def number_to_bindex(number,temp,lengths):
    col = number % lengths[1]
    row = (number-col)//lengths[1]
    return [row, col]


# it locates the cell according to layout
def locate(row, column, temp, possible, layout, lengths):
    if layout[row][column] == "L" and neighbor_check(row, column, temp, possible[0], lengths) and neighbor_check(row, column + 1, temp, possible[1], lengths):
        temp[row][column] = possible[0]
        temp[row][column+1] = possible[1]
    elif layout[row][column] == "U" and neighbor_check(row, column, temp, possible[0], lengths) and neighbor_check(row + 1, column, temp, possible[1], lengths):
        temp[row][column] = possible[0]
        temp[row+1][column] = possible[1]
    else:
        return False


# recursion function is to check template whether rules are followed for template
def check_template(do_list,constrain,type,list,i):  # "i" is starting index
    if i == len(do_list):
        return True
    else:
        return list[do_list[i]].count(type) == int(constrain[do_list[i]]) and check_template(do_list,constrain,type,list,i + 1)


# it controls row and column at the same time by using  recursive function check_template
def together_control(constrain, temp, lenghts):
    return check_template(restriction_index(constrain[0]), constrain[0], "H", temp, 0) and check_template(restriction_index(constrain[1]), constrain[1], "B", temp, 0) and check_template(restriction_index(constrain[3]), constrain[3], "B", create_column_list(temp, lenghts), 0) and check_template(restriction_index(constrain[2]), constrain[2], "H", create_column_list(temp, lenghts), 0)


# it turns the cell to its layout state
def undo(row, column, template, layout):
    template[row][column] = copy.deepcopy(layout[row][column])
    if template[row][column] == "L":
        template[row][column + 1] = copy.deepcopy(layout[row][column + 1])
    else:
        template[row + 1][column] = copy.deepcopy(layout[row + 1][column])


# firstly it tries selections than if it is not correct ,it turns back by undoing its action
def backtrack_recursion(template, do_list, constrain, number, layout, lengths):
    if number == len(do_list):
        if together_control(constrain, template,lengths):
            return True
    else:
        (row,column) = (number_to_bindex(do_list[number],template,lengths)[0],number_to_bindex(do_list[number],template,lengths)[1])
        for possible in [["H", "B"], ["B", "H"], ["N", "N"]]:
            if locate(row, column, template, possible, layout, lengths)!=False:
                if backtrack_recursion(template, do_list, constrain, number + 1, layout, lengths):
                    return True
            undo(row, column, template, layout)


def writing_output(output_file, template, layout,lengths):
    if layout == template:
        output_file.write("No solution!")
    else:
        len_column = lengths[1]
        len_row = lengths[0]
        for j in range(len_row):
            if j != 0:
                output_file.write("\n")
            for i in range(len_column):
                if i == len_column-1:
                    output_file.write("%s"%(template[j][i]))
                else:
                    output_file.write("%s "%(template[j][i]))
    output_file.flush()
    output_file.close()


# it solves problem by using all function
# number represents that index of do_list
def solving_blind_valley(template, output_file, constrain):
    layout = copy.deepcopy(template)
    do_list = find_searchlist(template)
    backtrack_recursion(template, do_list, constrain, 0, layout, calculate_len(template))
    writing_output(output_file, template, layout,calculate_len(template))


def main():
    with open (sys.argv[1],"r") as file:
        constrain = []
        template = []
        for line in file:
            if len(constrain) < 4:
                constrain.append(line.split())
            else:
                template.append(line.split())
    output_file = open(sys.argv[2], "w")
    solving_blind_valley(template, output_file, constrain)


if __name__ == "__main__":
    main()