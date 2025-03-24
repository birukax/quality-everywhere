import os
from django.conf import settings
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Flowable, Paragraph, TableStyle, Table, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors, utils


class Header(Flowable):
    def __init__(self, report_header, width=550, height=70):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.report_header = report_header
        self.assessment_type = self.report_header.report
        self.machine = self.report_header.machine

        self.styles = getSampleStyleSheet()

    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height - y * unit
        return x, y

    def create_text(self, text, size=10, bold=False):
        if bold:
            return Paragraph(
                """
                             <font size={size}><b>{text}</b></font>
                             """.format(
                    size=size, text=text
                ),
                self.styles["Normal"],
            )
        return Paragraph(
            """
                         <font size={size}>{text}</font>
                         """.format(
                size=size, text=text
            ),
            self.styles["Normal"],
        )

    def draw(self):
        doc_no = self.report_header.no
        # machine = "BOBST"
        h_text = f"{self.assessment_type} INSPECTION FOR {self.machine.name.upper()}"
        page_no = 1
        logo_path = os.path.join(settings.STATIC_ROOT, "logo_sm.png")
        img = utils.ImageReader(logo_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        logo_image = Image(logo_path, width=50, height=(50 * aspect))
        logo_image.hAlign = "CENTER"
        logo_image.vAlign = "CENTER"
        colWidths = [90, 275, 90, 90]
        data = [
            [
                logo_image,
                self.create_text("Company Name:", bold=True),
                self.create_text("Document No.", bold=True),
            ],
            [
                "",
                self.create_text("QUALABELS MANUFACTURERS PLC", bold=False),
                self.create_text("{doc_no}".format(doc_no=doc_no.upper()), bold=False),
            ],
            [
                "",
                self.create_text("Title:", bold=True),
                self.create_text("Issue No.", bold=True),
                self.create_text("Page No.:", bold=True),
            ],
            [
                "",
                self.create_text(
                    h_text,
                    bold=False,
                ),
                self.create_text("01", bold=False),
                self.create_text("Page {p}".format(p=page_no), bold=False),
            ],
        ]
        hTblStyle = TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.50, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("SPAN", (0, 0), (0, -1)),
                ("SPAN", (-2, 0), (-1, 0)),
                ("SPAN", (-2, 1), (-1, 1)),
            ]
        )
        tbl = Table(data, colWidths=colWidths, hAlign="CENTER")
        tbl.setStyle(hTblStyle)
        tbl.wrapOn(self.canv, self.width, self.height)
        t_width, t_height = tbl.wrapOn(self.canv, self.width, self.height)
        x = (self.width - t_width) / 2
        y = self.height - t_height
        tbl.drawOn(self.canv, x, y)
