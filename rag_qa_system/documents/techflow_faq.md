# TechFlow Customer FAQ

## About TechFlow

TechFlow is a cloud-based project management platform that helps teams collaborate, track progress, and deliver projects on time. Founded in 2018, TechFlow serves over 50,000 teams worldwide across industries.

---

## Pricing and Plans

### What pricing plans does TechFlow offer?

TechFlow offers three pricing tiers:

**Free Plan** — $0/month
- Up to 3 projects
- Up to 5 team members
- 1 GB total file storage
- Basic task management and kanban boards
- Community forum support only

**Pro Plan** — $12/user/month (billed annually) or $15/user/month (billed monthly)
- Unlimited projects
- Unlimited team members
- 5 GB file storage per user
- Advanced reporting and analytics
- Custom integrations via API and Zapier
- Time tracking and workload view
- Priority email support (response within 4 business hours)

**Enterprise Plan** — Custom pricing (contact sales)
- Everything included in Pro
- Dedicated account manager
- Single Sign-On (SSO) with SAML 2.0
- Advanced security controls and audit logs
- Custom contracts, SLAs, and billing terms
- Bank transfer (ACH/wire) payment option
- 24/7 phone and dedicated Slack support

All paid plans come with a **14-day free trial** — no credit card required.

### How many projects can I create on the Free plan?

The Free plan allows you to create up to **3 projects**. Each project can have up to 5 team members and uses shared storage from your 1 GB team allocation. If you need more than 3 projects, upgrading to the Pro plan gives you unlimited projects starting at $12/user/month.

### What payment methods does TechFlow accept?

TechFlow accepts the following payment methods:

- **Credit cards**: Visa, Mastercard, American Express, and Discover
- **PayPal**: Link your PayPal account for automatic billing
- **Bank transfer (ACH/wire)**: Available exclusively for Enterprise plan customers

All credit card and PayPal transactions are processed securely through Stripe. TechFlow does not store raw card numbers on its servers. Invoices are emailed automatically each billing cycle.

---

## Account Management

### How do I reset my password?

To reset a forgotten password:

1. Go to the TechFlow login page at **app.techflow.io**
2. Click **"Forgot Password?"** below the login form
3. Enter the email address associated with your account and click **"Send Reset Link"**
4. Check your inbox for the password reset email — it may take up to 5 minutes to arrive
5. Click the reset link in the email (the link expires after **24 hours**)
6. Enter your new password and confirm it
7. Click **"Reset Password"** — you will be automatically logged in

If you are already logged in, you can change your password at any time via **Account Settings → Security → Change Password**.

### How do I invite team members to a project?

To invite team members to a TechFlow project:

1. Open the project you want to share
2. Click **"Settings"** in the left sidebar
3. Navigate to the **"Members"** tab
4. Click **"Invite Members"**
5. Enter one or more email addresses (comma-separated to add multiple at once)
6. Choose a permission level: **Viewer**, **Editor**, or **Admin**
7. Click **"Send Invitation"**

Each invitee receives an email invitation with a join link. If they do not yet have a TechFlow account, they will be prompted to create one. Invitations expire after 7 days but can be resent from the Members tab.

---

## Features and Integrations

### Does TechFlow integrate with Slack?

Yes — TechFlow has a native Slack integration. Once connected, your team can:

- Receive real-time Slack notifications for task assignments, comments, status changes, and approaching deadlines
- Create new TechFlow tasks directly from any Slack message using the `/techflow create` command
- Receive a daily digest of project activity in a designated Slack channel
- Configure notification rules per project (choose which events trigger alerts)

To set up the Slack integration:
1. Go to **Settings → Integrations**
2. Click **"Connect Slack"**
3. Authorize TechFlow in your Slack workspace
4. Choose which projects and events to sync

TechFlow also supports integrations with **GitHub**, **GitLab**, **Jira**, **Google Drive**, **Notion**, **Zapier**, and 50+ additional tools via the Integrations page.

### Does TechFlow have a mobile app?

Yes — TechFlow is available on both major mobile platforms:

- **iOS**: Download from the **Apple App Store** (requires iOS 14 or later; compatible with iPhone and iPad)
- **Android**: Download from the **Google Play Store** (requires Android 9 or later)

The mobile app supports all core features: task creation and management, comments and @mentions, file attachments, push notifications, and Kanban board views. A small number of advanced features — complex reporting dashboards and Gantt chart exports — are currently available on the web app only and will be added to mobile in a future release.

---

## Files and Storage

### What is the maximum file upload size?

The maximum size for a single file upload in TechFlow is **25 MB per file**. Files larger than 25 MB must be compressed or split before uploading.

Total storage limits by plan:
- **Free plan**: 1 GB total shared across the entire team
- **Pro plan**: 5 GB per user
- **Enterprise plan**: 10 GB per user (expandable with add-on storage packs)

Supported file types include documents (PDF, DOCX, XLSX, PPTX), images (JPG, PNG, GIF, SVG, WebP), videos (MP4, MOV up to 25 MB), design files (Figma links, Sketch), and most other common formats. Executable files (.exe, .sh) are blocked for security reasons.

### How can I export my TechFlow project data?

TechFlow supports exporting project data in three formats:

- **CSV**: Exports all tasks with their fields (title, assignee, due date, status, priority, tags) as a spreadsheet — ideal for Excel or Google Sheets analysis
- **PDF**: Generates a formatted project report including task lists, Gantt timeline, and summary statistics
- **JSON**: Full structured data export for developers or migrating to another platform

To export a project:
1. Open the project
2. Click the **"···" (More Options)** menu in the top-right corner
3. Select **"Export Project"**
4. Choose your desired format: **CSV**, **PDF**, or **JSON**
5. Click **"Download"** — the file is prepared and downloads immediately for CSV/JSON; PDF may take a few seconds for large projects

You can also request a **full account data export** (all projects, members, and attachments zipped) from **Account Settings → Data & Privacy → Export All Data**. This complies with GDPR Article 20 data portability rights.

---

## Security and Reliability

### What is TechFlow's uptime guarantee?

TechFlow guarantees **99.9% uptime** as defined in our Service Level Agreement (SLA). This equates to no more than 8 hours and 45 minutes of unplanned downtime per year.

Our infrastructure is hosted on **AWS** across multiple availability zones with:
- Automatic failover and load balancing
- Real-time health monitoring and on-call incident response
- Daily encrypted backups retained for 30 days

You can monitor live service status at **status.techflow.io**. Any incident affecting availability is posted there within 15 minutes, along with updates and post-mortems.

Scheduled maintenance windows are communicated at least **72 hours in advance** via email and the status page. Maintenance is typically performed between 02:00–04:00 UTC on Sundays and is excluded from uptime calculations.

### How do I contact TechFlow support?

Support channels depend on your plan:

- **Free plan**: Community forum at community.techflow.io and self-service documentation at docs.techflow.io
- **Pro plan**: Priority email support at support@techflow.io — first response within 4 business hours
- **Enterprise plan**: Dedicated account manager plus 24/7 phone support and a private Slack channel

### Is TechFlow GDPR compliant?

Yes. TechFlow is fully GDPR compliant and CCPA compliant. All data is encrypted in transit (TLS 1.3) and at rest (AES-256). TechFlow is SOC 2 Type II certified and undergoes annual third-party security audits. Two-factor authentication (2FA) via authenticator app or SMS is available for all accounts and required by default on Enterprise plans.

### Can I cancel my subscription at any time?

Yes. You can cancel anytime from **Account Settings → Billing → Cancel Subscription**. Access continues until the end of the current billing period. TechFlow does not charge cancellation fees or prorate unused time, but partial-month refunds are not issued. Annual subscribers who cancel within the first 30 days are eligible for a full refund upon request.
