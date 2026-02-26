# Phase 3: Advanced Form Controls & Workflow Components for Themis-Revamp

## Overview
Phase 3 implements sophisticated form controls and multi-step workflow components. These include custom checkboxes/radios, tab navigation, dropdown menus, steppers, popovers, and advanced data tables with sorting/filtering capabilities.

## 🎯 Phase 3 Components

### 1. **Checkbox** (`templates/components/checkbox.html`)
Custom styled checkbox with enhanced accessibility and label support.

**Features:**
- Accent color (primary blue)
- Label integration
- Help text support
- Disabled state
- Smooth focus rings
- Dark mode support

**Parameters:**
- `checkbox_id` - Unique identifier
- `checkbox_name` - Form field name
- `checkbox_label` - Label text
- `checkbox_value` - Form value
- `checkbox_checked` - Pre-checked state
- `checkbox_disabled` - Disabled state
- `checkbox_help_text` - Helper text below

**Usage:**
```jinja2
<div>
  <input type="checkbox" id="agree" name="agree_terms" value="yes"
    class="w-5 h-5 rounded border border-slate-300 accent-primary cursor-pointer"
  />
  <label for="agree" class="ml-2 text-sm font-medium">I agree to the terms</label>
</div>
```

**Styling:**
```css
/* Checked state */
checked:bg-primary checked:border-primary

/* Focus visible */
focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2

/* Disabled */
disabled:cursor-not-allowed disabled:opacity-50
```

---

### 2. **Radio Button** (`templates/components/radio.html`)
Custom styled radio button with group support.

**Features:**
- Accent primary color
- Grouped radio options
- Label support
- Disabled state
- Help text
- Smooth transitions

**Parameters:**
- `radio_id` - Unique identifier
- `radio_name` - Group name (same for all in group)
- `radio_label` - Label text
- `radio_value` - Form value
- `radio_checked` - Selected state
- `radio_disabled` - Disabled state
- `radio_help_text` - Helper text

**Usage:**
```html
<!-- Radio Group -->
<fieldset class="space-y-3">
  <legend class="font-semibold text-sm">Select Option</legend>

  <div>
    <input type="radio" id="opt1" name="option" value="1" checked
      class="w-5 h-5 rounded-full border border-slate-300 accent-primary"
    />
    <label for="opt1" class="ml-2">Option 1</label>
  </div>

  <div>
    <input type="radio" id="opt2" name="option" value="2"
      class="w-5 h-5 rounded-full border border-slate-300 accent-primary"
    />
    <label for="opt2" class="ml-2">Option 2</label>
  </div>
</fieldset>
```

---

### 3. **Tabs** (`templates/components/tabs.html`)
Tab navigation with Alpine.js state management.

**Features:**
- Active state styling with underline
- Smooth transitions
- Keyboard focus support
- Responsive overflow
- Dark mode support

**Parameters:**
- `tabs_items` - Array of {id, label} objects
- `activeTab` - Current active tab (Alpine.js x-data)

**Usage:**
```html
<div x-data="{ activeTab: 'tab1' }">
  <!-- Tab Navigation -->
  <div class="border-b border-slate-200 dark:border-slate-800">
    <div class="flex gap-0">
      <button
        @click="activeTab = 'tab1'"
        :class="{'border-b-2 border-primary text-primary': activeTab === 'tab1'}"
        class="px-4 py-3 font-medium text-sm">
        Tab 1
      </button>
      <button
        @click="activeTab = 'tab2'"
        :class="{'border-b-2 border-primary text-primary': activeTab === 'tab2'}"
        class="px-4 py-3 font-medium text-sm">
        Tab 2
      </button>
    </div>
  </div>

  <!-- Tab Content -->
  <div x-show="activeTab === 'tab1'" class="pt-4">Content 1</div>
  <div x-show="activeTab === 'tab2'" class="pt-4">Content 2</div>
</div>
```

**Styling:**
```css
/* Active tab */
border-b-2 border-primary text-primary

/* Inactive tab */
border-b-2 border-transparent text-slate-600

/* Hover */
hover:text-slate-900 dark:hover:text-slate-300
```

---

### 4. **Dropdown Menu** (`templates/components/dropdown.html`)
Click-triggered dropdown menu with click-outside support.

**Features:**
- Alpine.js integration
- Smooth transitions (scale + fade)
- Click-outside to close
- Divider support
- Destructive actions
- Disabled items
- Icon support

**Parameters:**
- `dropdown_trigger_text` - Button label
- `dropdown_items` - Array of menu items:
  - `label` - Item text
  - `value` - Item value
  - `divider` - True to show separator
  - `destructive` - Red text for delete actions
  - `disabled` - Grayed out item
  - `icon` - Optional emoji/icon

**Usage:**
```html
<div x-data="{ open: false }" @click.outside="open = false" class="relative">
  <button @click="open = !open" class="...">
    Actions
    <svg class="w-4 h-4"><!-- chevron --></svg>
  </button>

  <div x-show="open" x-transition class="absolute mt-2 w-48 z-50 bg-white rounded-lg shadow-lg">
    <div class="py-1">
      <button @click="open = false" class="w-full text-left px-4 py-2 hover:bg-slate-100">
        Edit
      </button>
      <button @click="open = false" class="w-full text-left px-4 py-2 hover:bg-slate-100">
        Copy
      </button>
      <div class="border-t my-1"></div>
      <button @click="open = false" class="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50">
        Delete
      </button>
    </div>
  </div>
</div>
```

---

### 5. **Stepper** (`templates/components/stepper.html`)
Multi-step form progress indicator with visual feedback.

**Features:**
- Step circles with numbers
- Check marks for completed steps
- Connecting lines with gradient
- Active step highlighting
- Label display
- Responsive layout

**Parameters:**
- `stepper_steps` - Array of step objects:
  - `number` - Step number (1, 2, 3...)
  - `label` - Step label text
  - `completed` - Boolean (shows checkmark)
  - `active` - Current step (highlighted)

**Usage:**
```html
<div class="space-y-4">
  <!-- Progress -->
  <div class="flex items-center gap-2">
    <!-- Step 1 -->
    <div class="w-10 h-10 rounded-full bg-emerald-600 text-white flex items-center justify-center">
      ✓
    </div>
    <div class="flex-1 h-1 bg-primary rounded-full"></div>

    <!-- Step 2 -->
    <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center ring-4 ring-primary/20">
      2
    </div>
    <div class="flex-1 h-1 bg-slate-300 rounded-full"></div>

    <!-- Step 3 -->
    <div class="w-10 h-10 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center">
      3
    </div>
  </div>

  <!-- Labels -->
  <div class="flex gap-2 justify-between">
    <div class="text-xs font-medium text-slate-600">Step 1</div>
    <div class="text-xs font-medium text-primary">Step 2</div>
    <div class="text-xs font-medium text-slate-600">Step 3</div>
  </div>
</div>
```

**Colors:**
- Completed: emerald-600 with checkmark
- Active: primary with ring glow
- Inactive: slate-200

---

### 6. **Popover** (`templates/components/popover.html`)
Click-triggered popover with interactive content and footer actions.

**Features:**
- Alpine.js state management
- Smooth scale + fade transitions
- Arrow indicator
- Click-outside to close
- Header, content, and footer sections
- Dark mode support

**Parameters:**
- `popover_trigger_text` - Button label
- `popover_title` - Popover header
- `popover_content` - Main content text
- `popover_footer` - Action buttons

**Usage:**
```html
<div x-data="{ open: false }" @click.outside="open = false">
  <button @click="open = !open" class="...">
    Settings
  </button>

  <div x-show="open" x-transition class="absolute mt-2 w-80 z-50 bg-white rounded-lg shadow-lg p-4">
    <!-- Arrow -->
    <div class="absolute -top-1 left-6 w-2 h-2 bg-white border-t border-l rotate-45"></div>

    <!-- Content -->
    <h4 class="font-semibold text-sm">Title</h4>
    <p class="text-sm text-slate-600 mt-1">Description text here.</p>

    <!-- Footer -->
    <div class="flex gap-2 pt-2 border-t mt-3">
      <button @click="open = false" class="...">Cancel</button>
      <button class="...">Save</button>
    </div>
  </div>
</div>
```

---

### 7. **Advanced Data Table** (`templates/components/data_table_advanced.html`)
Feature-rich data table with search, sort, and filtering.

**Features:**
- Search/filter input
- Sortable columns (with direction indicator)
- View toggle (table/list)
- Responsive horizontal scroll
- Results count display
- Pagination controls
- Hover effects on rows

**Parameters:**
- `table_columns` - Column definitions with sortable flag
- `table_rows` - Data rows
- `table_searchable` - Enable search input
- `table_view_toggle` - Show table/list view switcher
- `table_show_footer` - Show pagination footer

**Usage:**
```html
<div class="space-y-4">
  <!-- Search Bar -->
  <div class="flex gap-2">
    <div class="flex-1 relative">
      <input
        type="text"
        placeholder="Search..."
        x-model="searchTerm"
        class="w-full px-4 py-2 text-sm rounded-md border border-slate-300"
      />
      <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4"><!-- search icon --></svg>
    </div>
  </div>

  <!-- Table -->
  <div class="overflow-x-auto rounded-lg border">
    <table class="w-full">
      <thead class="bg-slate-50">
        <tr>
          <th class="px-4 py-3 text-left font-semibold text-xs uppercase">
            <button @click="sortColumn('name')" class="flex items-center gap-2">
              Name
              <svg class="w-4 h-4"><!-- sort indicator --></svg>
            </button>
          </th>
          <th class="px-4 py-3 text-left font-semibold text-xs uppercase">Status</th>
        </tr>
      </thead>
      <tbody class="divide-y">
        <template x-for="row in filteredRows">
          <tr class="hover:bg-slate-50">
            <td class="px-4 py-3 text-sm" x-text="row.name"></td>
            <td class="px-4 py-3 text-sm" x-text="row.status"></td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>

  <!-- Footer -->
  <div class="flex items-center justify-between text-sm text-slate-600">
    <p>Showing 1 to 10 of 100 results</p>
    <div class="flex gap-2">
      <button class="px-3 py-1 border rounded hover:bg-slate-100">Previous</button>
      <button class="px-3 py-1 border rounded hover:bg-slate-100">Next</button>
    </div>
  </div>
</div>
```

---

## 🎨 Design Patterns

### Form Control Spacing
```html
<div class="space-y-3">
  <!-- Individual controls with consistent gaps -->
</div>
```

### Fieldset Grouping
```html
<fieldset class="space-y-2">
  <legend class="font-semibold text-sm">Group Title</legend>
  <!-- Radio options or checkboxes -->
</fieldset>
```

### Tab Content Switching
```html
<div x-data="{ active: 'tab1' }">
  <!-- Nav -->
  <!-- Content with x-show="active === 'tab1'" -->
</div>
```

### Dropdown Positioning
```css
/* Top-left alignment -->
position: absolute;
top: 100%;
left: 0;
margin-top: 0.5rem;
```

### Multi-Step Indicator
```html
<!-- Progress line: completed > active > pending -->
<!-- Check marks for completed steps -->
<!-- Ring glow for active step -->
```

---

## 🔧 Integration Examples

### Multi-Step Form with Stepper
```html
<div x-data="{ currentStep: 1 }">
  <!-- Stepper -->
  <!-- Step 1: Personal Info -->
  <div x-show="currentStep === 1">
    {% include "components/form_input.html" %}
  </div>

  <!-- Step 2: Contact -->
  <div x-show="currentStep === 2">
    {% include "components/form_input.html" %}
  </div>

  <!-- Navigation -->
  <div class="flex gap-2">
    <button @click="currentStep--">Previous</button>
    <button @click="currentStep++">Next</button>
  </div>
</div>
```

### Tabbed Settings
```html
<div x-data="{ tab: 'general' }">
  <!-- Tab Navigation -->
  <div class="border-b">
    <button @click="tab = 'general'" :class="{'border-b-2 border-primary': tab === 'general'}">
      General
    </button>
    <button @click="tab = 'privacy'" :class="{'border-b-2 border-primary': tab === 'privacy'}">
      Privacy
    </button>
  </div>

  <!-- Tab Content -->
  <div x-show="tab === 'general'" class="space-y-4">
    <!-- Settings -->
  </div>
  <div x-show="tab === 'privacy'" class="space-y-4">
    <!-- Privacy controls -->
  </div>
</div>
```

### Data Table with Actions
```html
<div x-data="{ search: '', sortBy: 'name', sortDir: 'asc' }">
  <input x-model="search" placeholder="Search..." />

  <table>
    <thead>
      <th @click="sortBy = 'name'; sortDir = sortDir === 'asc' ? 'desc' : 'asc'">
        Name
      </th>
    </thead>
    <tbody>
      <template x-for="row in data.filter(...)">
        <!-- Row with edit/delete dropdown -->
      </template>
    </tbody>
  </table>
</div>
```

---

## 📊 Component Showcase

View all Phase 3 components in action:
- **Route:** `/admin/components/phase3`
- **File:** `templates/components_showcase_phase3.html`

This page demonstrates:
- Checkbox variations
- Radio button groups
- Tab navigation
- Dropdown menus
- Stepper progress
- Popover interaction
- Data table features

---

## 📋 Files Created/Modified

### Created
- `templates/components/checkbox.html`
- `templates/components/radio.html`
- `templates/components/tabs.html`
- `templates/components/dropdown.html`
- `templates/components/stepper.html`
- `templates/components/popover.html`
- `templates/components/data_table_advanced.html`
- `templates/components_showcase_phase3.html`
- `SHADCN_PHASE3_GUIDE.md` (this file)

### Modified
- `app/routes/admin.py` - Added `/admin/components/phase3` route

---

## ✅ Accessibility Features

### Form Controls
- ✅ Proper label associations
- ✅ Focus visible states
- ✅ ARIA labels for icons
- ✅ Disabled state styling

### Navigation
- ✅ Keyboard accessible tabs
- ✅ Tab focus indicators
- ✅ Arrow key support (future enhancement)

### Tables
- ✅ Semantic `<table>` structure
- ✅ Column headers with `<th>`
- ✅ Sortable column indicators
- ✅ High contrast badges

---

## 💡 Best Practices

### Checkboxes & Radios
1. Always pair with labels
2. Use fieldset for radio groups
3. Provide help text for clarity
4. Show disabled state clearly
5. Use `accent-primary` for consistency

### Tabs
1. Show 3-5 tabs max (use dropdown for more)
2. Preserve tab state in URL if possible
3. Ensure content is independent per tab
4. Highlight current tab clearly
5. Provide keyboard navigation

### Dropdowns
1. Keep menu items to 10 or fewer
2. Group related items with dividers
3. Highlight destructive actions in red
4. Close on selection (unless multi-select)
5. Support click-outside to close

### Data Tables
1. Make columns sortable when data-heavy
2. Provide search for 20+ rows
3. Show result count and pagination
4. Use hover states for row selection
5. Keep column count reasonable on mobile

---

## 🎯 Next Phases (Future)

### Phase 4 (Proposed)
- Autocomplete input with API
- Date picker calendar
- Time picker dropdown
- File upload with progress
- Search with highlights
- Advanced modals (confirmation, alerts)

### Phase 5+
- Combobox (searchable select)
- Slider/Range input
- Color picker
- Multi-select dropdown
- Rich text editor
- Chart components

---

## 🚀 Performance Optimization

### Alpine.js
```html
<!-- Lazy load data -->
<div x-init="loadData()"></div>

<!-- Debounce search -->
@input.debounce.400ms="search()"

<!-- Lazy evaluation -->
:disabled="row.status === 'locked'"
```

### DOM Optimization
- Use `x-cloak` to prevent flashing
- Template for list rendering
- Limit DOM updates with conditions
- Use key binding for list uniqueness

---

## 📖 Full Documentation

For detailed usage and advanced patterns:
- **Phase 1:** See `SHADCN_PHASE1_GUIDE.md`
- **Phase 2:** See `SHADCN_PHASE2_GUIDE.md`
- **Phase 3:** See this file
- **All Components:** See `SHADCN_COMPONENTS_SUMMARY.md`

---

**Last Updated:** 2026-02-26
**Components:** 7 (Checkbox, Radio, Tabs, Dropdown, Stepper, Popover, Data Table)
**Documentation:** 400+ lines
**Code Examples:** 20+
