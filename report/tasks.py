import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Indenter,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from .headers import Header
from reportlab.lib import colors, utils
from assessment.models import Assessment, Lamination, Substrate, Viscosity
from job.models import Job, JobTest
from misc.models import Color
from machine.models import Machine


class BaseReport:
    def __init__(self, buffer, elements, id):
        self.doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=18,
            leftMargin=18,
            topMargin=18,
            bottomMargin=18,
        )
        self.elements = elements
        self.styles = getSampleStyleSheet()
        self.colors = colors
        self.width, self.height = A4
        self.job_test = JobTest.objects.get(id=id)

    def save(self):
        self.doc.build(self.elements)

    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height - y * unit
        return x, y

    def ptext(self, name, value, align="left"):

        fsize = 9
        return Paragraph(
            """<para align={align} size={fsize}>{name}:<font color=darkslategray> <b>  {value}  </b></font></para>""".format(
                fsize=fsize, name=name, value=value, align=align
            ),
            self.styles["Normal"],
        )

    def fotext(self, name, value, remark):
        fsize = 10
        value_color = "black"
        if remark == None:
            remark = "No Remark"
        if value:
            value_color = "green"
            value = "Passed"
        elif not value:
            value_color = "red"
            value = "Failed"
        else:
            value_color = "gray"
            value = "Not Tested"
        return Paragraph(
            f"""<font>{name}: ---------- <font color={value_color}>{value}</font><br/>
            Remark: ---------- {remark}
            </font>"""
        )

    def split_list_ranges(self, rows=0, list_count=0):

        if rows <= 0 or list_count <= 0:
            return []
        column_size = list_count // rows
        reminder = list_count % rows
        ranges = []
        start = 0

        for i in range(rows):
            end = start + column_size
            if i < reminder:
                end += 1
            ranges.append((start, end))
            start = end
        return ranges

    def split_list_numbers(self, rows=0, list_count=0):
        if rows <= 0 or list_count <= 0:
            return []

        column_size = list_count // rows
        reminder = list_count % rows
        result = []
        start = 0

        for i in range(rows):
            end = start + column_size
            if i < reminder:
                end += 1
            result.append(list(range(start, end)))
            start = end

        return result

    def create_text(self, text, size=8, underline=False, bold=False, header=True):
        if not header:
            return Paragraph(
                """
                             <font name=times size={size}>{text}</font>
                             """.format(
                    size=size, text=text
                ),
                self.styles["Normal"],
            )
        else:
            if bold:
                return Paragraph(
                    """
                                <font size={size}><b>{text}</b></font>
                                """.format(
                        size=size, text=text.upper()
                    ),
                    self.styles["Normal"],
                )
            if underline:
                return Paragraph(
                    """
                                <font  size={size}><u>{text}</u></font>
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


class FirstOff(BaseReport):
    def __init__(self, buffer, elements, assessment, id):
        BaseReport.__init__(self, buffer, elements, id)
        self.first_off = assessment
        if assessment.machine.type == "LAMINATION":
            self.lamination = assessment.lamination
        else:
            self.lamination = ""
        self.machine = assessment.machine

    def create_header(self):
        header = Header(
            width=(self.width - self.doc.rightMargin - self.doc.leftMargin),
            assessment_type="FIRST-OFF",
            machine=self.machine,
        )
        self.elements.append(header)
        self.elements.append(Spacer(1, 10))

    def create_job_info(self):

        job_text = self.ptext("Job", self.job_test, align="right")
        date_text = self.ptext("Date", self.first_off.date, align="right")
        self.elements.append(Indenter(left=410))
        self.elements.append(job_text)
        self.elements.append(Spacer(1, 5))
        self.elements.append(date_text)
        self.elements.append(Spacer(1, 10))
        self.elements.append(Indenter(left=-410))

        self.elements.append(
            self.create_text(
                "Job Detail",
                bold=True,
                size=10,
            )
        )
        self.elements.append(Spacer(1, 5))

        colWidths = [220, 220, 160]
        data = [
            [
                self.ptext("Customer", self.job_test.job.customer),
                self.ptext("Machine", self.first_off.machine.name),
                self.ptext("Shift", self.first_off.shift.name),
            ],
            [
                self.ptext(
                    "Product Name",
                    self.job_test.job.product.name,
                ),
                self.ptext(
                    "Raw Material",
                    self.job_test.raw_material.name,
                ),
                self.ptext("Date", self.first_off.date),
            ],
            [
                self.ptext("Product No.", self.job_test.job.product.no),
                self.ptext("Batch No.", self.job_test.batch_no),
                self.ptext("Time", self.first_off.time.strftime("%I:%M %p")),
            ],
        ]
        tbl1 = Table(data, colWidths=colWidths, hAlign="LEFT")
        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
        # tbl1.setStyle(tblStyle)
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl1)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def create_color_info(self):

        self.elements.append(
            self.create_text(
                "Color Detail",
                bold=True,
                size=10,
            )
        )
        self.elements.append(Spacer(1, 5))
        color_s_text = self.ptext("Color Standard", self.job_test.color_standard)
        self.elements.append(Indenter(left=20))
        self.elements.append(color_s_text)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 5))
        colWidths = [100, 100, 100]
        rows = 3
        color_list = self.job_test.color_standard.colors.all()
        # colors = Color.objects.all()
        color_ranges = self.split_list_ranges(rows=rows, list_count=len(color_list))
        data = []
        for [start, end] in color_ranges:
            data.append(
                [f"{c.name} | {c.viscosity}" for c in color_list[start:end]],
            )
        # data = [[f"{c.name} - ({c.viscosity})" for c in colors]]
        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, self.colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, self.colors.black),
            ]
        )
        tbl = Table(data, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def create_lamination_info(self):

        self.elements.append(
            self.create_text(
                "Lamination Detail",
                bold=True,
                size=10,
            )
        )
        self.elements.append(Spacer(1, 5))
        colWidths = [200, 200]
        data = [
            [
                self.ptext(
                    "Ply Structure",
                    self.lamination.ply_structure,
                ),
                self.ptext("Lamination Type", self.lamination.type),
            ],
            [
                self.ptext("Supplier", self.lamination.supplier),
                self.ptext(
                    "Mixing Ratio(Adhesive:Hardner)",
                    self.lamination.mixing_ratio,
                ),
            ],
            [
                self.ptext("Adhesive", self.lamination.adhesive),
                self.ptext("Hardner", self.lamination.hardner),
            ],
            [
                self.ptext("Adhesive Batch No.", self.lamination.adhesive_batch_no),
                self.ptext("Hardner Batch No.", self.lamination.hardner_batch_no),
            ],
        ]
        data.append(
            [
                [
                    self.ptext(f"Raw Material (S{s.no})", s.raw_material.name)
                    for s in self.lamination.substrates.all()
                ],
                [
                    self.ptext(f"Batch No. (S{s.no})", s.batch_no)
                    for s in self.lamination.substrates.all()
                ],
            ]
            # for s in Substrate.objects.all()
        )
        tbl = Table(data, hAlign="LEFT")
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def first_off_info(self):
        self.elements.append(
            self.create_text(
                "First Off Detail",
                bold=True,
                size=10,
            )
        )
        self.elements.append(Spacer(1, 5))
        colWidths = [150, 150, 150, 150]
        rows = 8
        test_list = self.first_off.first_offs.all()
        count = len(test_list)
        test_ranges = self.split_list_ranges(
            rows=(count // 2) + 1, list_count=len(test_list)
        )
        data = []
        for [start, end] in test_ranges:
            data.append(
                [
                    self.fotext(t.test.name, t.value, t.remark)
                    for t in test_list[start:end]
                ],
            )
        tbl = Table(data, hAlign="LEFT")
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def inspection_info(self):
        self.elements.append(
            self.create_text(
                "Inspection Detail",
                bold=True,
                size=10,
            )
        )
        self.elements.append(Spacer(1, 5))

        image_path = os.path.join(settings.STATIC_ROOT, "controlled_30.png")
        img = utils.ImageReader(image_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        controlled_image = Image(image_path, width=150, height=(150 * aspect))
        # self.elements.append(controlled_image)

        data = [
            [
                self.create_text("INSPECTION COMPLETED BY:", size=11, header=False),
                self.ptext("QA INSPECTOR", self.first_off.inspected_by.username),
                controlled_image,
            ],
            [
                "",
                self.ptext(
                    "SHIFT SUPERVISOR",
                    self.first_off.approvals.filter(approver="SUPERVISOR")
                    .first()
                    .by.username,
                ),
                "",
            ],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
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
        tbl = Table(data, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def create(self):
        self.create_header()
        self.create_job_info()
        self.create_color_info()
        if self.machine.type == "LAMINATION":
            self.create_lamination_info()
        self.first_off_info()
        self.inspection_info()
        self.elements.append(PageBreak())
        # self.save()


class OnProcess(BaseReport):
    def __init__(self, buffer, elements, assessment, id):
        BaseReport.__init__(self, buffer, elements, id)
        self.on_process = assessment
        self.viscosities = assessment.viscosities
        self.machine = assessment.machine

    def create_header(self):
        header = Header(
            width=(self.width - self.doc.rightMargin - self.doc.leftMargin),
            assessment_type="ON-PROCESS",
            machine=self.machine,
        )
        self.elements.append(header)
        self.elements.append(Spacer(1, 10))

    def create_job_info(self):
        colWidths = [200, 200, 120]

        data = [
            [
                self.ptext("Job", self.job_test.job.no),
                self.ptext("Date", self.on_process.date),
            ],
            [
                self.ptext("Product Name", self.job_test.job.product.name),
                self.ptext("Machine", self.on_process.machine.name),
            ],
            [
                self.ptext("Product No.", self.job_test.job.product.no),
                self.ptext("Raw Material", self.job_test.raw_material.name),
            ],
            [
                self.ptext("Customer", self.job_test.job.customer),
                self.ptext("Batch No.", self.job_test.batch_no),
            ],
        ]
        tbl = Table(data, colWidths=colWidths, hAlign="LEFT")
        self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def create_inspection_section(self):
        self.elements.append(self.create_text("Inspection Section", bold=True, size=10))
        self.elements.append(Spacer(1, 10))
        colWidths = [95, 65, 65, 65, 65, 190]

        def conf(c):
            if c.conformity is None:
                return "OK"
            else:
                return f"{c.conformity.name}"

        data = [
            ["NC", "Sample No.", "Shift", "Created at", "Created by", "Action Taken"],
            *(
                [
                    self.create_text(text=conf(c), size=9),
                    self.create_text(text=c.sample_no, size=9),
                    self.create_text(text=c.shift.name, size=9),
                    self.create_text(
                        text=c.created_at.strftime("%d-%m-%Y %I:%M %p"), size=9
                    ),
                    self.create_text(text=c.created_by.username, size=9),
                    self.create_text(text=c.action, size=9),
                ]
                for c in self.on_process.on_processes.all()
            ),
        ]
        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("VALIGN", (0, 1), (-1, -1), "TOP"),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )

        tbl = Table(data, colWidths=colWidths, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        # self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        # self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def create_viscosity_section(self):
        self.elements.append(self.create_text("Viscosity Section", bold=True, size=10))
        self.elements.append(Spacer(1, 5))

        data = [
            [
                self.create_text(text="Reel No.", size=8, bold=True),
                *(
                    self.create_text(
                        text=f"{c.name} ({c.viscosity})", size=8, bold=True
                    )
                    for c in self.job_test.color_standard.colors.all()
                ),
            ]
        ]
        reel_numbers = [value for value in self.viscosities.values_list("reel_no")[0]]
        for s in reel_numbers:
            data.append(
                [
                    s,
                    *(
                        [
                            f"{v.value} "
                            for v in Viscosity.objects.filter(
                                reel_no=s, assessment=self.on_process
                            )
                        ]
                    ),
                ]
            )

        tblStyle = TableStyle(
            [
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
            ]
        )
        tbl = Table(data, hAlign="LEFT")
        tbl.setStyle(tblStyle)
        # self.elements.append(Indenter(left=20))
        self.elements.append(tbl)
        # self.elements.append(Indenter(left=-20))
        self.elements.append(Spacer(1, 10))

    def inspection_info(self):
        image_path = os.path.join(settings.STATIC_ROOT, "controlled_30.png")
        img = utils.ImageReader(image_path)
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width)
        controlled_image = Image(image_path, width=150, height=(150 * aspect))
        self.elements.append(controlled_image)

    def create(self):
        self.create_header()
        self.create_job_info()
        self.create_inspection_section()
        if self.machine.viscosity_test:
            self.create_viscosity_section()
        self.inspection_info()
        self.elements.append(PageBreak())
