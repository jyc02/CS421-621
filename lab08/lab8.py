#!/usr/bin/env python3
# Turn on debug mode
import cgitb
import cgi
cgitb.enable()

form = cgi.FieldStorage()

#print required headers 
print("Content-Type:text/html;charset=utf-8")
print()

#connect to database
import pymysql

#create an pymysql object and assign the credidentals
my_con = pymysql.connect(db='student', user='root', passwd='password', host='localhost')
c=my_con.cursor()

#clear the database if not empty
# c.execute("TRUNCATE mytable")

if "save" in form:
    fullname=str(form.getvalue('name'))
    midterm1=str(form.getvalue('midterm1'))
    midterm2=str(form.getvalue('midterm2'))
    final=str(form.getvalue('final'))
    atag = f'<a href="lab8.html">go back</a>'
    avg = 0
    if midterm1.replace(".", "").isnumeric() and midterm2.replace(".", "").isnumeric() and final.replace(".", "").isnumeric():
        avg = int((float(midterm1) + float(midterm2) + (2*float(final)))/4)
        c.execute("""INSERT INTO student_grade VALUES(%s, %s)""", (fullname, avg))
        print("success!")
    
        print("<br>" + atag)
    else:
        print("WARNING: INVALID INPUT")
        print("<br>" + atag)
    

    my_con.commit()

if "delete" in form:
    name = str(form.getvalue('delname'))
    atag = f'<a href="lab8.html">go back</a>'
    print(atag)
    c.execute("SELECT name FROM student_grade")
    print("deleted if exists:")
    print(name)
    c.execute("""DELETE FROM student_grade WHERE name= %s""", (name))
    my_con.commit()

if "record" in form:
    # c.execute("SELECT * FROM student_grade")
    # print(c.fetchall())
    atag = f'<a href="lab8.html">go back</a>'
    print("<br>" + atag)
    print("<style>")
    print("table, th, td { border:1px solid black; }")
    print("</style>")
    print("<table>")
    print("<tr>")
    print("<th>Name</th>")
    print("<th>Avg Grade</th>")
    print("</tr>")

    c.execute("SELECT * FROM student_grade")
    for i in c.fetchall():
        print("<tr>")
        print("<td>" + i[0] + "</td>")
        print("<td>" + str(i[1]) + "</td>")
        print("</tr>")
    
    print("</table>")



