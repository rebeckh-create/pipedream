# 🔄 HiYoga Pipedream Integration Setup

Since you already have OAuth set up on Pipedream, we can leverage that to make all your API integrations super simple and secure!

## Why Use Pipedream? 🚀

- ✅ **OAuth already configured** - No need to handle API keys manually
- ✅ **Visual workflow builder** - Easy to modify automations
- ✅ **Built-in integrations** - Mindbody, WhatsApp, Google, Facebook all supported
- ✅ **Reliable delivery** - Automatic retries and error handling
- ✅ **Real-time triggers** - Instant responses to events

## Required Pipedream Workflows

I'll help you create these 5 workflows in your Pipedream account:

### **1. Mindbody Sync Workflow** 🏢
**Purpose:** Sync clients, classes, and bookings from Mindbody
**Trigger:** HTTP webhook or scheduled
**Steps:**
- Connect to Mindbody (Site ID: 32353)
- Fetch new/updated clients
- Send data to HiYoga automation system

### **2. WhatsApp Messaging Workflow** 📱
**Purpose:** Send WhatsApp messages via Twilio
**Trigger:** HTTP webhook
**Steps:**
- Receive message data from automation system
- Format message using templates
- Send via Twilio WhatsApp API (from +64 21 199 9642)
- Log delivery status

### **3. Email Automation Workflow** 📧
**Purpose:** Send branded emails to clients
**Trigger:** HTTP webhook
**Steps:**
- Receive email data and template
- Format email with HiYoga branding
- Send via Gmail/SendGrid
- Track opens/clicks

### **4. Social Media Workflow** 📘
**Purpose:** Post to Facebook/Instagram
**Trigger:** HTTP webhook or scheduled
**Steps:**
- Receive post content
- Post to Facebook page (using your existing OAuth)
- Cross-post to Instagram
- Track engagement

### **5. Google Review Workflow** ⭐
**Purpose:** Request and track Google reviews
**Trigger:** HTTP webhook
**Steps:**
- Send review request email
- Track review responses
- Update Google Business Profile

## Setup Steps

### **Step 1: Get Your Pipedream Workflow IDs**

For each workflow you create in Pipedream:
1. Go to your workflow
2. Copy the **Workflow ID** (looks like: `p_abc123`)
3. Update your `.env` file with these IDs

### **Step 2: Configure Webhook URLs**

Each workflow will give you a webhook URL like:
`https://webhook.pipedream.com/p_abc123`

### **Step 3: Test Each Workflow**

I've created a test script that will verify all workflows:
```bash
python src/pipedream_integration.py
```

## Pipedream Workflow Templates

### **Mindbody Sync Workflow**
```javascript
// Trigger: HTTP or Cron
// Step 1: Mindbody API
export default defineComponent({
  async run({ steps, $ }) {
    const mindbody = require('@pipedream/mindbody')
    
    const clients = await mindbody.getClients({
      siteId: 32353,
      // Your existing OAuth will handle auth
    })
    
    return clients
  },
})

// Step 2: Send to HiYoga system
// (HTTP request to your automation system)
```

### **WhatsApp Workflow**
```javascript
// Trigger: HTTP webhook
// Step 1: Receive message data
export default defineComponent({
  async run({ steps, $ }) {
    const { to, message, template_name, variables } = steps.trigger.event.body
    
    // Step 2: Format message with template
    let formattedMessage = message
    if (template_name) {
      // Load template and substitute variables
      formattedMessage = formatTemplate(template_name, variables)
    }
    
    // Step 3: Send via Twilio
    const twilio = require('twilio')
    const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN)
    
    const result = await client.messages.create({
      from: 'whatsapp:+640211999642',
      to: `whatsapp:${to}`,
      body: formattedMessage
    })
    
    return result
  },
})
```

## Benefits of This Approach

### **For You:**
- ✅ **Visual interface** - See your automations in Pipedream's UI
- ✅ **Easy modifications** - Change workflows without coding
- ✅ **Built-in monitoring** - See success/failure rates
- ✅ **OAuth handled** - No API key management

### **For Your Clients:**
- ✅ **Reliable delivery** - Messages won't get lost
- ✅ **Faster responses** - Real-time triggers
- ✅ **Better experience** - Consistent, professional communication

### **For Your Business:**
- ✅ **Scalable** - Handles growing client base
- ✅ **Maintainable** - Easy to update and modify
- ✅ **Cost-effective** - Pay only for what you use

## Next Steps

1. **Share your Pipedream account access** (if you want me to help set up workflows)
2. **Or create the 5 workflows** using the templates above
3. **Get the workflow IDs** and update your `.env` file
4. **Test each workflow** using the test script
5. **Launch your automation!** 🚀

## What You'll Need from Pipedream

```
PIPEDREAM_API_KEY=your_api_key_here
PIPEDREAM_MINDBODY_WORKFLOW_ID=p_abc123
PIPEDREAM_WHATSAPP_WORKFLOW_ID=p_def456  
PIPEDREAM_EMAIL_WORKFLOW_ID=p_ghi789
PIPEDREAM_FACEBOOK_WORKFLOW_ID=p_jkl012
PIPEDREAM_GOOGLE_WORKFLOW_ID=p_mno345
```

## Testing Your Setup

Once configured, you can test everything with:
```bash
# Test all workflows
python src/pipedream_integration.py

# Test specific automation
python scripts/run_automations.py --test

# Send a test welcome message
python scripts/run_automations.py --trigger welcome --client-id test_client
```

## 🎉 The Result

Your studio will have:
- **Automatic welcome sequences** for new clients
- **Smart class reminders** via WhatsApp
- **No-show follow-ups** that actually work
- **Membership renewal automation** 
- **Review requests** that get results
- **Social media posting** on autopilot

All managed through Pipedream's visual interface with your existing OAuth! 🧘‍♀️✨