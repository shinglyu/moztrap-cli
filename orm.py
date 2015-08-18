import re
import json
import logging

def formatCaseversion(caseversion):
    # Downloaded json obj => plaintext
    # FIXME: remove this try catch when resource uri is parsed
    #print(caseversion)
    txt = ""

    txt += ("## {name}\n"
            "`{status}`\n"
           ).format(name=caseversion['name'],
                    status=caseversion['status'])
    for step in caseversion['steps']:
        txt += ("WHEN {instr}\n"
                "THEN {expected}\n"
                "\n"
               ).format(instr=step['instruction'].replace('\015',''),
                        expected=step['expected'].replace('\015',''))
    return txt


def parseCaseversion(caseversion_txt):
    # plaintext => json obj
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
    #caseversion['resource_uri'] = uri.strip()
    caseversion['name'] = title.strip()
    caseversion['description'] = desc.strip()
    caseversion['steps'] = map(parseStep, enumerate(steps, start=1))
    #logging.info("hi")
    #return json.dumps(caseversion)
    # TODO: compose it as a valid moztrap json
    return caseversion


def formatSuite(suite, sname):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['id'])
    txt = "# {sname}\n".format(sname=sname)
    for caseversion in sortedCaseVersions:
        txt += formatCaseversion(caseversion)
    return txt


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
        step["instruction"] = step_txt[0].strip()
        step["expected"] = step_txt[1].strip()
        step["number"] = index
        return step

    regex = re.compile(ur'WHEN(.*?)\nTHEN([^\n]*)', re.IGNORECASE | re.DOTALL)
    steps = re.findall(regex, case_step_txt)

    case_step = []

    for index, step in enumerate(steps):
        case_step.append(parseStep(index + 1, step))

    return case_step
