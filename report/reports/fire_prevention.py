import os
from django.conf import settings
from reportlab.platypus import Spacer, Indenter, Table, TableStyle, Image, Paragraph
from .headers import Header
from reportlab.lib import colors, utils
from she.models import Checkpoint, FirePrevention, FPChecklist
from report.reports import BaseReport


class BaseFPReport(BaseReport):

    def __init__(self, buffer, elements, id):
        BaseReport.__init__(self, buffer, elements)
        self.fire_prevention = FirePrevention.objects.get(id=id)


class FirePreventionReport(BaseFPReport):
    def __init__(self, buffer, elements, report_header, id):
        BaseFPReport.__init__(self, buffer, elements, id)
        self.checklists = FPChecklist.objects.filter(
            fire_prevention=self.fire_prevention
        )
        self.report_header = report_header.first()

    def header(self):
        header = Header(
            width=(self.width - self.doc.rightMargin - self.doc.leftMargin),
            report_header=self.report_header,
        )
        self.elements.append(header)
        self.elements.append(Spacer(1, 20))

    def prevention_info(self):
        colWidths = [200, 200]
        data = [
            [
                self.ptext(
                    "Created at",
                    self.fire_prevention.created_at.strftime("%d-%m-%Y %I:%M %p"),
                ),
                self.create_text("APPROVED BY", bold=True, header=False, size=9),
            ],
            [
                self.ptext("Completed by", self.fire_prevention.inspected_by.username),
                self.create_text(
                    f"<font> > {self.fire_prevention.approvals.all()[0].by.username  or None} <b> ({self.fire_prevention.approvals.all()[0].approver.lower() or None}) </b> </font>",
                    size=9,
                ),
            ],
            [
                self.ptext("Shift", self.fire_prevention.shift.name),
                self.create_text(
                    f"<font> > {self.fire_prevention.approvals.all()[1].by.username or None} <b> ({self.fire_prevention.approvals.all()[1].approver.lower() or None}) </b> </font>",
                    size=9,
                ),
            ],
        ]
        tblStyle = TableStyle(
            [
                (
                    "SPAN",
                    (-1, 0),
                    (-1, -1),
                )
            ]
        )
        tbl = Table(data, colWidths=colWidths, hAlign="LEFT")
        # tbl.setStyle(tblStyle)
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def checklist(self):
        colWidths = [25, 225, 50, 220]
        data = [
            ["NO.", "CHECKPOINT", "CHECKED", "REMARK"],
            *(
                [
                    self.create_text(text=i + 1, size=9),
                    self.create_text(text=c.checkpoint.name, size=9),
                    self.create_text(text=c.get_value_display(), size=9),
                    self.create_text(text=c.remark, size=9),
                ]
                for i, c in enumerate(self.checklists)
            ),
        ]
        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
            ]
        )
        tbl = Table(data, colWidths=colWidths, style=tblStyle, hAlign="CENTER")
        tbl.setStyle(tblStyle)
        self.elements.append(tbl)
        self.elements.append(Spacer(1, 10))

    def comment(self):
        self.elements.append(
            self.create_text("Comment for Next Shift:", header=False, bold=True, size=9)
        )
        if self.fire_prevention.comment:
            self.elements.append(Spacer(1, 5))
            self.elements.append(Indenter(left=20))
            self.elements.append(
                self.create_text(f"- {self.fire_prevention.comment}", size=9)
            )
            self.elements.append(Indenter(left=-20))
            self.elements.append(Spacer(1, 20))

    def controlled_detail(self):
        image_path = os.path.join(settings.STATIC_ROOT, "controlled_30.png")
        img = utils.ImageReader(image_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        controlled_image = Image(image_path, width=150, height=(150 * aspect))
        self.elements.append(controlled_image)

    def create(self):
        self.header()
        self.prevention_info()
        self.checklist()
        self.comment()
        self.controlled_detail()
