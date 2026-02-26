# Phase 2: Advanced Shadcn UI Components for Themis-Revamp

## Overview
Phase 2 implements advanced shadcn-inspired components for professional data display, user feedback, and interaction patterns. These components extend Phase 1 with tables, dialogs, progress tracking, alerts, tooltips, and loading states.

## 🎯 Phase 2 Components

### 1. **Table Components** (`templates/components/table*.html`)
Professional data table with responsive design and interactive rows.

**Components:**
- `table.html` - Main wrapper with borders and responsive scroll
- `table_head.html` - Header section with background styling
- `table_header_cell.html` - Individual header cells with uppercase labels
- `table_body.html` - Body wrapper with row dividers
- `table_row.html` - Individual rows with hover effects
- `table_cell.html` - Data cells

**Features:**
- Responsive overflow with horizontal scroll
- Row hover states with smooth transitions
- Header styling with gray background
- Border and divider separation
- Dark mode support
- Selected row highlighting

**Usage:**
```jinja2
<div class="overflow-x-auto rounded-md border">
  <table class="w-full border-collapse text-sm">
    <thead class="bg-slate-50 dark:bg-slate-950">
      <tr>
        <th class="px-4 py-3 text-left font-semibold">Column 1</th>
        <th class="px-4 py-3 text-left font-semibold">Column 2</th>
      </tr>
    </thead>
    <tbody class="divide-y">
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-900/50">
        <td class="px-4 py-3">Data 1</td>
        <td class="px-4 py-3">Data 2</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### 2. **Progress Bar** (`templates/components/progress.html`)
Smooth gradient progress indicator with optional labels.

**Features:**
- Gradient fill (primary → blue)
- Optional label and value display
- Smooth transitions
- Custom height (h-3 default)
- Dark mode support

**Parameters:**
- `progress_value` - Current value (0-100 range)
- `progress_max` - Maximum value (default: 100)
- `progress_label_text` - Left-side label text
- `progress_label` - Right-side value display (e.g., "65%")
- `progress_class` - Additional Tailwind classes

**Usage:**
```jinja2
{% include "components/progress.html" with context %}
{# progress_value=65, progress_max=100, progress_label="65 of 100" #}
```

**Examples:**
```html
<!-- Simple progress -->
<div class="w-full h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
  <div class="h-full bg-gradient-to-r from-primary to-blue-500" style="width: 65%"></div>
</div>

<!-- With label -->
<div class="flex items-center justify-between mb-2">
  <p class="text-sm font-medium">Progress</p>
  <p class="text-sm font-semibold">65%</p>
</div>
<div class="w-full h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
  <div class="h-full bg-gradient-to-r from-primary to-blue-500" style="width: 65%"></div>
</div>
```

---

### 3. **Alert** (`templates/components/alert.html`)
Semantic alerts with icon, title, message, and dismissible option.

**Variants:**
- `info` (default) - Blue background
- `success` - Green background
- `warning` - Amber background
- `error` - Red background

**Features:**
- Icon matching alert type
- Title and message support
- Dismissible with fade animation
- Alpine.js integration
- Responsive layout
- Full dark mode support

**Parameters:**
- `type` - One of: info, success, warning, error
- `title` - Alert title
- `message` - Alert message
- `dismissible` - Set to true for close button
- `x-data` - Alpine.js state

**Usage:**
```jinja2
{% include "components/alert.html" with context %}
{# type="success", title="Success!", message="Your changes saved." #}

{% include "components/alert.html" with context %}
{# type="error", title="Error", message="Something went wrong.", dismissible=true #}
```

**With Alpine.js:**
```html
<div x-data="{ open: true }" x-show="open" x-transition>
  <!-- Alert content -->
  <button @click="open = false">Close</button>
</div>
```

---

### 4. **Spinner/Loading** (`templates/components/spinner.html`)
Animated loading spinner with customizable size and label.

**Features:**
- Smooth CSS animation
- Multiple size variants
- Optional label
- Color variants (primary, secondary, success, destructive)
- Dark mode support
- Flexbox centering

**Parameters:**
- `spinner_size` - One of: sm (w-4), md (w-8 default), lg (w-12)
- `spinner_label` - Optional loading text
- `spinner_variant` - Color variant: primary, secondary, success, destructive

**Usage:**
```jinja2
{% include "components/spinner.html" with context %}
{# spinner_size="md", spinner_label="Loading..." #}
```

**Styles:**
```html
<div class="animate-spin rounded-full border-4 border-slate-200 dark:border-slate-700 border-t-primary w-8 h-8"></div>
```

---

### 5. **Tooltip** (`templates/components/tooltip.html`)
Hover-triggered tooltip with smart positioning.

**Features:**
- Alpine.js x-data integration
- 4 position variants (top, right, bottom, left)
- Arrow indicator
- Dark background
- Smooth fade transition
- Keyboard support (focus/blur)

**Parameters:**
- `tooltip_text` - Tooltip content
- `tooltip_trigger` - Element that triggers tooltip
- `tooltip_position` - One of: top (default), right, bottom, left

**Usage:**
```html
<div x-data="{ showTooltip: false }" @mouseenter="showTooltip = true" @mouseleave="showTooltip = false">
  <button>Hover me</button>
  <div x-show="showTooltip" class="...tooltip styles...">
    Helpful text
  </div>
</div>
```

**Positioning Examples:**
```html
<!-- Top (default) -->
<div class="absolute bottom-full mb-2 left-1/2 -translate-x-1/2">

<!-- Right -->
<div class="absolute left-full ml-2 top-1/2 -translate-y-1/2">

<!-- Bottom -->
<div class="absolute top-full mt-2 left-1/2 -translate-x-1/2">

<!-- Left -->
<div class="absolute right-full mr-2 top-1/2 -translate-y-1/2">
```

---

### 6. **Dialog/Modal** (`templates/components/dialog.html`)
Full-screen modal overlay with glassmorphism and smooth animations.

**Features:**
- Glassmorphism backdrop (backdrop-blur-sm)
- Gradient top accent line
- Close button in top-right
- Smooth enter/leave animations
- Keyboard escape to close
- Click-outside to close
- Header with title and description
- Footer with action buttons

**Parameters:**
- `dialog_open` - Boolean state (Alpine.js)
- `dialog_title` - Modal title
- `dialog_description` - Subtitle text
- `dialog_content` - Main content
- `dialog_footer` - Button footer (optional)

**Usage:**
```html
<div x-data="{ dialogOpen: false }">
  <button @click="dialogOpen = true">Open Dialog</button>

  <div x-show="dialogOpen" @keydown.escape.window="dialogOpen = false"
       class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
    <!-- Modal content -->
  </div>
</div>
```

**Structure:**
```html
<div class="bg-white dark:bg-slate-900 rounded-lg shadow-2xl max-w-lg">
  <!-- Accent bar -->
  <div class="h-1 bg-gradient-to-r from-primary to-blue-400"></div>

  <!-- Close button -->
  <button @click="dialogOpen = false" class="absolute top-4 right-4">×</button>

  <!-- Header -->
  <div class="border-b px-6 py-4">
    <h2>Title</h2>
    <p>Description</p>
  </div>

  <!-- Content -->
  <div class="px-6 py-4">Content</div>

  <!-- Footer -->
  <div class="border-t px-6 py-4 flex gap-2 justify-end">Buttons</div>
</div>
```

---

## 🎨 Design System Integration

### Color Palette
All Phase 2 components use:
- **Primary Color:** #137fec (Blue)
- **Gray Scale:** slate-* series for backgrounds and text
- **Semantic Colors:**
  - Success: emerald-* (green)
  - Warning: amber-* (yellow/orange)
  - Destructive: red-* (error)
  - Info: blue-* (default)

### Typography
- Headers: font-semibold, text-sm/text-lg
- Body: text-sm, text-slate-600/dark:text-slate-400
- Labels: font-medium, text-xs/text-sm

### Spacing
- Padding: px-4 py-3 (tables), px-6 py-4 (dialogs/cards)
- Gaps: gap-2 (buttons), gap-3 (alert content), gap-4 (dialog sections)
- Margins: mt-1, mt-2, mb-2, mb-4

### Transitions
- `transition-all duration-500` - Progress bars
- `transition-colors` - Button and table rows
- `transition-opacity` - Tooltips and alerts
- `transition ease-out duration-300` - Dialog enter
- `transition ease-in duration-200` - Dialog exit

---

## 📱 Responsive Design

### Tables
```html
<div class="w-full overflow-x-auto rounded-md border">
  <!-- Scrolls horizontally on small screens -->
</div>
```

### Dialogs
```html
<div class="w-full max-w-lg mx-auto">
  <!-- Always centered, max 512px width -->
</div>
```

### Progress
```html
<div class="w-full h-3">
  <!-- Full width, adapts to container -->
</div>
```

---

## 🔧 Integration Examples

### Dashboard with Progress
```jinja2
<div class="space-y-4">
  <div class="flex justify-between items-center">
    <h3 class="font-semibold">Assessment Progress</h3>
    <p class="text-sm text-slate-500">{{ completed }} of {{ total }}</p>
  </div>

  {% include "components/progress.html" with context %}
  {# progress_value=completed, progress_max=total #}
</div>
```

### Data Table with Actions
```jinja2
<table class="w-full">
  <thead class="bg-slate-50 dark:bg-slate-950">
    <tr>
      <th class="px-4 py-3 text-left font-semibold">Name</th>
      <th class="px-4 py-3 text-left font-semibold">Status</th>
      <th class="px-4 py-3 text-left font-semibold">Actions</th>
    </tr>
  </thead>
  <tbody class="divide-y">
    {% for item in items %}
    <tr class="hover:bg-slate-50 dark:hover:bg-slate-900/50">
      <td class="px-4 py-3">{{ item.name }}</td>
      <td class="px-4 py-3">
        {% include "components/badge.html" with context %}
        {# badge_text=item.status #}
      </td>
      <td class="px-4 py-3">
        <button class="text-primary hover:underline text-sm">Edit</button>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

### Form with Validation Feedback
```jinja2
<form class="space-y-4">
  {% include "components/form_input.html" with context %}
  {# field_name="email", label="Email", required=true #}

  <div class="pt-4">
    {% include "components/alert.html" with context %}
    {# type="error", title="Validation Error", message="Please check the fields above." #}
  </div>

  <div class="flex gap-2 justify-end">
    {% include "components/button.html" with context %}
    {# button_text="Cancel", button_variant="outline" #}
    {% include "components/button.html" with context %}
    {# button_text="Save", button_variant="primary" #}
  </div>
</form>
```

### Async Operation Feedback
```html
<div x-data="{ loading: false, success: false }">
  <!-- Loading state -->
  <div x-show="loading">
    {% include "components/spinner.html" with context %}
    {# spinner_label="Processing..." #}
  </div>

  <!-- Success feedback -->
  <div x-show="success" x-transition>
    {% include "components/alert.html" with context %}
    {# type="success", title="Complete", message="Operation successful!" #}
  </div>

  <!-- Action button -->
  <button @click="async () => { loading = true; await doAsync(); loading = false; success = true; }">
    Start
  </button>
</div>
```

---

## 📊 Component Showcase

View all Phase 2 components in action:
- **Route:** `/admin/components/phase2`
- **File:** `templates/components_showcase_phase2.html`

This page demonstrates:
- Table with sample data
- Progress bars at different completion levels
- All alert types and states
- Spinner size variants
- Tooltip positioning
- Modal dialog interaction

---

## 📋 Files Created/Modified

### Created
- `templates/components/table.html`
- `templates/components/table_head.html`
- `templates/components/table_header_cell.html`
- `templates/components/table_body.html`
- `templates/components/table_row.html`
- `templates/components/table_cell.html`
- `templates/components/dialog.html`
- `templates/components/progress.html`
- `templates/components/tooltip.html`
- `templates/components/spinner.html`
- `templates/components_showcase_phase2.html`
- `SHADCN_PHASE2_GUIDE.md` (this file)

### Modified
- `templates/components/alert.html` - Redesigned with shadcn styling
- `app/routes/admin.py` - Added `/admin/components/phase2` route

---

## 🚀 Next Steps

### Phase 3 (Future)
- **Data Table** - Sorting, filtering, pagination
- **Dropdown Menu** - Keyboard navigation, search
- **Popover** - Advanced tooltips with interactive content
- **Checkbox/Radio** - Enhanced form controls
- **Stepper** - Multi-step forms and workflows

### Performance Optimization
- Consider lazy-loading for large tables
- Virtualize long lists with Alpine.js
- Implement debouncing for filter/search inputs

### Accessibility
- Add ARIA labels to all components
- Test keyboard navigation thoroughly
- Ensure color contrast ratios meet WCAG standards
- Add focus visible indicators

---

## 💡 Best Practices

1. **Table Usage**
   - Keep header text concise (use abbreviations if needed)
   - Align numerical data to the right
   - Keep number of columns to 5-6 max on mobile
   - Use row actions sparingly

2. **Progress Bars**
   - Always show percentage with label
   - Use consistent width (usually full width)
   - Update in real-time for async operations

3. **Alerts**
   - Use appropriate type for semantic meaning
   - Keep messages concise and actionable
   - Dismiss automatically after 5-10 seconds for success
   - Keep error alerts until user acknowledges

4. **Dialogs**
   - Confirm before destructive actions
   - Keep content focused and modal (no sidebars)
   - Always provide escape/cancel option
   - Center important actions (Save, Confirm)

5. **Tooltips**
   - Use for supplementary information only
   - Keep text to one sentence max
   - Position above interactive element when possible
   - Use dark background for contrast

---

## 🔗 References

- Shadcn UI: https://ui.shadcn.com/
- Tailwind CSS: https://tailwindcss.com/
- Alpine.js: https://alpinejs.dev/
- Themis Project: /home/lasitha/Documents/Projects/Themis-Revamp
