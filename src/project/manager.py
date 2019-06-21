import asyncio
import json
from .models import File, Project

# The goal of this class is to notify any consumers that have subscribed to updates for a certain project
# this is used to keep users updated on what other users of the same project are doing.
class ProjectManager():

    def __init__(self):
        if(hasattr(self, 'projectSessions')):
            pass
        else:
            self.projectSessions = {}

    def subscribe(self, projectid, consumer):
        print(projectid not in self.projectSessions)
        if(projectid not in self.projectSessions):
            self.projectSessions[projectid] = []
        self.projectSessions[projectid].append(consumer)
        self.update(projectid, "test")

    def unsubscribe(self, projectid, consumer):
        pass

    def update(self, projectid, contentid): #NOSONAR
        if (projectid in self.projectSessions):
            if (contentid == 'fileupload'):
                project = Project.objects.get(id=projectid)
                for consumer in self.projectSessions[projectid]:
                    f = File.objects.filter(project=project)
                    package = []
                    for target in f:
                        package.append(target.table)
                    message = {}
                    message["command"] = "STC-fileuploaded"
                    message["message"] = package
                    x = json.dumps(message)
                    consumer.send_message(x)
                    break
            if(contentid == 'chat'):
                pass
            print("projectid found")
            if (contentid == "test"):
                print(self.projectSessions[projectid])
                for consumer in self.projectSessions[projectid]:
                    message = {}
                    message["command"] = "STC-userjoinedtest"
                    message["message"] = ""
                    consumer.send_message(json.dumps(message))
                    break
