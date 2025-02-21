import os
import reportlab
import time
from django.conf import settings
from io import BytesIO
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import mm, inch
from assessment.models import Test
from reportlab.lib import colors, pdfencrypt
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Frame,
    PageTemplate,
    NextPageTemplate,
    PageBreak,
    Table,
    TableStyle,
    Preformatted,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.sequencer import getSequencer


def test(request):

    response = FileResponse(
        generate_pdf(),
        as_attachment=True,
        filename="test.pdf",
    )

    return response


def generate_pdf():
    buffer = BytesIO()

    def string_alignment(c):
        width, height = A4

        c.drawString(80, 700, "Standard String")
        c.drawRightString(80, 680, "Right String")

        numbers = [987.15, 44, -1, 234.56, (456.78)]
        y = 650
        for number in numbers:
            c.drawAlignedString(80, y, str(number))
            y -= 20

        c.drawCentredString(width / 2, 550, "Centered String")

    def rotate_demo(c):
        c.translate(inch, inch)
        c.setFont("Helvetica", 14)
        c.drawString(inch, inch, "Normal")
        c.line(inch, inch, inch + 100, inch)

        c.rotate(45)
        c.drawString(inch, -inch, "45 Degrees")
        c.line(inch, inch, inch + 100, inch)

        c.rotate(45)
        c.drawString(inch, -inch, "90 Degrees")
        c.line(inch, inch, inch + 100, inch)

    def font_demo(c, fonts):
        pos_y = 350
        for font in fonts:
            c.setFont(font, 12)
            c.drawString(100, pos_y, font)
            pos_y -= 10

    def coord(x, y, height, unit=1):
        x, y = x * unit, y * unit
        return x, y

    def unit_converter(c):
        c.drawString(
            *coord(width / 2, height / 2, inch),
            text=f"welcome to reportlab!{[*coord(width, height, inch)]}",
        )

    def draw_lines(c):
        c.setLineWidth(2)
        start_y = 710
        c.line(0 + 2, start_y, A4[0] - 2, start_y)
        for x in range(10):
            start_y -= 10
            c.line(30, start_y, 580, start_y)

    def draw_shapes(c):
        c.setStrokeColorRGB(0.2, 0.5, 0.3)
        c.rect(10, 740, 100, 80, stroke=1, fill=0)
        c.ellipse(10, 680, 100, 630, stroke=1, fill=1)
        c.wedge(10, 600, 100, 550, 45, 90, stroke=1, fill=0)
        c.circle(300, 600, 50)

    def gray_color_demo(c):
        c.setFont("Helvetica", 10)
        x = 30

        grays = [0.0, 0.25, 0.50, 0.75, 1.0]

        for g in grays:
            c.setFillGray(g)
            c.circle(x, 730, 20, fill=1)
            gray_str = "Gray={gray}".format(gray=g)
            c.setFillGray(0.5)
            c.drawString(x - 10, 700, gray_str)
            x += 75

    def color_demo(c):
        c.setFont("Helvetica", 10)
        x = 30

        sample_colors = [
            colors.aliceblue,
            colors.aquamarine,
            colors.lavender,
            colors.beige,
            colors.chocolate,
        ]

        for color in sample_colors:
            c.setFillColor(color)
            c.circle(x, 730, 20, fill=1)
            color_str = "{color}".format(color=color._lookupName())
            c.setFillColor(colors.black)
            c.drawString(x - 10, 700, color_str)
            x += 75

    def textobject_demo(c):
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)

        textobject.setFont("Times-Roman", 12)
        textobject.textLine(text="This line is for Rock and Python.")
        textobject.setFillColor(colors.red)
        textobject.textLine(text="And this line is for Python, Red and Rock!")
        c.drawText(textobject)

    def textobject_cursor(c):
        to = c.beginText(10, 730)
        for indent in range(4):
            to.textLine("ReportLab cursor demo")
            to.moveCursor(15, 15)
        c.drawText(to)

    def textobject_char_spacing(c):
        to = c.beginText()
        to.setTextOrigin(10, 730)
        spacing = 0
        for indent in range(8):
            to.setCharSpace(spacing)
            line = "{} - ReportLab spacing demo".format(spacing)
            to.textLine(line)
            spacing += 0.7
        c.drawText(to)

    def wordspacer(c):
        to = c.beginText()
        to.setTextOrigin(10, 730)

        word_spacing = 0

        for indent in range(8):
            to.setWordSpace(word_spacing)
            line = " {} - ReportLab spacing demo".format(word_spacing)
            to.textLine(line)
            word_spacing += 1.5
        c.drawText(to)

    def create_form(date, amount, receiver, c):
        cvs = c
        cvs.setLineWidth(0.3)
        cvs.setFont("Helvetica", 24)
        cvs.drawString(30, 750, "OFFICIAL COMMUNIQUE")
        cvs.drawString(30, 735, "OF ACME INDUSTRIES")
        cvs.drawString(500, 750, date)
        cvs.line(480, 747, 580, 747)
        cvs.drawString(275, 725, "AMOUNT OWED:")
        cvs.drawString(500, 725, amount)
        cvs.line(378, 723, 580, 723)
        cvs.drawString(30, 703, "RECEIVED BY:")
        cvs.line(120, 700, 580, 700)
        cvs.drawString(120, 703, receiver)

    def embedded_font_demo(c):
        reportlab_folder = os.path.dirname(reportlab.__file__)
        fonts_folder = os.path.join(reportlab_folder, "fonts")
        print("ReportLab font folder is located at {ff}".format(ff=fonts_folder))
        afm = os.path.join(fonts_folder, "DarkGardenMK.afm")
        pfb = os.path.join(fonts_folder, "DarkGardenMK.pfb")

        font_face = pdfmetrics.EmbeddedType1Face(afm, pfb)
        pdfmetrics.registerTypeFace(font_face)

        face_name = "DarkGardenMK"
        font = pdfmetrics.Font("DarkGardenMK", face_name, "WinAnsiEncoding")
        pdfmetrics.registerFont(font)

        c.setFont("DarkGardenMK", 40)
        c.drawString(10, 730, "The DarkGardenMK font")

    def hello():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        styles = getSampleStyleSheet()

        flowables = []
        text = "Hello, I'm a Paragraph Hello, I'm a Paragraph Hello, I'm a Paragraph."
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)
        for i in range(100):
            flowables.append(para)
        doc.build(flowables)

    def form_letter():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        flowables = []
        logo = os.path.join(settings.STATICFILES_DIRS[0], "python_logo.png")
        magName = "Pythonista"
        issueNum = 12
        subPrice = "99.00"
        limitedDate = "03/05/2025"
        freeGift = "tin foil hat"

        formatted_time = time.ctime()
        full_name = "Mike Driscoll"
        address_parts = ["411 State St.", "Waterloo, IA 50158"]

        im = Image(logo, 2 * inch, 2 * inch)
        flowables.append(im)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
        ptext = "<font size=12>%s</font>" % formatted_time

        flowables.append(Paragraph(ptext, styles["Normal"]))

        flowables.append(Spacer(1, 12))

        ptext = "<font size=12>%s</font>" % full_name
        flowables.append(Paragraph(ptext, styles["Normal"]))
        for part in address_parts:
            ptext = "<font size=12>%s</font>" % part.strip()
            flowables.append(Paragraph(ptext, styles["Normal"]))

        flowables.append(Spacer(1, 12))
        ptext = "<font size=12>Dar %s:</font>" % full_name.split()[0].strip()
        flowables.append(Paragraph(ptext, styles["Normal"]))
        flowables.append(Spacer(1, 12))

        ptext = """<font size=12> We would like to welcome you tu our subscriber
        base for {magName} Magazine! you will receive {issueNum} issues at <br/>
        the excellent introductory price of ${subPrice}. Please respond by
        {limitedDate} to start receiving your subscription and get the
        following free gift: {freeGift}.</font>
        """.format(
            magName=magName,
            issueNum=issueNum,
            subPrice=subPrice,
            limitedDate=limitedDate,
            freeGift=freeGift,
        )
        flowables.append(Paragraph(ptext, styles["Justify"]))
        flowables.append(Spacer(1, 12))

        ptext = """<font size=12> Thank you very much and we look 
        forward to serving you.Thank you very much and we look 
        forward to serving you.Thank you very much and we look 
        forward to serving you.</font>
        """

        flowables.append(Paragraph(ptext, styles["Justify"]))
        flowables.append(Spacer(1, 12))
        ptext = "<font size=12>Sincerly,</font>"
        flowables.append(Paragraph(ptext, styles["Normal"]))
        flowables.append(Spacer(1, 48))
        ptext = "<font size=12>Ima Sucker</font>"
        flowables.append(Paragraph(ptext, styles["Normal"]))
        flowables.append(Spacer(1, 12))
        doc.build(flowables)

    def first_page(canvas, document):
        title = "PLATYPUS Demo"
        PAGE_HEIGHT = defaultPageSize[1]
        PAGE_WIDTH = defaultPageSize[0]

        canvas.saveState()
        canvas.setFont("Times-Bold", 18)
        canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, title)

        canvas.setFont("Times-Roman", 10)
        text = "Welcome to the first PLATYPUS Page!"
        canvas.drawString(inch, 10 * inch, text)
        canvas.restoreState()

    def later_pages(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawString(7 * inch, 0.5 * inch, "Page {}".format(document.page))
        canvas.restoreState()

    def create_document():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
            showBoundary=1,
        )
        styles = getSampleStyleSheet()
        flowables = []
        spacer = Spacer(1, 0.25 * inch)

        for i in range(50):
            text = "Paragraph #{}".format(i)
            para = Paragraph(text, styles["Normal"])
            flowables.append(para)
            flowables.append(spacer)
        doc.build(flowables, onFirstPage=first_page, onLaterPages=later_pages)

    def mixed():
        cvs = Canvas(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        width, height = letter

        text = "Hello, I'm a Paragraph."
        para = Paragraph(text, style=styles["Normal"])
        para.wrapOn(cvs, width - 20, height - 20)
        para.drawOn(cvs, 20, 760)
        cvs.showPage()
        cvs.save()

    def frame_demo():
        cvs = Canvas(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        heading = styles["Heading1"]

        flowables = []
        flowables.append(Paragraph("Heading #1", heading))
        for i in range(100):

            flowables.append(
                Paragraph(
                    "Paragraph #1Paragraph #1Paragraph #1Paragraph #1Paragraph #1Paragraph #1Paragraph #{}".format(
                        i
                    ),
                    normal,
                )
            )

        right_flowables = []
        right_flowables.append(Paragraph("Heading #2", heading))
        right_flowables.append(Paragraph("Ipsum lorem", normal))
        right_flowables.append(Paragraph("Ipsum lorem", normal))
        right_flowables.append(Paragraph("Ipsum lorem", normal))
        right_flowables.append(Paragraph("Ipsum lorem", normal))

        left_frame = Frame(inch, inch, width=3 * inch, height=9 * inch, showBoundary=1)
        right_frame = Frame(4 * inch, inch, width=3 * inch, height=9 * inch)
        left_frame.addFromList(flowables, cvs)
        right_frame.addFromList(right_flowables, cvs)
        cvs.save()

    def landscape_orientation():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

    def alternate_orientations():
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
            showBoundary=1,
        )
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        margin = 0.5 * inch
        frame = Frame(margin, margin, doc.width, doc.height, id="frame")
        portrait_template = PageTemplate(id="portrait", frames=[frame], pagesize=letter)
        landscape_template = PageTemplate(
            id="landscape", frames=[frame], pagesize=landscape(letter)
        )

        doc.addPageTemplates([portrait_template, landscape_template])

        story = []
        story.append(Paragraph("This is a page in portrait orientation", normal))

        story.append(NextPageTemplate("landscape"))
        story.append(PageBreak())
        story.append(Spacer(inch, 2 * inch))
        story.append(Paragraph("This is a page in landscape orientation", normal))

        story.append(NextPageTemplate("portrait"))
        story.append(PageBreak())
        story.append(Paragraph("Now we're back in portrait mode again", normal))
        doc.build(story)

    def paragraph_para_markup():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Centered", alignment=TA_CENTER))

        flowables = []
        text = "<para align=center>Hello, I'm a paragraph</para>"
        para = Paragraph(text, style=styles["Centered"])
        flowables.append(para)
        doc.build(flowables)

    def intra_tags():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        flowables = []
        text = """
        This <b>text</b> is important,
        not <strong>strong</strong>.<br/><br/>
        A book title should be in <i>italics</i><br/><br/>
        You can also <u>underline</u> your text.<br/><br/>
        Bad text should be <strike>Struk-through</strike>!<br/><br/>
        You can link to <a href="https://www.google.com" color="green">Google</a>
        like this.
        """
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)
        doc.build(flowables)

    def paragraph_spacing():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        styles["Normal"].spaceBefore = 5
        styles["Normal"].spaceAfter = 50

        flowables = []

        text = """
        This <b>text</b> is important,
        not <strong>strong</strong>.
        """
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = "A book title should be in <i>italics</i>"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = "You can also <u>underline</u> your text."
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = "Bad text should be <strike>struk-through</strike>!"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = """
        You can link to <a href='https://www.google.com' color='red'>Google</a>
        like this.
        """
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        doc.build(flowables)

    def paragraph_fonts():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        flowables = []

        ptext = (
            "<font name=helvetica size=12>Welcome to Reportlab! " "(helvetica)</font>"
        )
        para = Paragraph(ptext, style=styles["Normal"])
        flowables.append(para)

        ptext = "<font face=courier size=24>Welcome to Reportlab! (courier)</font>"
        para = Paragraph(ptext, style=styles["Normal"])
        flowables.append(para)

        ptext = "<font face=times-roman size=48>Welcome to <font color=green> Reportlab!</font> (times-roman)</font>"
        para = Paragraph(ptext, style=styles["Normal"])
        flowables.append(para)

        doc.build(flowables)

    def paragraph_numbering():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = []

        for item in range(1, 4):
            ptext = '<seq id="test"> things(s)'
            para = Paragraph(ptext, style=styles["Normal"])
            flowables.append(para)

        seq = getSequencer()
        seq.setFormat("Section", "1")
        seq.setFormat("FigureNo", "A")

        for item in range(4, 8):
            text = 'Fig. <seq template="%(Section+)s-%(FigureNo+)s"/>'
            para = Paragraph(text, style=styles["Normal"])
            flowables.append(para)

        doc.build(flowables)

    def simple_table():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        data = [
            ["col_{}".format(x) for x in range(1, 9)],
            [str(x) for x in range(1, 7)],
            ["a", "b", "c", "d", "e"],
        ]
        tbl = Table(data)
        story.append(tbl)
        doc.build(story)

    def simple_table_with_style():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        data = [
            ["col_{}".format(x) for x in range(1, 6)],
            [str(x) for x in range(1, 6)],
            ["a", "b", "c", "d", "e"],
        ]
        tblstyle = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.red),
                ("TEXTCOLOR", (0, 1), (-1, 1), colors.blue),
            ]
        )
        tbl = Table(data)
        tbl.setStyle(tblstyle)
        story.append(tbl)
        doc.build(story)

    def table_background_gradient():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        data = data = [
            ["col_{}".format(x) for x in range(1, 6)],
            [str(x) for x in range(1, 6)],
            ["a", "b", "c", "d", "e"],
        ]
        tblstyle = TableStyle(
            [
                # (
                #     "BACKGROUND",
                #     (0, 0),
                #     (-1, -1),
                #     ["HORIZONTAL", colors.red, colors.blue],
                # ),
                # ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("INNERGRID", (0, 0), (-1, -1), 1.25, colors.green),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
        tbl = Table(data)
        tbl.setStyle(tblstyle)
        story.append(tbl)
        story.append(Spacer(0, 25))
        tbl = Table(data, style=[("GRID", (0, 0), (-1, -1), 0.5, colors.blue)])
        story.append(tbl)
        doc.build(story)

    def preformatted_paragraph():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = []

        text = "<para align=center>Hello, I'm a Paragraph</para>"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = "<para align=center>Hello, I'm a Preformatted Paragraph</para>"
        para = Preformatted(text, style=styles["Normal"])
        flowables.append(para)

        doc.build(flowables)

    def list_flowable_squares():
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        normal = styles["Normal"]
        story = []

        flowables = [
            Paragraph("Paragraph numero uno", normal),
            ListItem(Paragraph("Paragraph #2", normal), bulletColor="Blue"),
            Paragraph("Paragraph #3", normal),
        ]
        flowables.append(
            ListFlowable(
                [
                    Paragraph("I'm a sublist item", normal),
                    ListItem(
                        Paragraph("I'm another sublist item", normal),
                        bulletColor="Blue",
                    ),
                    ListItem(
                        Paragraph("I'm the last sublist item", normal),
                        bulletColor="red",
                    ),
                ],
                bulletType="bullet",
                start="square",
            ),
        )
        lflow = ListFlowable(flowables, bulletType="I")
        story.append(lflow)
        doc.build(story)

    def encryption_demo(
        userPassword, ownerPassword, canPrint=1, canModify=1, canCopy=1, canAnnotate=1
    ):
        encrypt = pdfencrypt.StandardEncryption(
            userPassword, ownerPassword, canPrint, canModify, canCopy, canAnnotate
        )
        cvs = Canvas(buffer, encrypt=encrypt)
        cvs.drawString(20, 750, "This is page one")
        cvs.save()

    c = Canvas(buffer, pagesize=A4)
    width, height = A4
    fonts = c.getAvailableFonts()

    encryption_demo(userPassword="bad_password", ownerPassword="XXXX_password")
    # list_flowable_squares()
    # table_background_gradient()
    # simple_table_with_style()
    # simple_table()
    # paragraph_numbering()
    # paragraph_fonts()
    # paragraph_spacing()
    # intra_tags()
    # paragraph_para_markup()
    # font_demo(c, fonts)
    # rotate_demo(c)
    # string_alignment(c)
    # draw_lines(c)
    # draw_shapes(c)
    # gray_color_demo(c)
    # color_demo(c)
    # textobject_demo(c)
    # textobject_cursor(c)
    # textobject_char_spacing(c)
    # wordspacer(c)
    # create_form("02/18/2025", "$7,900", "John Doe", c)
    # embedded_font_demo(c)
    # hello()
    # form_letter()
    # create_document()
    # mixed()
    # frame_demo()
    # alternate_orientations()
    # c.showPage()
    # c.save()
    buffer.seek(0)
    return buffer
