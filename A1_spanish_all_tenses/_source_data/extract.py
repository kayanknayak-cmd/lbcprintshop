import verbecc, json, re, unicodedata, sys

LANG='es'
c = verbecc.CompleteConjugator(lang=LANG)

# 18 tenses. Imperfect subjunctive and past perfect subjunctive each have -ra/-se
# forms; each counts as ONE tense shown in two forms.
LAYOUT = [
 ("Indicative", [
   ("indicativo","presente","Present","Presente"),
   ("indicativo","pretérito-imperfecto","Imperfect","Pretérito imperfecto"),
   ("indicativo","pretérito-perfecto-simple","Preterite","Pretérito perfecto simple"),
   ("indicativo","futuro","Future","Futuro"),
   ("indicativo","pretérito-perfecto-compuesto","Present Perfect","Pretérito perfecto compuesto"),
   ("indicativo","pretérito-pluscuamperfecto","Past Perfect","Pluscuamperfecto"),
   ("indicativo","pretérito-anterior","Preterite Perfect","Pretérito anterior"),
   ("indicativo","futuro-perfecto","Future Perfect","Futuro perfecto"),
 ]),
 ("Conditional", [
   ("condicional","presente","Conditional","Condicional simple"),
   ("condicional","perfecto","Conditional Perfect","Condicional perfecto"),
 ]),
 ("Subjunctive", [
   ("subjuntivo","presente","Present Subjunctive","Presente"),
   ("subjuntivo","pretérito-imperfecto-1","Imperfect Subj. (-ra)","Imperfecto (-ra)"),
   ("subjuntivo","pretérito-imperfecto-2","Imperfect Subj. (-se)","Imperfecto (-se)"),
   ("subjuntivo","futuro","Future Subjunctive","Futuro"),
   ("subjuntivo","pretérito-perfecto","Present Perfect Subj.","Pretérito perfecto"),
   ("subjuntivo","pretérito-pluscuamperfecto-1","Past Perfect Subj. (-ra)","Pluscuamperfecto (-ra)"),
   ("subjuntivo","pretérito-pluscuamperfecto-2","Past Perfect Subj. (-se)","Pluscuamperfecto (-se)"),
   ("subjuntivo","futuro-perfecto","Future Perfect Subj.","Futuro perfecto"),
 ]),
 ("Imperative", [
   ("imperativo","afirmativo","Affirmative Command","Imperativo afirmativo"),
   ("imperativo","negativo","Negative Command","Imperativo negativo"),
 ]),
]

# The six standard persons an English-speaking learner expects.
PERSONS = [
  ("yo",       ["yo"]),
  ("tú",       ["tú"]),
  ("él/ella/Ud.", ["él"]),
  ("nosotros", ["nosotros"]),
  ("vosotros", ["vosotros"]),
  ("ellos/Uds.", ["ellos"]),
]
IMP_PERSONS = [
  ("tú",       ["tú"]),
  ("Ud.",      ["usted"]),
  ("nosotros", ["nosotros"]),
  ("vosotros", ["vosotros"]),
  ("Uds.",     ["ustedes"]),
]

def strip_pronoun(form, pronoun):
    """verbecc returns 'yo hablo'. Remove the leading pronoun token(s) only."""
    f = form.strip()
    for p in (pronoun, "no "+pronoun):
        if f.startswith(p+" "):
            return f[len(p)+1:].strip()
    # imperativo negativo comes back as 'no hables' style with pronoun first
    m = re.match(r'^(?:no\s+)?'+re.escape(pronoun)+r'\s+(.*)$', f)
    if m: return ("no "+m.group(1)) if f.startswith("no ") else m.group(1)
    return f

def build(verb):
    r = c.conjugate(verb)
    info = json.loads(str(r._verb_info))
    assert info["predicted"] is False, f"{verb}: verbecc PREDICTED the forms. Not shippable."
    moods = json.loads(str(r._moods_conjugation))
    out = {"verb": verb, "template": info["template"], "stem": info["stem"],
           "predicted": info["predicted"], "groups": []}
    for gname, tenses in LAYOUT:
        g = {"group": gname, "tenses": []}
        for mood, tense, en, es in tenses:
            rows = moods[mood][tense]
            persons = IMP_PERSONS if mood == "imperativo" else PERSONS
            cells = []
            for label, prons in persons:
                hit = None
                for row in rows:
                    if row.get("pr") in prons:
                        hit = row; break
                if hit is None:
                    cells.append({"person": label, "form": None}); continue
                raw = hit["c"][0]
                cells.append({"person": label, "form": strip_pronoun(raw, hit["pr"]), "raw": raw})
            g["tenses"].append({"en": en, "es": es, "mood": mood, "key": tense, "cells": cells})
        out["groups"].append(g)
    # voseo: only where vos actually differs from tú
    vos = []
    for mood, tense, en, es in [("indicativo","presente","Present","Presente"),
                                ("subjuntivo","presente","Present Subjunctive","Presente"),
                                ("imperativo","afirmativo","Affirmative Command","Imperativo afirmativo")]:
        rows = moods[mood][tense]
        tu  = next((strip_pronoun(r0["c"][0], r0["pr"]) for r0 in rows if r0.get("pr")=="tú"), None)
        v   = next((strip_pronoun(r0["c"][0], r0["pr"]) for r0 in rows if r0.get("pr")=="vos"), None)
        if v and tu and v != tu:
            vos.append({"en": en, "es": es, "tu": tu, "vos": v})
    out["voseo"] = vos
    return out

verbs = ["hablar","comer","vivir"]
data = {"lang":"es","source":"verbecc","verbs":[build(v) for v in verbs]}
n_t = sum(len(g["tenses"]) for g in data["verbs"][0]["groups"])
data["tense_blocks_shown"] = n_t
data["tense_count_claimed"] = 18   # -ra/-se pairs each count once
json.dump(data, open("/home/claude/a1/data/conjugations.json","w"), ensure_ascii=False, indent=1)
print("verbs:", verbs)
print("tense blocks shown per verb:", n_t)
for v in data["verbs"]:
    print(v["verb"], "template=",v["template"], "predicted=",v["predicted"], "voseo rows=",len(v["voseo"]))
print()
print("hablar / Present:", [x["form"] for x in data["verbs"][0]["groups"][0]["tenses"][0]["cells"]])
print("hablar / Preterite:", [x["form"] for x in data["verbs"][0]["groups"][0]["tenses"][2]["cells"]])
print("hablar / Affirm cmd:", [x["form"] for x in data["verbs"][0]["groups"][3]["tenses"][0]["cells"]])
print("hablar / Neg cmd:", [x["form"] for x in data["verbs"][0]["groups"][3]["tenses"][1]["cells"]])
print("vivir  / Pres Subj:", [x["form"] for x in data["verbs"][2]["groups"][2]["tenses"][0]["cells"]])
print("voseo hablar:", data["verbs"][0]["voseo"])
