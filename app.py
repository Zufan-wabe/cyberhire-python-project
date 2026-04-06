from flask import Flask, render_template, request, jsonify
from database import db, Application, TargetCompany
from datetime import date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberhire.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if TargetCompany.query.count() == 0:
        seed = [
            # ── Las Vegas ──────────────────────────────────────────
            ("MGM Resorts International", "Gaming / Hospitality", "Las Vegas, NV", "https://careers.mgmresorts.com", "Major 2023 breach — heavily investing in cybersecurity. SOC, IR, analyst roles.", "High"),
            ("Caesars Entertainment", "Gaming / Hospitality", "Las Vegas, NV", "https://caesars.com/careers", "Paid ransom in 2023 attack. Now aggressively hiring cyber talent.", "High"),
            ("Wynn Las Vegas", "Gaming / Hospitality", "Las Vegas, NV", "https://wynnlasvegas.com/careers", "SOC and cybersecurity analyst openings regularly.", "High"),
            ("The Venetian Resort", "Gaming / Hospitality", "Las Vegas, NV", "https://venetianlasvegas.com/careers", "Active hiring — security analyst and compliance roles.", "Medium"),
            ("Virgin Hotels Las Vegas", "Gaming / Hospitality", "Las Vegas, NV", "https://virginhotels.com/las-vegas", "Security Analyst IT roles posted regularly.", "Medium"),
            ("Switch", "Data Center / Tech", "Las Vegas, NV", "https://switch.com/careers", "SOC Analyst roles, renewable energy data centers. Growing fast.", "High"),
            ("Gaming Laboratories International (GLI)", "Gaming Tech", "Las Vegas, NV", "https://gaminglabs.com/careers", "Cybersecurity and compliance roles. Entry-level friendly.", "High"),
            ("Mission Support and Test Services (MSTS)", "Government / Defense", "North Las Vegas, NV", "https://msts.com/careers", "DoD-adjacent. IR and forensics roles. Clearance a big plus.", "High"),
            ("Lockheed Martin (Nellis AFB)", "Defense Contractor", "Nellis AFB, NV", "https://lockheedmartin.com/careers", "Entry-level systems and security roles. Will sponsor clearance.", "High"),
            ("Clark County School District", "Government / Education", "Las Vegas, NV", "https://ccsd.net/employees/current/employment", "Info Security Analyst roles. Stable, good benefits.", "Medium"),
            ("City of Las Vegas", "Government", "Las Vegas, NV", "https://lasvegasnevada.gov/Government/Departments/Human-Resources", "IT security and compliance positions.", "Medium"),
            ("State of Nevada", "Government", "Las Vegas, NV", "https://careers.nv.gov", "IT Professional roles including network and security.", "Medium"),
            ("Booz Allen Hamilton", "Defense Consulting", "Las Vegas / Remote", "https://boozallen.com/careers", "Cyber analyst roles. Often requires or sponsors clearance.", "Medium"),
            ("SAIC", "Defense Contractor", "Las Vegas / Remote", "https://saic.com/careers", "Cyber and IT roles. Clearance-friendly employer.", "Medium"),
            ("College of Southern Nevada (CSN)", "Education", "Las Vegas, NV", "https://csn.edu/employment", "Part-time cybersecurity instructor. Good for resume + network.", "Low"),
            # ── Big Tech (Remote / Nationwide) ─────────────────────
            ("Microsoft", "Big Tech", "Remote / Nationwide", "https://careers.microsoft.com", "Massive security division — Azure Security, MSTIC threat intel, SOC analyst roles. Search 'security analyst'. Entry-level friendly with Security+ or SC-200.", "High"),
            ("Google", "Big Tech", "Remote / Nationwide", "https://careers.google.com", "Google Trust & Safety, Mandiant (owned by Google), and GCP security roles. Highly competitive but worth applying.", "High"),
            ("Amazon (AWS)", "Big Tech", "Remote / Nationwide", "https://amazon.jobs", "AWS Security, Amazon Security Operations roles. Look for 'security engineer' and 'SOC analyst'. Remote options available.", "High"),
            ("Meta", "Big Tech", "Remote / Nationwide", "https://metacareers.com", "Security engineer and threat intel roles. Competitive pay. Look for 'security operations'.", "Medium"),
            ("IBM", "Big Tech / Consulting", "Remote / Nationwide", "https://ibm.com/employment", "IBM Security / QRadar division. Actively hires entry-level SOC analysts. Good for building experience.", "High"),
            # ── Cybersecurity Firms (Remote / Nationwide) ──────────
            ("CrowdStrike", "Cybersecurity", "Remote / Nationwide", "https://crowdstrike.com/careers", "Top EDR company. Hires SOC analysts, threat hunters, IR specialists. Strong remote culture. Dream employer for cyber professionals.", "High"),
            ("Palo Alto Networks", "Cybersecurity", "Remote / Nationwide", "https://paloaltonetworks.com/company/careers", "Unit 42 threat intel and IR team. Also hires SOC analysts. Security+ and PCNSE valued.", "High"),
            ("SentinelOne", "Cybersecurity", "Remote / Nationwide", "https://sentinelone.com/careers", "Growing fast — SOC analyst and threat intel roles. Remote-friendly. Good entry-level opportunities.", "High"),
            ("Mandiant (Google)", "Cybersecurity / IR", "Remote / Nationwide", "https://careers.google.com", "World-class incident response firm now under Google. IR analyst and threat intel roles.", "High"),
            ("Secureworks", "Cybersecurity / MSSP", "Remote / Nationwide", "https://secureworks.com/careers", "Managed security services — actively hires SOC analysts. Good entry-level pathway. Remote options.", "High"),
            ("Tenable", "Cybersecurity", "Remote / Nationwide", "https://tenable.com/careers", "Vulnerability management company. Security analyst and support roles. Good for learning Nessus.", "Medium"),
            ("Rapid7", "Cybersecurity", "Remote / Nationwide", "https://rapid7.com/careers", "SIEM and IR platform company. SOC analyst and threat intel roles. Remote-friendly.", "Medium"),
            ("Fortinet", "Cybersecurity", "Remote / Nationwide", "https://fortinet.com/corporate/careers", "Network security company. SOC and security analyst roles. NSE certifications valued.", "Medium"),
            # ── Defense Contractors (Nationwide) ───────────────────
            ("Leidos", "Defense Contractor", "Remote / Nationwide", "https://leidos.com/careers", "One of the largest defense IT employers. Actively hires cyber analysts. Often sponsors clearance. Many remote roles.", "High"),
            ("Northrop Grumman", "Defense Contractor", "Nationwide", "https://northropgrumman.com/careers", "Cyber analyst and SOC roles. Sponsors clearance. Strong benefits and job stability.", "High"),
            ("General Dynamics IT (GDIT)", "Defense Contractor", "Nationwide", "https://gdit.com/careers", "Large cyber workforce. Entry-level SOC and analyst roles. Clearance sponsorship available.", "High"),
            ("Raytheon Technologies", "Defense Contractor", "Nationwide", "https://rtx.com/careers", "Cyber analyst and IR roles. Sponsors TS/SCI clearance. Good salary and benefits.", "Medium"),
            ("ManTech", "Defense Contractor", "Remote / Nationwide", "https://mantech.com/careers", "Cyber focused defense contractor. Actively hires SOC and IR analysts. Sponsors clearance.", "High"),
            # ── Washington DC / Government ─────────────────────────
            ("CISA (Cybersecurity & Infrastructure Security Agency)", "Federal Government", "Washington DC / Remote", "https://cisa.gov/careers", "The main US cyber defense agency. Analyst and IR roles. Competitive federal pay and benefits.", "High"),
            ("NSA (National Security Agency)", "Federal Government / Intel", "Washington DC / Fort Meade MD", "https://intelligencecareers.gov/nsa", "Elite cyber agency. Requires TS/SCI clearance. Exceptional training and experience.", "Medium"),
            ("DHS (Dept of Homeland Security)", "Federal Government", "Washington DC / Remote", "https://dhs.gov/homeland-security-careers", "Cyber analyst roles across multiple divisions. Good entry point into federal cyber.", "High"),
            ("FBI Cyber Division", "Federal Government / Law Enforcement", "Washington DC / Nationwide", "https://fbijobs.gov", "Cyber crime investigation roles. Very competitive. Strong background check required.", "Medium"),
            ("Department of Defense (DoD)", "Federal Government / Defense", "Nationwide", "https://defenseciviliancareers.dodea.edu", "Broad cyber roles across branches. Clearance required. USAJobs.gov is where to apply.", "High"),
            ("US Cyber Command", "Federal Government / Military", "Fort Meade, MD / Remote", "https://usajobs.gov", "Top military cyber unit. Civilian analyst roles available. TS/SCI clearance required.", "Medium"),
            # ── Texas ──────────────────────────────────────────────
            ("Dell Technologies", "Big Tech", "Austin / Remote TX", "https://dell.com/careers", "Large security team. SOC analyst and IR roles. Austin HQ. Good entry-level cyber opportunities.", "High"),
            ("AT&T Cybersecurity", "Telecom / Cybersecurity", "Dallas, TX / Remote", "https://att.com/careers", "AT&T has a dedicated cybersecurity division (AlienVault/USM). SOC analyst roles. Good for SIEM experience.", "High"),
            ("Texas Instruments", "Tech / Manufacturing", "Dallas, TX", "https://ti.com/careers", "IT security analyst roles. Stable employer. Good benefits.", "Medium"),
            ("American Airlines", "Aviation", "Fort Worth, TX", "https://jobs.aa.com", "Large IT security team. SOC analyst and cyber analyst roles. Good entry-level opportunities.", "Medium"),
            ("USAA", "Finance / Insurance", "San Antonio, TX / Remote", "https://usaa.com/careers", "Financial services with strong cyber team. SOC analyst roles. Veteran-friendly employer.", "High"),
            ("Hewlett Packard Enterprise (HPE)", "Big Tech", "Houston, TX / Remote", "https://hpe.com/us/en/living-progress/careers.html", "Security analyst and SOC roles. Remote options. Good for building enterprise security experience.", "Medium"),
            # ── Banks & Finance (Remote / Nationwide) ──────────────
            ("JPMorgan Chase", "Finance / Banking", "Remote / Nationwide", "https://jpmorganchase.com/careers", "One of the largest cyber teams in private sector — 3000+ security staff. SOC analyst roles. Competitive pay.", "High"),
            ("Bank of America", "Finance / Banking", "Remote / Nationwide", "https://bankofamerica.com/careers", "Large SOC and IR team. Actively hires cyber analysts. Good entry-level pathway.", "High"),
            ("Capital One", "Finance / Banking", "Remote / Nationwide", "https://capitalone.com/careers", "Tech-forward bank with strong cyber culture. Cloud security and SOC roles. Remote-friendly.", "High"),
            ("Wells Fargo", "Finance / Banking", "Remote / Nationwide", "https://wellsfargo.com/careers", "Large cyber team. SOC analyst and IR roles. Actively hiring entry-level.", "Medium"),
            ("Visa", "Finance / Payments", "Remote / Nationwide", "https://visa.com/careers", "Payment security — fraud detection and SOC analyst roles. Excellent pay.", "Medium"),
        ]
        for name, industry, location, url, notes, priority in seed:
            db.session.add(TargetCompany(name=name, industry=industry, location=location,
                careers_url=url, notes=notes, priority=priority, watching=True))
        db.session.commit()

@app.route('/')
def index():
    apps = Application.query.order_by(Application.date_applied.desc()).all()
    targets = TargetCompany.query.order_by(TargetCompany.name).all()
    stats = {
        'total': len(apps),
        'applied': sum(1 for a in apps if a.status == 'Applied'),
        'interviewing': sum(1 for a in apps if a.status == 'Interviewing'),
        'offer': sum(1 for a in apps if a.status == 'Offer'),
        'rejected': sum(1 for a in apps if a.status == 'Rejected'),
    }
    return render_template('index.html', applications=apps, stats=stats, targets=targets)

@app.route('/add', methods=['POST'])
def add_application():
    data = request.json
    entry = Application(
        company=data['company'], role=data['role'],
        job_url=data.get('job_url', ''), status=data.get('status', 'Applied'),
        contact_name=data.get('contact_name', ''), contact_email=data.get('contact_email', ''),
        notes=data.get('notes', ''), clearance=data.get('clearance', 'None'),
        certs_required=data.get('certs_required', ''), work_type=data.get('work_type', 'On-site'),
        sector=data.get('sector', ''), date_applied=date.today()
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({'success': True, 'id': entry.id})

@app.route('/update/<int:app_id>', methods=['POST'])
def update_application(app_id):
    data = request.json
    entry = Application.query.get_or_404(app_id)
    for key, val in data.items():
        if hasattr(entry, key):
            setattr(entry, key, val)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete/<int:app_id>', methods=['POST'])
def delete_application(app_id):
    entry = Application.query.get_or_404(app_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/targets/add', methods=['POST'])
def add_target():
    data = request.json
    t = TargetCompany(name=data['name'], industry=data.get('industry', ''),
        location=data.get('location', 'Las Vegas, NV'), careers_url=data.get('careers_url', ''),
        notes=data.get('notes', ''), priority=data.get('priority', 'Medium'), watching=True)
    db.session.add(t)
    db.session.commit()
    return jsonify({'success': True, 'id': t.id})

@app.route('/targets/delete/<int:t_id>', methods=['POST'])
def delete_target(t_id):
    t = TargetCompany.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/generate_email/<int:app_id>', methods=['POST'])
def generate_email(app_id):
    import anthropic
    entry = Application.query.get_or_404(app_id)
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return jsonify({'error': 'Add your ANTHROPIC_API_KEY to .env'}), 400
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""Write a professional follow-up email for a cybersecurity job application.
Company: {entry.company}
Role: {entry.role}
Applied: {entry.date_applied}
Contact: {entry.contact_name or 'Hiring Manager'}
Clearance required: {entry.clearance}
Notes: {entry.notes or 'N/A'}
Write a concise confident follow-up email (3-4 short paragraphs).
Subject line first then email body. Professional specific to cybersecurity."""
    msg = client.messages.create(model="claude-opus-4-6", max_tokens=600,
        messages=[{"role": "user", "content": prompt}])
    return jsonify({'email': msg.content[0].text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
