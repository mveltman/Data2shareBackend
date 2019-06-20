from channels.generic.websocket import WebsocketConsumer
from project.models import Project, ProjectUser, Right
from project.models import File, Chat, Scheme, Dataset
from authentication.models import User
from django.db.models import Subquery
from .apps import ProjectConfig
from django.forms.models import model_to_dict
import json
import asyncio


class ProjectConsumer(WebsocketConsumer):

    def connect(self):
        print("connected to projectconsumer...")
        self.accept()
        self.manager = ProjectConfig.manager

    def disconnect(self, close_code):
        print("disconnected from projectconsumer...")

    def receive(self, text_data):
        print("a message was recieved")
        text_data_json = json.loads(text_data)
        print("command: " + text_data_json["command"])
        self.handle_message(
            text_data_json['command'],
            text_data_json['message'])

    def handle_message(self, command, message): #NOSONAR
        if command == "CTS-test":
            print('Succesfully recieved a testmessage from the client')
            message = {}
            message["command"] = "STC-test"
            message["message"] = "this is a server-to-client test command"
            self.send_message(json.dumps(message))
        if command == "CTS-getprojects":
            self.get_projects(message)
        if command == "CTS-getusersforproject":
            self.get_users_for_project(message)
        if command == "CTS-createproject":
            self.create_project(message)
        if command == "CTS-openproject":
            self.open_project(message)
        if command == "CTS-getusersandrights":
            self.get_users_and_rights_for_project(message)
        if command == "CTS-addusertoprojecttemp":
            self.add_user_to_project_temp(message)
        if command == "CTS-removeuserfromprojecttemp":
            self.remove_user_from_project(message)
        if command == "CTS-checksuperuser":
            self.checkSuperuser(message)
        if command == "CTS-savefile":
            self.savefile(message)
        if command == "CTS-getchat":
            self.getChat(message)
        if command == "CTS-getfiles":
            self.getFiles(message)
        if command == "CTS-savescheme":
            self.saveScheme(message)
        if command == "CTS-getschemes":
            self.getSchemes(message)
        if command == "CTS-savedataset":
            self.saveDataset(message)
        if command == "CTS-getdatasets":
            self.getDatasets(message)
        if command == "CTS-removeuser":
            self.removeUser(message)

    def send_message(self, messageJSON):
        print("sending")
        self.send(text_data=messageJSON)

    def get_projects(self, message):
        projectuser_ids = ProjectUser.objects.values('project_id').filter(user_id=message)
        x = Project.objects.all().filter(id__in=projectuser_ids)
        package = []
        for val in x:
            kval = {}
            kval["id"] = val.id
            kval["projectname"] = val.projectname
            package.append(kval)
        message = {}
        message["command"] = "STC-getprojects"
        message["message"] = package
        self.send_message(json.dumps(message))

    def add_user_to_project_temp(self, message):
        print(message)
        project = Project.objects.get(id=message["projectid"])
        user = User.objects.get(id=message["userid"])
        projectuser = ProjectUser(user=user, project=project)
        projectuser.save()

    def savefile(self, message):

        p = Project.objects.get(id=message["projectid"])
        u = User.objects.get(id=message["uploader"])
        f = File(uploader=u, table=message["file"], project=p)
        f.save()
        self.manager.update(int(message["projectid"]), 'fileupload')

    def open_project(self, message):
        p = Project.objects.values("projectname").get(id=message)
        self.manager.subscribe(message, self)
        message = {}
        message["command"] = "STC-openproject"
        message["message"] = p
        self.send_message(json.dumps(message))

    def removeUser(self, message):
        p = Project.objects.get(id=message["projectid"])
        u = User.objects.get(username=message["username"])
        projectuser = ProjectUser.objects.get(project=p, user=u)
        projectuser.delete()

    def create_project(self, message):
        print(message)
        u = User.objects.get(id=message["userid"])
        p = Project(projectname=message["projectname"], projectowner=u)
        p.save()
        pu = ProjectUser(project=p, user=u)
        pu.save()
        r = Right.objects.get(name="Admin")
        pu.rights.add(r)
        pu.save()

    def get_users_for_project(self, message):
        userids = ProjectUser.objects.values('user_id').filter(project_id=message)
        u = User.objects.filter(id__in=userids).only('id', 'username', 'email')
        package = []
        for val in u:
            kval = {}
            kval["username"] = val.username
            kval["email"] = val.email
            package.append(kval)
        message = {}
        message["command"] = "STC-getusersforproject"
        message["message"] = package
        self.send_message(json.dumps(message))

    def checkSuperuser(self, message):
        print(message)
        _user = User.objects.get(id=message[0].get("userid"))
        _project = Project.objects.get(id=message[0].get("projectid"))
        _projectuser = ProjectUser.objects.get(user_id=_user.id, project_id=_project.id)
        returnable = False
        for value in Right.objects.filter(projectuser=_projectuser):
            if(value.name == 'Admin'):
                returnable = True
        message = {}
        message["command"] = "STC-checksuperuser"
        message["message"] = returnable
        self.send_message(json.dumps(message))

    def getChat(self, message):
        p = Project.objects.get(id=message)
        chatqs = Chat.objects.filter(Project=p)
        package = []
        for t in chatqs:
            package.append(t)
        message = {}
        message["command"] = "STC-getchat"
        message["message"] = package
        self.send_message(json.dumps(message))

    def sendChatMessage(self, message):
        p = Project.objects.get(id=message)
        u = User.objects.get(id=message)
        chat = Chat(Project=p, sender=u, message=message)
        chat.save()
        self.manager.update(int(message["projectid"]), 'chat')

    def getFiles(self, message):
        project = Project.objects.get(id=message)
        f = File.objects.filter(project=project)
        package = []
        for target in f:
            package.append(target.table)
        message = {}
        message["command"] = "STC-getfiles"
        message["message"] = package
        self.send_message(json.dumps(message))

    def saveScheme(self, message):
        project = Project.objects.get(id=message["projectid"])
        user = User.objects.get(id=message["creatorid"])
        scheme = Scheme(Project=project,
                        Creator=user,
                        schemejson=message["scheme"])
        scheme.save()

        self.manager.update(int(message["projectid"]), 'scheme')

    def getSchemes(self, message):
        project = Project.objects.get(id=message)
        package = []
        schemes = Scheme.objects.filter(Project=project)
        for target in schemes:
            package.append(target.schemejson)
        message = {}
        message["command"] = "STC-getschemes"
        message["message"] = package
        self.send_message(json.dumps(message))

    def getDatasets(self, message):
        project = Project.objects.get(id=message)
        package = []
        datasets = Dataset.objects.filter(Project=project)
        for target in datasets:
            package.append(target.datasetjson)
        message = {}
        message["command"] = "STC-getdatasets"
        message["message"] = package
        self.send_message(json.dumps(message))

    def saveDataset(self, message):
        project = Project.objects.get(id=message["projectid"])
        user = User.objects.get(id=message["creatorid"])
        dataset = Dataset(Project=project,
                          Uploader=user,
                          datasetjson=message["dataset"])
        dataset.save()
        self.manager.update(int(message["projectid"]), 'newdataset')
