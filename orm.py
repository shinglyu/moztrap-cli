import re
import json
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
    def parseStep((index, step_txt)):
        step = {}
        step["instruction"] = step_txt[0].strip()
        step["expected"] = step_txt[1].strip()
        step["number"] = index
        return step

    p = re.compile(ur'TEST THAT(.*?)\n(.*?)(WHEN.*)', re.IGNORECASE | re.DOTALL)

    (title, desc, steps_txt) = re.findall(p, caseversion_txt)[0]

    sre = re.compile(ur'WHEN(.*?)THEN(.*?)\n', re.IGNORECASE | re.DOTALL)
    steps = re.findall(sre, steps_txt)
    caseversion = {}
    caseversion['name'] = title.strip()
    caseversion['description'] = desc.strip()
    caseversion['steps'] = map(parseStep, enumerate(steps, start=1))
    return json.loads(json.dumps(caseversion))
    #return json.dumps(caseversion)
    # TODO: compose it as a valid moztrap json
    raise NotImplementedError


def formatSuite(suite, sid):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['productversion'])
    txt = "{{ \"resource_uri\":\"/api/v1/suite/{sid}/\" }}\n".format(sid=sid)
    for caseversion in sortedCaseVersions:
        txt += formatCaseversion(caseversion)
        txt += "\n=====\n\n"
    return txt


def parseURL(url):
    import re
    p = re.compile(ur'\/api\/v1\/(.*)\/(.*)\/')
    return  re.findall(p, url)[0] # (resource_type, rid)
