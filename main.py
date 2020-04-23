import pywikibot
import re
from pywikibot import pagegenerators, logentries

def commit(old_text, new_text, page, summary):
    """Show diff and submit text to page."""
    out("\nAbout to make changes at : '%s'" % page.title())
    pywikibot.showDiff(old_text, new_text)
    #page.put(new_text, summary=summary, watchArticle=True, minorEdit=False)

def findEndOfTemplate(text, template):
    """Find end of any template, by Zitrax"""
    m = re.search(r"{{\s*%s" % template, text)
    if not m:
        return 0
    lvl = 0
    cp = m.start() + 2
    while cp < len(text):
        ns = text.find("{{", cp)
        ne = text.find("}}", cp)
        # If we see no end tag, we give up
        if ne == -1:
            return 0
        # Handle case when there are no more start tags
        if ns == -1:
            if not lvl:
                return ne + 2
            else:
                lvl -= 1
                cp = ne + 2
        elif not lvl and ne < ns:
            return ne + 2
        elif ne < ns:
            lvl -= 1
            cp = ne + 2
        else:
            lvl += 1
            cp = ns + 2
    # Apparently we never found it
    return 0

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

def add_template(cat):
    gen = pagegenerators.CategorizedPageGenerator(pywikibot.Category(SITE,cat))
    
    summary = "Adding {{Do not crop}} template, requested by Pigsonthewing @ commons.wikimedia.org/w/index.php?title=Commons:Bots/Work_requests&oldid=414102776"
    for file in gen:
        file_name = file.title()
        if file_name.startswith("File:"):
            page = pywikibot.Page(SITE, file_name)
            old_rev = page.oldest_revision
            if 'crop' in (old_rev.comment).lower():
                out('already cropped', color="white)
                continue
            old_text = page.get()
            if 'do not crop' in old_text.lower():
                out('already marked with DNC', color="white)
                continue
            end = findEndOfTemplate(old_text, "[Ss]pecimen")
            new_text = (old_text[:end]+  "\n{{Do not crop}}\n" + old_text[end:])
            try:
                commit(old_text, new_text, page, summary,)
            except:
                continue

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
