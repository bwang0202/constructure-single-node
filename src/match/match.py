import util
import config

from config import MatchWorkersConstants, MatchTeamWorkerConstants
from util import longest_common_prefix


def _match_age(age1, age2):
    return 100 - abs(age1 - age2)

def _match_work_age(work_age1, work_age2):
    return 100 - abs(work_age1 - work_age2)

def _match_specialites(specialities1, specialities2):
    """
    dictionary of {speciality_id: spciality_name}
    """
    value = 0
    for speciality_id1 in specialities1:
        if speciality_id1 in specialities2:
            value += 1
    return 100 * (2 * value) / (len(specialities1) + len(specialities2))

def _match_certificates(certificates1, certificates2):
    """
    {cert_id: name}
    """
    value = 0
    for cert_id1 in certificates1:
        if cert_id1 in certificates2:
            value += 1
        else if certificates1[cert_id1] in certificates2.values():
            value += 0.8
    return 100 * (2 * value)/(len(specialities1) + len(specialities2))

def _match_hometown(hometown1, hometown2):
    # FIXME:
    return 100 * (2 * longest_common_prefix(hometown1, hometown2)) / (len(hometown1) + len(hometown2))

def _match_education(education1, education2):
    # TODO:
    return 100

def match_workers(worker_id1, workder_id2):
    (name1, age1, work_age1, specialities1, certificates1, education1, hometown1) = util.get_worker_info(worker_id1)
    (name2, age2, work_age2, specialities2, certificates2, education2, hometown2) = util.get_worker_info(worker_id2)
    experiences = util.get_workers_experience(worker_id1, worker_id2)
    add some weights