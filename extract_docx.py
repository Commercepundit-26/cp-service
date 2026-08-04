import docx
import re
import json

def parse_docx(filepath):
    doc = docx.Document(filepath)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    
    data = {
        "meta": {"title": "", "description": ""},
        "hero": {},
        "stats": [],
        "what_is": {},
        "services": {"title": "", "items": []},
        "why_choose": {"title": "", "items": []},
        "case_studies": {"title": "", "items": []},
        "process": {"title": "", "subtitle": "", "items": []},
        "tech_stack": {"title": "", "subtitle": "", "items": []},
        "faqs": {"title": "", "items": []}
    }
    
    current_section = None
    
    for i, line in enumerate(lines):
        if line.startswith("Meta Title:"):
            data["meta"]["title"] = line.split("Meta Title:")[1].strip()
            continue
        elif line.startswith("Meta Description:"):
            data["meta"]["description"] = line.split("Meta Description:")[1].strip()
            continue
        elif line.startswith("SECTION 1: Hero"):
            current_section = "hero"
            continue
        elif line.startswith("SECTION 2: Stats"):
            current_section = "stats"
            continue
        elif line.startswith("SECTION 4: What Is") or line.startswith("SECTION 4: What are") or line.startswith("SECTION 3: What"):
            current_section = "what_is"
            continue
        elif line.startswith("SECTION 5: Services") or line.startswith("SECTION 4: Services"):
            current_section = "services"
            continue
        elif line.startswith("SECTION 6: Why Choose Us") or line.startswith("SECTION 5: Why Choose Us"):
            current_section = "why_choose"
            continue
        elif line.startswith("SECTION 7: Case Studies") or line.startswith("SECTION 6: Case Studies"):
            current_section = "case_studies"
            continue
        elif line.startswith("SECTION 8: Process") or line.startswith("SECTION 7: Process"):
            current_section = "process"
            continue
        elif line.startswith("SECTION 9: Technology Stack") or line.startswith("SECTION 8: Tech Stack"):
            current_section = "tech_stack"
            continue
        elif line.startswith("SECTION 11: FAQ") or line.startswith("SECTION 10: FAQ") or line.startswith("SECTION 9: FAQ"):
            current_section = "faqs"
            continue
            
        if current_section == "hero":
            if "Headline:" in line: data["hero"]["title"] = line.split("Headline:")[1].strip()
            elif "H1:" in line: data["hero"]["title"] = line.split("H1:")[1].strip()
            elif "Subheadline:" in line: data["hero"]["subtitle"] = line.split("Subheadline:")[1].strip()
            elif "Subheading:" in line: data["hero"]["subtitle"] = line.split("Subheading:")[1].strip()
            elif not data["hero"].get("title") and len(line) > 20: data["hero"]["title"] = line
        
        elif current_section == "stats":
            if line.startswith("-"):
                parts = line.lstrip("- ").split(":")
                if len(parts) == 2:
                    data["stats"].append({"value": parts[0].strip(), "label": parts[1].strip()})
            elif len(line.split()) > 1 and not ":" in line and line[0].isdigit():
                # example: "600+ Projects Tested and Delivered"
                data["stats"].append({"value": line.split()[0], "label": " ".join(line.split()[1:])})
                    
        elif current_section == "what_is":
            if not data["what_is"].get("title"):
                data["what_is"]["title"] = line
            else:
                data["what_is"]["paragraphs"] = data["what_is"].get("paragraphs", []) + [line]
                
        elif current_section == "services":
            if not data["services"]["title"]:
                data["services"]["title"] = line
            elif line.startswith("Service Name:"):
                data["services"]["items"].append({"title": line.split("Service Name:")[1].strip(), "desc": ""})
            elif line.startswith("Description:"):
                if data["services"]["items"]: data["services"]["items"][-1]["desc"] = line.split("Description:")[1].strip()
            elif ":" in line and not line.startswith("Headline:"): # alternative format
                parts = line.split(":", 1)
                data["services"]["items"].append({"title": parts[0].strip(), "desc": parts[1].strip()})
            else:
                if len(line) < 100 and not line.startswith("Talk To") and not line.startswith("["):
                    # likely a title
                    data["services"]["items"].append({"title": line.strip(), "desc": ""})
                elif data["services"]["items"]:
                    data["services"]["items"][-1]["desc"] += line.strip() + " "
                
        elif current_section == "why_choose":
            if not data["why_choose"]["title"]:
                data["why_choose"]["title"] = line
            elif ":" in line and not line.startswith("Headline:") and not line.startswith("Description:"):
                parts = line.split(":", 1)
                data["why_choose"]["items"].append({"title": parts[0].strip(), "desc": parts[1].strip()})
            else:
                if len(line) < 100 and not line.startswith("["):
                    data["why_choose"]["items"].append({"title": line.strip(), "desc": ""})
                elif data["why_choose"]["items"]:
                    data["why_choose"]["items"][-1]["desc"] += line.strip() + " "
                
        elif current_section == "case_studies":
            if not data["case_studies"]["title"]:
                data["case_studies"]["title"] = line
            elif line.startswith("Tag:") or line in ["SaaS and Technology", "Ecommerce and Retail", "Healthcare and Enterprise", "Agrochemicals", "B2B"]:
                data["case_studies"]["items"].append({"tag": line.replace("Tag:", "").strip(), "title": "", "challenge": "", "solution": "", "stats": []})
            elif data["case_studies"]["items"]:
                curr = data["case_studies"]["items"][-1]
                if not curr["title"] and len(line) > 10 and not line.startswith("Challenge"):
                    curr["title"] = line
                elif line.startswith("Challenge"):
                    curr["challenge"] = line.replace("Challenge", "").strip(" :")
                elif line.startswith("Solution"):
                    curr["solution"] = line.replace("Solution", "").strip(" :")
                elif ":" in line:
                    curr["stats"].append(line)
                    
        elif current_section == "process":
            if not data["process"]["title"]:
                data["process"]["title"] = line
            elif not data["process"]["subtitle"]:
                data["process"]["subtitle"] = line
            elif line.startswith("Step"):
                m = re.match(r'Step \d+ (.*?) (We.*|Test.*|Manual.*|A final.*)', line)
                if m:
                    data["process"]["items"].append({"title": m.group(1).strip(), "desc": m.group(2).strip()})
                else:
                    data["process"]["items"].append({"title": line, "desc": ""})
                    
        elif current_section == "tech_stack":
            if not data["tech_stack"]["title"]:
                data["tech_stack"]["title"] = line
            elif not data["tech_stack"]["subtitle"]:
                data["tech_stack"]["subtitle"] = line
            elif "[+]" in line or "[-]" in line:
                parts = re.split(r'\[\+\]|\[\-\]', line)
                data["tech_stack"]["items"].append({"category": parts[0].strip(), "tech": parts[1].strip()})
                
        elif current_section == "faqs":
            if not data["faqs"]["title"]:
                data["faqs"]["title"] = line
            elif line.endswith("?"):
                data["faqs"]["items"].append({"q": line.strip(), "a": ""})
            elif data["faqs"]["items"]:
                data["faqs"]["items"][-1]["a"] += line + " "

    return data

if __name__ == '__main__':
    d = parse_docx('/Users/cp/Ronak/CP/CP Website/service pages/Software Testing Services.docx')
    print(json.dumps(d, indent=2))
