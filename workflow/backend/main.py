from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors 

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "hello"

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'beach6'
app.config['MYSQL_DB'] = 'workflow'

mysql = MySQL(app)



#GETTERS
def getPasswordByEmail(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT password FROM users WHERE email = %s"
    target = (email,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    if dbdata:
        return dbdata
    else:
        return ""


def getMaxId(table,id):
    cursor = mysql.connection.cursor()
    sql = f'SELECT {id} FROM {table} ORDER BY {id} DESC'
    cursor.execute(sql,)
    maxId = cursor.fetchone()
    cursor.close()
    if maxId == None:
        return 0
    else:
        return maxId[0]


def getUserInfoByEmail(userEmail):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT userid, email, firstname, lastname,role FROM users WHERE email = %s"
    target = (userEmail,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close()
    return jsonify(dbdata)


def getUserLoginInfoByEmail(userEmail):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT email,password FROM users WHERE email = %s"
    target = (userEmail,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close()
    return jsonify(dbdata)


def getUserInfoById(userId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE userid = %s"
    target = (userId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    return jsonify(dbdata)


def getUserIdByName(firstname,lastname):
    print(firstname,lastname)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT userid FROM users WHERE firstname = %s AND lastname = %s"
    target = (firstname,lastname)
    cursor.execute(sql, target)
    print("test 124215")
    dbdata = cursor.fetchone()
    cursor.close
    print(dbdata)
    return dbdata["userid"]


def getOrgIdByOrgName(orgName):
    cursor = mysql.connection.cursor()
    sql = "SELECT orgid FROM organizations WHERE name = %s"
    target = (orgName,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    return dbdata[0]
    

def getOrgIdByUserId(userId):
    cursor = mysql.connection.cursor()
    sql = "SELECT orgid FROM users WHERE userid = %s"
    target = (userId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    return dbdata[0]


def getUserIdByEmail(userEmail):
    cursor = mysql.connection.cursor()
    sql = "SELECT userid FROM users WHERE email = %s"
    target = (userEmail,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    print(dbdata)
    return dbdata[0]


def getAllUsersInOrg(userEmail):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    cursor = mysql.connection.cursor()
    sql = "SELECT firstname,lastname,email,gender,age,role FROM users WHERE orgid = %s"
    target = (orgId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchall()
    cursor.close
    return jsonify(dbdata)


def getDataOfAllUsersInOrg(userEmail):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT firstname,lastname,email,gender,age,role FROM users WHERE orgid = %s ORDER BY firstname"
    target = (orgId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchall()
    cursor.close
    return jsonify(dbdata)


def getAllAdminsInOrg(userEmail):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT firstname,lastname,email,gender,age,role FROM users WHERE orgid = %s AND role = %s ORDER BY firstname"
    target = (orgId,"A")
    cursor.execute(sql, target)
    dbdata = cursor.fetchall()
    cursor.close
    return jsonify(dbdata)


def getAllPosts(userEmail):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
    SELECT postid,author,title,content,date 
    FROM posts 
    JOIN users ON users.userid = posts.author 
    WHERE orgid=%s 
    ORDER BY date DESC
    """
    target = (orgId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    postsArray =jsonify(dbdata).get_json()
    for postRecord in postsArray:
        authorId = postRecord["author"]
        authorDataObj = getUserInfoById(authorId).get_json()
        authorFullName = f'{authorDataObj["firstname"]} {authorDataObj["lastname"]}'
        postRecord["author"] = authorFullName
    return jsonify(postsArray)
    

def getAllTasks(userEmail):
    userId = getUserIdByEmail(userEmail)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM tasks WHERE receiver=%s ORDER BY duedate DESC"
    target = (userId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    tasksArray =jsonify(dbdata).get_json()
    for taskRecord in tasksArray:
        senderId = taskRecord["sender"]
        senderDataObj = getUserInfoById(senderId).get_json()
        senderFullName = f'{senderDataObj["firstname"]} {senderDataObj["lastname"]}'
        taskRecord["sender"] = senderFullName
    return jsonify(tasksArray)


def getTaskByTitleAndDate(taskTitle):
    cursor = mysql.connection.cursor()
    sql = "SELECT taskid FROM tasks WHERE title = %s"
    target = (taskTitle,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchone()
    cursor.close
    if dbdata == None:
        raise Exception("Task not in database")
    else:
        return dbdata[0]
    

def getGroupData(groupId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
    SELECT *
    FROM groups 
    WHERE groupid = %s
    """
    target = (groupId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    return dbdata


def getGroupsUserIsMember(userEmail):
    userId = getUserIdByEmail(userEmail)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
    SELECT groupid
    FROM groupmanager 
    WHERE userid = %s
    """
    target = (userId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    return dbdata


def getNumberOfUsersInGroup(selectedGroup):
    groupId = selectedGroup
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT userid FROM groupmanager WHERE groupid = %s"
    target = (groupId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    return len(dbdata)


def getAllMessages(groupId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM messages WHERE groupid = %s"
    target = (groupId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchall()
    cursor.close
    return jsonify(dbdata)


def getUserEmailAndNameFromUserId(userId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT email,firstname,lastname FROM users WHERE userid = %s"
    target = (userId,)
    cursor.execute(sql,target)
    dbdata = cursor.fetchone()
    cursor.close
    return dbdata


def getAllGroupsInOrg(userEmail):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
    SELECT groupid,name,leader
    FROM groups 
    JOIN users ON users.userid = groups.leader 
    WHERE orgid=%s 
    ORDER BY orgid
    """
    target = (orgId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchall()
    cursor.close
    return dbdata


def getAllGroupsUserIsMemberOf(userEmail):
    userId = getUserIdByEmail(userEmail)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
    SELECT *
    FROM groups 
    JOIN groupmanager ON groupmanager.groupid = groups.groupid 
    WHERE groupmanager.userid=%s 
    """
    target = (userId,)
    cursor.execute(sql, target)
    dbdata = cursor.fetchall()
    cursor.close
    return jsonify(dbdata)


def getGroupIdFromNameAndLeaderId(groupName,groupLeaderId):
    cursor = mysql.connection.cursor()
    sql = "SELECT groupid FROM groups WHERE name = %s AND leader = %s"
    target = (groupName,groupLeaderId)
    cursor.execute(sql,target)
    dbdata = cursor.fetchone()
    cursor.close
    print(dbdata)
    return dbdata[0]


def getOperator(operatorString):
    match operatorString:
        case "Equal to:":
            return "="
        case "Lower than:":
            return "<"
        case "Greater than:":
            return ">"
        case "Must start with:":
            return "%"
        case _:
            return 0

#ADDERS/CREATORS
def addNewPost(recordObj):
    cursor = mysql.connection.cursor()
    nId = getMaxId("posts","postid")+1
    nTitle = recordObj["title"]
    nAuthor = getUserIdByEmail(recordObj["email"])
    nContent = recordObj["content"]
    nDate = recordObj["datePublished"]
    cursor.execute("INSERT INTO posts VALUES (%s,%s,%s,%s,%s)",(nId,nAuthor,nTitle,nContent,nDate))
    mysql.connection.commit()
    cursor.close()


def createNewUserInExistingOrg(userDict,orgId):
    userId = getMaxId("users","userid")+1
    fname = userDict["fname"]
    lname = userDict["lname"]
    email = userDict["email"]
    password = userDict["password"]
    role = userDict["role"]
    cursor = mysql.connection.cursor()
    #triple quote mark to make a multi line string, easier to read
    query = """
    INSERT INTO users (userid, email, password, firstname, lastname,role, orgid) 
    VALUES (%s, %s, %s, %s, %s,%s, %s) 
    """ 
    values = (userId, email, password, fname, lname,role,orgId)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()


def createNewOrg(userDict):
    orgId = getMaxId("organizations","orgid")+1
    orgName = userDict["orgName"]
    cursor = mysql.connection.cursor()
    query = "INSERT INTO organizations (orgid, name ) VALUES (%s, %s)"
    values = (orgId, orgName)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    

def createNewTask(taskObj):
    cursor = mysql.connection.cursor()
    nId = getMaxId("tasks","taskid")+1
    nTitle = taskObj["title"]
    nSender = getUserIdByEmail(taskObj["sender"])
    nReceiverId = getUserIdByName(taskObj["receiverFirstname"],taskObj["receiverLastname"])
    nContent = taskObj["content"]
    nDuedate = taskObj["duedate"]
    nSentdate = taskObj["sentdate"]
    nStatus = "F"
    cursor.execute("INSERT INTO tasks VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(nId,nTitle,nContent,nSentdate,nDuedate,nStatus,nSender,nReceiverId))
    mysql.connection.commit()
    cursor.close()


def addUserToGroup(userEmail,groupName,groupLeaderId):
    userId = getUserIdByEmail(userEmail)
    groupId = getGroupIdFromNameAndLeaderId(groupName,groupLeaderId)
    cursor = mysql.connection.cursor()
    query = "INSERT INTO groupmanager VALUES (%s,%s)"
    values = (userId,groupId)
    cursor.execute(query,values)
    mysql.connection.commit()
    cursor.close()


def createNewGroup(groupName,groupLeaderId):
    groupId = getMaxId("groups","groupid")+1
    cursor = mysql.connection.cursor()
    query = "INSERT INTO groups VALUES (%s,%s,%s)"
    values = (groupId, groupName, groupLeaderId)
    cursor.execute(query,values)
    mysql.connection.commit()
    cursor.close()


def createQuery(userEmail,field,operator,value):
    userId = getUserIdByEmail(userEmail)
    orgId = getOrgIdByUserId(userId)
    fieldInDBformat = (''.join(field.split(" "))).lower()
    sqlTemplate = "SELECT email,firstname,lastname,gender,age,role FROM users WHERE orgid = %s AND "
    if operator != "%":
        sqlWhereStatement = f"{fieldInDBformat} {operator} "
    else:
        sqlWhereStatement = f"{fieldInDBformat} LIKE "
        value = value+"%"
    sqlQuery = sqlTemplate + sqlWhereStatement + "%s"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    values = (orgId,value)
    cursor.execute(sqlQuery,values)
    dbdata = cursor.fetchall()
    cursor.close()
    return jsonify(dbdata)


#SETTERS
def setHeadAdmin(orgId,userId):
    cursor = mysql.connection.cursor()
    query1 = "UPDATE organizations SET headadmin = %s WHERE orgid = %s;"
    target1 = (userId,orgId)
    cursor.execute(query1,target1)

    query2 = "UPDATE users SET role = 'H' WHERE userid = %s;"
    target2 = (userId,)
    cursor.execute(query2,target2)
    mysql.connection.commit()
    cursor.close()


def toggleTaskStatus(taskId,nStatus):
    cursor = mysql.connection.cursor()
    query = "UPDATE tasks SET status = %s WHERE taskid = %s;"
    target = (nStatus,taskId)
    cursor.execute(query,target)
    mysql.connection.commit()
    cursor.close()


def setNewUserLoginData(oldEmail,newEmail,oldPassword,newPassword):
    userId = getUserIdByEmail(oldEmail)
    dbpassword = getPasswordByEmail(oldEmail)
    if oldPassword == dbpassword["password"]:
        cursor = mysql.connection.cursor()
        query = "UPDATE users SET email = %s, password = %s WHERE userid = %s;"
        values = (newEmail, newPassword,userId)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()


def setNewUserDetails(userEmail,newFirstname,newLastname):
    userId = getUserIdByEmail(userEmail)
    cursor = mysql.connection.cursor()
    query = "UPDATE users SET firstname = %s, lastname = %s WHERE userid = %s;"
    values = (newFirstname, newLastname,userId)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()


def addNewMessage(mSender,mContent,mGroup,mDate):
    mId = getMaxId("messages","messageid")+1
    cursor = mysql.connection.cursor()
    query = "INSERT INTO messages VALUES (%s,%s,%s,%s,%s)"
    values = (mId,mContent,mDate,mGroup,mSender)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()


def setUserNewRole(userEmail,newRole):
    userId = getUserIdByEmail(userEmail)
    cursor = mysql.connection.cursor()
    query = "UPDATE users SET role = %s WHERE userid = %s;"
    values = (newRole,userId)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()


#DELETERS
def deleteAllMessagesInGroup(groupId):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM messages WHERE groupid = %s"
    values = (groupId,)
    cursor.execute(query,values)
    mysql.connection.commit()
    cursor.close()


def deleteAllUsersInGroup(groupId):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM groupmanager WHERE groupid = %s"
    values = (groupId,)
    cursor.execute(query,values)
    mysql.connection.commit()
    cursor.close()


def deleteThisgroup(groupId):
    deleteAllMessagesInGroup(groupId)
    print("test 2")
    deleteAllUsersInGroup(groupId)
    print("test 4")
    cursor = mysql.connection.cursor()
    query = "DELETE FROM groups WHERE groupid = %s"
    values = (groupId,)
    cursor.execute(query,values)
    mysql.connection.commit()
    cursor.close()


#APP ROUTES
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "login":
            try:
                dbpwdDict = getPasswordByEmail(content[0])
                if dbpwdDict:
                    dbpassword = dbpwdDict["password"]
                    userPwd = content[1]
                    if dbpassword == userPwd:           
                        return "Succesfull login"
                    else:               
                        return "Incorrect password"
                else:
                    return "user doesnt exist"
            except Exception as e:
                return f"An error occurred in fetching db data: {e}"
        elif responseData["operation"] == "signin":
            if "orgId" in content:
                try:
                    createNewUserInExistingOrg(content,content["orgId"])
                    return "Created new user"
                except Exception as e:
                    return f"An error occurred in creating new user: {e}"
            else:
                try:
                    print(content)
                    createNewOrg(content)
                    createNewUserInExistingOrg(content,getOrgIdByOrgName(content["orgName"]))
                    setHeadAdmin(getOrgIdByOrgName(content["orgName"]),getUserIdByEmail(content["email"]))
                    return "Successfuly create organization and user"
                except Exception as e:
                    return f"An error occurred in creating new organization: {e}"
                



@app.route("/handleuser",methods=["POST","GET"])
def getuser():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "getuserdata":
            try:
                return getUserInfoByEmail(content)
            except Exception as e:
                return f"An error occured in fetching user data: {e}"
        elif responseData["operation"] == "updateuserpersonalinfo":
            try:
                setNewUserDetails(content["email"],content["newFirstname"],content["newLastname"])
                return f"Succesfully updated user personal details."
            except Exception as e:
                return f"An error occured in updating user personal data: {e}"
        elif responseData["operation"] == "getuserlogininfo":
            try:
                return getUserLoginInfoByEmail(content)
            except Exception as e:
                return f"An error occured in fetching user login data: {e}"
        elif responseData["operation"] == "updateuserlogininfo":
            try:
                setNewUserLoginData(content["currentEmail"],content["newEmail"],content["oldPassword"],content["newPassword"])
                return f"Succesfully updated user login details."
            except Exception as e:
                return f"An error occured in updating user login data: {e}"
        elif responseData["operation"] == "getuseremail":
            try:
                return jsonify(getUserEmailAndNameFromUserId(content))
            except Exception as e:
                return f"An error has occured fetching user email: {e}"
    else:
        return f"Error, only POST responses are taken."
            


@app.route("/posts",methods=["GET","POST"])
def posts():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "createnewpost":
            try:
                addNewPost(content)
                return "Successfuly created a new post."
            except Exception as e:
                return f"An error occured in database: {e}"
        elif responseData["operation"] == "getallposts":
            try:
                return getAllPosts(content)
            except Exception as e:
                return f"An error occured in fetching posts: {e}"


         
@app.route("/tasks",methods=["POST","GET"])
def tasks():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "getalltasks":
            try:
                return getAllTasks(content)
            except Exception as e:
                return f"An error occured in fetching task data: {e}"
        elif responseData["operation"] == "createnewtask":
            try:
                createNewTask(content)
                return "Created new task succesfully."
            except Exception as e:
                return f"An error occured in creating new task: {e}"
        elif responseData["operation"] == "getallusersinorg":
            try:
                return getAllUsersInOrg(content)
            except Exception as e:
                return f"An error occured in creating new task: {e}"
        elif responseData["operation"] == "updatetaskstatus":
            try:
                newStatus = content["newStatus"]
                taskTitle = content["title"]
                taskId = getTaskByTitleAndDate(taskTitle)
                toggleTaskStatus(taskId,newStatus)
                return "Updated task succesfully"
            except Exception as e:
                return f"An error occured in updating task status: {e}"
            
            #GIVE FRONTEND DIRECT ACCESS TO TASK ID SO THAT IT CAN GIVE IT TO BACK END INSTEAD OF TITLE + DATE


@app.route("/groups",methods=["POST","GET"])
def groups():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "getallgroups":
            try:
                allGroupsArray = getAllGroupsInOrg(content)
                for group in allGroupsArray:
                    group["noOfMembers"] = getNumberOfUsersInGroup(group["groupid"])
                    group["leader"] = getUserInfoById(group["leader"]).get_json()
                return jsonify(allGroupsArray)
            
            except Exception as e:
                return f"An error occured in fetching all groups: {e}"
        elif responseData["operation"] == "getusergroups":
            try:
                return getAllGroupsUserIsMemberOf(content)
            
            except Exception as e:
                return f"An error occured in fetching all groups: {e}"
        elif responseData["operation"] == "creategroup":
            try:
                createNewGroup(content["newGroupName"],getUserIdByEmail(content["newGroupLeader"]))
                addUserToGroup(content["newGroupLeader"],content["newGroupName"],getUserIdByEmail(content["newGroupLeader"]))
                return "Successfuly created group"
            
            except Exception as e:
                return f"An error occured in creating new group: {e}"    
        elif responseData["operation"] == "addusertogroup":
            try:
                userDictionary = content["userToAdd"]
                groupDictionary = content["groupToAdd"]
                groupLeaderDictionary = groupDictionary["leader"]
                addUserToGroup(userDictionary["email"],groupDictionary["name"],getUserIdByEmail(groupLeaderDictionary["email"]))
                return "Successfuly added user to group"
            except Exception as e:
                errorCode = str(e)
                errorCode = errorCode.split(",")[0]
                if errorCode[1:] == "1062":
                    return f"The user selected is already in that group."
                return f"An error occured in creating new group: {e}"       
        elif responseData["operation"] == "deletegroup":
            try:
                groupData = content["group"]
                leaderData = content["leader"]
                groupId = getGroupIdFromNameAndLeaderId(groupData["name"],getUserIdByEmail(leaderData["email"]))
                deleteThisgroup(groupId)
            except Exception as e:
                return f"An error occured in deleting groups: {e}"


@app.route('/messages',methods=["POST","GET"])
def messages():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "storenewmessage":
            try:
                messageSender=content["sender"]
                messageContent=content["content"]
                messageSentDate=content["sentdate"]
                messageGroup=content["group"]
                addNewMessage(messageSender,messageContent,messageGroup,messageSentDate)
                return "Sent message"
            except Exception as e:
                return f"An error occured in saving your message: {e}"
        elif responseData["operation"] == "getallmessages":
            try:
                return getAllMessages(content)
            except Exception as e:
                return f"An error occured in fetching all messages: {e}"


@app.route('/admin',methods=["POST","GET"])
def admin():
    if request.method=="POST":
        responseData = request.get_json()
        content = responseData["content"]
        if responseData["operation"] == "memberslist":
            try:
                return getDataOfAllUsersInOrg(content)
            except Exception as e:
                return f"An error occured in fetching the data for all your users: {e}"
        elif responseData["operation"] == "getalladmins":
            try:
                return getAllAdminsInOrg(content)
            
            except Exception as e:
                return f"An error occured in fetching the data for all the admins: {e}"
        elif responseData["operation"] == "setnewrole":
            try:
                setUserNewRole(content["userEmail"],content["newRole"])
                return "Succesfully updated user's role"
            
            except Exception as e:
                return f"An error occured in updating role of the user: {e}"
        elif responseData["operation"]=="executequery":
            try:
                #content will include field, operator and value. 
                operator = getOperator(content["operator"])
                return createQuery(content["currentUser"],content["field"],operator,content["value"])
            except Exception as e:
                return f"An error occured in executing SQL query: {e}"
        
            
            

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
