import gc
gc.collect()


def free(full=True):

    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    if not full:
        return P
    else :
        return 'Total:{0} Free:{1} ({2})'.format(T, F, P)


def get_root_html(title):

    html = '<!DOCTYPE html>'
    structure = {
        'html'  : '',
        'head'  : '',
        'title' : title,
        'meta'  : [
            'charset="utf-8"',
            'name="robots" content="noindex"',
            'name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5"',
        ],
        'style': {
            '*'                           : '{font-family: Arial, Helvetica, sans-serif;box-sizing: border-box;}',
            'body'                        : '{display: flex;min-height: 100vh;padding: 0; margin: 0;}',
            '#pgside'                     : '{width: 200px;flex-shrink: 0;transition: width 0.2s;background: #283039;}',
            '#pgside #pguser'             : '{display: flex;align-items: center;padding: 10px 5px}',
            '#pgside #pguser img'         : '{width: 50px;margin-right: 5px;border-radius: 50%}',
            '#pgside, #pgside a'          : '{color: #fff;}',
            '#pgside a'           : '{display: block;padding: 20px;width: 100%;text-decoration: none;cursor: pointer;}',
            '#pgside a.current'           : '{ background: #7c1919; }',
            '#pgside a:hover'             : '{ background: #9b2323; }',
            '#pgside i.ico, #pgside i.txt': '{ font-style: normal; }',
            '#pgside i.ico'               : '{font-size: 1.1em;margin-right: 10px;}',
            '@media screen and (max-width:768px)':
"""{#pgside {width:70px;}#pgside #pguser { justify-content: center;}
#pgside a {text-align: center;padding: 20px 0;}
#pgside i.ico {font-size: 1.5em;margin-right: 0;}
#pgside i.txt { display: none;}}""",
            '#pgmain': '{flex-grow: 1;padding: 20px;background: #f2f2f2;}',
            'table.zebra': '{width: 100%;border-collapse: collapse;}',
            'table.zebra tr:nth-child(odd)': '{background: #f2f2f2;}',
            'table.zebra td': '{padding: 10px;}',
            'ul.zebra, ol.zebra': '{padding: 0;margin: 0;list-style: none;}',
            'ul.zebra li, ol.zebra li': '{ padding: 10px; }',
            'ul.zebra li:nth-child(odd), ol.zebra li:nth-child(odd)': '{ background: #f2f2f2; }',
            '.form': '{max-width: 600px; /* optional */padding: 20px;border: 1px solid #eee;background: #f2f2f2;}',
            '.form label, .form input, .form textarea, .form select, .form button ': '{display: block;width: 100%;}',
            '.form label': '{ padding: 10px 0; }',
            '.form input, .form textarea, .form select': '{ padding: 10px; }',
            'input[type=button], input[type=submit], button': """{font-size: 1em;font-weight: 700;padding: 10px;border: 0;color: #fff;background: #870000;cursor: pointer;}""",
            'input[type=submit]': '{ margin-top: 20px; }',
        },
    }

    for key, items in structure.items():

        if items == '':# not closed
            html += '<{}>\n'.format(key)
        elif type(items) == str and items != '':# closed
            html += '<{}>{}</{}>\n'.format(key, items, key)
        elif type(items) == list:# closed
            for item in items:
                html += '<{} {} />\n'.format(key, item)

        elif type(items) == dict:# closed
            html += '<{}>\n'.format(key)
            for name, value in items.items():
                html += '{} {}\n'.format(name, value)
            html += '</{}></head><body><div id="pgside"></div><main id="pgmain"></main></body>\n'.format(key)

    return html


def get_sidebar(devices):

    nav = ''
    active = ''
    for id, device in enumerate(devices):
        if id == 0:
            active = 'current'
        onclick = "action('/{}', 'pgmain');".format(device)
        nav += '<a href="#" class="{}" onclick="{}"><i class="ico">&#9733;</i>'.format(active, onclick)
        nav += '<i class="txt">{}</i></a>'.format(device)

    nav += '<a href="#"><i class="ico">&#9728;</i>'
    nav += '<i class="txt">{}</i></a>'.format(free())

    return nav
