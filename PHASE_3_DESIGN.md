# Phase 3: Advanced Components & Polish

Professional advanced components with real-world functionality.

---

## What's New in Phase 3

### ✅ Pagination Component
Professional pagination for data browsing:

**Features**:
- Previous/Next buttons with chevron icons
- Page number buttons (dynamic range)
- Current page highlighting (primary color)
- Result info ("Showing 1 to 10 of 42")
- Disabled state for boundary pages
- Hover effects on all buttons

**Usage**:
```html
{% include "components/pagination.html" with
    current_page=current_page
    total_pages=total_pages
    start=offset + 1
    end=min(offset + limit, total)
    total=total
    has_prev=current_page > 1
    has_next=current_page < total_pages
    prev_url=prev_page_url
    next_url=next_page_url %}
```

### ✅ Loading Skeletons
Placeholder components while loading data:

**Types**:
- **Table** - Header + 5 rows with columns
- **Card** - Title + content + buttons
- **Form** - Input fields with labels
- **List** - Avatar + text items

**Features**:
- Animated pulse effect
- Dark mode colors
- Matches layout of actual content
- Smooth fade-in

**Usage**:
```html
{% include "components/skeleton.html" with type="table" %}
{% include "components/skeleton.html" with type="card" %}
{% include "components/skeleton.html" with type="form" %}
{% include "components/skeleton.html" with type="list" %}
```

### ✅ Toast Notifications
Non-blocking notifications system:

**Types**:
- **Info** (blue) - General information
- **Success** (emerald) - Confirmations
- **Warning** (amber) - Cautions
- **Error** (red) - Error messages

**Features**:
- Auto-dismiss after 5 seconds
- Manual close button
- Slide-in animation (right)
- Stacks vertically
- Dark mode support

**JavaScript API**:
```javascript
showToast('Project created successfully', 'success');
showToast('An error occurred', 'error', 5000);
showToast('Action completed', 'info', 3000);
showToast('Warning: unsaved changes', 'warning');
```

### ✅ Form Validation Component
Advanced form inputs with validation states:

**Features**:
- Error state (red border + icon)
- Success state (green icon)
- Error message display
- Help text support
- Validation on input event
- Focus ring styling

**States**:
- **Default** - Blue focus ring
- **Error** - Red border + error icon + message
- **Success** - Green checkmark icon
- **Focused** - Primary color ring

**Usage**:
```html
{% include "components/form_input_validated.html" with
    field_name="email"
    label="Email Address"
    input_type="email"
    placeholder="you@example.com"
    required=true
    error="Invalid email format"
    help_text="We'll never share your email" %}
```

### ✅ Advanced Data Table
Professional data table with sorting & filtering:

**Features**:
- Search/filter input
- View toggle (table/list)
- Sortable columns with indicators
- Pagination with page numbers
- Result count display
- Empty state with icon
- HTMX integration for live updates

**Column Options**:
```python
columns = [
    {'key': 'name', 'label': 'Name', 'sortable': True},
    {'key': 'status', 'label': 'Status', 'sortable': False},
    {'key': 'created', 'label': 'Created', 'sortable': True},
]
```

**Usage**:
```html
{% include "components/data_table.html" with
    title="Projects"
    columns=columns
    items=projects
    current_sort=sort_by
    sort_order=order
    current_page=page
    total=total_count
    limit=per_page %}
```

---

## Component Code Examples

### Pagination
```html
<div class="flex items-center justify-between px-6 py-4 border-t border-slate-200">
    <div class="text-sm text-slate-600">
        Showing <span class="font-semibold">{{ start }}</span> to
        <span class="font-semibold">{{ end }}</span> of
        <span class="font-semibold">{{ total }}</span>
    </div>
    <div class="flex items-center gap-2">
        <!-- Previous Button -->
        <a href="{{ prev_url }}" class="p-2 rounded-lg hover:text-primary
            {% if not has_prev %}opacity-50 pointer-events-none{% endif %}">
            <span class="material-symbols-outlined">chevron_left</span>
        </a>
        <!-- Page Numbers -->
        <!-- Next Button -->
        <a href="{{ next_url }}" class="p-2 rounded-lg hover:text-primary
            {% if not has_next %}opacity-50 pointer-events-none{% endif %}">
            <span class="material-symbols-outlined">chevron_right</span>
        </a>
    </div>
</div>
```

### Loading Skeleton
```html
<div class="space-y-3">
    {% for i in range(4) %}
    <div class="flex items-center gap-3 p-4 bg-slate-50 rounded-lg">
        <div class="w-10 h-10 rounded-full bg-slate-200 animate-pulse"></div>
        <div class="flex-1 space-y-2">
            <div class="h-4 bg-slate-200 rounded w-1/3 animate-pulse"></div>
            <div class="h-3 bg-slate-200 rounded w-2/3 animate-pulse"></div>
        </div>
    </div>
    {% endfor %}
</div>
```

### Toast Notification
```javascript
// Call from any template or JavaScript
showToast('Project saved successfully', 'success');

// Custom duration
showToast('Processing...', 'info', 10000);

// Error handling
showToast('Failed to save project', 'error');
```

### Validated Form Input
```html
<div class="form-group">
    <label class="block text-sm font-semibold mb-2">Email</label>
    <div class="relative">
        <input type="email"
            class="w-full px-4 py-2.5 border-2 border-slate-200
            focus:border-primary focus:ring-2 focus:ring-primary/50
            rounded-lg" />
        {% if error %}
        <span class="absolute right-3 top-1/2 -translate-y-1/2 text-red-500">
            <span class="material-symbols-outlined">error</span>
        </span>
        {% endif %}
    </div>
    {% if error %}
    <p class="mt-2 text-sm text-red-600">{{ error }}</p>
    {% endif %}
</div>
```

### Data Table
```html
<div class="rounded-xl bg-white shadow-sm border overflow-hidden">
    <!-- Search & View Toggle -->
    <div class="p-4 border-b flex items-center justify-between">
        <input type="text" placeholder="Search..." class="flex-1 px-3 py-2 rounded-lg border" />
        <div class="flex gap-1">
            <button class="p-2 rounded-lg hover:bg-slate-100">
                <span class="material-symbols-outlined">table_chart</span>
            </button>
            <button class="p-2 rounded-lg hover:bg-slate-100">
                <span class="material-symbols-outlined">list</span>
            </button>
        </div>
    </div>

    <!-- Table -->
    <table class="w-full">
        <thead>
            <tr class="bg-slate-50 border-b">
                <th class="px-6 py-4 text-left font-bold uppercase text-xs">
                    <button class="flex items-center gap-2">
                        Name
                        <span class="material-symbols-outlined text-[14px]">unfold_more</span>
                    </button>
                </th>
            </tr>
        </thead>
        <tbody>
            <!-- Rows -->
        </tbody>
    </table>

    <!-- Pagination -->
    <div class="px-6 py-4 border-t bg-slate-50 flex justify-between">
        <p class="text-sm text-slate-600">Showing 1 to 10 of 42</p>
        <div class="flex gap-2">
            <!-- Page buttons -->
        </div>
    </div>
</div>
```

---

## File Changes in Phase 3

### New Components
```
templates/components/
├── pagination.html                    [NEW] Table pagination
├── skeleton.html                      [NEW] Loading placeholders
├── form_input_validated.html         [NEW] Form with validation
└── data_table.html                   [NEW] Advanced data table with sorting
```

### Updated Templates
```
templates/
└── base.html                          [UPDATED] Toast container + JS
```

---

## Dark Mode Support

All Phase 3 components include full dark mode:

**Skeleton Colors**:
```
Light: bg-slate-200
Dark: dark:bg-slate-700
```

**Table Colors**:
```
Header: bg-slate-50 dark:bg-slate-800/50
Body: dark:bg-slate-900
Borders: dark:border-slate-800
Hover: dark:hover:bg-slate-800/50
```

**Form Colors**:
```
Background: bg-slate-50 dark:bg-slate-800
Border: border-slate-200 dark:border-slate-700
Focus Ring: focus:ring-primary/50
Error: border-red-500 dark:border-red-500
```

---

## JavaScript Integration

### Toast System
```javascript
// Global function available in all templates
window.showToast(message, type, duration);

// Types: 'info', 'success', 'warning', 'error'
// Duration: milliseconds (default 5000)

// Examples
showToast('Saved!', 'success');
showToast('Error occurred', 'error');
showToast('Please confirm', 'warning', 10000);
```

### Form Validation
```javascript
// Can be extended for custom validation
function validateField(fieldName, value) {
    // Validate and show error/success state
    if (isValid(value)) {
        showSuccess(fieldName);
    } else {
        showError(fieldName, 'Invalid input');
    }
}
```

---

## Responsive Design

- **Tables**: Horizontal scroll on mobile
- **Forms**: Full width, stacked on mobile
- **Pagination**: Compact on small screens
- **Skeletons**: Adapt to container size
- **Toasts**: Fixed position, adapts width

---

## Animation & Transitions

**Toast Animations**:
- Slide in: 300ms from right
- Slide out: 300ms to right
- Easing: ease-out / ease-in

**Skeleton Animation**:
- Pulse: `animate-pulse` continuous
- Colors shift between shades

**Table Interactions**:
- Row hover: 200ms background change
- Button hover: 200ms color change
- Sort indicator: Color transition

---

## Accessibility

- ✅ Semantic HTML
- ✅ ARIA labels
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ Color + icon combos
- ✅ Sufficient contrast

---

## Performance Notes

- **CSS**: ~70KB (compiled Tailwind)
- **JavaScript**: ~2KB (showToast function)
- **Icons**: CDN-based (no local files)
- **Animations**: GPU-accelerated (transform, opacity)
- **Load Time**: Sub-second with caching

---

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers

---

## Testing Checklist

- [ ] Pagination displays correct info
- [ ] Previous/Next buttons work
- [ ] Page numbers clickable
- [ ] Skeleton animate smoothly
- [ ] Toast appears and auto-dismisses
- [ ] Toast can be manually closed
- [ ] Form shows validation states
- [ ] Data table search works
- [ ] Sort indicators change
- [ ] All in dark mode
- [ ] Mobile responsive

---

## Troubleshooting

**Toast not showing?**
- Check toast-container exists in base.html
- Call `showToast()` with proper type

**Skeleton animation not smooth?**
- Ensure `animate-pulse` is in Tailwind
- Check dark mode colors match content

**Form validation not working?**
- Verify `validateField()` function defined
- Check input has `@input` handler

**Table sorting not working?**
- Ensure HTMX is loaded
- Check sort_url() function exists
- Verify backend returns sorted data

---

## Next Steps (Phase 4+)

- [ ] Advanced form fields (date, time, select)
- [ ] Modal dialog enhancements
- [ ] Breadcrumb with dropdown
- [ ] File upload component
- [ ] Tag input component
- [ ] Date picker integration
- [ ] Rich text editor
- [ ] Code highlighting
- [ ] Chart components
- [ ] Accessibility audit

---

## Questions or Issues?

Refer to:
- `DESIGN_SYSTEM.md` - Component patterns
- `PHASE_2_DESIGN.md` - Form/table basics
- Code comments in component files
