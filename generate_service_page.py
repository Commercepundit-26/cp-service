import os
import copy
from bs4 import BeautifulSoup
from extract_docx import parse_docx

def map_docx_to_html(docx_path, template_path, output_path):
    print(f"Parsing DOCX: {docx_path}")
    data = parse_docx(docx_path)
    
    print(f"Reading Template: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Hero Banner
    print("Mapping Hero Banner...")
    h1 = soup.find('h1')
    if h1 and data['hero'].get('title'):
        h1.string = data['hero']['title']
    
    if h1:
        # the subtitle is usually a <p> after h1 in the hero content block
        hero_content = h1.find_parent('div', class_='hero-content') or h1.parent
        p = hero_content.find('p')
        if p and data['hero'].get('subtitle'):
            p.string = data['hero']['subtitle']
            
    # 2. Stats
    print("Mapping Stats...")
    stat_boxes = soup.find_all('div', class_='stat-box')
    if not stat_boxes:
        stat_boxes = soup.find_all('div', class_='fun-fact-inner') # alternative class
        
    if stat_boxes and data['stats']:
        # We assume 3 stats in the design
        for i, stat in enumerate(data['stats'][:len(stat_boxes)]):
            h3 = stat_boxes[i].find('h3')
            p = stat_boxes[i].find('p')
            if h3: h3.string = stat['value']
            if p: p.string = stat['label']

    # 3. What Is (Google Ads Section)
    print("Mapping What Is...")
    # Find the section containing the "What Is" heading
    h2s = soup.find_all('h2')
    what_is_h2 = None
    for h in h2s:
        if 'What is' in h.text or 'What Is' in h.text or 'Why Businesses' in h.text:
            what_is_h2 = h
            break
            
    if what_is_h2 and data['what_is'].get('title'):
        what_is_h2.string = data['what_is']['title']
        # The paragraphs are usually next siblings or inside a specific container
        content_container = what_is_h2.find_next('div', class_='ads-text')
        if not content_container:
            content_container = what_is_h2.find_parent('section').find('div', class_='google-ads-content')
            if content_container:
                content_container = content_container.find('div', class_='ads-text')
        
        # We will just replace paragraphs inside content_container
        if content_container and data['what_is'].get('paragraphs'):
            ps = content_container.find_all('p', recursive=False)
            # clear existing paragraphs
            for p in ps:
                p.decompose()
            # prepend new paragraphs before the Vibe Section (the list)
            vibe_section = content_container.find('section', class_='vibe-section')
            for p_text in reversed(data['what_is']['paragraphs']):
                new_p = soup.new_tag('p')
                new_p.string = p_text
                if vibe_section:
                    vibe_section.insert_before(new_p)
                else:
                    content_container.append(new_p)

    # 4. Services (AI Adoption / Cards)
    print("Mapping Services...")
    # Find the services section by looking for ai-adoption-cards or similar grid
    services_grid = soup.find('div', class_='ai-adoption-cards')
    if not services_grid:
        services_grid = soup.find('div', class_='vc_tta-tabs-container') # if it's WP tabs
        
    if services_grid and data['services']['items']:
        # Update the title
        section_parent = services_grid.find_parent('section')
        if section_parent:
            s_title = section_parent.find('h2')
            if s_title and data['services']['title']:
                s_title.string = data['services']['title']

        cards = services_grid.find_all('div', class_='ai-card')
        if cards:
            # We need to match the number of cards to data items
            num_data = len(data['services']['items'])
            num_cards = len(cards)
            if num_data > num_cards:
                for _ in range(num_data - num_cards):
                    new_card = copy.copy(cards[0])
                    services_grid.append(new_card)
            elif num_data < num_cards:
                for c in cards[num_data:]:
                    c.decompose()
                    
            cards = services_grid.find_all('div', class_='ai-card')
            for i, item in enumerate(data['services']['items']):
                h3 = cards[i].find('h3')
                p = cards[i].find('p')
                if h3: h3.string = item['title']
                if p: p.string = item['desc']
                
        # What if it's the WP tabs?
        elif soup.find('div', class_='vc_tta-tabs-container'):
            # This requires complex WP Bakery mapping (tabs and panels)
            tabs_container = soup.find('ul', class_='vc_tta-tabs-list')
            panels_container = soup.find('div', class_='vc_tta-panels-container')
            if tabs_container and panels_container:
                tabs = tabs_container.find_all('li')
                panels = panels_container.find_all('div', class_='vc_tta-panel')
                
                num_data = len(data['services']['items'])
                num_tabs = len(tabs)
                
                if num_data > num_tabs:
                    for _ in range(num_data - num_tabs):
                        tabs_container.append(copy.copy(tabs[0]))
                        panels_container.find('div', class_='vc_tta-panels').append(copy.copy(panels[0]))
                elif num_data < num_tabs:
                    for t in tabs[num_data:]: t.decompose()
                    for p in panels[num_data:]: p.decompose()
                    
                tabs = tabs_container.find_all('li')
                panels = panels_container.find_all('div', class_='vc_tta-panel')
                
                for i, item in enumerate(data['services']['items']):
                    # Tab title
                    span = tabs[i].find('span', class_='vc_tta-title-text')
                    if span: span.string = item['title']
                    
                    # Panel title and desc
                    panel_title = panels[i].find('h2') or panels[i].find('h3')
                    if panel_title: panel_title.string = item['title']
                    
                    panel_desc = panels[i].find('div', class_='wpb_text_column')
                    if panel_desc:
                        p = panel_desc.find('p')
                        if p: p.string = item['desc']

    # 5. Why Choose Us
    print("Mapping Why Choose Us...")
    why_section = None
    for h in h2s:
        if 'Why Choose' in h.text or 'Why Businesses Choose' in h.text:
            why_section = h.find_parent('section')
            if why_section and data['why_choose']['title']:
                h.string = data['why_choose']['title']
            break
            
    if why_section and data['why_choose']['items']:
        why_cards = why_section.find_all('div', class_='why-cp-feature-card')
        if not why_cards:
            # Maybe it uses the WP bento layout or similar
            why_cards = why_section.find_all('div', class_='wpb_wrapper')
            # Fallback simple logic...
        
        if why_cards:
            num_data = len(data['why_choose']['items'])
            num_cards = len(why_cards)
            
            # Since these are inside specific grid wrappers, cloning might be tricky. Let's assume the template has enough, or we just overwrite existing ones.
            for i, item in enumerate(data['why_choose']['items']):
                if i < len(why_cards):
                    h3 = why_cards[i].find('h3')
                    p = why_cards[i].find('p')
                    if h3: h3.string = item['title']
                    if p: p.string = item['desc']
                    
    # 6. Case Studies
    print("Mapping Case Studies...")
    case_section = soup.find('section', class_='case-study-workflow')
    if case_section and data['case_studies']['items']:
        h2 = case_section.find('h2')
        if h2 and data['case_studies']['title']: h2.string = data['case_studies']['title']
        
        cards = case_section.find_all('div', class_='case-card')
        if cards:
            num_data = len(data['case_studies']['items'])
            num_cards = len(cards)
            
            grid = cards[0].parent
            if num_data > num_cards:
                for _ in range(num_data - num_cards):
                    grid.append(copy.copy(cards[0]))
            elif num_data < num_cards:
                for c in cards[num_data:]: c.decompose()
                
            cards = case_section.find_all('div', class_='case-card')
            for i, item in enumerate(data['case_studies']['items']):
                tag = cards[i].find('span', class_='tag')
                if tag: tag.string = item['tag']
                title = cards[i].find('h2', class_='case-title')
                if title: title.string = item['title']
                
                ps = cards[i].find_all('p', recursive=False)
                if len(ps) >= 2:
                    ps[0].string = "Challenge: " + item['challenge']
                    ps[1].string = "Solution: " + item['solution']
                    
                ul = cards[i].find('ul')
                if ul:
                    lis = ul.find_all('li')
                    for li in lis: li.decompose()
                    for stat in item['stats']:
                        new_li = soup.new_tag('li')
                        new_li.string = stat
                        ul.append(new_li)

    # 7. Process
    print("Mapping Process...")
    process_section = soup.find('section', class_='our-process')
    if process_section and data['process']['items']:
        h2 = process_section.find('h2')
        if h2 and data['process']['title']: h2.string = data['process']['title']
        
        steps = process_section.find_all('div', class_='step')
        if steps:
            num_data = len(data['process']['items'])
            num_steps = len(steps)
            
            grid = steps[0].parent
            if num_data > num_steps:
                for _ in range(num_data - num_steps):
                    grid.append(copy.copy(steps[0]))
            elif num_data < num_steps:
                for s in steps[num_data:]: s.decompose()
                
            steps = process_section.find_all('div', class_='step')
            for i, item in enumerate(data['process']['items']):
                num = steps[i].find('p', class_='step-number')
                if num: num.string = f"{i+1:02d}"
                title = steps[i].find('h3', class_='step-title')
                if title: title.string = item['title']
                desc = steps[i].find('p', class_='sub-title')
                if desc: desc.string = item['desc']

    # 8. Tech Stack (Accordion)
    print("Mapping Tech Stack...")
    tech_section = soup.find('section', class_='tech-stack')
    if tech_section and data['tech_stack']['items']:
        h2 = tech_section.find('h2')
        if h2 and data['tech_stack']['title']: h2.string = data['tech_stack']['title']
        
        items = tech_section.find_all('div', class_='acc-item')
        contents = tech_section.find_all('div', class_='acc-content')
        
        if items and contents:
            num_data = len(data['tech_stack']['items'])
            num_items = len(items)
            
            grid = items[0].parent
            if num_data > num_items:
                # Append copies of BOTH item and content
                for _ in range(num_data - num_items):
                    grid.append(copy.copy(items[-1]))
                    grid.append(copy.copy(contents[-1]))
            elif num_data < num_items:
                for it in items[num_data:]: it.decompose()
                for ct in contents[num_data:]: ct.decompose()
                
            items = tech_section.find_all('div', class_='acc-item')
            contents = tech_section.find_all('div', class_='acc-content')
            
            for i, item in enumerate(data['tech_stack']['items']):
                title = items[i].find('span', class_='acc-title')
                if title: title.string = item['category']
                
                p = contents[i].find('p')
                if p: p.string = item['tech']
                
                # Clear logo grid (the little badges) as they are hardcoded
                logo_grid = contents[i].find('div', class_='logo-grid')
                if logo_grid: logo_grid.decompose()

    # 9. FAQs
    print("Mapping FAQs...")
    faq_section = soup.find('div', class_='services_faqs')
    if faq_section and data['faqs']['items']:
        h2 = faq_section.find('h2')
        if h2 and data['faqs']['title']: h2.string = data['faqs']['title']
        
        items = faq_section.find_all('div', class_='faq-item')
        if items:
            num_data = len(data['faqs']['items'])
            num_items = len(items)
            
            grid = items[0].parent
            if num_data > num_items:
                for _ in range(num_data - num_items):
                    grid.append(copy.copy(items[-1]))
            elif num_data < num_items:
                for it in items[num_data:]: it.decompose()
                
            items = faq_section.find_all('div', class_='faq-item')
            for i, item in enumerate(data['faqs']['items']):
                # FAQ title is inside h3, but has a span inside it. We need to preserve the span.
                h3 = items[i].find('h3')
                if h3:
                    span = h3.find('span')
                    h3.clear()
                    h3.append(item['q'])
                    if span: h3.append(span)
                    
                p = items[i].find('p')
                if p: p.string = item['a']

    # Final Output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Generated successfully: {output_path}")

if __name__ == '__main__':
    map_docx_to_html(
        '/Users/cp/Ronak/CP/CP Website/service pages/Software Testing Services.docx',
        '/Users/cp/Ronak/CP/CP Website/services_cp/aws-development-services.html',
        '/Users/cp/Ronak/CP/CP Website/services_cp/software-testing-services.html'
    )
