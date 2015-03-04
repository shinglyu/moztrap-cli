import logging

def formatCaseversion(caseversion):
    txt = "{{ \"resource_uri\":\"{uri}\" }}\n".format(uri=caseversion[u'resource_uri'])
    txt += ("TEST THAT {name}\n"
           "{desc}\n"
           "\n"
          ).format(name=caseversion['name'],
                   desc=caseversion['description'])
    for step in caseversion['steps']:
        txt += ("WHEN {instr}\n"
                "THEN {expected}\n"
                "\n"
               ).format(instr=step['instruction'],
                        expected=step['expected'])
    return txt

def parseCaseversion(caseversion_txt):
    raise NotImplementedError


def formatSuite(suite, sid):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['productversion'])
    txt = "{{ \"resource_uri\":\"/api/v1/suite/{sid}/\" }}\n".format(sid=sid)
    for caseversion in sortedCaseVersions:
        txt += formatCaseversion(caseversion)
        txt += "\n=====\n\n"
    return txt

