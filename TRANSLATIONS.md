# Translation System Guide

## Overview

The Cave Tech Labs website now supports multiple languages: **Norwegian (Norsk)**, **English**, and **Simplified Chinese (中文)**. The site uses a two-part translation system:

1. **Static UI Translations** - Built into the codebase (hardcoded)
2. **Dynamic Content Translations** - Stored in the database (managed via admin panel)

---

## Language Switcher

Users can switch languages using the globe icon (🌐) in the navigation bar. The selected language is saved to browser localStorage, so the preference persists across page reloads.

### Language Codes
- `nb` - Norwegian (Bokmål) - Default
- `en` - English
- `zh-hans` - Simplified Chinese

---

## Static UI Translations

All buttons, navigation labels, and generic text are hardcoded in `templates/base.html` as a JavaScript object. These are automatically translated when users switch languages.

### Supported Labels
- Navigation: Home, About, Members, Projects, Admin
- Footer: Contact, Follow, Location, Year, Type
- Homepage: Title, Description, Buttons
- Pages: All page headers, subheadings, and generic UI text

To add or modify static translations:
1. Edit `templates/base.html` - find the `allTranslations` JavaScript object
2. Add your new text under each language key (nb, en, zh-hans)
3. Commit and deploy

---

## Dynamic Content Translations (SiteSettings)

The following fields in **Site Settings** can be translated:

- **About Title** (`about_title_translations`)
- **About Content** (`about_content_translations`)
- **History** (`history_translations`)

These are managed via the Django admin panel.

### How to Add Translations via Admin

1. Go to **Admin Panel**: https://www.cavetechlabs.com/admin/
2. Navigate to **Site Settings** (under Cavetechapp)
3. Edit the existing SiteSettings entry
4. Find the translation fields (About Title Translations, About Content Translations, History Translations)
5. Each field accepts a JSON object with language codes as keys

### Example JSON Format

For "About Content Translations", enter:

```json
{
  "nb": "Norsk tekst her...",
  "en": "English text here...",
  "zh-hans": "中文文本这里..."
}
```

### Admin Panel Field Names

- **About Title Translations** → Stored as `about_title_translations`
- **About Content Translations** → Stored as `about_content_translations`  
- **History Translations** → Stored as `history_translations`

### Adding Translations via Django Shell

If you prefer command line:

```bash
ssh www.cavetechlabs.com
cd /home/elisabeth/projects/cavetechlabs
docker-compose exec -T web python manage.py shell
```

Then in Python:

```python
from cavetechapp.models import SiteSettings

s = SiteSettings.get_settings()

s.about_content_translations = {
    'nb': 'Norsk tekst',
    'en': 'English text',
    'zh-hans': '中文文本'
}

s.save()
print('✓ Translations added!')
```

---

## How It Works

### On Page Load
1. JavaScript reads the `language` value from browser localStorage (defaults to 'nb')
2. It loads the embedded `allTranslations` object for static UI text
3. It parses the `site-translations` JSON script tag for dynamic content
4. All elements with `data-i18n` attributes get their text replaced
5. All elements with `data-field` attributes get their translated content from the database

### When User Switches Language
1. User clicks language button in the globe dropdown
2. JavaScript saves the language code to localStorage
3. Page reloads with the new language applied
4. All UI text and dynamic content translates

---

## Testing Translations

### Desktop
1. Open https://www.cavetechlabs.com/
2. Click the globe icon (🌐) in the top-right navigation
3. Select a different language
4. Verify the page content changes
5. Go to About page to see both static UI and dynamic content translations

### Mobile
The language switcher is available on mobile as well, though the UI label may be hidden on smaller screens.

---

## Technical Notes

### Template System
- Base template: `templates/base.html` - Contains translation JavaScript
- About template: `templates/cavetechapp/about.html` - Includes `data-field` attributes for dynamic content

### Database Schema
```python
# In cavetechapp/models.py
class SiteSettings(models.Model):
    about_title_translations = JSONField(default=dict, blank=True)
    about_content_translations = JSONField(default=dict, blank=True)
    history_translations = JSONField(default=dict, blank=True)
```

### JavaScript Keys for Dynamic Content
```javascript
// In the about.html template:
// <p data-field="about_content" data-default="...">

// This is read by JavaScript:
// if (siteTranslations['about_content']['en']) { ... }
```

---

## Troubleshooting

### Translations Not Appearing
1. **Clear browser cache** - Press Ctrl+Shift+Delete and clear cache
2. **Check localStorage** - Open browser DevTools, go to Application > Storage > LocalStorage
3. **Verify JSON format** - Ensure translations are valid JSON in admin panel
4. **Check deployment** - Confirm changes were deployed: `git log` on the server

### Language Reverts to Norwegian
This is expected behavior. The default language is set to Norwegian ('nb'). Users must explicitly select another language, which is saved to localStorage.

### Specific Language Not Showing
1. Make sure the language code matches exactly (nb, en, zh-hans)
2. Open browser DevTools console to check for JavaScript errors
3. Verify the translations JSON is properly formatted

---

## File Locations

- **Static UI Translations**: `templates/base.html` (lines 268-270)
- **Dynamic Translations Config**: `cavetechapp/models.py` (SiteSettings model)
- **Admin Configuration**: `cavetechapp/admin.py` (SiteSettings admin)
- **About Template**: `templates/cavetechapp/about.html`
- **View Logic**: `cavetechapp/views.py` (AboutView)

---

## Future Enhancements

Possible improvements:
- Add more dynamic fields to translations (e.g., contact form labels)
- Add translation support to Project and Person models
- Implement auto-detection of user's browser language
- Create a dedicated translation management interface
