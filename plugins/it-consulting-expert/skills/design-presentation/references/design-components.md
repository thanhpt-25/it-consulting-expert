# Design Components Library (デザインコンポーネント集)

## SVG Icon Set

Inline SVG icons for consistent use across slides. All icons are 24×24 viewBox, stroke-based.

### Common Presentation Icons

```svg
<!-- Checkmark (for features, completed items) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <polyline points="20 6 9 17 4 12"></polyline>
</svg>

<!-- Arrow Right (for flow, next steps) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <line x1="5" y1="12" x2="19" y2="12"></line>
  <polyline points="12 5 19 12 12 19"></polyline>
</svg>

<!-- Users (for team slides) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
  <circle cx="9" cy="7" r="4"></circle>
  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
</svg>

<!-- Shield (for security) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
</svg>

<!-- Server (for infrastructure) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
  <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
  <line x1="6" y1="6" x2="6.01" y2="6"></line>
  <line x1="6" y1="18" x2="6.01" y2="18"></line>
</svg>

<!-- Calendar (for timeline) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
  <line x1="16" y1="2" x2="16" y2="6"></line>
  <line x1="8" y1="2" x2="8" y2="6"></line>
  <line x1="3" y1="10" x2="21" y2="10"></line>
</svg>

<!-- Yen (for cost) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <line x1="12" y1="1" x2="12" y2="23"></line>
  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
</svg>

<!-- Warning (for risks) -->
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
  <line x1="12" y1="9" x2="12" y2="13"></line>
  <line x1="12" y1="17" x2="12.01" y2="17"></line>
</svg>
```

## Chart Components (Inline SVG)

### Horizontal Bar Chart

```html
<div class="bar-chart" style="width:100%; max-width:600px;">
  <div style="display:flex; align-items:center; margin-bottom:12px;">
    <span style="width:120px; font-size:14px; color:#334155;">要件定義</span>
    <div style="flex:1; background:#e2e8f0; border-radius:4px; height:24px;">
      <div style="width:15%; background:#3b82f6; border-radius:4px; height:24px;
                  display:flex; align-items:center; justify-content:flex-end; padding-right:8px;
                  color:white; font-size:12px; font-weight:600;">15%</div>
    </div>
  </div>
  <!-- Repeat for each phase -->
</div>
```

### Donut Chart (for budget allocation)

```svg
<svg width="200" height="200" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="80" fill="none" stroke="#e2e8f0" stroke-width="30"/>
  <!-- Segment 1: 40% -->
  <circle cx="100" cy="100" r="80" fill="none" stroke="#1a365d" stroke-width="30"
          stroke-dasharray="201 503" stroke-dashoffset="0" transform="rotate(-90 100 100)"/>
  <!-- Segment 2: 30% -->
  <circle cx="100" cy="100" r="80" fill="none" stroke="#3b82f6" stroke-width="30"
          stroke-dasharray="151 503" stroke-dashoffset="-201" transform="rotate(-90 100 100)"/>
  <!-- Center label -->
  <text x="100" y="95" text-anchor="middle" font-size="24" font-weight="700" fill="#1e293b">¥80M</text>
  <text x="100" y="115" text-anchor="middle" font-size="12" fill="#64748b">Total Budget</text>
</svg>
```

## Slide Layout Patterns

### Two-Column with Icon Headers

```html
<div style="display:grid; grid-template-columns:1fr 1fr; gap:40px; margin-top:20px;">
  <div>
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
      <div style="width:40px; height:40px; background:#eff6ff; border-radius:8px;
                  display:flex; align-items:center; justify-content:center; color:#1a365d;">
        <!-- Icon SVG here -->
      </div>
      <h3 style="font-size:20px; font-weight:600; color:#1a365d; margin:0;">見出し</h3>
    </div>
    <p style="font-size:16px; line-height:1.6; color:#334155;">本文テキスト</p>
  </div>
  <!-- Column 2 same structure -->
</div>
```

### KPI Card Row

```html
<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:20px; margin-top:24px;">
  <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px;
              padding:24px; text-align:center;">
    <div style="font-size:14px; color:#64748b; margin-bottom:8px;">プロジェクト期間</div>
    <div style="font-size:32px; font-weight:700; color:#1a365d;">12</div>
    <div style="font-size:14px; color:#64748b;">ヶ月</div>
  </div>
  <!-- Repeat for each KPI -->
</div>
```

### Timeline / Gantt Bar

```html
<div style="position:relative; margin-top:24px;">
  <!-- Phase row -->
  <div style="display:flex; align-items:center; margin-bottom:8px;">
    <div style="width:120px; font-size:13px; color:#334155;">要件定義</div>
    <div style="flex:1; position:relative; height:28px;">
      <!-- Bar positioned at correct start/width -->
      <div style="position:absolute; left:0%; width:15%; height:100%;
                  background:#1a365d; border-radius:4px;
                  display:flex; align-items:center; justify-content:center;
                  color:white; font-size:11px;">2ヶ月</div>
    </div>
  </div>
  <!-- Repeat for each phase, adjusting left% and width% -->
</div>
```

### Organization Chart Node

```html
<div style="display:flex; flex-direction:column; align-items:center;">
  <div style="width:160px; background:white; border:2px solid #1a365d;
              border-radius:8px; padding:12px; text-align:center;">
    <div style="font-size:11px; color:#64748b; margin-bottom:4px;">プロジェクトマネージャー</div>
    <div style="font-size:15px; font-weight:600; color:#1e293b;">山田 太郎</div>
    <div style="font-size:11px; color:#3b82f6; margin-top:4px;">PMP / 15年経験</div>
  </div>
  <!-- Connecting line -->
  <div style="width:2px; height:20px; background:#cbd5e1;"></div>
</div>
```

## Japanese Enterprise Design Rules

### Do's

- White or very light backgrounds — dark themes feel casual in Japanese enterprise
- Consistent header bar on every content slide
- Page numbers bottom-right on every slide
- Company logo in footer, small and unobtrusive
- Formal keigo in all text
- Numbers right-aligned in tables
- ¥ symbol with comma separators (¥1,234,567)
- Date format: YYYY年MM月DD日 or YYYY/MM/DD

### Don'ts

- No dark/black slide backgrounds for formal proposals
- No casual fonts (Comic Sans, handwriting styles)
- No clip art or stock photos with watermarks
- No gradient text or text shadows
- No more than 3 colors beyond black/white/gray
- No animation descriptions (animations are added in Claude Design or PowerPoint)
- No English-only slides for Japanese client presentations (bilingual OK)

### Accessibility Minimums

- Text contrast ratio ≥ 4.5:1 against background (WCAG AA)
- Minimum body text size: 16px (projected slides need larger text)
- Don't rely on color alone to convey information (add labels/patterns)
- Alt text concepts for diagrams (included in speaker notes)

## Integration with Claude Design

### Import Checklist

Before importing to Claude Design via `import-claude-design-from-url`:

- [ ] All images inlined as base64 data URIs or SVG
- [ ] All fonts specified with web-safe fallbacks
- [ ] All CSS inline (no external stylesheets)
- [ ] No external JavaScript dependencies
- [ ] File size under 5MB
- [ ] HTML validates (no unclosed tags)

### Post-Import Refinement in Claude Design

After import, use Claude Design to:

1. **Adjust spacing** — fine-tune margins between elements interactively
2. **Add transitions** — subtle slide transitions for presentation mode
3. **Insert images** — add real screenshots, architecture diagrams, or photos
4. **Apply design system** — if you have a GitHub-hosted design system, import it
5. **Iterate with prompts** — ask Claude Design to refine specific slides
6. **Export** — PowerPoint for client submission, PDF for printing, Vercel for sharing
