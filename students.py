
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import sys
import re
import os
class Database:# The Database class initializes a connection to a SQLite database 
# and provides methods to execute SQL statements on that database.

    def __init__(self, db):
        # Connects to the SQLite database file and initializes 
        # a database cursor. Creates the students table 
        # if it does not exist with the specified columns.
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                stage TEXT NOT NULL,
                gender TEXT NOT NULL 
                
            )
        """
        self.cur.execute(sql)
        self.con.commit()

class Student(Database):
# The Student class inherits from the Database class. It represents a student 
# record in the database and provides methods to insert, update, delete and 
# query student records.

    def __init__(self, root, db_file):
        self.db_file = db_file
        super().__init__(db_file)
        self.root = root
        self.w=1200
        self.h=622
        self.sw= root.winfo_screenwidth()
        self.sh= root.winfo_screenheight()
        self.x= (self.sw-self.w)/2
        self.y= (self.sh-self.h)/2
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, self.x, self.y))
        # self.root.geometry("1200x622+50+50")
        self.root.title("برنامج تسجيل الطلاب")
        self.root.resizable(False, False)
        lb1=Label(self.root, text="برنامج تسجيل الطلاب " ,font = ("Courier New",14) ,bg="#ff8a80")
        lb1.place(x=450 , y=10)
        lb1.pack(fill=X)
        frame1= Frame(self.root,bg="#bbdefb" , width=250 , height=610)
        frame1.place(x=947, y=30)

         #---------------- VARIABLE NAMES -------------

        self.id_var    = StringVar()
        self.name_var  = StringVar()
        self.email_var  =StringVar()
        self.phone_var  =StringVar()
        self.stage_var  =StringVar()
        self.gender_var =StringVar()
        self.search_var = StringVar()
        self.find_var   = StringVar()
        self.se_by_var = StringVar()
         #---------------------- lables and entries -------------------------------

        frame2= Frame(frame1,bg="#455a64" , width=250 , height=40)
        frame2.place(x=0, y=0)
        lb_info = Label(frame2,text = "بيانات الطالب",fg="white" ,bg="#455a64",font = ("Helvetica World",13,"bold"))
        lb_info.place(x=85,y=3)

        lb_id=Label(frame1, text=" :رقم التسجيل", font = ("Helvetica World",10),bg="#bbdefb").place(x=160, y=45)
        en_id= Entry(frame1,justify="right",textvariable=self.id_var,width=25)
        en_id.place(x=5, y=50)

        lb_name=Label(frame1, text=" :اسم الطالب", font = ("Helvetica World",10),bg="#bbdefb", compound ="center").place(x=160 , y=75) 
        en_name= Entry(frame1,justify="right",textvariable=self.name_var,width=25)
        en_name.place(x=5, y=80)

        lb_email =Label(frame1, text=" :ايميل الطالب", font = ("Helvetica World",10),bg="#bbdefb", compound ="center").place(x=160 , y=105)
        en_email= Entry(frame1,justify="right",textvariable=self.email_var,width=25)
        en_email.place(x=5, y=110)

        lb_phone =Label(frame1, text=" :هاتف الطالب", font = ("Helvetica World",10),bg="#bbdefb" ).place(x=160 , y=135)
        en_phone= Entry(frame1,justify="right",textvariable=self.phone_var,width=25)
        en_phone.place(x=5, y=140)

        lb_stage =Label(frame1, text=" :المرحلة الدراسية", font = ("Helvetica World",10),bg="#bbdefb").place(x=145 , y=170)
        comb_stage= ttk.Combobox(frame1,justify="center",textvariable=self.stage_var,font = ("Helvetica World",9),state="readonly",width= 17, height=2)
        comb_stage["values"] = ("ابتدائي", "اعدادي", "ثانوي ")
        comb_stage.place(x=5 , y=170)

        lb_gender =Label(frame1, text="  : الجنس  ", font = ("Helvetica World",10),bg="#bbdefb").place(x=160 , y=205)
        comb_gender= ttk.Combobox(frame1,justify="center",textvariable=self.gender_var,font = ("Helvetica World",9),state="readonly",width= 17)
        comb_gender["values"] = ("ذكر", "انثى")
        comb_gender.place(x=5 , y=205)

        #------------------------لوحة التحكم والازرار ------------------------------
        frame2= Frame(frame1,bg="#455a64" , width=250 , height=40)
        frame2.place(x=0, y=330)
        #------------------------ زر البحث  -----------------------------
         
        lb_find = Label(frame1, text =" حذف طالب برقم التسجيل" ,fg="red", font = ("Helvetica World",12),bg="#bbdefb")
        lb_find.place(x=38 ,y=250)
        
        en_find= Entry(frame1,justify ='center',  font = ("Janna LT",9),textvariable=self.find_var)
        en_find.place(x=43, y=280)
        #-----------------------------ازرار التحكم------------------------  
        lb_control = Label(frame1,text = "لوحة التحكم" ,fg="white",bg="#455a64",font = ("Helvetica World",12,"bold")).place(x=90,y=333)

        btn_add=Button(frame1, text="إضافة طالب",width=26, font = ("Janna LT",9,'bold'),bg="#90a4ae",command=self.add_student)
        btn_add.place(x=6, y=375)

        btn_del=Button(frame1, text="حذف طالب",width=26, font = ("Janna LT",9,'bold'),bg="#90a4ae",command= self.delete )
        btn_del.place(x=6, y=415)

        btn_edit=Button(frame1, text=" تعديل بيانات طالب",width=26, font = ("Janna LT",9,'bold'),bg="#90a4ae",command=self.update)
        btn_edit.place(x=6, y=455)

        btn_clear=Button(frame1, text="افراغ الحقول",width=26, font = ("Janna LT",9,'bold'),bg="#90a4ae",command=self.clear)
        btn_clear.place(x=6, y=495)

        btn_exit=Button(frame1, text=" اغلاق البرنامج",width=26, font = ("Janna LT",9,'bold'),bg="#90a4ae",command=self.popup)
        btn_exit.place(x=6, y=535)
        #----------------------------      ----------------
        
        #------------------------ازرار البحث -----------------------------
        fr_se = Frame(self.root ,bg="#78909c",width=943 ,height= 40  ).place(x=2 ,y=30)
        lbl_se = Label(fr_se, text=" البحث عن طالب " ,fg= "red" ,bg="#78909c" ,font = ("Helvetica World",10 )).place(x=850 ,y=35) 
        btn_search=Button(fr_se, text="بحث",width=10, font = ("Janna LT",7,'bold'),bg="#448aff",command= self.search_by)
        btn_search.place(x=422, y=34)
        comb_se= ttk.Combobox(fr_se ,justify="center",textvariable= self.se_by_var ,font = ("Helvetica World",9),state="readonly",width= 17)
        comb_se["values"] = ("id", "name" ,"email", "phone")
        comb_se.place(x=700 ,y=35)
        en_se= Entry(fr_se,justify="right",width=25,textvariable=self.search_var, font = ("Helvetica World",9))
        en_se.place(x=515, y=36)
        
        #--------------------------treeview ------------------------------
        fr_tv=Frame(self.root, bg= "#cfd8dc", height=640 ,width=943 ).place(x=2, y=67)
        scroll_x = Scrollbar(fr_tv,orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM , fill=X)
        scroll_y = Scrollbar(fr_tv,orient=VERTICAL)
        scroll_y.pack(side=RIGHT , fill=Y)

        self.tree=ttk.Treeview(fr_tv,xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        self.tree.place(x=2,y=67 , height=535 ,width=942)
        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview) 
        #----------------------columns-----------------------
        self.tree["columns"]=("gender","stage","phone","email","name","id")
        self.tree.column("id",width=30 ,anchor="center")
        self.tree.column("name",width=60 ,anchor="center")
        self.tree.column("email",width=60 ,anchor="center")
        self.tree.column("phone",width=50 ,anchor="center")
        self.tree.column("stage",width=40 ,anchor="center")
        self.tree.column("gender",width=40 ,anchor="center")

        #------------------headings-----------------------
        self.tree['show']='headings'
        self.tree.heading("gender",text= "الجنس")
        self.tree.heading("stage",text= "المرحلة")
        self.tree.heading("phone",text=" رقم الهاتف")
        self.tree.heading("email",text=" الايميل")
        self.tree.heading("name",text=" اسم الطالب")
        self.tree.heading("id",text=" رقم التسجيل")
        self.tree.bind("<ButtonRelease-1>", self.get_cursor)
        #---------------------- con + cur   ----------------------------
        
    
    def add_student(self):
        # Adds a new student record to the students table. Gets input values from the UI form, 
        # constructs an INSERT statement with parameters to avoid SQL injection, executes the statement,
        # commits the transaction, displays success/error message, clears the form, and refreshes the treeview.
        # Get the values from the entry fields
        id_val = self.id_var.get()
        name_val = self.name_var.get()
        email_val = self.email_var.get()
        phone_val = self.phone_var.get()
        stage_val = self.stage_var.get()
        gender_val = self.gender_var.get()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\d{10}$'
        # existing_emails = []
        # self.con = sqlite3.connect('students.db')
        # self.cur = self.con.cursor()
        # self.cur.execute("SELECT email FROM students")
        # ems=self.cur.fetchall()
        # for em in ems:
        #     existing_emails.append(em)
        # existing_ids = []
        # print(existing_ids)
        # self.con = sqlite3.connect('students.db')
        # self.cur = self.con.cursor()
        # self.cur.execute("SELECT id FROM students")
        # ids=self.cur.fetchall()
        # for i in ids:
        #     existing_ids.append(i)

        # Check if the values are empty
        if id_val==""or name_val=="" or email_val=="" or phone_val=="" or stage_val=="" or gender_val=="":
            messagebox.showerror("تنبيه", "من فضلك ادخل البيانات الناقصة")
            return
        elif not re.fullmatch(email_pattern, self.email_var.get()):
            messagebox.showerror("تنبيه", "خطأ في كتابة البريد الالكتروني")
            return
        elif not re.fullmatch(phone_pattern, self.phone_var.get()):
            messagebox.showerror("تنبيه", "خطأ في كتابة رقم الهاتف")
            return
            
        # # elif self.email_var.get() in existing_emails:
        #     messagebox.showerror("تنبيه", "Email already exists")
        #     return
        
        else:
            sql = """
                INSERT INTO students ( id,gender, stage,phone,name,email )
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (   id_val, gender_val,stage_val,phone_val,name_val,email_val )

            try:
                self.cur.execute(sql, values)
                self.con.commit()
                messagebox.showinfo("اشعار", "تم اضافة الطالب بنجاح")
               # existing_ids.append("id_val")
                self.clear()
                self.fetch_all()
            except sqlite3.Error as e:
                messagebox.showerror("Error", str(e))
            #------------------------- treeview اظهار البيانات على ----------
    def fetch_all(self) :
        # Connects to the SQLite database file students.db to manage student data.
        # Opens a connection to the database file students.db.
        # Gets a cursor object to execute SQL statements.
        # Executes a SELECT statement to get all rows from the students table. 
        # Fetches all rows returned by the SELECT statement into the records variable.
        # Checks if records is not empty.
        # Deletes existing rows from the treeview widget.
        # Loops through the rows and inserts them into the treeview.
        # Commits the changes to the database.
        self.con = sqlite3.connect('students.db'        # Connects to the SQLite database file students.db to manage 
        # Connects to the SQLite database file students.db to manage student data. 
        # The database connection and cursor objects are used for executing SQL statements.
        # student data. The database connection and cursor objects 
        # are used for executing SQL statements.
)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM students")
        records = self.cur.fetchall()
        if len(records) != 0 :
            self.tree.delete(*self.tree.get_children())
            for record in records:
                self.tree.insert("",END,values=record)
        self.con.commit()
             
    def delete (self):
        if self.find_var.get() =="" :
            messagebox.showinfo("تنبيه", " من فضلك أدخل رقم التسجبل في حقل الادخال")
            return
        else:
            response= messagebox.askquestion("حذف", "هل انت متأكد من حذف الطالب نهائيا?", icon='warning')
            print(response)
            if response=="yes":
                self.con = sqlite3.connect('students.db')
                self.cur = self.con.cursor()
                self.cur.execute('DELETE FROM students WHERE id = ?', (self.find_var.get(),))
                 # cur.execute('delete  FROM students WHERE "id" = 0')
                messagebox.showinfo("Success", " تم حذف الطالب بنجاح")
            elif response=="no" :
                return
        self.con.commit()
        self.fetch_all()
        self.clear()
        self.con.close()

    def clear (self):
        # Clears all student data fields by setting them to empty strings.
        # This resets the form fields after an operation like updating or deleting a student.
        # Allows entering data for a new student.
        self.id_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.stage_var.set("")
        self.gender_var.set("")
        self.find_var.set("")
        self.search_var.set("")
    
    def get_cursor (self,ev):
        # Gets the data from the selected row in the Treeview widget
        # and populates the input fields with the corresponding data
        # for editing the student record.
        cursor_row = self.tree.focus()
        cursor_item = self.tree.item(cursor_row)
        row = cursor_item ['values']
        self.id_var.set(row[5])
        self.name_var.set(row[4])
        self.email_var.set(row[3])
        self.phone_var.set(row[2])
        self.stage_var.set(row[1])
        self.gender_var.set(row[0])

    def update(self):
        # Updates a student record in the database by taking input from the UI form fields
        # Validates form fields are not empty before updating
        # Connects to the SQLite database, gets a cursor 
        # Executes an UPDATE statement to update the student record with the given ID
        # Commits the change, refreshes the UI table, clears the form fields
        # Closes the database connection
        if self.id_var.get() == '' or self.name_var.get() == "" or self.email_var.get()=="" or self.phone_var.get()=="" or self.stage_var.get()=="" or self.gender_var.get()=="" :
            messagebox.showerror("خطأ","من فضلك املأ كافة الحقول ")
        else:
            self.con = sqlite3.connect('students.db')
            self.cur = self.con.cursor()
        
            self.cur.execute("UPDATE students SET name=?,email=?,phone=?,stage=?,gender=? WHERE id=?",
                                                                (self.name_var.get(),
                                                                 self.email_var.get(),
                                                                 self.phone_var.get(),
                                                                 self.stage_var.get(),
                                                                 self.gender_var.get(),
                                                                 self.id_var.get()))
        self.con.commit()
        self.fetch_all()
        self.clear()
        self.con.close()
    def search_by (self) :
        # Searches the students table by the given search criteria 
        # Connects to the SQLite database, gets a cursor
        # Executes a SELECT statement to get matching records
        # Checks if there are results, deletes existing rows in the UI
        # Inserts the result records into the UI table
        # Commits changes and closes the database connection
        self.con = sqlite3.connect('students.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM students where " +
        str(self.se_by_var.get())+" LIKE '%"+ str(self.search_var.get())+"%'" )
        records = self.cur.fetchall()
        if len(records) != 0 :
            self.tree.delete(*self.tree.get_children())
            for record in records:
                self.tree.insert("",END,values=record)
        self.con.commit()
        # self.fetch_all()        
        self.con.close()
    
    def popup(self):
        # Shows a confirmation popup to ask if the user wants to close the program
        # Prints and returns the response 
        # If 'yes', exits the program
        # If 'no', returns to continue running
        response=messagebox.askquestion("اغلاق ","هل تريد اغلاق البرنامج  ?", 
        icon='warning')
        if   response == "yes":
            sys.exit()
        else:
            return
        
db = Database("students.db")
db.cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, stage TEXT NOT NULL, gender TEXT NOT NULL)")
root = Tk()
student = Student(root, "students.db")
student.fetch_all()
root.mainloop()
