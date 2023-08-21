import sys

class read:
    def __init__(self):
        self.table = dict()
        self.linenum = 0
        self.varnum = 16
        #infill tabel with predefined values
        self.table["R0"] = 0
        self.table["R1"] = 1
        self.table["R2"] = 2
        self.table["R3"] = 3
        self.table["R4"] = 4
        self.table["R5"] = 5
        self.table["R6"] = 6
        self.table["R7"] = 7
        self.table["R8"] = 8
        self.table["R9"] = 9
        self.table["R10"] = 10
        self.table["R11"] = 11
        self.table["R12"] = 12
        self.table["R13"] = 13
        self.table["R14"] = 14
        self.table["R15"] = 15
        self.table["SP"] = 0
        self.table["LCL"] = 1
        self.table["ARG"] = 2
        self.table["THIS"] = 3
        self.table["THAT"] = 4
        self.table["SCREEN"] = 16384
        self.table["KBD"] = 24576

    def comment(self,s):
        self.temp_file_1 = open("tempfile.txt","+a")
        sfind = s.find("//")
        #print("sfind is:"+str(sfind))
        if(sfind == -1):
             #print("not comment")
             self.temp_file_1.write(s)
        if(sfind == 0):
            pass
            #print("starts with comment")
        if(sfind>0):
            substr = s[0:sfind]
            self.temp_file_1.write(substr + '\n')
            #print("instruction is: "+substr)
        self.temp_file_1.flush()
        self.temp_file_1.close()
    
    def label(self,s): #scans for labels and create table entry
        self.temp_file_2 = open("tempfile_label.txt","+a")
        sfind_open_param = s.find("(")
        sfind_close_param = s.find(")")
        if(sfind_open_param>=0 and sfind_close_param >0):
            skey = s[sfind_open_param+1:sfind_close_param]
            self.table[skey] = self.linenum - 2  #why two???
        else:
            self.linenum =self.linenum + 1
       
        if(len(s.strip())>1):
            #print(s)
            self.temp_file_2.write(s)
        self.temp_file_2.close()

    def replace_label(self,s): # replace labels with numbers for tabel
        self.label_free = open("tempfile_lf.txt","+a")
        schar = s.strip()[0]
        if (schar == '@'):
            label = s.strip()
            label = label[1:]
            if(label in self.table):
                s2 = str(self.table[label])
                self.label_free.write('@'+s2+'\n')
            else:
                if(label.isdigit()):
                    self.label_free.write("@"+label+'\n')
                else:
                    self.label_free.write("@"+str(self.varnum)+'\n')
                    self.table[label] = self.varnum
                    self.varnum = self.varnum + 1
        else:
            sfind_open_param = s.find("(")
            sfind_close_param = s.find(")")
            if not (sfind_open_param>=0 and sfind_close_param >0):
                self.label_free.write(s.strip()+'\n')
        self.label_free.close()

#this is main
r = read()
f = open(sys.argv[1]) 
for x in f:
    r.comment(x)

temp_file_1 = open("tempfile.txt","r")
for x in temp_file_1:
    r.label(x)

temp_file_2 = open("tempfile_label.txt","r")
for x in temp_file_2:
    r.replace_label(x) 

temp_file_3 = open("tempfile_lf.txt","+a")
temp_file_3.close()

print(r.table)