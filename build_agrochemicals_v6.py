import re
from bs4 import BeautifulSoup

# Load pristine solution page
with open('/Users/cp/Ronak/CP/CP Website/Old/smart-epsilon-redesign/solution-anti-counterfeiting.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Update title and meta
title_tag = soup.find('title')
if title_tag:
    title_tag.string = "Agrochemicals | Smart Epsilon"

meta_desc = soup.find('meta', {'name': 'description'})
if meta_desc:
    meta_desc['content'] = "Smart Epsilon gives agrochemical manufacturers plant-to-field visibility, verified authenticity, and dealer accountability."

# 1. HERO SECTION
hero_section = soup.find('section', id='hero')
if hero_section:
    eyebrow = hero_section.find('p', class_='eyebrow')
    if not eyebrow:
        eyebrow = soup.new_tag('p', attrs={'class': 'eyebrow', 'style': 'color: #ffffff; margin-bottom: 1rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;'})
        internal_content = hero_section.find(class_='internal-hero-content')
        if internal_content:
            internal_content.insert(0, eyebrow)
    eyebrow.string = 'AGROCHEMICALS'
    
    h1 = hero_section.find('h1')
    if h1: h1.string = 'From bag to field, nothing goes unverified.'
    
    p = hero_section.find('p', class_='hero-lede')
    if p: p.string = "Smart Epsilon gives agrochemical manufacturers plant-to-field visibility, verified authenticity, and dealer accountability, so spurious product, misapplication liability, and channel disputes get caught before they cost you a season's trust."
    
    # Replace trust items cleanly to avoid duplication
    trust_items = hero_section.find_all('span', class_='features-pill-tag')
    if trust_items:
        parent = trust_items[0].parent
        parent.clear()
        parent.append(BeautifulSoup('''
        <span class="features-pill-tag" style="background: rgba(255,255,255,0.08); color: #ffffff; border: 1px solid rgba(255,255,255,0.15);"><svg class="icon" width="14" height="14" style="color: #6862a7;"><use href="#icon-check"/></svg> EPA / FIFRA-ready compliance</span>
        <span class="features-pill-tag" style="background: rgba(255,255,255,0.08); color: #ffffff; border: 1px solid rgba(255,255,255,0.15);"><svg class="icon" width="14" height="14" style="color: #6862a7;"><use href="#icon-check"/></svg> Works with your ERP</span>
        <span class="features-pill-tag" style="background: rgba(255,255,255,0.08); color: #ffffff; border: 1px solid rgba(255,255,255,0.15);"><svg class="icon" width="14" height="14" style="color: #6862a7;"><use href="#icon-check"/></svg> Live in ~6 weeks</span>
        ''', 'html.parser'))

    cta_btn = hero_section.find('a', class_='btn-primary')
    if cta_btn:
        cta_btn.clear()
        cta_btn.append(BeautifulSoup('Schedule an Agrochemicals Demo <svg class="icon" width="16" height="16"><use href="#icon-arrow-right"/></svg>', 'html.parser'))

    level_titles = hero_section.find_all('div', class_='level-title')
    level_descs = hero_section.find_all('p', class_='level-desc')
    if len(level_titles) >= 3 and len(level_descs) >= 3:
        level_titles[0].string = 'Plant-to-field visibility'
        level_descs[0].string = 'Track every bag from the moment it leaves the formulation plant to the moment a grower opens it.'
        level_titles[1].string = 'Dealer Accountability'
        level_descs[1].string = 'Automated payouts built on verified sell-through data, not self-reported shipment numbers.'
        level_titles[2].string = 'Brand Protection'
        level_descs[2].string = 'Stop spurious look-alikes from destroying your brand reputation in the field.'
        
    card_header = hero_section.find('h3', class_='card-header-title')
    if card_header: card_header.string = 'Real-world impact'

# INJECT NEW CSS
new_css = """
<style>
/* AGROCHEMICALS REDESIGN V6: Premium UI/UX Light Mode & Carousels */
:root {
  --agro-surface: #ffffff;
  --agro-surface-alt: #f7f7fa;
  --agro-border: rgba(0,0,0,0.08);
  --agro-dark: #111111;
  --agro-text: #4a4a5a;
  --agro-primary: #6862a7;
  --agro-primary-light: rgba(104, 98, 167, 0.08);
}

.agro-section {
  padding: 120px 0;
  background: var(--agro-surface);
  position: relative;
}
.agro-section.alt {
  background: var(--agro-surface-alt);
}
.agro-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}
.agro-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px;
}
.agro-header h2 {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: 800;
  color: var(--agro-dark);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}
.agro-header p {
  font-size: 1.125rem;
  color: var(--agro-text);
  line-height: 1.6;
}

/* Fix Hero Spacing */
.internal-hero-content {
  padding-top: 70px !important;
  padding-bottom: 60px !important;
}

/* CAROUSEL BASE STYLES */
.agro-carousel {
  display: flex;
  overflow-x: auto;
  gap: 24px;
  padding-top: 20px;
  margin-top: -20px;
  padding-bottom: 40px;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: var(--agro-primary-light) transparent;
  -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
  mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}
.agro-carousel::-webkit-scrollbar {
  height: 8px;
}
.agro-carousel::-webkit-scrollbar-track {
  background: transparent;
}
.agro-carousel::-webkit-scrollbar-thumb {
  background-color: rgba(104, 98, 167, 0.3);
  border-radius: 20px;
}
.agro-carousel:hover::-webkit-scrollbar-thumb {
  background-color: var(--agro-primary);
}

/* 1. Risks Carousel */
.agro-prob-card {
  flex: 0 0 380px;
  background: var(--agro-surface);
  border: 1px solid var(--agro-border);
  border-radius: 20px;
  padding: 40px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.agro-prob-card:hover {
  transform: translateY(-4px);
  border-color: rgba(104, 98, 167, 0.4);
  box-shadow: 0 12px 40px rgba(15, 15, 37, 0.1);
}
.agro-prob-num {
  font-size: 3.5rem;
  font-weight: 900;
  color: rgba(104, 98, 167, 0.15);
  margin-bottom: 24px;
  line-height: 1;
}
.agro-prob-card h3 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--agro-dark);
  margin-bottom: 16px;
}
.agro-prob-card p {
  font-size: 1.0625rem;
  color: var(--agro-text);
  line-height: 1.6;
  margin: 0;
}

/* 2. Platform Capabilities Carousel */
.agro-bento-item {
  flex: 0 0 320px;
  background: var(--agro-surface);
  border: 1px solid var(--agro-border);
  border-radius: 24px;
  padding: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
  overflow: hidden;
}
.agro-bento-item:hover {
  transform: translateY(-4px);
  border-color: rgba(104, 98, 167, 0.4);
  box-shadow: 0 12px 40px rgba(15, 15, 37, 0.1);
}
.agro-bento-img {
  width: 100%;
  height: 234px;
  object-fit: cover;
  border-bottom: 1px solid var(--agro-border);
}
.agro-bento-content {
  padding: 32px;
}
.agro-bento-item p {
  font-size: 1.0625rem;
  color: var(--agro-dark);
  font-weight: 600;
  line-height: 1.5;
  margin: 0;
}

/* 3. Stacked Implementation Cards */
.agro-stack-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.agro-stack-card {
  background: var(--agro-surface);
  border: 1px solid var(--agro-border);
  border-radius: 24px;
  overflow: hidden;
  position: sticky;
  top: 100px;
  box-shadow: 0 -10px 40px rgba(0,0,0,0.02);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.agro-stack-card:hover {
  transform: translateY(-4px);
  border-color: rgba(104, 98, 167, 0.4);
  box-shadow: 0 12px 40px rgba(15, 15, 37, 0.1);
}
.agro-stack-card:nth-child(1) { top: 100px; }
.agro-stack-card:nth-child(2) { top: 120px; }
.agro-stack-card:nth-child(3) { top: 140px; }
.agro-stack-card:nth-child(4) { top: 160px; }

.agro-stack-header {
  background: var(--agro-surface-alt);
  color: var(--agro-dark);
  padding: 32px 48px;
  border-bottom: 1px solid var(--agro-border);
}
.agro-stack-header h3 {
  font-size: 1.75rem;
  font-weight: 800;
  margin: 0;
}
.agro-stack-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.agro-stack-col {
  padding: 48px;
}
.agro-stack-col:first-child {
  border-right: 1px solid var(--agro-border);
}
.agro-stack-col h4 {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--agro-primary);
  margin-bottom: 24px;
  font-weight: 800;
}
.agro-stack-list {
  list-style: none;
  padding: 0; margin: 0;
}
.agro-stack-list li {
  position: relative;
  padding-left: 28px;
  margin-bottom: 20px;
  font-size: 1.0625rem;
  line-height: 1.6;
  color: var(--agro-text);
}
.agro-stack-list li::before {
  content: '→';
  position: absolute;
  left: 0; top: 0;
  color: var(--agro-primary);
  font-weight: bold;
}

/* 4. Enterprise Value UI/UX Redesign */
.agro-value-wrapper, .agro-comp-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: flex-start;
}
.agro-comp-inner {
  grid-template-columns: 1fr 2fr;
}

.agro-value-sticky, .agro-comp-sidebar {
  position: sticky;
  top: 50vh; 
  transform: translateY(-50%);
}

.agro-value-sticky h2, .agro-comp-sidebar h2 {
  font-size: clamp(2.5rem, 4vw, 3.5rem);
  font-weight: 800;
  color: var(--agro-dark);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 24px;
}
.agro-value-sticky p, .agro-comp-sidebar p {
  font-size: 1.125rem;
  color: var(--agro-text);
  line-height: 1.6;
}

.agro-value-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.agro-value-card {
  background: #ffffff;
  padding: 32px 40px;
  border-radius: 20px;
  border: 1px solid var(--agro-border);
  transition: transform 0.3s ease, background 0.3s ease;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}
.agro-value-card:hover {
  background: var(--agro-surface-alt);
  transform: translateY(-4px);
  border-color: rgba(104, 98, 167, 0.4);
  box-shadow: 0 12px 40px rgba(15, 15, 37, 0.1);
}
.agro-value-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: var(--agro-surface-alt);
  color: var(--agro-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: none;
}
.agro-value-card h3 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--agro-dark);
  margin-bottom: 8px;
}
.agro-value-card p {
  font-size: 1.0625rem;
  color: var(--agro-text);
  line-height: 1.6;
  margin: 0;
}

/* 5. Compliance Sidebar items */
.agro-comp-list {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.agro-comp-item {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  padding-bottom: 40px;
  border-bottom: 1px solid var(--agro-border);
}
.agro-comp-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}
.agro-comp-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: var(--agro-primary-light);
  color: var(--agro-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.agro-comp-text h3 {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--agro-dark);
  margin-bottom: 12px;
}
.agro-comp-text p {
  font-size: 1.0625rem;
  color: var(--agro-text);
  line-height: 1.6;
  margin: 0;
}

/* Responsive */
@media (max-width: 992px) {
  .agro-stack-body, .agro-value-wrapper, .agro-comp-inner { grid-template-columns: 1fr; gap: 40px; }
  .agro-stack-col:first-child { border-right: none; border-bottom: 1px solid var(--agro-border); }
  .agro-value-sticky, .agro-comp-sidebar { position: static; transform: none; }
  .agro-prob-card { flex: 0 0 320px; }
  .agro-bento-item { flex: 0 0 280px; }
}

/* Carousel Buttons */
.carousel-arrow-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    background: #fff;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 50%;
    font-size: 20px;
    color: var(--agro-primary);
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    z-index: 10;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}
.carousel-arrow-btn:hover {
    background: var(--agro-primary);
    color: #fff;
}
.carousel-arrow-btn.left { left: -24px; }
.carousel-arrow-btn.right { right: -24px; }
</style>
<script>
document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.agro-carousel');
    carousels.forEach(carousel => {
        let autoScroll;

        // Auto rotation logic
        const startAutoScroll = () => {
            autoScroll = setInterval(() => {
                if (carousel.matches(':hover')) return; // pause on hover
                carousel.scrollBy({ left: 1, behavior: 'auto' });
                // If reached end, jump to start
                if(carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 1) {
                    carousel.scrollTo({ left: 0, behavior: 'auto' });
                }
            }, 40);
        };
        startAutoScroll();
        
        // Wrap the carousel in a relative container for absolute arrow buttons
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        carousel.parentNode.insertBefore(wrapper, carousel);
        wrapper.appendChild(carousel);

        const leftBtn = document.createElement('button');
        leftBtn.innerHTML = '&#8592;';
        leftBtn.className = 'carousel-arrow-btn left';
        
        const rightBtn = document.createElement('button');
        rightBtn.innerHTML = '&#8594;';
        rightBtn.className = 'carousel-arrow-btn right';
        
        wrapper.appendChild(leftBtn);
        wrapper.appendChild(rightBtn);

        let manualTimeout;
        const manualScroll = (amount) => {
            clearInterval(autoScroll);
            clearTimeout(manualTimeout);
            carousel.scrollBy({ left: amount, behavior: 'smooth' });
            manualTimeout = setTimeout(startAutoScroll, 1500); // Resume auto scroll after 1.5s
        };

        leftBtn.addEventListener('click', () => manualScroll(-380));
        rightBtn.addEventListener('click', () => manualScroll(380));
    });
});
</script>
"""
if hero_section:
    hero_section.insert_before(BeautifulSoup(new_css, 'html.parser'))

# MIDDLE SECTIONS CONTENT
middle_html = """
<!-- 1. THE REAL SUPPLY CHAIN PROBLEMS -->
<section class="agro-section">
  <div class="agro-container">
    <div class="agro-header">
      <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Real-world risks</p>
      <h2>Real Supply Chain Problems</h2>
      <p>Agrochemical supply chains break in more ways than any one page can cover. Here are the five that cost the most, most often.</p>
    </div>
    
    <div class="agro-carousel">
      <div class="agro-prob-card">
        <div class="agro-prob-num">01</div>
        <h3>Spurious Product in the Channel</h3>
        <p>Your biggest ag retailer is quietly stocking a look-alike at 20% below your list price. Can you prove to a grower which bag is real? Unregistered formulators and repackagers sell copies that look right on the shelf. A grower finds out only when the spray fails.</p>
      </div>
      <div class="agro-prob-card">
        <div class="agro-prob-num">02</div>
        <h3>Sell-In Doesn't Equal Sell-Out</h3>
        <p>Distributor orders looked strong all season. Why is next year's demand forecast already wrong? What shipped and what actually moved through the dealer network to a grower are different numbers, and production plans get built on the wrong one.</p>
      </div>
      <div class="agro-prob-card">
        <div class="agro-prob-num">03</div>
        <h3>Regulatory Audit, No Notice</h3>
        <p>A State Lead Agency inspector wants batch-level RUP records and WPS documentation. This week. Reconstructing that from spreadsheets turns a routine inspection into a multi-day scramble.</p>
      </div>
      <div class="agro-prob-card">
        <div class="agro-prob-num">04</div>
        <h3>Misapplication Liability</h3>
        <p>A grower used the wrong dosage, and now there's a crop-failure claim with your name on it. The liability conversation starts with your brand, whether or not the product was ever the actual problem.</p>
      </div>
      <div class="agro-prob-card">
        <div class="agro-prob-num">05</div>
        <h3>Dealer Trust and Channel Loyalty</h3>
        <p>Your dealer's incentive payout has been stuck in review for six weeks. Why would they push your product this season? Slow, disputed rebate programs cost the shelf space the payout was supposed to buy.</p>
      </div>
    </div>
  </div>
</section>

<!-- 2. PLATFORM CAPABILITIES -->
<section class="agro-section alt">
  <div class="agro-container">
    <div class="agro-header">
      <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Platform Capabilities</p>
      <h2>Solutions</h2>
      <p>Ten specific problems Smart Epsilon solves for agrochemical manufacturers.</p>
    </div>
    
    <div class="agro-carousel">
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-1.jpg" alt="Authenticity">
        <div class="agro-bento-content"><p>Verify a crop protection product’s authenticity before purchase, no device required for the first check.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-5.jpg" alt="Demand Estimates">
        <div class="agro-bento-content"><p>Replace shipment-based demand estimates with real, scan-confirmed sell-through data.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-2.jpg" alt="Audit Records">
        <div class="agro-bento-content"><p>Produce audit-ready batch records for a state or federal inspection in minutes, not days.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-8.jpg" alt="Safety Guidance">
        <div class="agro-bento-content"><p>Deliver dosage, tank-mix compatibility, and safety guidance at the point of scan, in the applicator’s language.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-6.jpg" alt="Incentive Payouts">
        <div class="agro-bento-content"><p>Calculate dealer incentive payouts automatically from verified sales, not self-reported invoice volume.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-7.jpg" alt="Detect Diverted Product">
        <div class="agro-bento-content"><p>Detect counterfeit or diverted product entering regional distribution before it reaches a shelf.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-3.jpg" alt="Loading Accuracy">
        <div class="agro-bento-content"><p>Confirm loading and unloading accuracy at regional distribution centers in real time.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-4.jpg" alt="Temperature Compliance">
        <div class="agro-bento-content"><p>Monitor temperature compliance for cold-sensitive seed treatments in storage and transit.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-9.jpg" alt="Flag Shrinkage">
        <div class="agro-bento-content"><p>Flag shrinkage or theft of high-value patented formulations as it happens, not at the next count.</p></div>
      </div>
      <div class="agro-bento-item">
        <img class="agro-bento-img" src="assets/images/card-bg-10.jpg" alt="Real-time Visibility">
        <div class="agro-bento-content"><p>Give every dealer real-time visibility into exactly what they’ve earned, and why.</p></div>
      </div>
    </div>
  </div>
</section>

<!-- 3. HOW EACH SOLUTION APPLIES -->
<section class="agro-section">
  <div class="agro-container">
    <div class="agro-header">
      <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Agrochemical Implementations</p>
      <h2>How Each Solution Applies</h2>
      <p>Horizontal stacked cards — left side: Agro-specific implementation. Right side: business impact.</p>
    </div>
    
    <div class="agro-stack-container">
      <div class="agro-stack-card">
        <div class="agro-stack-header">
          <h3>Track & Trace</h3>
        </div>
        <div class="agro-stack-body">
          <div class="agro-stack-col">
            <h4>Agro-specific implementation</h4>
            <ul class="agro-stack-list">
              <li>Serialization at the point of formulation, tied to each product’s EPA registration number</li>
              <li>Dispatch and receipt confirmed at every regional distribution center, not assumed from an invoice</li>
              <li>Real, scan-verified sell-through data from the dealer network, replacing shipment-based estimates</li>
            </ul>
          </div>
          <div class="agro-stack-col">
            <h4>Business impact</h4>
            <ul class="agro-stack-list">
              <li>Demand forecasts built on what actually sold, not what was shipped</li>
              <li>Audit-ready compliance records in minutes instead of a multi-day scramble</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="agro-stack-card">
        <div class="agro-stack-header">
          <h3>Anti-Counterfeiting Solution</h3>
        </div>
        <div class="agro-stack-body">
          <div class="agro-stack-col">
            <h4>Agro-specific implementation</h4>
            <ul class="agro-stack-list">
              <li>Tamper-evident holographic label on every bag or container, verified in seconds before purchase</li>
              <li>Geo-tagged clone detection flags a duplicate code the moment it’s scanned somewhere it shouldn’t be</li>
              <li>Dosage, tank-mix compatibility, and safety guidance delivered at the point of scan, in the applicator’s language</li>
            </ul>
          </div>
          <div class="agro-stack-col">
            <h4>Business impact</h4>
            <ul class="agro-stack-list">
              <li>Fewer efficacy complaints traced back to spurious product</li>
              <li>Fewer misapplication-driven liability claims, backed by a timestamped record of what was communicated</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="agro-stack-card">
        <div class="agro-stack-header">
          <h3>AI Video Intelligence</h3>
        </div>
        <div class="agro-stack-body">
          <div class="agro-stack-col">
            <h4>Agro-specific implementation</h4>
            <ul class="agro-stack-list">
              <li>Loading and unloading verification at regional distribution centers, confirming dispatch matches the manifest</li>
              <li>Purpose-placed thermal monitoring for temperature-sensitive seed treatments in storage</li>
              <li>Targeted coverage on high-value patented formulations to catch shrinkage as it happens</li>
            </ul>
          </div>
          <div class="agro-stack-col">
            <h4>Business impact</h4>
            <ul class="agro-stack-list">
              <li>Freight disputes resolved with visual proof, not guesswork</li>
              <li>Temperature excursions caught before an entire batch of seed treatment is lost</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="agro-stack-card">
        <div class="agro-stack-header">
          <h3>Payment Linked Incentives</h3>
        </div>
        <div class="agro-stack-body">
          <div class="agro-stack-col">
            <h4>Agro-specific implementation</h4>
            <ul class="agro-stack-list">
              <li>Dealer incentive payouts calculated automatically from verified, scan-confirmed sell-through, not invoice volume</li>
              <li>Real-time dashboard shows every dealer exactly what they’ve earned, and why</li>
            </ul>
          </div>
          <div class="agro-stack-col">
            <h4>Business impact</h4>
            <ul class="agro-stack-list">
              <li>Faster, dispute-resistant payouts that reward dealers for real sell-through</li>
              <li>Protected shelf space and loyalty at the next reorder</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 4. ENTERPRISE VALUE -->
<section class="agro-section alt">
  <div class="agro-container">
    <div class="agro-value-wrapper">
      <div class="agro-value-sticky">
        <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Enterprise Value</p>
        <h2>Business Impact</h2>
        <p>What this adds up to across an agrochemical manufacturing operation.</p>
      </div>
      
      <div class="agro-value-list">
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></div>
          <div>
            <h3>End-to-End Product Visibility</h3>
            <p>From formulation to field, know where every unit is at every stage, not just inside your own four walls.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div>
          <div>
            <h3>Protected Brand Trust</h3>
            <p>Fewer efficacy complaints and liability disputes traced back to spurious product reaching the shelf.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg></div>
          <div>
            <h3>Reduced Liability Exposure</h3>
            <p>A timestamped, defensible record of exactly what dosage and safety guidance was communicated, if a misapplication claim ever surfaces.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg></div>
          <div>
            <h3>Accurate Demand Planning</h3>
            <p>Production and inventory decisions built on real, verified sell-through, not shipment estimates that turn out wrong by harvest.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg></div>
          <div>
            <h3>Audit-Ready Compliance</h3>
            <p>Batch-level FIFRA, RUP, and WPS records available in minutes during a state or federal inspection, not reconstructed under deadline pressure.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg></div>
          <div>
            <h3>Stronger Dealer Relationships</h3>
            <p>Faster, dispute-resistant incentive payouts that reward what a dealer actually sold, protecting shelf space at the next reorder.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg></div>
          <div>
            <h3>Faster Dispute Resolution</h3>
            <p>Visual and data-backed proof resolves freight, distributor, and dealer disagreements in minutes instead of open-ended back-and-forth.</p>
          </div>
        </div>
        <div class="agro-value-card">
          <div class="agro-value-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path><path d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z"></path></svg></div>
          <div>
            <h3>Protected Cold-Chain Integrity</h3>
            <p>Real-time temperature monitoring catches an excursion before an entire batch of seed treatment is lost.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 5. REGULATORY ALIGNMENT -->
<section class="agro-section">
  <div class="agro-container">
    <div class="agro-comp-inner">
      <div class="agro-comp-sidebar">
        <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Regulatory Alignment</p>
        <h2>Compliance & Regulatory Context</h2>
        <p style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6;">FIFRA, EPA registration, and state pesticide law: handled, not hoped for.</p>
      </div>
      <div class="agro-comp-list">
        <div class="agro-comp-item">
          <div class="agro-comp-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg></div>
          <div class="agro-comp-text">
            <h3>FIFRA / EPA registration alignment</h3>
            <p>Serialization ties directly to each product's EPA registration number, the identifier regulators and state inspectors check first.</p>
          </div>
        </div>
        <div class="agro-comp-item">
          <div class="agro-comp-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path></svg></div>
          <div class="agro-comp-text">
            <h3>Restricted Use Pesticide (RUP) tracking</h3>
            <p>Purchase and application records tied to certified-applicator data, supporting the recordkeeping FIFRA requires.</p>
          </div>
        </div>
        <div class="agro-comp-item">
          <div class="agro-comp-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg></div>
          <div class="agro-comp-text">
            <h3>Worker Protection Standard (WPS) support</h3>
            <p>Point-of-scan delivery of Restricted Entry Interval (REI), Pre-Harvest Interval (PHI), and safety guidance, in the applicator's preferred language.</p>
          </div>
        </div>
        <div class="agro-comp-item">
          <div class="agro-comp-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"></path></svg></div>
          <div class="agro-comp-text">
            <h3>State Lead Agency compliance</h3>
            <p>Every state enforces pesticide law through its own Department of Agriculture, coordinated nationally via AAPCO; batch and dealer-level data support audit-readiness during inspection.</p>
          </div>
        </div>
        <div class="agro-comp-item">
          <div class="agro-comp-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg></div>
          <div class="agro-comp-text">
            <h3>Maximum Residue Limit (MRL) traceability</h3>
            <p>Batch-level data supports residue-testing queries and export-market compliance.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# Find sections to remove from pristine HTML
qw = soup.find('section', class_='quote-wall-section')
st = soup.find('section', class_='sticky-tabs-section')
fs = soup.find('section', class_='features-section')
bs = soup.find('section', class_='bento-section')
is_sec = soup.find('section', class_='integration-section')
cs = soup.find('section', class_='comparison-section')
vs = soup.find('section', class_='vstep-section')

# Remove them
for sec in [st, fs, bs, is_sec, cs, vs]:
    if sec:
        sec.decompose()

# Insert the new middle_html exactly where qw was
if qw:
    qw.insert_after(BeautifulSoup(middle_html, 'html.parser'))
    qw.decompose()

# Update Voices -> Case Study
voices_section = soup.find('section', id='voices')
if voices_section:
    voices_section.clear()
    voices_section['style'] = 'background: #ffffff; padding: 120px 0; border-top: 1px solid rgba(0,0,0,0.08); border-bottom: 1px solid rgba(0,0,0,0.08);'
    case_study_html = """
    <div class="agro-container">
        <div class="agro-header">
            <p class="eyebrow" style="color: #6862a7; margin-bottom: 0.75rem; font-size: 11px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">Case Study</p>
            <h2>The Challenge</h2>
        </div>
        <div style="max-width: 800px; margin: 0 auto;">
            <p style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6; margin-bottom: 1.5rem;">Operating across 100+ countries, this agrochemical manufacturer had already built a world-class production and distribution network. But the moment product left the factory, visibility started to fade.</p>
            <blockquote style="font-size: 1.25rem; font-style: italic; color: var(--agro-dark); border-left: 4px solid var(--agro-primary); padding-left: 1.5rem; margin: 2rem 0;">“Secondary sales relied on delayed reporting. Retail movement stayed fragmented. Commercial planning leaned on assumptions instead of verified product movement.”</blockquote>
            <p style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6; margin-bottom: 1.5rem;">Leadership wanted more than operational tidiness. They wanted a straight answer to one question:</p>
            <blockquote style="font-size: 1.25rem; font-style: italic; color: var(--agro-dark); border-left: 4px solid var(--agro-primary); padding-left: 1.5rem; margin: 2rem 0;">“Where is every product, and what’s happening to it across the entire channel?”</blockquote>
            <p style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6; margin-bottom: 1.5rem;">Without that answer, the business couldn’t:</p>
            <ul style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6; list-style: none; padding: 0; margin: 0 0 3rem 0; display: flex; flex-direction: column; gap: 12px;">
                <li style="position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--agro-primary);">•</span> See secondary sales and liquidation in anything close to real time</li>
                <li style="position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--agro-primary);">•</span> Understand what was actually happening at the retailer level</li>
                <li style="position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--agro-primary);">•</span> Forecast demand from real channel activity instead of shipment estimates</li>
                <li style="position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--agro-primary);">•</span> Build a complete history for a single serialized product</li>
                <li style="position: relative; padding-left: 24px;"><span style="position: absolute; left: 0; color: var(--agro-primary);">•</span> Make a fast commercial call with any real confidence behind it</li>
            </ul>
            <h3 style="font-size: 1.75rem; font-weight: 800; color: var(--agro-dark); margin-bottom: 1.5rem;">What We Deployed</h3>
            <p style="font-size: 1.125rem; color: var(--agro-text); line-height: 1.6; margin-bottom: 3rem;">Every product was given a unique digital identity at the point of manufacturing. From there, six connected capabilities carried that identity through the entire commercial lifecycle, an unbroken thread from Identity to Loyalty.</p>
        </div>
    </div>
    """
    voices_section.append(BeautifulSoup(case_study_html, 'html.parser'))

# Update FAQ
faq_section = soup.find('section', class_='faq-section')
if faq_section:
    items = faq_section.find_all('div', class_='faq-item')
    qs = [
        "Does this support Restricted Use Pesticide (RUP) recordkeeping?",
        "Can safety and application information reach our applicator network in multiple languages?",
        "How does this integrate with our existing distributor and ERP systems?",
        "During a state inspection, can we produce batch-level records on demand?"
    ]
    ans = [
        "Yes. Purchase and application records for RUPs are tied to certified-applicator data at the point of scan, supporting FIFRA's recordkeeping requirements.",
        "Yes. Dosage, tank-mix, and safety guidance can be delivered in the applicator's preferred language at the point of scan, supporting WPS accessibility requirements.",
        "Smart Epsilon connects to SAP, Oracle, and other major ERPs without rip-and-replace, via GS1 EPCIS 2.0. Most agrochemical clients are live in about six weeks.",
        "Yes. Batch and dealer-level data is queryable in real time, tied to each product's EPA registration number, for audit-readiness during State Lead Agency inspection."
    ]
    
    # Keep only 4 FAQ items
    for i, item in enumerate(items):
        if i < 4:
            q_elem = item.find('span', class_='faq-q-text')
            a_elem = item.find('div', class_='faq-answer-inner')
            if q_elem: q_elem.string = qs[i]
            if a_elem: 
                a_elem.clear()
                a_p = soup.new_tag('p')
                a_p.string = ans[i]
                a_elem.append(a_p)
        else:
            item.decompose()

# Update CTA
cta_section = soup.find('section', id='cta')
if cta_section:
    cta_intro = cta_section.find('h2', class_='cta-intro__title')
    cta_lede = cta_section.find('p', class_='cta-intro__lede')
    if cta_intro:
        cta_intro['style'] = 'font-size: 250%; max-width: none;'
        cta_intro.clear()
        cta_intro.append(BeautifulSoup("See what end-to-end visibility could look like across your own supply chain.", 'html.parser'))
        # Add the requested CTA button after the text
        btn_html = '<div style="margin-top: 30px;"><a class="btn btn-primary" href="#contact">Schedule a Demo <svg class="icon" width="16" height="16"><use href="#icon-arrow-right"/></svg></a></div>'
        cta_intro.insert_after(BeautifulSoup(btn_html, 'html.parser'))
        
    if cta_lede: cta_lede.string = ""

# Write to agrochemicals-smart-epsilon.html
with open('/Users/cp/Ronak/CP/CP Website/services_cp/agrochemicals-smart-epsilon.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Redesign HTML correctly written.")
