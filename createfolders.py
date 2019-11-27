from git import Repo
import hackbi_eventbrite as he
import json
import os
import stat
import shutil
import time


def clone_and_copy(clone_from:str, dest:str, folder_names:list):
    def on_rm_error(func, path, exc_info):
        #from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
    Repo.clone_from(clone_from, "cloned")
    for folder in folder_names:
        shutil.copytree("cloned", f"{dest}/{folder}")
    shutil.rmtree("cloned", onerror=on_rm_error)

def main():
    with open("info.json", "r") as file:
        settings = json.load(file)
    attendees = he.get_attendee_list(settings["event_id"], settings["token"])
    eighth = he.get_people_answered(attendees, "8th grade", "26350001")
    seventh = he.get_people_answered(attendees, "7th grade", "26350003")
    seventh.extend(he.get_people_answered(attendees, "7th", "26350003"))
    seventh.extend(he.get_people_answered(attendees, "7", "26350003"))
    sixth = he.get_people_answered(attendees, "6", "26350003")
    ms = []
    ms.extend(eighth)
    ms.extend(seventh)
    ms.extend(sixth)
    names = []
    for person in ms:
        name = (person["profile"]["first_name"] + "_" + person["profile"]["last_name"]).lower()
        if name not in names:
            names.append(name)
    clone_and_copy(settings["repo_url"], "dest", names)

if __name__ == "__main__":
    main()
