# Themis Revamp — TODO

## UI / Styling

- [x] Fix the glitchiness of the Edit Project popup (animation / overlay jank)
- [x] Fix UI issues in the Edit Project and Add/Edit Client popups (layout, spacing)
- [x] Match dropdown colors with the main color theme (active item uses bg-primary)
- [x] Improve visual weight of input fields and dropdowns (borders, focus rings, styling)
- [x] Reduce dropdown list item size to match the rest of the app scale
- [x] Highlight the active/selected item in the sidebar nav
- [x] Fix font color mismatch in the Frameworks detail view
- [x] Fix client name font color mismatch in the Clients list view
- [x] Replace the Controls and Settings sidebar icons with better alternatives
- [x] Enhance the Icons of the client names and avatars across all views

## UI / Styling (Backlog)

- [ ] Fix Frameworks list page — old gray-* classes, no dark mode, cards need redesign to match app style
- [ ] Audit and fix Admin controls page styling (likely same gray-* mismatch)
- [ ] Sidebar collapse chevron should flip direction when sidebar is open/closed
- [ ] Fix "Finalize & Submit Audit" button in project detail — use bg-primary instead of bg-slate-900
- [ ] Fix dashboard project card progress bar — currently hardcoded to 0%
- [ ] Add proper empty state to dashboard when no active projects exist
- [ ] Polish the login page to match the current design system
- [ ] The profile hovering model window not align with the theme

## Features & Functionality

- [ ] (Future items to be added)

## Antigravity UX/UI suggestions

- [ ] **Sticky Action Buttons in Control Detail**: In `_control_detail.html`, move "Save & Continue" and "Cancel" buttons to a fixed bottom bar or sticky header so they remain accessible when long observations are added.
- [ ] **Empty State Polish**: Elevate the "No observations added yet" empty state in `_control_detail.html` using a subtle icon illustration or dotted-border drop-zone style.
- [ ] **Dropdown Positioning**: Custom Alpine.js dropdowns in filters (`list.html`) can be clipped by `overflow-hidden` containers. Consider adding Floating UI (Popper.js) for robust absolute positioning.
- [ ] **Scrollable Content Friction**: Requirements and Testing Procedures in `_control_detail.html` use `max-h-64` with inner scrollbars. Consider an expandable "Read More / Show Less" toggle instead of forcing scroll within a small box.
- [ ] **Dropdown Text Truncation**: Predefined observation dropdowns truncate text at ~60 characters, hiding crucial information. Consider a multi-line layout or adding a hover tooltip for long findings.
- [ ] **Mobile Filter UX**: The filter bar in `list.html` stacks large dropdowns vertically on mobile/tablet. Consider hiding filters behind a "Filters" button that opens a slide-out drawer or modal on smaller screens.
