# Configuration Guide

This folder contains configuration files for external services integration.

## Google AdSense Configuration

**File:** `adsense.json`

### Setup Instructions:

1. **Get your AdSense Client ID:**
   - Go to [Google AdSense](https://www.google.com/adsense/)
   - Sign in and create an account if you haven't
   - Navigate to "Ads" → "Overview"
   - Copy your Publisher ID (format: `ca-pub-XXXXXXXXXXXXXXXX`)

2. **Get Ad Slot IDs:**
   - Go to "Ads" → "By ad unit"
   - Create new ad units or use existing ones
   - Copy the Ad Slot ID for each unit

3. **Update Configuration:**
   ```json
   {
     "enabled": true,  // Set to true to enable AdSense
     "client_id": "ca-pub-1234567890123456",  // Your Publisher ID
     "slots": {
       "top": {
         "enabled": true,
         "slot_id": "1234567890",  // Your ad unit slot ID
         "format": "auto",
         "full_width_responsive": true,
         "style": "display:block"
       },
       "bottom": {
         "enabled": true,
         "slot_id": "0987654321",
         "format": "auto",
         "full_width_responsive": true,
         "style": "display:block"
       }
     }
   }
   ```

### Ad Slot Positions:

- **top**: Appears below the platform badges, before the download form
- **bottom**: Appears after the features section
- **sidebar**: (Optional) Can be enabled for desktop sidebar ads

---

## Google Analytics Configuration

**File:** `analytics.json`

### Setup Instructions:

1. **Create a Google Analytics Property:**
   - Go to [Google Analytics](https://analytics.google.com/)
   - Sign in and create a new property
   - Choose "Web" as platform
   - Copy your Measurement ID (format: `G-XXXXXXXXXX`)

2. **Update Configuration:**
   ```json
   {
     "enabled": true,  // Set to true to enable Analytics
     "tracking_id": "G-ABC123XYZ",  // Your Measurement ID
     "settings": {
       "anonymize_ip": true,
       "cookie_expires": 63072000,
       "send_page_view": true
     },
     "events": {
       "track_downloads": true,
       "track_language_change": true,
       "track_errors": true
     }
   }
   ```

### Tracked Events:

When enabled, the following events are automatically tracked:

- **download_start**: When user initiates a video download
- **download_success**: When download completes successfully
- **download_error**: When download fails
- **language_change**: When user changes language
- **platform_detect**: Which platform was detected (youtube, tiktok, etc.)

### Privacy Settings:

- **anonymize_ip**: Anonymizes user IP addresses (GDPR compliant)
- **cookie_expires**: Cookie expiration time in seconds (default: 2 years)
- **send_page_view**: Automatically track page views

---

## Important Notes:

1. **Before Deployment:**
   - Replace all placeholder IDs with your actual IDs
   - Set `enabled: true` for services you want to use
   - Test in development environment first

2. **Privacy Compliance:**
   - Ensure you have a privacy policy that discloses use of AdSense and Analytics
   - Consider implementing cookie consent banner for EU users (GDPR)
   - Analytics is configured with IP anonymization by default

3. **Testing:**
   - AdSense ads may not show immediately in development
   - Use AdSense test mode for development testing
   - Analytics events can be viewed in real-time reports

4. **Performance:**
   - Both services load asynchronously to not block page rendering
   - Configuration is cached by the server for better performance
   - Changes to config require app restart to take effect

---

## File Structure:

```
web/
├── config/
│   ├── adsense.json      # Google AdSense configuration
│   ├── analytics.json    # Google Analytics configuration
│   └── README.md         # This file
├── locales/              # Language translations
├── templates/            # HTML templates
└── app.py               # Flask application
```

---

## Support:

- [Google AdSense Help](https://support.google.com/adsense/)
- [Google Analytics Help](https://support.google.com/analytics/)
- [AdSense Policies](https://support.google.com/adsense/answer/48182)
