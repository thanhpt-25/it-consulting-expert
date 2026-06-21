---
name: design-presentation
description: >
  Create visually polished proposal presentations using Claude Design with
  Japanese enterprise design conventions. Use this skill when the user asks to
  "design the presentation in Claude Design", "Claude Designでプレゼン作成",
  "create a visual presentation", "ビジュアルプレゼン", "design beautiful slides",
  "make the presentation look professional", "polish the proposal deck",
  "デザインプレゼン", or wants to leverage Claude Design for high-quality
  visual presentation output. Also trigger for "Claude Design presentation",
  "visual deck", "デザイン提案資料", and any request that specifically mentions
  Claude Design for presentation work. This skill complements proposal-presentation
  — use proposal-presentation for content structure and Q&A prep, then this skill
  for visual polish via Claude Design.
metadata:
  version: "0.1.0"
---

# Visual Presentation Designer (Claude Design連携プレゼン)

Create visually polished, brand-consistent proposal presentations using Claude Design. This skill bridges the content extracted by `proposal-presentation` with Claude Design's visual capabilities, producing presentation-ready HTML slides that can be imported into Claude Design for further refinement and exported to PowerPoint, PDF, or deployed to Vercel.

## Why This Matters

In Japanese enterprise bidding, visual quality signals professionalism. Two proposals with identical content will score differently based on presentation quality. Claude Design enables designer-grade visual output — proper layout grids, consistent spacing, professional diagrams — without requiring a graphic designer. This matters especially for competitive bids where the presentation IS the differentiator.

## Prerequisites

- **proposal-presentation skill** should run first to generate the content structure, slide outline, and Q&A preparation
- **NotebookLM** with the client's RFP (for grounding — inherited from proposal-presentation)
- **Vercel MCP** connected (for `import-claude-design-from-url` tool)
- **Claude Design** accessible (Claude Pro, Max, Team, or Enterprise subscription)

## Workflow

### Step 0: Gather Proposal Content

If the user hasn't already run `proposal-presentation`, prompt them to do so first. The content structure from that skill feeds this one.

Collect from the user or from the prior skill output:
- **Slide outline** (15-slide structure from proposal-presentation)
- **Key data points** from NotebookLM extraction
- **Company branding**: Logo URL/file, primary color, secondary color, font preference
- **Client name** and project name
- **Presentation duration** (determines content density per slide)
- **Design impression**: Conservative/trustworthy, modern/innovative, or warm/approachable

### Step 1: Design System Setup

Define the visual design system for the presentation. Japanese enterprise presentations follow specific conventions.

**Color Palette Selection:**

| Impression | Primary | Secondary | Accent | Background | Text |
|-----------|---------|-----------|--------|------------|------|
| Conservative (金融・官公庁) | Navy #1a365d | Slate #334155 | Blue #3b82f6 | White #ffffff | Dark Gray #1e293b |
| Modern (IT・DX) | Deep Blue #1e40af | Teal #0d9488 | Cyan #06b6d4 | White #ffffff | Slate #334155 |
| Warm (医療・教育) | Royal Blue #1d4ed8 | Orange #d97706 | Amber #f59e0b | White #ffffff | Gray #374151 |

**Typography:**
- Japanese: Meiryo, Yu Gothic, or Noto Sans JP
- English: Calibri, Arial, or Inter
- Title: 28-32px bold
- Subtitle: 20-24px semibold
- Body: 16-18px regular
- Caption: 12-14px light

**Layout Grid:**
- Slide dimensions: 1280 × 720px (16:9 widescreen)
- Margins: 40px all sides
- Header bar height: 60px
- Footer height: 30px (page number + company logo)
- Content area: 1200 × 590px

### Step 2: Generate Slide HTML

Create a self-contained HTML file that renders as a slide deck. Each slide is a `<section>` element styled to fill exactly 1280×720px.

**HTML Structure:**

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1280">
  <title>[Project Name] 提案書</title>
  <style>
    /* Design system variables */
    :root {
      --primary: #1a365d;
      --secondary: #334155;
      --accent: #3b82f6;
      --bg: #ffffff;
      --text: #1e293b;
      --text-light: #64748b;
      --font-ja: 'Meiryo', 'Yu Gothic', sans-serif;
      --font-en: 'Calibri', 'Arial', sans-serif;
    }

    /* Slide base */
    section.slide {
      width: 1280px;
      height: 720px;
      position: relative;
      overflow: hidden;
      background: var(--bg);
      font-family: var(--font-ja);
      page-break-after: always;
      box-sizing: border-box;
      padding: 40px;
    }

    /* Header bar */
    .slide-header {
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 60px;
      background: var(--primary);
      color: white;
      display: flex;
      align-items: center;
      padding: 0 40px;
      font-size: 18px;
      font-weight: 600;
    }

    /* Footer */
    .slide-footer {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      height: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 40px;
      font-size: 11px;
      color: var(--text-light);
      border-top: 1px solid #e2e8f0;
    }

    /* Content area (below header, above footer) */
    .slide-content {
      margin-top: 70px;
      margin-bottom: 40px;
      height: 570px;
    }
  </style>
</head>
<body>
  <!-- Slides rendered here -->
</body>
</html>
```

**Slide Templates by Type:**

**Title Slide (表紙):**
- Full-height primary color background OR white with large logo
- Project title centered, 36px bold
- Client name with 御中, 24px
- Company name, date, presenter name
- 秘密保持 (Confidential) badge in corner

**Section Divider (セクション区切り):**
- Primary color background, white text
- Section number + title centered
- Subtle geometric pattern or gradient

**Content Slide (本文):**
- Header bar with section title
- Left-aligned title, 24px bold
- Body content with 16px text
- Maximum 6-7 lines or bullet points
- Optional right-side visual (diagram, chart, icon)

**Comparison Slide (比較):**
- 2-column or 3-column layout
- Consistent card styling per column
- Color-coded headers per option
- Check/cross icons for feature comparison

**Architecture Diagram Slide:**
- Full content area for diagram
- Use SVG for clean, scalable diagrams
- Component boxes with rounded corners
- Directional arrows with labels
- Color-coded by layer (frontend/backend/data/infra)

**Timeline/Gantt Slide:**
- Horizontal bars with phase labels
- Milestone diamonds at key dates
- Color-coded by status or team
- Today line if showing current progress

**Team Slide (体制図):**
- Organizational tree layout
- Role boxes with name + title
- Connecting lines showing reporting structure
- Photo placeholders (rounded circles)

**Cost Summary Slide:**
- Summary table with phase/category rows
- Total highlighted row
- Bar chart or pie chart alongside
- Payment schedule timeline below

### Step 3: Visual Enhancement Techniques

Apply these techniques to elevate visual quality:

**Icons:**
- Use inline SVG icons from a consistent set (Lucide, Heroicons, or Phosphor)
- 24px standard size, matching primary color
- Place beside section titles and key points

**Data Visualization:**
- Inline SVG charts (bar, donut, line) — no external dependencies
- Consistent color palette from design system
- Always label axes and include units
- Use the client's own numbers from the RFP (via NotebookLM)

**Whitespace:**
- Generous margins between elements (24px minimum)
- Never fill more than 60% of a slide with content
- Use whitespace to guide the eye to key information

**Visual Hierarchy:**
- Primary color for key numbers and differentiators
- Bold for emphasis, not underline or italic
- Size contrast: title (28px) → subtitle (20px) → body (16px) → caption (12px)

**Consistency Checks:**
- Same margin, padding, font sizes across all slides
- Header bar identical on every content slide
- Footer with page number on every slide
- Color usage follows the design system exactly

### Step 4: Import to Claude Design

Once the HTML is generated, import it into Claude Design for interactive refinement:

```
1. Host the HTML file at a publicly accessible URL
   (use Vercel deployment or a temporary hosting service)

2. Use the import tool:
   import-claude-design-from-url
     url: "<public URL of the HTML file>"
     title: "[Client Name] 提案プレゼン"

3. In Claude Design, refine:
   - Adjust layouts interactively
   - Add animations or transitions
   - Fine-tune typography and spacing
   - Import company design system from GitHub (if available)
   - Add real images, logos, or screenshots
```

**Alternative workflow — direct Claude Design prompting:**

If the user prefers to work entirely in Claude Design, provide the slide content as structured prompts:

```
Slide 1 (Title):
- Title: [Project Name] ご提案書
- Subtitle: [Client Name] 御中
- Company: [Your Company]
- Date: [Date]
- Style: Navy background, white text, corporate, Japanese enterprise

Slide 2 (Agenda):
- Title: 本日のご説明内容
- Items: 1. お客様の課題認識 (3分) 2. ご提案内容 (5分) ...
- Style: White background, numbered list with accent color
```

### Step 5: Export Options

Claude Design supports multiple export formats:

| Format | Use Case | How |
|--------|----------|-----|
| PowerPoint (.pptx) | Client submission, offline viewing | Export → PowerPoint |
| PDF | Formal submission, print | Export → PDF |
| HTML (Vercel) | Interactive viewing, web sharing | Deploy to Vercel |
| Canva | Further design editing | Send to Canva |
| Image (PNG) | Individual slide images for documents | Export → Images |

For Japanese enterprise submissions, **PowerPoint** is the standard format. Export to .pptx for the formal submission, and optionally deploy to Vercel for internal team review.

### Step 6: Quality Checklist

Before finalizing, verify:

- [ ] All slides follow the design system (colors, fonts, spacing)
- [ ] Every client-specific fact is grounded in the RFP ([RFP] labels in speaker notes)
- [ ] Page numbers on every slide (except title)
- [ ] Company logo in footer, consistent placement
- [ ] Client name with proper honorific (御中)
- [ ] 秘密保持 marking present
- [ ] No more than 6-7 lines of text per slide
- [ ] All diagrams are readable at presentation distance
- [ ] Japanese text uses appropriate keigo level
- [ ] Slide count matches allocated presentation time (~1 slide per 1.5 minutes)
- [ ] Font rendering correct for both Japanese and English mixed content

### Step 7: Output

Deliver:
1. Self-contained HTML slide deck (for Claude Design import)
2. Claude Design project link (after import)
3. Exported .pptx (for client submission)
4. Q&A preparation document (from proposal-presentation skill, not duplicated here)

## Key Principles

- **Content first, design second**: Never sacrifice accuracy for aesthetics. The RFP-grounded content from proposal-presentation is the foundation
- **Consistency over creativity**: Japanese enterprise evaluators value professionalism and consistency over creative flair
- **Less is more**: Every element on a slide must earn its place. Remove anything that doesn't directly support the message
- **Test at distance**: Slides are projected, not read on a laptop. Text must be readable from 5 meters
- **Respect the brand**: Use the client's industry-appropriate color palette, not trendy designs
- **Accessible**: Sufficient color contrast (WCAG AA minimum), clear fonts, no information conveyed by color alone

For design templates and component library, read `references/design-components.md`.
