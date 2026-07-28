import re

with open('/Users/cp/Ronak/CP/CP Website/servicepages/solution-track-trace.html', 'r') as f:
    template = f.read()

# Fix CSS alignment for check mark icons
template = template.replace('.bento-impact {\n  display: inline-flex;\n  align-items: center;', '.bento-impact {\n  display: inline-flex;\n  align-items: flex-start;')

# We can also add flex-shrink: 0 to the svg in .bento-impact by modifying the html.
# The SVG is <svg class="icon" width="16" height="16"><use href="#icon-check"/></svg>
template = template.replace(
    '<div class="bento-impact"><svg class="icon" width="16" height="16">',
    '<div class="bento-impact"><svg class="icon" width="16" height="16" style="flex-shrink:0; margin-top:1px;">'
)

# 1. Update Section 3 icons (Stage 1, 3, 4, 5)
template = template.replace(
    '''<div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-shield"/></svg>
            </div>
            <div class="stb-text">
              <span class="stb-layer">Stage 1</span>
              <span class="stb-label">Plant</span>''',
    '''<div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-box"/></svg>
            </div>
            <div class="stb-text">
              <span class="stb-layer">Stage 1</span>
              <span class="stb-label">Plant</span>'''
)
template = template.replace(
    '''<button class="sticky-tab-btn" data-stab="tab-distributor" id="stab-distributor" aria-controls="panel-distributor" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-fingerprint"/></svg>
            </div>''',
    '''<button class="sticky-tab-btn" data-stab="tab-distributor" id="stab-distributor" aria-controls="panel-distributor" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-truck"/></svg>
            </div>'''
)
template = template.replace(
    '''<button class="sticky-tab-btn" data-stab="tab-retailer" id="stab-retailer" aria-controls="panel-retailer" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-fingerprint"/></svg>
            </div>''',
    '''<button class="sticky-tab-btn" data-stab="tab-retailer" id="stab-retailer" aria-controls="panel-retailer" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-users"/></svg>
            </div>'''
)
template = template.replace(
    '''<button class="sticky-tab-btn" data-stab="tab-consumer" id="stab-consumer" aria-controls="panel-consumer" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-fingerprint"/></svg>
            </div>''',
    '''<button class="sticky-tab-btn" data-stab="tab-consumer" id="stab-consumer" aria-controls="panel-consumer" aria-selected="false">
            <div class="stb-icon">
              <svg class="icon" width="20" height="20"><use href="#icon-search"/></svg>
            </div>'''
)

# 2. Fix Section 6 Header
template = template.replace(
    '''<p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Fits the stack you already run</p>
          <h2>No rip-and-replace required.</h2>
          <p>We built Smart Epsilon to plug into the systems your production lines and warehouses already depend on.</p>''',
    '''<p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Integrations</p>
          <h2>Fits the Stack You Already Run</h2>
          <p>We built Smart Epsilon to plug into the systems your production lines and warehouses already depend on.</p>'''
)

# 3. Fix Section 8 Header and Content
old_vstep = re.search(r'<section class="vstep-section">.*?</section>', template, re.DOTALL)
if old_vstep:
    new_vstep = """<section class="vstep-section">
      <div class="vstep-inner">
        <div class="vstep-header">
          <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Deployment</p>
          <h2>One Rollout Process, Sized to What You're Deploying</h2>
          <p>A single line on one SKU moves fast. A multi-site, multi-ERP rollout takes longer. The sequence below is what stays constant either way. It's how we scope the real timeline with you, instead of quoting one before we've seen your stack.</p>
        </div>

        <div class="vstep-list">
          <div class="vstep-progress-line"></div>
          
          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-search"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">01</div>
              <h3 class="vstep-title">Discovery</h3>
              <p class="vstep-desc">Map your current stages, systems, and data gaps. This is what actually sets the timeline.</p>
            </div>
          </div>
          
          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-database"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">02</div>
              <h3 class="vstep-title">Scoping</h3>
              <p class="vstep-desc">Agree on the lines, SKUs, and integration points, and set a realistic date, in writing.</p>
            </div>
          </div>
          
          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-box"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">03</div>
              <h3 class="vstep-title">POC</h3>
              <p class="vstep-desc">Prove the model end-to-end on one line before committing further.</p>
            </div>
          </div>

          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-route"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">04</div>
              <h3 class="vstep-title">Pilot Batch</h3>
              <p class="vstep-desc">Run a real batch through the full five-stage journey.</p>
            </div>
          </div>

          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-users"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">05</div>
              <h3 class="vstep-title">Team Training</h3>
              <p class="vstep-desc">Get plant, warehouse, and field teams trained and confident on the new workflow.</p>
            </div>
          </div>

          <div class="vstep-item">
            <div class="vstep-icon"><svg class="icon" width="20" height="20"><use href="#icon-trend"/></svg></div>
            <div class="vstep-content">
              <div class="vstep-outline-num">06</div>
              <h3 class="vstep-title">Complete Rollout</h3>
              <p class="vstep-desc">Scale across remaining lines, sites, and partners at your pace.</p>
            </div>
          </div>
        </div>
      </div>
    </section>"""
    template = template.replace(old_vstep.group(0), new_vstep)

with open('/Users/cp/Ronak/CP/CP Website/servicepages/solution-track-trace.html', 'w') as f:
    f.write(template)

print("Done")
