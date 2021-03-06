from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for,flash
from functools import wraps

from ..controller import *
admin = Blueprint('admin',
                __name__,
                template_folder="admin_templates",
                static_folder="admin_static",
                url_prefix='/admin')

# @admin.route('/index')
# def index():
#     testing()
#     return "render_template('index.html')"

@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return redirect(url_for('admin.personalinfo'))

@admin.route('/personalinfo',methods=['GET','POST'])
@login_required
def personalinfo():
    if request.method =="POST":
        bttn = request.form['bttn']
        print(bttn)
        mysql_query(''' UPDATE `bcms`.`user_master`
                    SET
                    `first_name` = '{}',
                    `middle_name` = '{}',
                    `last_name` = '{}',
                    `gender` = '{}',
                    `dob` = '{}',
                    `contact_no` = '{}',
                    `email` = '{}',
                    `password` = '{}',
                    `address_line_1` = '{}',
                    `address_line_2` = '{}',
                    `city` = '{}',
                    `state` = '{}',
                    `pincode` = '{}'
                    WHERE `UID` = {};  '''.format(
                        request.form['firstname'],request.form['middlename'],request.form['lastname'],
                        request.form['gender'],request.form['dob'],request.form['mobileno'],request.form['email'],
                        request.form['password'],request.form['addressline1'],request.form['addressline2'],
                        request.form['city'],request.form['state'],request.form['pincode'],request.form['bttn'] ) )
        flash("Personal Info Updated.")
        return redirect(url_for('admin.personalinfo'))
    data = mysql_query("select * from user_master where email ='{}'; ".format(session['email']))
    # print(data)
    return render_template('admin_personalinfo.html',data=data)

@admin.route('/changepassword',methods=['GET','POST'])
@login_required
def changepassword():
    if request.method=="POST":
        oldpassword = request.form['oldpassword']
        newpassword = request.form['retypepassword']
        mysql_query("update user_master SET password='{}' where email='{}'; ".format(newpassword,session['email']))
        flash("Password Changed")
        return redirect(url_for('admin.changepassword'))
    return render_template("admin_cp.html")

@admin.route('/branch')
@login_required
def branch():
    branchdetails=mysql_query(''' SELECT 
    branch_master.BID,
    branch_master.branch_name,
    branch_master.branch_email,
    CONCAT(branch_master.Address_Line1,
            ', ',branch_master.Address_Line2,
            ', ',branch_master.Address_Line3) AS 'address',
    branch_master.area,
    branch_master.city,
    branch_master.pincode,
    branch_master.state,
    
    CONCAT(user_master.first_name,
            ' ',
            user_master.last_name) AS 'fullname'
FROM
    branch_master
        INNER JOIN
    manager_master ON manager_master.bid = branch_master.bid
        INNER JOIN
    user_master ON user_master.uid = manager_master.uid; ''')

    # return "hello there is an error! please fixx it bruh"

    return render_template('admin_branch.html',branchdetails=branchdetails)




@admin.route('/addbranch',methods=["POST"])
@login_required
def addbranch():
    if request.method=="POST":
        if "insert" in request.form:
            try:
                mysql_query('''INSERT INTO `bcms`.`branch_master`
                            (`branch_name`,
                            `branch_email`,
                            `Address_Line1`,
                            `Address_Line2`,
                            `Address_Line3`,
                            `area`,
                            `city`,
                            `state`,
                            `pincode`)
                            VALUES('{}','{}','{}','{}','{}','{}','{}','{}',{}); '''.format(request.form['branch_name'],request.form['email'],request.form['addr1'],request.form['addr2'],request.form['addr3'],request.form['area'],request.form['city'],request.form['state'],request.form['pincode']))
            except Exception as e:
                return str(e)
            return redirect(url_for("admin.branch"))

        if "edit" in request.form:
            mysql_query('''UPDATE `bcms`.`branch_master`
                            SET
                            `branch_name` = '{}',
                            `branch_email` = '{}',
                            `Address_Line1` = '{}',
                            `Address_Line2` = '{}',
                            `Address_Line3` = '{}',
                            `area` = '{}',
                            `city` = '{}',
                            `state` = '{}',
                            `pincode` = {}
                            WHERE `BID` = {};
                            '''.format(request.form['branch_name'],request.form['email'],request.form['addr1'],request.form['addr2'],request.form['addr3'],request.form['area'],request.form['city'],request.form['state'],request.form['pincode'],request.form['edit']))


            return redirect(url_for("admin.branch"))


@admin.route('/empdetails')
@login_required
def empdetails():
    EmpDetail = mysql_query('''SELECT 
                                employee_category.Description,
                                employee_master.Joining_Date,
                                employee_master.Leaving_Date,
                                employee_master.Time_period,
                                employee_master.Salary,
                                user_master.gender,
                                user_master.dob,
                                user_master.contact_no,
                                user_master.email,
                                CONCAT(user_master.first_name,
                                        ' ',
                                        user_master.middle_name,
                                        ' ',
                                        user_master.Last_name) AS 'fullname',
                                CONCAT(user_master.address_line_1,
                                        ', ',
                                        user_master.address_line_2,
                                        ', ',
                                        user_master.address_area,
                                        ',',
                                        user_master.city,
                                        ', ',
                                        user_master.state,
                                        ',',
                                        user_master.pincode,
                                        ',',
                                        user_master.country) AS 'address'
                            FROM
                                user_master
                                    INNER JOIN
                                employee_master ON employee_master.uid = user_master.uid
                                    INNER JOIN
                                employee_category ON employee_category.ecatid = employee_master.ecatid;''')

    return render_template('emp_details.html',EmpDetail=EmpDetail)


@admin.route('/mandetails')
@login_required
def mandetails():
    branch = mysql_query("select branch_master.BID,branch_master.branch_name from branch_master left join manager_master on manager_master.BID =branch_master.BID where manager_master.BID IS NULL ")
    Man_Detail = mysql_query('''SELECT 
                                    branch_master.branch_name,
                                    manager_master.joining_date,
                                    manager_master.leaving_date,
                                    user_master.gender,
                                    user_master.dob,
                                    user_master.contact_no,
                                    user_master.email,
                                    CONCAT(user_master.first_name,
                                            ' ',
                                            user_master.middle_name,
                                            ' ',
                                            user_master.Last_name) AS 'fullname',
                                    CONCAT(user_master.address_line_1,
                                            ', ',
                                            user_master.address_line_2,
                                            ', ',
                                            user_master.address_area,
                                            ',',
                                            user_master.city,
                                            ', ',
                                            user_master.state,
                                            ',',
                                            user_master.pincode,
                                            ',',
                                            user_master.country) AS 'address'
                                FROM
                                    user_master
                                        INNER JOIN
                                    manager_master ON manager_master.uid = user_master.uid
                                        INNER JOIN
                                    branch_master ON manager_master.bid = branch_master.bid;''')

    return render_template('manager_details.html', Man_Detail=Man_Detail,branch=branch)




@admin.route('/memberdetails')
@login_required
def memberdetails():
    MemDetail = mysql_query ('''SELECT  
                                membership_master.memid,
                                membership_master.description,
                                membership_master.duration,
                                user_master.gender,
                                user_master.dob,
                                user_master.contact_no,
                                user_master.email,
                                CONCAT(user_master.first_name,
                                        ' ',
                                        user_master.middle_name,
                                        ' ',
                                        user_master.Last_name) AS 'fullname',
                                CONCAT(user_master.address_line_1,
                                        ', ',
                                        user_master.address_line_2,
                                        ', ',
                                        user_master.address_area,
                                        ',',
                                        user_master.city,
                                        ', ',
                                        user_master.state,
                                        ',',
                                        user_master.pincode,
                                        ',',
                                        user_master.country) AS 'address'
                                FROM
                                    user_master
                                        INNER JOIN
                                    member_master ON member_master.uid = user_master.uid
                                        INNER JOIN
                                    membership_master ON membership_master.memid = member_master.memid;''')
    
    
    return render_template('member_details.html',MemDetail=MemDetail)


@admin.route('/MemComplaints')
@login_required
def mem_complaint_history():
    complaint_history = mysql_query(''' SELECT 
                                        `user_complaint`.`CID`,
                                        `user_complaint`.`BID`,
                                        `user_complaint`.`MID`,
                                        `user_complaint`.`Subject`,
                                        `user_complaint`.`Description`,
                                        `user_complaint`.`Timestamp`
                                    FROM
                                        `bcms`.`user_complaint`;''')

    return render_template('member_complaints.html',complaint_history=complaint_history)



@admin.route('/EmpComplaints')
@login_required
def emp_complaint_hist():
    complaint_hist = mysql_query(''' SELECT 
                                        `employee_complaint`.`ECOMID`,
                                        `employee_complaint`.`EID`,
                                        `employee_complaint`.`BID`,
                                        `employee_complaint`.`Subject`,
                                        `employee_complaint`.`Description`,
                                        `employee_complaint`.`Timestamp`
                                    FROM
                                        `bcms`.`employee_complaint`;''')

    return render_template('emp_complaints.html',complaint_hist=complaint_hist)

@admin.route('/ViewFeedbacks')
@login_required
def mem_feedbacks():
    feedbacks = mysql_query(''' SELECT 
                                        `feedback`.`FID`,
                                        `feedback`.`BID`,
                                        `feedback`.`MID`,
                                        `feedback`.`Subject`,
                                        `feedback`.`Description`,
                                        `feedback`.`Timestamp`
                                    FROM
                                        `bcms`.`feedback`;''')

    return render_template('admin_feedback.html',feedbacks=feedbacks)


@admin.route('/addmanager',methods=["POST"])
@login_required
def addmanager():
    if request.method=="POST":
        if "insert" in request.form:
            mysql_query('''insert into user_master
                        (UTMID,first_name,middle_name,last_name,gender,email,password,dob,contact_no,address_line_1,address_line_2,address_area,city,state,country,pincode) values(2,'{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}','{}','{}',{});'''.format(
                request.form['firstname'], request.form['middlename'], request.form['lastname'], request.form['gender'],
                request.form['email'], request.form['password'],
                request.form['dob'], request.form['contactno'], request.form['adl1'], request.form['adl2'],
                request.form['area'], request.form['city'], request.form['state'], request.form['country'],
                request.form['pincode']))

            UID = mysql_query("select UID from user_master where email='{}'; ".format(request.form['email']))
            UID= UID[0]['UID']

            mysql_query('''insert into manager_master
                        (BID,UID,Joining_Date) values({},{},'{}');'''.format(request.form['brch_id'],UID,request.form['joiningdate']))

            return redirect(url_for("admin.mandetails"))


####################################################################################################################################################
####################################################################################################################################################
#                                                                       REPORTS
@admin.route('/user_master/',methods=['GET','POST'])
def user_master():
    if request.method == "POST":
        data = mysql_query("select user_master.First_Name,user_master.middle_name,user_master.last_name,user_master.email,user_master.contact_no from user_master inner join user_type_master on user_master.UTMID=user_type_master.UTMID where user_master.gender like '{}' or user_master.city like '{}' or user_master.state like '{}' or user_master.country like '{}';".format(request.form['gender'],request.form['city'],request.form['state'],request.form['country']   ))
        ch = data[0].keys()
        print(ch)
        return render_template('reports/locationwise.html',data=data,ch=ch)
    gender = mysql_query("Select distinct(gender) from user_master")
    city = mysql_query("Select distinct(city) from user_master")
    state = mysql_query("select distinct(state) from user_master")
    country = mysql_query("select distinct(country) from user_master")
    role = mysql_query("select role from user_type_master")
    return render_template('reports/locationwise.html',gender=gender,city=city,state=state,country=country,role=role,data='')

@admin.route('/sdata/',methods=['GET','POST'])
def salrieddata():
    if request.method=="POST":
        if request.form['branch'] =="":
            data = mysql_query("select branch_master.branch_name,employee_category.description,truncate(AVG(employee_master.Salary),2) AS 'Average Salary' from employee_master inner join branch_master on employee_master.BID=branch_master.BID inner join employee_category  on employee_category.ECATID = employee_master.ECATID group by employee_category.Description;")
        else:
            data = mysql_query("select branch_master.branch_name,employee_category.description,truncate(AVG(employee_master.Salary),2) AS 'Average Salary' from employee_master inner join branch_master on employee_master.BID=branch_master.BID inner join employee_category  on employee_category.ECATID = employee_master.ECATID where branch_master.BID={} group by employee_category.Description; ".format(request.form['branch']))
        return render_template('reports/salariedata.html', data=data, ch=data[0].keys())

    branch = mysql_query("select BID,branch_name from branch_master")
    return render_template('reports/salariedata.html', branch=branch, data='')

@admin.route('/membershipwise/',methods=['GET','POST'])
def membershipwise():
    if request.method == "POST":
        branch = request.form['branch']
        if branch != "":
            data = mysql_query('''select branch_master.branch_name,count(member_master.MID) as 'Total No of of Members' from membership_master inner join member_master on membership_master.MEMID = member_master.MEMID inner join branch_master on branch_master.BID=member_master.BID where branch_master.bid ={} group by branch_master.BID ;'''.format(request.form['branch']))

            return render_template('reports/membershipwise.html', 
            branch=request.form['branch'], data=data, ch=data[0].keys())
 
    data = mysql_query('''select branch_master.branch_name,count(member_master.MID) as 'Total No of of Members' from membership_master inner join member_master on membership_master.MEMID = member_master.MEMID inner join branch_master on branch_master.BID=member_master.BID group by branch_master.BID; ''')


    branch = mysql_query("select BID,branch_name from branch_master")
    return render_template('reports/membershipwise.html',branch=branch,data=data,
    ch=data[0].keys())

@admin.route('/leavesGranted/',methods=['GET','POST'])
def leavesGranted():
    if request.method=='POST':
        data = mysql_query('''SELECT 
        branch_master.branch_name,
        SUM(IF(emp_leave.Status = 'Approved',1,0)) AS 'Leaves Approved',
        SUM(IF(emp_leave.Status = 'Disapproved',1,0)) AS 'Leaves Disapproved'
        FROM
        branch_master
            INNER JOIN
        emp_leave ON branch_master.BID = emp_leave.BID where branch_master.BID={} group by branch_master.BID;'''.format(request.form['branch']))
        return render_template('reports/leavesGranted.html', branch=request.form['branch'],data=data, ch=data[0].keys())
    data = mysql_query('''SELECT 
    branch_master.branch_name,
    SUM(IF(emp_leave.Status = 'Approved',1,0)) AS 'Leaves Approved',
    SUM(IF(emp_leave.Status = 'Disapproved',1,0)) AS 'Leaves Disapproved'
    FROM
    branch_master
        INNER JOIN
    emp_leave ON branch_master.BID = emp_leave.BID group by branch_master.BID;''')
    branch = mysql_query("select BID,branch_name from branch_master")
    return render_template('reports/leavesGranted.html', branch=branch, data=data,
                           ch=data[0].keys())


@admin.route('/MaxComplaints',methods=['GET','POST'])
def MaxComplaints():
    if request.method == "POST":
        start = request.form['st_date']
        end = request.form['end_date']
        complaint = request.form['complaint']

        if complaint.lower() == "member" and start == "" and end == "":
            data = mysql_query("select count(user_complaint.cid) as 'Total',branch_master.bid,branch_master.branch_name from user_complaint inner join branch_master on user_complaint.bid = branch_master.bid group by(branch_master.bid) order by count(user_complaint.cid) desc;")
            return render_template('reports/max_complaints.html', data=data)

        if complaint.lower() == "member" and start != "" and end != "":
            data = mysql_query("select count(user_complaint.cid) as 'Total', date(user_complaint.timestamp) as 'comp_dt' ,branch_master.bid,branch_master.branch_name from user_complaint inner join branch_master on user_complaint.bid = branch_master.bid  where date(user_complaint.timestamp) between '{start}' and '{end}' group by(branch_master.bid) order by count(user_complaint.cid) desc;".format(start=start,end=end))
            return render_template('reports/max_complaints.html', data=data, start=start, end=end)

        if complaint.lower() == "employee" and start == "" and end == "":
            data = mysql_query("select count(employee_complaint.ecomid) as 'Total',branch_master.bid,branch_master.branch_name from employee_complaint inner join branch_master on employee_complaint.bid = branch_master.bid group by(branch_master.bid) order by count(employee_complaint.ecomid) desc;")
            return render_template('reports/max_complaints.html', data=data)

        if complaint.lower() == "employee" and start != "" and end != "":
            data = mysql_query("select count(employee_complaint.ecomid) as 'Total', date(employee_complaint.timestamp) as 'comp_dt' ,branch_master.bid,branch_master.branch_name from employee_complaint inner join branch_master on employee_complaint.bid = branch_master.bid where date(employee_complaint.timestamp) between '{start}' and '{end}' group by(branch_master.bid) order by count(employee_complaint.ecomid) desc;".format(start=start,end=end))
            return render_template('reports/max_complaints.html', data=data, start=start, end=end)

    return render_template('reports/max_complaints.html')



@admin.route('/MaxFeedback',methods=['GET','POST'])
def MaxFeedback():
    data = mysql_query("select count(feedback.fid) as 'total',branch_master.bid,branch_master.branch_name from feedback inner join branch_master on feedback.bid = branch_master.bid group by(branch_master.bid) order by count(feedback.fid) desc;")
    # return render_template('reports/max_feedback.html', data=data)
    if request.method == "POST":
        start = request.form['st_date']
        end = request.form['end_date']
        # if start == "" and end == "":
        if start != "" and end != "":
            data = mysql_query("select count(feedback.fid) as 'total', date(feedback.timestamp) as 'fb_date' ,branch_master.bid,branch_master.branch_name from feedback inner join branch_master on feedback.bid = branch_master.bid where date(feedback.Timestamp) between '{start}' and '{end}' group by branch_master.bid order by 'total' desc;".format(start=start,end=end))
            return render_template('reports/max_feedback.html',data=data,start=start,end=end)

    return render_template('reports/max_feedback.html',data=data)


# employees in each category report

@admin.route('/emp_category',methods=['GET','POST'])
def emp_category():
    #if request.method == 'POST':
    data = mysql_query ("select employee_category.ecatid AS 'CATEGORY ID',  employee_category.description AS 'CATEGORY', count(employee_master.eid) AS 'TOTAL EMPLOYEES'  from employee_master inner join employee_category on employee_master.ecatid = employee_category.ecatid group by(employee_category.ecatid) order by count(employee_master.eid) desc");
    return render_template('reports/emp_category.html', data=data,ch=data[0].keys())


@admin.route('/emp_maxbranch',methods=['GET','POST'])
def emp_max_branch():
    data = mysql_query("select branch_master.bid AS 'BRANCH ID', branch_master.branch_name AS 'BRANCH NAME' , count(employee_master.eid) AS 'NUMBER OF EMPLOYEES'from employee_master inner join branch_master on employee_master.bid = branch_master.bid group by(branch_master.bid) order by count(employee_master.eid) desc;");
    if request.method == "POST":
        start = request.form['st_date']
        end = request.form['end_date']
        if start != "" and end != "":
            data = mysql_query("select branch_master.bid AS 'BRANCH ID', branch_master.branch_name AS 'BRANCH NAME' , count(employee_master.eid) AS 'NUMBER OF EMPLOYEES'from employee_master inner join branch_master on employee_master.bid = branch_master.bid where date(employee_master.joining_date) between '{start}' and '{end}' group by(branch_master.bid) order by count(employee_master.eid) desc;".format(start=start,end=end))
            return render_template('reports/emp_maxbranch.html', data=data, start=start, end=end, ch=data[0].keys())

    return render_template('reports/emp_maxbranch.html', data=data,ch=data[0].keys())

@admin.route('/payment',methods=['GET','POST'])
def payment():
    if request.method== "POST":
        branch = request.form['branch']
        data = mysql_query('''select branch_master.branch_name,AVG(payment.Amount) as 'Annual Average Payment',SUM(payment.Amount) AS 'Annual Total Payment' from payment inner join member_master on member_master.MID=payment.MID inner join branch_master on branch_master.BID=member_master.BID where branch_master.BID={} group by branch_master.BID;'''.format(branch))
        return render_template('reports/payment_report.html', data=data, branch=branch,
                               ch=data[0].keys())
        
    data = mysql_query('''select branch_master.branch_name,AVG(payment.Amount) as 'Annual Average Payment',SUM(payment.Amount) AS 'Annual Total Payment' from payment inner join member_master on member_master.MID=payment.MID inner join branch_master on branch_master.BID=member_master.BID group by branch_master.BID;''')
    branch= mysql_query("select BID,branch_name from branch_master")
    return render_template('reports/payment_report.html',data=data,branch=branch,
    ch=data[0].keys())

@admin.route('/indipayments',methods=['GET','POST'])
def indipayments():
    data = mysql_query('''select concat(user_master.First_name," ",user_master.last_name) as 'Full Name',SUM(transaction.amount)as 'Amount Paid',payment.amount as 'Total Membership Amount' from transaction inner join payment on payment.PAYID = transaction.PAYID inner join member_master on member_master.MID = payment.MID inner join branch_master on branch_master.BID=member_master.BID inner join user_master ON user_master.UID = member_master.UID group by payment.amount;  ''')
    return render_template('reports/indipayments.html',data=data)
