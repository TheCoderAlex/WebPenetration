from ansi2html import Ansi2HTMLConverter


def convert_ansi_to_html(ansi_text):
    conv = Ansi2HTMLConverter()
    html_text = conv.convert(ansi_text, full=False)
    return html_text


def ansi_to_html(ansi_text):
    colors = {
        '30': 'black', '31': 'red', '32': 'green', '33': 'yellow',
        '34': 'blue', '35': 'purple', '36': 'cyan', '37': 'white',
        '90': 'darkgrey', '91': 'lightred', '92': 'lightgreen', '93': 'lightyellow',
        '94': 'lightblue', '95': 'lightpurple', '96': 'lightcyan', '97': 'lightgrey',
    }

    html_text = ""
    current_color = None
    buffer = ""
    i = 0

    while i < len(ansi_text):
        if ansi_text[i:i+3] == '\033[':
            i += 3
            buffer = ""
            while ansi_text[i] != 'm':
                buffer += ansi_text[i]
                i += 1
            if buffer in colors:
                html_text += f'</span><span style="color: {colors[buffer]}">'
            i += 1
        else:
            html_text += ansi_text[i]
            i += 1

    return f'<span>{html_text}</span>'