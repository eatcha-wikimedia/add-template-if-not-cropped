import pywikibot
from pywikibot import pagegenerators, logentries

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to page."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text, new_text)
    page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)

def out(text, newline=True, date=False, color=None):
    """Just output some text to the consoloe or log."""
    if color:
        text = "\03{%s}%s\03{default}" % (color, text)
    dstr = (
        "%s: " % datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if date
        else ""
    )
    pywikibot.stdout("%s%s" % (dstr, text), newline=newline)

add_template(cat):
    gen = pagegenerators.CategorizedPageGenerator(pywikibot.Category(SITE,cat))
    for file in gen:
        file_name = file.title()
        if file_name.startswith("File:"):
            
            
    

def main():
    global SITE
    SITE = pywikibot.Site()
    cat_array = [
        "Type specimens of the Natural History Museum, London",
        ]
    for cat in cat_array:
        add_template(cat)

if __name__ == "__main__":
  try:
    main()
  finally:
    pywikibot.stopme()
