# Themis Design System

A professional, cohesive design system built with **Tailwind CSS v3.4.19** and **CoreUI patterns**.

## Color Palette

### Light Mode
- **Background**: `hsl(0 0% 98.8235%)` (off-white)
- **Foreground**: `hsl(0 0% 9.0196%)` (dark slate)
- **Primary**: `hsl(151.3274 66.8639% 66.8627%)` (teal-green)
- **Primary Dark**: `hsl(153.3333 13.0435% 13.5294%)`
- **Secondary**: `hsl(0 0% 99.2157%)` (almost white)
- **Border**: `hsl(0 0% 87.4510%)` (light gray)
- **Destructive**: `hsl(9.8901 81.9820% 43.5294%)` (red)

### Dark Mode
- **Background**: `hsl(0 0% 7.0588%)` (very dark)
- **Foreground**: `hsl(214.2857 31.8182% 91.3725%)` (off-white)
- **Primary**: `hsl(154.8980 100.0000% 19.2157%)` (dark teal)
- **Primary Light**: `hsl(152.7273 19.2982% 88.8235%)`
- **Border**: `hsl(0 0% 16.0784%)` (dark gray)

## Typography

- **Font Family**: `Outfit, sans-serif`
- **Heading Sizes**:
  - H1: `text-4xl font-bold` (36px)
  - H2: `text-2xl font-bold` (24px)
  - H3: `text-lg font-bold` (18px)
- **Body**: `text-base` (16px)
- **Small**: `text-sm` (14px)
- **Tiny**: `text-xs` (12px)

## Components

### Stat Cards
Professional cards displaying key metrics with:
- Icon background in brand color
- Large number display
- Supporting label
- Subtle hover effect

```html
<div class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-lg transition-shadow">
    <div class="flex items-center justify-between">
        <div>
            <p class="text-slate-500 dark:text-slate-400 text-sm font-semibold uppercase tracking-wide">Label</p>
            <p class="text-3xl font-bold text-slate-900 dark:text-white mt-2">42</p>
        </div>
        <div class="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
            <span class="material-symbols-outlined text-blue-600">icon_name</span>
        </div>
    </div>
</div>
```

### Card with Header Accent
Cards with colored top border for visual hierarchy:
- Gradient accent line at top
- Organized content sections
- Clear action footer
- Smooth hover effects

```html
<div class="group bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-lg transition-all overflow-hidden">
    <div class="h-1 bg-gradient-to-r from-primary via-primary to-blue-400"></div>
    <div class="p-6">
        <!-- Content -->
    </div>
</div>
```

### Badges & Status Indicators
Status badges with contextual colors:

```html
<!-- Success -->
<span class="inline-flex items-center gap-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 px-3 py-1 rounded-full text-xs font-semibold">
    <span class="material-symbols-outlined text-[14px]">check_circle</span>
    Completed
</span>

<!-- Warning -->
<span class="inline-flex items-center gap-1 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 px-3 py-1 rounded-full text-xs font-semibold">
    <span class="material-symbols-outlined text-[14px]">schedule</span>
    In Progress
</span>

<!-- Info -->
<span class="inline-flex items-center gap-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 px-3 py-1 rounded-full text-xs font-semibold">
    <span class="material-symbols-outlined text-[14px]">info</span>
    Pending
</span>
```

### Buttons

#### Primary Button
```html
<a class="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-all">
    <span class="material-symbols-outlined">icon</span>
    Button Text
</a>
```

#### Secondary Button
```html
<button class="px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
    Button Text
</button>
```

#### Icon Button
```html
<button class="p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors">
    <span class="material-symbols-outlined">icon_name</span>
</button>
```

### Tables
Professional table styling with:
- Clear header styling
- Striped rows (optional)
- Hover effects
- Responsive behavior

```html
<table class="w-full text-sm">
    <thead class="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50">
        <tr>
            <th class="px-6 py-3 text-left font-semibold text-slate-900 dark:text-white">Column</th>
        </tr>
    </thead>
    <tbody>
        <tr class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <td class="px-6 py-4">Content</td>
        </tr>
    </tbody>
</table>
```

### Forms

#### Input Field
```html
<div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Label</label>
    <input type="text" placeholder="Placeholder..."
        class="w-full px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors" />
</div>
```

#### Select Field
```html
<div>
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Label</label>
    <div class="relative">
        <select class="w-full px-4 py-2.5 appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary">
            <option>Option 1</option>
        </select>
        <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
            <span class="material-symbols-outlined text-slate-400">expand_more</span>
        </span>
    </div>
</div>
```

### Progress Bar
```html
<div class="space-y-2">
    <div class="flex justify-between items-center">
        <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Progress</span>
        <span class="text-sm font-bold text-slate-900">45%</span>
    </div>
    <div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
        <div class="bg-gradient-to-r from-primary to-blue-400 h-full rounded-full transition-all" style="width: 45%"></div>
    </div>
</div>
```

## Shadows

Use these shadow classes for elevation:

```tailwind
/* Subtle */
shadow-sm   /* 0px 1px 3px rgba(0,0,0,0.17) */

/* Card */
hover:shadow-lg  /* 0px 4px 6px rgba(0,0,0,0.17) */

/* Modal/Overlay */
shadow-xl   /* 0px 8px 10px rgba(0,0,0,0.17) */
```

## Spacing Scale

- **Padding/Margin**: Use Tailwind's default scale
  - `p-4` = 1rem (16px)
  - `p-6` = 1.5rem (24px)
  - `p-8` = 2rem (32px)

## Border Radius

- **Cards**: `rounded-xl` (12px)
- **Buttons**: `rounded-lg` (8px)
- **Icons**: `rounded-full` (50%)
- **Badges**: `rounded-full` (50%)

## Transitions

- **Quick**: `transition-all` (150ms)
- **Hover**: `hover:shadow-lg`, `hover:text-primary`
- **Easing**: `ease-in-out` (default)

## Icons

All icons use Google Material Symbols:

```html
<span class="material-symbols-outlined text-[18px]">icon_name</span>
```

Common sizes:
- `text-[16px]` - Small
- `text-[18px]` - Medium (default)
- `text-[22px]` - Large
- `text-[28px]` - Extra Large

## Responsive Design

Breakpoints (Tailwind defaults):
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

Example:
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- Mobile: 1 column, Tablet: 2 columns, Desktop: 4 columns -->
</div>
```

## Best Practices

1. **Use CSS Variables** - Reference the design system colors via CSS custom properties
2. **Consistent Spacing** - Use the spacing scale for all padding/margins
3. **Icon + Text** - Always pair icons with text labels for clarity
4. **Color Hierarchy** - Use primary color for main actions, secondary for alternatives
5. **Hover States** - Always include hover effects for interactive elements
6. **Dark Mode** - Test all components in both light and dark modes
7. **Accessibility** - Use proper contrast ratios and semantic HTML
