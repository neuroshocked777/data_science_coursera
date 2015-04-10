import os.path
import java.sql.Connection as Connection
import java.sql.Statement as Statement

#================================

def read_scen(scenfile):
    """(file open for reading) -> list

    	Read file returns list

    >>> read_scen(obj_file)
    [['1.', 'BM_AB9014BIC', '-', 'ACTIVATE'], ['2.', 'LOAD_DPD', '-'],   
    """
    scens = []
    for line in scenfile.readlines():
        scen = line.split()
        scens.append(scen)

    return scens


def only_new(pop_list):
    """(nested list) -> nested list

    Add element 'NEW' into the list where <4 of elements. Outputs ONLY new list.

    >>> obj_file = [['1.', 'BM_AB9014BIC', '-', 'ACTIVATE'], ['2.', 'LOAD_DPD', '-']]
    >>> extend_list(obj_file)
    [['1.', 'BM_AB9014BIC', '-', 'ACTIVATE'], ['2.', 'LOAD_DPD', '-', 'NEW']]
    """
    ext_list = []
    for item in pop_list:
        if len(item)<4:
            item.extend(['NEW'])
            ext_list.append(item)

    return ext_list


def del_from_list(del_list):
    """(nested list) -> nested list

    Outputs ONLY list where elements>=4

    >>> [['1.', 'BM_AB9014BIC', '-', 'ACTIVATE'], ['2.', 'LOAD_DPD', '-']]
    >>> extend_list(del_list)
    [['1.', 'BM_AB9014BIC', '-', 'ACTIVATE']]
    """
    dell_list = []
    for item in del_list:
        if len(item) >= 4:
            dell_list.append(item)

    return dell_list    


def clear_list(str_list):
    """(list) -> list

    Deletes from list elements(lists), that includes 'DELETE', 'DEACTIVATE'
   
    """
    status = ['DELETE', 'DEACTIVATE']
    cl_list = []
    for item in str_list:
        if item[3] not in status:
            cl_list.append(item)

    return cl_list


def scen_list(strr_list):
    """(list) -> list

	Selects names of scenarious from elements of list.
   
    """
    scenarios = []
    for item in strr_list:
        scenarios.append(item[1])

    return scenarios

#================================

con = odiRef.getJDBCConnection("SRC")
stm = con.createStatement()

filepath = r'<%=odiRef.getOption("PATH_OBJ")%>\objects.txt'
filepath2 = filepath.replace('\\', '/')
obj_file = open(filepath2, 'r')

str_list = read_scen(obj_file)             #Nested List from file
cor_list = del_from_list(str_list)         #List only with elements >= 4
new_list = only_new(str_list)           #List only with 'NEW'
new_list.extend(cor_list)			#new_list + cor_list
modyf_list = clear_list(new_list)
scens = scen_list(modyf_list)

res_list = []
for item in scens:
    res_list.append("'" + item + "'")

repository_name = '<%=odiRef.getSchemaName("ODI_WORKREP","D")%>'

res_list2 = []
for item in res_list:
   res_list2.append("update " + repository_name + ".SNP_SCEN SC SET SC.I_SCEN_FOLDER =( select SF.I_SCEN_FOLDER from " + repository_name + ".SNP_SCEN_FOLDER sf where sf.SCEN_FOLDER_NAME = 'PREVIOUS_VERSION' ) where SC.SCEN_NAME =" + item + "\n")

for item3 in res_list2:
   stm.execute(item3)

obj_file.close()
con.commit()
#con.close()
