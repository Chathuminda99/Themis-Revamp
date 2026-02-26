# Phase 1: Shadcn UI Components for Themis-Revamp

## Overview
Phase 1 implements shadcn-inspired UI components adapted for Jinja2 templates. These components follow shadcn design patterns with Tailwind CSS styling, dark mode support, and accessibility best practices.

## 🎯 Phase 1 Components

### 1. **Button** (`templates/components/button.html`)
Versatile button component with 6 variants and 3 sizes.

**Variants:**
- `primary` (default) - Blue background
- `secondary` - Gray background
- `outline` - Bordered style
- `ghost` - Transparent background
- `destructive` - Red background
- `link` - Text-only style

**Sizes:**
- `sm` - Small (12px text)
- `md` - Medium default (14px text)
- `lg` - Large (16px text)
- `icon` - Square button for icons

**Usage:**
```jinja2
{% include "components/button.html" with context %}
{# button_text="Click Me", button_variant="primary", button_size="md" #}
```

**Parameters:**
- `button_text` - Button label text
- `button_variant` - One of: primary, secondary, outline, ghost, destructive, link
- `button_size` - One of: sm, md, lg, icon
- `button_type` - HTML type attribute (button, submit, reset)
- `button_id` - HTML id attribute
- `button_class` - Additional Tailwind classes
- `button_disabled` - Set to true to disable
- `button_hx` - HTMX attributes
- `button_icon_left` - SVG for left icon
- `button_icon_right` - SVG for right icon

---

### 2. **Badge** (`templates/components/badge.html`)
Status badge component with semantic color variants.

**Variants:**
- `default` (primary) - Blue background
- `secondary` - Gray background
- `destructive` - Red background
- `outline` - Bordered style
- `success` - Green background
- `warning` - Amber background
- `info` - Blue background

**Usage:**
```jinja2
{% include "components/badge.html" with context %}
{# badge_text="Status", badge_variant="success" #}
```

**Parameters:**
- `badge_text` - Badge label text
- `badge_variant` - Color variant
- `badge_icon` - Icon SVG
- `badge_class` - Additional Tailwind classes

---

### 3. **Card** (`templates/components/card.html`, `card_header.html`, `card_content.html`, `card_footer.html`)
Composite card component with header, content, and footer sections.

**Usage:**
```jinja2
<div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-sm">
  <!-- Card Header -->
  <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-800">
    <h3 class="text-lg font-semibold">Card Title</h3>
    <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Description</p>
  </div>

  <!-- Card Content -->
  <div class="px-6 py-4">
    Content goes here
  </div>

  <!-- Card Footer (optional) -->
  <div class="px-6 py-4 border-t border-slate-200 dark:border-slate-800 flex gap-2 justify-end">
    Footer content
  </div>
</div>
```

**Parameters:**
- `card_title` - Header title
- `card_description` - Header description
- `card_content` - Main content
- `card_footer_content` - Footer content
- `card_hover` - Add hover shadow effect
- `card_class` - Additional Tailwind classes

---

### 4. **Form Input** (`templates/components/form_input.html`)
Enhanced text input with label, help text, and validation states.

**Usage:**
```jinja2
{% include "components/form_input.html" with context %}
{#
  field_name="email",
  label="Email Address",
  input_type="email",
  placeholder="john@example.com",
  help_text="We'll never share your email",
  required=true
#}
```

**Parameters:**
- `field_name` - Input name and id attribute
- `label` - Label text
- `input_type` - HTML input type (text, email, password, etc.)
- `placeholder` - Placeholder text
- `value` - Current value
- `help_text` - Help message below input
- `required` - Set to true for required field

---

### 5. **Form Label** (`templates/components/form_label.html`)
Standalone label component for custom form layouts.

**Usage:**
```jinja2
{% include "components/form_label.html" with context %}
{# label_for="email", label_text="Email", required=true #}
```

**Parameters:**
- `label_for` - Associated input id
- `label_text` - Label text
- `required` - Show red asterisk

---

### 6. **Form Select** (`templates/components/form_select.html`)
Enhanced dropdown with label and help text.

**Usage:**
```jinja2
{% include "components/form_select.html" with context %}
{#
  field_name="status",
  label="Select Status",
  placeholder="Choose an option",
  options=[
    {"value": "draft", "label": "Draft"},
    {"value": "active", "label": "Active"},
    {"value": "archived", "label": "Archived"}
  ],
  required=true
#}
```

**Parameters:**
- `field_name` - Select name and id
- `label` - Label text
- `options` - List of {value, label} dicts
- `placeholder` - Default option text
- `selected` - Pre-selected value
- `help_text` - Help message
- `required` - Set to true for required field

---

## 🎨 Design Features

### Dark Mode Support
All components include dark mode variants using `dark:` prefix classes:
- Colors automatically adapt in dark mode
- Focus rings adjusted for dark backgrounds
- Text contrast maintained

### Accessibility
- Focus visible states with ring styles
- Proper semantic HTML (labels, fieldset, etc.)
- Keyboard navigation support
- ARIA attributes where needed

### Animations
- Smooth transitions on all interactive elements
- Focus ring animations
- Hover state transitions
- Disabled state styling

---

## 📋 Component Showcase

View all Phase 1 components in action:
- **Route:** `/admin/components`
- **File:** `templates/components_showcase.html`

This page demonstrates all button variants, badge variants, cards, and form components with code examples.

---

## 🔧 Integration with Existing Templates

### Updating Dashboard Stats
```jinja2
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-sm p-6">
    <div class="flex items-center gap-4">
      <div class="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
        <!-- Icon -->
      </div>
      <div>
        <p class="text-sm text-slate-500 dark:text-slate-400">Total Projects</p>
        <p class="text-3xl font-bold text-slate-900 dark:text-slate-50">{{ total_count }}</p>
      </div>
    </div>
  </div>
</div>
```

### Status Badges
```jinja2
{% if project.status == 'in_progress' %}
  {% include "components/badge.html" with context %}
  {# badge_text=project.status|upper, badge_variant="warning" #}
{% elif project.status == 'completed' %}
  {% include "components/badge.html" with context %}
  {# badge_text=project.status|upper, badge_variant="success" #}
{% else %}
  {% include "components/badge.html" with context %}
  {# badge_text=project.status|upper, badge_variant="secondary" #}
{% endif %}
```

### Form Layouts
```jinja2
<form class="space-y-4">
  {% include "components/form_input.html" with context %}
  {# field_name="name", label="Full Name", required=true #}

  {% include "components/form_select.html" with context %}
  {# field_name="client_id", label="Client", options=clients, required=true #}

  <div class="flex gap-2 justify-end pt-4">
    {% include "components/button.html" with context %}
    {# button_text="Cancel", button_variant="outline" #}
    {% include "components/button.html" with context %}
    {# button_text="Save", button_variant="primary", button_type="submit" #}
  </div>
</form>
```

---

## 🎯 Next Steps (Phase 2)

Phase 2 will include:
- **Enhanced Tables** - Sorting, filtering, pagination
- **Dialogs** - Modal overlays with better styling
- **Progress Bars** - Loading and completion indicators
- **Alerts** - Info, warning, error messages
- **Tooltips** - Hover information
- **Spinners** - Loading animations

---

## 📊 Files Created/Modified

### Created
- `templates/components/button.html`
- `templates/components/badge.html`
- `templates/components/card.html`
- `templates/components/card_header.html`
- `templates/components/card_content.html`
- `templates/components/card_footer.html`
- `templates/components/form_label.html`
- `templates/components_showcase.html`
- `app/routes/admin.py` (added /admin/components route)
- `SHADCN_PHASE1_GUIDE.md` (this file)

### Modified
- `templates/components/form_input.html` - Enhanced with shadcn styling
- `templates/components/form_select.html` - Enhanced with shadcn styling

---

## 💡 Tips

1. **Consistent Spacing** - Use `space-y-4` for form groups
2. **Button Groups** - Wrap buttons in a flex container with `gap-2`
3. **Form Layout** - Use `space-y-4` between form fields
4. **Card Sections** - Always use header, content, footer structure for consistency
5. **Dark Mode** - Test components in both light and dark modes

---

## 🔗 References

- Shadcn UI: https://ui.shadcn.com/
- Tailwind CSS: https://tailwindcss.com/
- Themis Project: /home/lasitha/Documents/Projects/Themis-Revamp
