import re

with open('/Users/cp/Ronak/CP/CP Website/servicepages/solution-track-trace.html', 'r') as f:
    template = f.read()
    
with open('/Users/cp/Ronak/CP/CP Website/servicepages/solution-anti-counterfeiting.html', 'r') as f:
    anti_template = f.read()

# 1. Revert Proof Section
old_proof = re.search(r'<!-- VOICES -->.*?</section>', template, re.DOTALL)
anti_proof = re.search(r'<!-- ============================================\s+SECTION 9: PROOF.*?</section>', anti_template, re.DOTALL)

if old_proof and anti_proof:
    template = template.replace(old_proof.group(0), anti_proof.group(0))

# 2. Update What It Actually Solves into a Table format
old_solves = re.search(r'<!-- ============================================\s+SECTION 5: WHAT IT ACTUALLY SOLVES.*?</section>', template, re.DOTALL)
if old_solves:
    new_solves = """<!-- ============================================
         SECTION 5: WHAT IT ACTUALLY SOLVES — COMPARISON TABLE
         Layout: Light bg, high-contrast table
         ============================================ -->
    <section class="comparison-section" style="padding-top: 60px;">
      <div class="comparison-inner">
        <div class="comparison-header" style="text-align: center; margin-bottom: 3rem;">
          <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Features</p>
          <h2 class="section-title">What It Actually Solves</h2>
        </div>

        <table class="comparison-table" role="table">
          <thead>
            <tr>
              <th scope="col" style="width: 25%;">Feature</th>
              <th scope="col" style="width: 35%;">The Problem It Solves</th>
              <th scope="col" class="col-smart" style="width: 40%;">The Impact</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-weight: 700;">Unit-level serialization at source</td>
              <td>No way to trace a specific unit back to its exact production batch, line, or shift</td>
              <td class="cell-smart">Recalls narrow to the exact affected batch, cutting recall cost and scope dramatically.</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">Dispatch/receipt confirmation at every stage</td>
              <td>"Shipped" and "received" are assumed to match, but it's rarely proven.</td>
              <td class="cell-smart">Disputed shipments and stuck working capital drop, because custody is proven, not assumed.</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">Real-time geolocation tracking</td>
              <td>Visibility disappears the moment product leaves your own four walls</td>
              <td class="cell-smart">Full visibility from plant to consumer, not just to your own warehouse door.</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">GS1 EPCIS 2.0 native data model</td>
              <td>Data is trapped in a proprietary format that can't be shared with partners or regulators</td>
              <td class="cell-smart">Standards-compliant data exchange on demand, no custom integration project needed each time.</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">Automated chain-of-custody trail</td>
              <td>Reconstructing a shipment's history for a legal or regulatory request takes weeks</td>
              <td class="cell-smart">Full history available in minutes, without a cross-functional fire drill.</td>
            </tr>
          </tbody>
        </table>
        
        <div style="text-align: center; margin-top: 3rem;">
          <span data-magnetic style="display: inline-block;"><a href="#" class="btn btn-primary" style="padding: 14px 28px; display: inline-flex; align-items: center; gap: 8px;">See the full technical capability breakdown <svg class="icon" width="16" height="16" aria-hidden="true"><use href="#icon-arrow-right"/></svg></a></span>
        </div>
      </div>
    </section>"""
    template = template.replace(old_solves.group(0), new_solves)

# 3. FAQ 
old_faq_list = re.search(r'<div class="faq-list">.*?</div>\s*</div>\s*</section>', template, re.DOTALL)
if old_faq_list:
    new_faq_list = """<div class="faq-list">
          <div class="faq-item" data-faq>
            <button class="faq-trigger" aria-expanded="false">
              <div class="faq-trigger-q">Does this slow down our production line?</div>
              <div class="faq-trigger-dot"></div>
            </button>
            <div class="faq-answer" role="region">
              <div class="faq-answer-inner">No. Activation happens at the point the product is already being packaged; it adds an identity, not a step.</div>
            </div>
          </div>

          <div class="faq-item" data-faq>
            <button class="faq-trigger" aria-expanded="false">
              <div class="faq-trigger-q">We already have an ERP. Why do we need this too?</div>
              <div class="faq-trigger-dot"></div>
            </button>
            <div class="faq-answer" role="region">
              <div class="faq-answer-inner">Your ERP tracks inventory counts. This tracks the identity of each physical unit. Different data, different purpose, and it feeds your ERP rather than replacing it.</div>
            </div>
          </div>

          <div class="faq-item" data-faq>
            <button class="faq-trigger" aria-expanded="false">
              <div class="faq-trigger-q">What happens to visibility once product leaves our own warehouse?</div>
              <div class="faq-trigger-dot"></div>
            </button>
            <div class="faq-answer" role="region">
              <div class="faq-answer-inner">That’s the point where most systems go dark. This is exactly where Track & Trace keeps working, through distributor and retailer, to the final scan.</div>
            </div>
          </div>
        </div>
      </div>
    </section>"""
    template = template.replace(old_faq_list.group(0), new_faq_list)

# 4. Final CTA
old_cta = re.search(r'<header class="cta-intro" data-reveal>.*?</header>', template, re.DOTALL)
if old_cta:
    new_cta = """<header class="cta-intro" data-reveal>
        <p class="eyebrow">Book a demo</p>
        <h2 class="cta-intro__title" style="margin-bottom: 2rem;">
          Want to see how Track & Trace works? We'll walk you through the full cycle.
        </h2>
        <span data-magnetic style="display: inline-block;"><a class="btn btn-primary" href="#">Schedule a Demo <svg class="icon" width="16" height="16" aria-hidden="true"><use href="#icon-arrow-right"/></svg></a></span>
      </header>"""
    template = template.replace(old_cta.group(0), new_cta)


with open('/Users/cp/Ronak/CP/CP Website/servicepages/solution-track-trace.html', 'w') as f:
    f.write(template)

print("Fixes applied successfully!")
