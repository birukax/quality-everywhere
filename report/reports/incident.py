import os
from django.conf import settings
from reportlab.platypus import (
    Spacer,
    Indenter,
    Table,
    TableStyle,
    Image,
)
from .headers import Header
from reportlab.lib import colors, utils
from she.models import Incident, IncidentType
from report.reports import BaseReport


class BaseIncidentReport(BaseReport):
    def __init__(self, buffer, elements, id):
        BaseReport.__init__(self, buffer, elements)
        self.incident = Incident.objects.get(id=id)

    def question_text(self, text, value):
        self.elements.append(self.create_text(text, header=False, bold=True, size=11))
        self.elements.append(Spacer(1, 5))
        self.elements.append(Indenter(left=20))
        self.elements.append(self.create_text(f"- {value}", size=10))
        self.elements.append(Indenter(left=-20))


class IncidentReport(BaseIncidentReport):
    def __init__(self, buffer, elements, report_header, id):
        BaseIncidentReport.__init__(self, buffer, elements, id)
        self.report_header = report_header
        self.witness_list = self.incident.witness_list.all()
        self.report_header = report_header.first()

    def header(self):
        header = Header(
            width=(self.width - self.doc.rightMargin - self.doc.leftMargin),
            report_header=self.report_header,
        )
        self.elements.append(header)
        self.elements.append(Spacer(1, 20))

    def employee_detail(self):

        image_path = os.path.join(settings.STATIC_ROOT, "controlled_30.png")
        img = utils.ImageReader(image_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        controlled_image = Image(image_path, width=150, height=(150 * aspect))
        colWidths = [350, 170]
        data = [
            [
                self.ptext("EMPLOYEE NAME", self.incident.employee.name, fsize=10),
                controlled_image,
            ],
            [
                self.ptext(
                    "DEPARTMENT", self.incident.employee.department.name, fsize=10
                ),
            ],
            [
                self.ptext("INCIDENT TYPE", self.incident.type.name, fsize=10),
            ],
            [
                self.ptext("REPORTED BY", self.incident.created_by.username, fsize=10),
            ],
            [
                self.create_text("WITNESS LIST:", bold=False, header=False, size=10),
            ],
            [
                [
                    self.create_text(f"- {w.name}", bold=False, header=False, size=10)
                    for w in self.witness_list
                ]
            ],
        ]
        # count = len(self.witness_list)
        # witness_ranges = self.split_list_ranges(rows=(count // 2) + 1, list_count=count)
        # for [start, end] in witness_ranges:
        #     data.append(
        #         [
        #             self.create_text(f"- {w.name}", bold=False, header=False, size=10)
        #             for w in self.witness_list[start:end]
        #         ]
        #     )
        tblStyle = TableStyle(
            [
                ("SPAN", (-1, 0), (-1, -1)),
            ]
        )
        tbl = Table(data, colWidths=colWidths, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 15))

    def other_details(self):
        colWidths = [125, 125, 125, 125]
        if self.incident.referred_to_hospital:
            referred = "Yes"
        else:
            referred = "No"
        data = [
            [
                self.create_text("Location", bold=True, header=False, size=10),
                self.create_text("Date", bold=True, header=False, size=10),
                self.create_text("Time", bold=True, header=False, size=10),
                self.create_text(
                    "Referred to Hospital?", bold=True, header=False, size=10
                ),
            ],
            [
                self.create_text(
                    self.incident.location.name, bold=False, header=False, size=9
                ),
                self.create_text(self.incident.date, bold=False, header=False, size=9),
                self.create_text(self.incident.time, bold=False, header=False, size=9),
                self.create_text(
                    referred,
                    bold=False,
                    header=False,
                    size=9,
                ),
            ],
        ]
        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
            ]
        )
        tbl = Table(data, colWidths=colWidths, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        self.elements.append(tbl)
        self.elements.append(Spacer(1, 15))

    def incident_detail(self):
        self.question_text("What caused the event?", self.incident.cause)
        self.elements.append(Spacer(1, 10))
        self.question_text(
            "What part of the body was injured?", self.incident.body_part_injured
        )
        self.elements.append(Spacer(1, 10))
        self.question_text(
            "What was the nature of the injury?", self.incident.nature_of_injury
        )
        self.elements.append(Spacer(1, 10))
        self.question_text(
            "What was the employee doing prior to the event?",
            self.incident.pre_incident_activity,
        )
        self.elements.append(Spacer(1, 10))
        self.question_text(
            "What equipment, tools were being used?",
            self.incident.tools_used_before_incident,
        )
        self.elements.append(Spacer(1, 10))
        self.question_text(
            "Recommendations regarding the incident?", self.incident.recommendation
        )
        self.elements.append(Spacer(1, 10))
        self.question_text("What action was taken?", self.incident.action_taken)
        self.elements.append(Spacer(1, 15))

    def create(self):
        self.header()
        self.employee_detail()
        self.other_details()
        self.incident_detail()
