from questionnaires.mhc_sf import questionnaire as mhc_sf
from questionnaires.shs import questionnaire as shs
from questionnaires.ces_d import questionnaire as ces_d
from questionnaires.dass21 import questionnaire as dass21
from questionnaires.phq9 import questionnaire as phq9
from questionnaires.cssrs import questionnaire as cssrs
from questionnaires.ttbq2_cg31 import questionnaire as ttbq2_cg31
from questionnaires.gad7 import questionnaire as gad7
from questionnaires.adnm4 import questionnaire as adnm4
from questionnaires.lec5 import questionnaire as lec5
from questionnaires.pcl5 import questionnaire as pcl5
from questionnaires.ptgi import questionnaire as ptgi
from questionnaires.sto import questionnaire as sto
from questionnaires.itq import questionnaire as itq
from questionnaires.oci_r import questionnaire as oci_r
from questionnaires.des import questionnaire as des
from questionnaires.tas20 import questionnaire as tas20
from questionnaires.pq_b import questionnaire as pq_b
from questionnaires.eat26 import questionnaire as eat26
from questionnaires.aq import questionnaire as aq
from questionnaires.iri import questionnaire as iri
from questionnaires.ders import questionnaire as ders

ALL_QUESTIONNAIRES = {
    "MHC-SF": mhc_sf,
    "SHS": shs,
    "CES-D": ces_d,
    "DASS-21": dass21,
    "PHQ-9": phq9,
    "C-SSRS": cssrs,
    "TTBQ2-CG31": ttbq2_cg31,
    "GAD-7": gad7,
    "ADNM-4": adnm4,
    "LEC-5": lec5,
    "PCL-5": pcl5,
    "PTGI": ptgi,
    "STO": sto,
    "ITQ": itq,
    "OCI-R": oci_r,
    "DES": des,
    "TAS-20": tas20,
    "PQ-B": pq_b,
    "EAT-26": eat26,
    "AQ": aq,
    "IRI": iri,
    "DERS": ders,
}
