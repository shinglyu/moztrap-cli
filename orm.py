# -*- coding: utf-8 -*-
import re
import json
import logging

def formatCaseversion(caseversion):
    # Downloaded json obj => plaintext
    # FIXME: remove this try catch when resource uri is parsed
    # print(json.dumps(caseversion, indent=2))

    steps = ""
    for num, step in enumerate(caseversion['steps']):
        steps += "{num}. {instr}\n  >>> {expected}\n\n".format(
        #steps += "{num}. {instr}$  >>> {expected}$$".format(
            num=(num + 1),
            instr=step['instruction'].replace('\015','').encode('utf8'),
            expected=step['expected'].replace('\015','').encode('utf8')
        )

    # print(steps)
    #txt = "{purpose},{plan},{tid},{test_case_name},{description},{steps},{tags},{note},{ux_spec}"
    #return txt
    #print caseversion['tags']
    return ["",#plan
            caseversion['id'], #tid
            caseversion['name'],
            caseversion['description'],
            steps,
            ",".join([t['name'] for t in caseversion['tags']]),
            "", #note
            "" #uxspec
           ]


def parseCaseversion(caseversion_txt):

    caseversion = {}
    #TODO: handle id, tags
    caseversion['name'] = caseversion_txt[2]
    caseversion['description'] = caseversion_txt[3]

    caseversion['steps'] = parseCaseStep(caseversion_txt[4])
    return caseversion


def formatSuite(suite, sname):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['id'])
    #txt = "# {sname}\n".format(sname=sname)
    cases = []
    for caseversion in sortedCaseVersions:
        cases.append([sname] + formatCaseversion(caseversion))
    return cases


def parseSuite(suite_txt):
    # plaintext => json obj
    # Get the first line, the suite uri
    # suite_uri, caseversions_txt = suite_txt.strip().split('\n', 1)

    caseversions = map(lambda x: parseCaseversion(x),
                       suite_txt.strip().rstrip('=====').split('====='))

    suite = {}
    suite['objects'] = caseversions
    return json.loads(json.dumps(suite))
    #return json.dumps(caseversion)
    # TODO: compose it as a valid moztrap json


def parseURL(url):
    import re
    p = re.compile(ur'\/api\/v1\/(.*)\/(.*)\/')
    return  re.findall(p, url)[0] # (resource_type, rid)


def parseCaseStep(case_step_txt):
    def parseStep(index, step_txt):
        step = {}
        # TODO: step_txt[0] is the number, should we use it?
        step_components = step_txt[1].split('>>>')
        step["instruction"] = step_components[0].strip()
        if len(step_components) == 2:
            step["expected"] = step_components[1].strip()
        else:
            step["expected"] = ""
        step["number"] = index
        return step

    sre = re.compile(ur'([\d]+\.)(.*?)(?=[\d]+\.|$)', re.DOTALL)
    steps = re.findall(sre, case_step_txt)

    case_step = []

    if len(steps) == 0:
        return [parseStep(0, [case_step_txt, ''])]

    for index, step in enumerate(steps):
        case_step.append(parseStep(index + 1, step))

    return case_step
