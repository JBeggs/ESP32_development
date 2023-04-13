
def get_html(title):
    f = open('static/index.txt')
    html = f.read().replace("{{__title__}}", title)
    return html


def get_sidebar(devices):

    nav = ''
    active = ''
    for id, device in enumerate(devices):
        if id == 0:
            active = 'active'
        nav += '<li class="{}"><a href="{}"><i class="tim-icons icon-chart-pie-36"></i>'.format(active, device)
        nav += '<p>{}</p></a></li>'.format(device)

    sidebar = '<div class="sidebar" data-color=""><div class="sidebar-wrapper"><ul class="nav">'
    sidebar += nav
    sidebar += '</ul></div>/div>'

    return sidebar
