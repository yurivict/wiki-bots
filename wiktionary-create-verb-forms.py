import pywikibot
import datetime

###
### This bot creates missing verb forms by the list (todo.txt)
###

## bot parameters
site = pywikibot.Site('en', 'wiktionary')  # The site we want to run our bot on

##
## log file
##

logfile = datetime.datetime.now().strftime('bot-run-%Y-%m-%d_%H:%M:%S.log')

##
## read todo/done lists
##
with open('./todo.txt') as f:
  todo = f.read().splitlines()
with open('./done.txt') as f:
  done = set(f.read().splitlines())

##
## helper procedures
##
def tm_log():
    return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
def log(s):
    print(s)
    with open(logfile, "a") as myfile:
        myfile.write('%s %s\n' % (tm_log(), s))
def writeDone(s):
    with open("done.txt", "a") as myfile:
        myfile.write("%s\n" % (s))

##
## procedure forming the page
##
def producePage(word,form):
  # -----
  if form == 'en-third-person singular':
    return """==English==

===Verb===
{{head|en|verb form}}
    
# {{en-third-person singular of|%s}}
""" % (word)
  # -----
  if form == 'present participle':
    return """==English==

===Verb===
{{head|en|present participle}}

# {{present participle of|%s|lang=en}}
""" % (word)
  # -----
  if form == 'en-past':
    return """==English==

===Verb===
{{head|en|verb form}}

# {{en-past of|%s}}
""" % (word)
  # -----
  if form == 'en-simple past':
    return """==English==

===Verb===
{{head|en|verb form}}

# {{en-simple past of|%s}}
""" % (word)
  # -----
  if form == 'past participle':
    return """==English==

===Verb===
{{head|en|past participle}}

# {{past participle of|%s|lang=en}}
""" % (word)
  # -----
  raise Exception('Unknown word form: %s' % (form))

##
## iterate
##
for pageDescr in todo:
  if not pageDescr in done:
    try:
      pageRec = pageDescr.split('|')
      wordStr = pageRec[0]
      wordForm = pageRec[1]
      wordFormKind = pageRec[2]
      #print("=====> NEW PAGE (word=%s form=%s(%s))=>>>%s<<<" % (wordStr,wordForm,wordFormKind,producePage(wordStr, wordFormKind)))
      page = pywikibot.Page(site, wordForm)
      if page.exists():
        log("page %s (%s) of word=%s already exists - not touching it" % (wordForm,wordFormKind,wordStr))
        continue
      log("writing page %s (%s) of word=%s ..." % (wordForm,wordFormKind,wordStr))
      page.text = producePage(wordStr, wordFormKind)
      page.save('creating %s of %s (test run)' % (wordFormKind,wordStr))  # Saves the page
      log("... done writing page %s (%s) of word=%s" % (wordForm,wordFormKind,wordStr))
      writeDone(pageDescr)
    except Exception as exc:
      log("caught an exception: %s" % (exc))

