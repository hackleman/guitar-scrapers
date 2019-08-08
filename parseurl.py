from bs4 import BeautifulSoup

def tab_from_url(url):
    html = url.content

    # Parse url and find pre tag with tabs
    soup = BeautifulSoup(html, "html.parser")
    tabs_html_content = soup.find_all('pre')
    formatted = ''.join(map(str, tabs_html_content[1].contents))

    # Parse each line into object
    lines = []

    for line in formatted.split('\n'):
        if '<span' in line:
            continue

        else:
            lines.append(line[:-2])

    # Construct tab
    tab = {}
    tab['lines'] = lines
    return tab