import requests
from datetime import datetime, timedelta
from fpdf import FPDF
# [Stores the web address haveibeenpound where we get the breach data from]
url = "https://haveibeenpwned.com/api/v3/breaches"

# [Fetches breach data from the API with required headers]
response = requests.get(url, headers={"User-Agent": "CTI-Lab-Student"})

if not response.ok:
    print("Error fetching data:", response.status_code)
    exit()

# [Converts API response to Python dictionary]
breaches = response.json()

# [This gets the calculation of the date and time from 7 days ago]
today = datetime.utcnow()
week_ago = today - timedelta(days=7)

# [This filters the breaches]
recent_breaches = []
for breach in breaches:
    added_date_str = breach.get("AddedDate", "")
    if added_date_str:
        added_date = datetime.strptime(added_date_str, "%Y-%m-%dT%H:%M:%SZ")
        if added_date >= week_ago:
            recent_breaches.append({
                "Name": breach["Name"],
                "Domain": breach["Domain"],
                "BreachDate": breach["BreachDate"],
                "AddedDate": added_date_str,
                "DataClasses": breach["DataClasses"],
                "Description": breach["Description"]
            })

# [This prints the breach information]
if not recent_breaches:
    print("No new breaches in the last 7 days.")
else:
    print("ALERT: Recent Breaches (Last 7 Days):\n")
    for breach in recent_breaches:
        print(f"Name: {breach['Name']}")
        print(f"Domain: {breach['Domain']}")
        print(f"Breach Date: {breach['BreachDate']}")
        print(f"Added to HIBP: {breach['AddedDate']}")
        print(f"Data Exposed: {', '.join(breach['DataClasses'])}")
        print(f"Summary: {breach['Description'][:150]}...")
        print("-" * 50)
# [These lines generates pdf report]
if recent_breaches:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly CTI Report: Recent Breaches", ln=True, align="C")
    pdf.ln(10)

    for breach in recent_breaches:
        pdf.multi_cell(0, 10, f"""
Name: {breach['Name']}
Domain: {breach['Domain']}
Breach Date: {breach['BreachDate']}
Added to HIBP: {breach['AddedDate']}
Data Exposed: {', '.join(breach['DataClasses'])}
Summary: {breach['Description'][:300]}...
        """)
        pdf.ln()

    filename = f"hibp_breach_report_{today.strftime('%Y-%m-%d')}.pdf"
    pdf.output(filename)
    print(f"\n PDF report saved as: {filename}")
# [Note: To run this script successfully we need to go to task schedular and create a task.]
