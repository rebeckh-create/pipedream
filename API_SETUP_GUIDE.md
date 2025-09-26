# 🔑 HiYoga API Keys Setup Guide

## How to Find Your API Keys and Credentials

### **1. Mindbody API Keys**

**Where to find:**
1. Log into your Mindbody business account
2. Go to Settings → Integrations → API Credentials
3. Look for "Developer API" section

**What you need:**
- API Key: `mb_XXXXXXXXXXXXXXXXX`
- Site ID: Usually a number like `12345`
- Username: Your Mindbody login username
- Password: Your Mindbody login password

**If you can't find API section:**
- Contact Mindbody support and request API access
- Tell them you need it for "custom automation integration"

---

### **2. WhatsApp Business API**

**Current Setup Check:**
- Are you using WhatsApp Business App or WhatsApp Business Platform?
- Do you have a business phone number set up?

**To get API access:**
1. Apply for WhatsApp Business API through Meta Business
2. OR use a service like Twilio, MessageBird, or 360Dialog
3. You'll get an API token and phone number ID

**What you need:**
- API Token: `whatsapp_XXXXXXXXXXXXXXXXX`
- Phone Number: `+64XXXXXXXXX` (your business number)
- Webhook URL: (I'll provide this)

---

### **3. MetaSuite API**

**Where to find:**
1. Log into your MetaSuite account
2. Go to Settings → API & Integrations
3. Generate new API key if needed

**What you need:**
- MetaSuite API Key: `ms_XXXXXXXXXXXXXXXXX`
- Facebook Page ID: Found in Facebook Page Settings
- Instagram Business Account ID: Found in Instagram Professional Dashboard

---

### **4. ManyChat API**

**Where to find:**
1. Log into ManyChat
2. Go to Settings → API
3. Generate API token

**What you need:**
- API Token: `mc_XXXXXXXXXXXXXXXXX`
- Page ID: Same Facebook Page ID as above

---

### **5. Google APIs**

**Google Analytics:**
1. Go to Google Analytics
2. Admin → Property Settings
3. Look for "Property ID" (starts with GA4-)

**Google Business Profile:**
1. Go to Google My Business
2. Settings → Business Profile ID

**Service Account (for API access):**
1. Go to Google Cloud Console
2. Create new Service Account
3. Download JSON key file

**What you need:**
- Analytics ID: `GA4-XXXXXXXXX`
- Business Profile ID: `XXXXXXXXXXXXXXXXX`
- Service Account JSON file
- Google Calendar ID (optional): `your-calendar@gmail.com`

---

### **6. Email Setup**

**If using Gmail:**
- Email: `info@hiyoga.nz` (or your main email)
- App Password: (Generate in Gmail settings)
- SMTP Server: `smtp.gmail.com`

**If using SendGrid/Mailchimp:**
- API Key from your email service provider
- From Email: `info@hiyoga.nz`

---

## 🔒 **Security Notes**

- **Never share API keys publicly**
- **Use environment variables in production**
- **Rotate keys regularly**
- **Only give minimum required permissions**

## 📞 **If You Need Help Finding Keys**

Contact each platform's support:
- **Mindbody:** support@mindbodyonline.com
- **WhatsApp:** Meta Business Support
- **MetaSuite:** Your MetaSuite account manager
- **ManyChat:** support@manychat.com
- **Google:** Google Cloud Support