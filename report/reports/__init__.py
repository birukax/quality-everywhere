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
from she.models import Checkpoint, FirePrevention, FPChecklist
from machine.models import Machine
from report.models import ReportHeader


class BaseReport:
    def __init__(self, buffer, elements):
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
