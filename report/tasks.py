from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .headers import Header


class FirstOff:
    def __init__(self, buffer):
        self.doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=18,
            leftMargin=18,
            topMargin=18,
            bottomMargin=18,
        )
        self.elements = []
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4

    def save(self):
        self.doc.build(self.elements)

    def create_text(self, text, size=8, bold=False):
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

    def create_header(self):
        header = Header(width=(self.width - self.doc.rightMargin - self.doc.leftMargin))
        self.elements.append(header)
        self.elements.append(Spacer(1, 50))

    def create_job_info(self):
        pass

    def create(self):
        self.create_header()
        self.save()
