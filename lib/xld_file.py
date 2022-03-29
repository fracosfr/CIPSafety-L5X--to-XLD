
class XldLine:
    def __init__(self, isComment: bool = False, input: str = "IN", output: str = "OUT", text: str = "") -> None:
        self.isComment = isComment
        self.input = input
        self.output = output
        self.text = text

    def get_xml(self):
        if self.isComment:
            return f"""\n				<typeLine>
					<emptyLine nbRows="1"></emptyLine>
				</typeLine>"""
        else:
            return f"""\n				<typeLine>
					<contact typeContact="openContact" contactVariableName="{self.input}"></contact>
					<HLink nbCells="14"></HLink>
					<coil typeCoil="coil" coilVariableName="{self.output}"></coil>
				</typeLine>"""

    def get_comment_xml(self, line):
        return f"""\n				<textBox width="16" height="1">{self.text}<objPosition posX="0" posY="{line}"></objPosition>
				</textBox>"""

class XldVar:
    def __init__(self, name: str, type: str = "EBOOL") -> None:
        self.name = name
        self.type = type

    def get_xml(self):
        return f"""\n		<variables name="{self.name}" typeName="{self.type}"></variables>"""

class XldFile:
    def __init__(self, name: str) -> None:
        self.lines: list[XldLine] = []
        self.vars: list[XldVar] = []
        self.name = name

    def generate_xld(self):
        vars_list = [o.get_xml() for o in self.vars]

        comments_list = []
        lines_list = []

        line_count = 0
        for line in self.lines:
            lines_list.append(line.get_xml())
            if line.isComment:
                comments_list.append(line.get_comment_xml(line_count))

            line_count += 1

         
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<LDExchangeFile>
	<fileHeader company="Schneider Automation" product="Control Expert V15.0 - 201016B" dateTime="date_and_time#2022-3-25-17:9:13" content="Fichier source LD" DTDVersion="41"></fileHeader>
	<contentHeader name="L5X TO XLS" version="0.0.1" dateTime="date_and_time#2022-3-21-16:5:3"></contentHeader>
	<program>
		<identProgram name="{self.name}" type="section" task="MAST" SectionOrder="1"></identProgram>
		<LDSource nbColumns="16">
			<networkLD>{"".join(lines_list)}{"".join(comments_list)}
			</networkLD>
		</LDSource>
	</program>
	<privateLocalVariables>{"".join(vars_list)}
	</privateLocalVariables>
</LDExchangeFile>"""
