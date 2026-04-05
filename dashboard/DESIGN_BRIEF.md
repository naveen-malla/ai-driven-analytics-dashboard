# Health Insights Dashboard — Design Brief

## Who uses this

The primary audience is a Chief Executive Officer or senior executive at a health-sector
organization — someone who allocates budgets, sets country strategy, and is accountable to a
board. They are not epidemiologists. They spend roughly two minutes on a dashboard before
forming a view. What they need to walk away knowing is: across Rwanda, Kenya, Uganda,
Ethiopia, and Tanzania — are we making progress on the core maternal and reproductive health
metrics that define Kasha's mission, and where are the critical gaps that need attention
right now?

## The story this dashboard tells

The six charts tell a single connected story about reproductive and maternal health in East
Africa. The story moves from **access** (do women have contraceptive choices and antenatal
care?) to **attendance** (are trained professionals present at birth?) to **outcomes** (are
mothers and children surviving?). HIV prevalence closes the loop as a cross-cutting indicator
that amplifies mortality risk. A CXO reading left-to-right, top-to-bottom should finish with
a clear mental model: which countries are leading, which are lagging, and which specific
indicator is the weakest link in the chain.

## Chart ordering rationale

The 6 charts are ordered to mirror the patient journey and the causal chain from prevention
through to survival outcome.

1. **contraceptive_prevalence** — First, because family planning is the entry point to the
   health system for women of reproductive age. It is also the most actionable metric for a
   distribution company: higher prevalence means higher demand for contraceptive products.
   Sets the market-access framing immediately.

2. **antenatal_care** — Second, because once a woman is pregnant, antenatal visits are her
   first structured contact with clinical care. This metric bridges the gap between family
   planning (preventing pregnancy) and safe delivery. Low antenatal coverage predicts bad
   downstream outcomes.

3. **skilled_birth** — Third, because skilled attendance at delivery is the single strongest
   structural predictor of maternal survival. The CXO can immediately compare this with
   antenatal coverage: a country might have strong ANC but weak skilled birth attendance,
   signalling a drop-off at the point of delivery.

4. **maternal_mortality** — Fourth, as the direct outcome metric for charts 2 and 3. By now
   the CXO understands the inputs; this chart shows the consequence. Lower = better, so high
   bars here against strong ANC/SBA scores signal a data quality or data lag issue worth
   flagging.

5. **under5_mortality** — Fifth, because child survival is downstream of maternal survival
   and the same structural factors. Placing it after maternal mortality shows the two
   together as a pair of outcome metrics. A CXO sees whether countries that struggle on
   maternal mortality also struggle on child mortality.

6. **hiv_prevalence** — Last, because HIV is a cross-cutting risk multiplier rather than a
   linear step in the patient journey. Ending with it signals: "here is the background
   epidemiological risk that complicates everything you just saw." High HIV prevalence
   countries face compounded mortality risk even when their health system metrics look
   reasonable.

## Information hierarchy

**First thing the CXO sees**: the page title and a one-sentence geographic scope line —
"5 East African countries · WHO Global Health Observatory data." This anchors what they are
looking at without requiring them to read further.

**Second**: the 2-column chart grid. Charts fill the viewport. The top row (contraceptive
prevalence, antenatal care) is immediately visible without scrolling and carries the
actionability message.

**Sidebar**: indicator definitions, data source attribution, and a brief "About" block. This
is secondary reference material — present but not competing for attention with the charts.
A CXO who wants to understand what "ANC 4+" means can find it there. One who does not can
ignore it.

**Below the chart grid**: the AI chat panel, full-width, separated by a visible divider.
It is intentionally below the fold — the static charts tell the story first, and the chat
panel is available for the CXO or their analyst who wants to dig deeper.

## AI chat panel

The chat panel serves the "what next" question after a CXO has seen something surprising in
the charts. Typical use cases:

- "Why is Kenya's contraceptive prevalence lower than Rwanda's?"
- "What was Ethiopia's under-5 mortality in 2015 versus 2020?"
- "Compare Uganda and Tanzania on skilled birth attendance."

The panel is full-width and placed below all 6 charts. It is NOT a central feature — it is
a drill-down tool. On demo day it should feel like a smart assistant the CXO can optionally
use, not the main attraction. If a chart is selected (the user clicked "Ask about this"),
the chat input is pre-primed with that chart's context.

The first suggested question shown in the chat input placeholder should always be
contextually relevant: if a chart is selected, reference that chart's indicator; otherwise
use a default open-ended prompt.

## Tone and visual language

**Professional and data-dense, not clinical.** This is an executive tool, not a patient
portal. The palette is blues and amber — trustworthy, authoritative, legible at a glance.
No pastels, no rounded cartoon elements.

**High contrast.** Text on background must pass WCAG AA (4.5:1 ratio). Chart labels are
legible at standard screen brightness. The sidebar background is a shade darker than the
main canvas to visually separate navigation from content.

**Calm but confident.** No gratuitous animation. Transitions are functional (loading states
only). The data speaks; the UI steps back.

**Africa-appropriate.** Country names are spelled in full. No three-letter ISO codes visible
to the end user. The map scope is implied by the data, not forced with decorative map
imagery.

## Design decisions locked

| Decision | Choice | Reason |
|---|---|---|
| Primary color | `#1E40AF` (deep blue) | Analytics dashboard blue from design system — trust, authority, data |
| Accent/highlight | `#F59E0B` (amber) | Contrast against blue; highlights the metric that needs attention |
| Background | `#F8FAFC` (near-white slate) | Easier on the eyes than pure white for long sessions |
| Sidebar background | `#EFF6FF` (light blue-tinted) | Visually separates nav from chart area without a hard border |
| Text color | `#1E3A8A` (dark navy) | Passes contrast against `#F8FAFC` and the sidebar color |
| Typography | Inter (all weights) | Minimal Swiss pairing — single font family, weight variations only. Optimal for dashboard readability. |
| Chart type (bars) | Horizontal bar chart | Country names are long enough that vertical bars truncate labels |
| Chart type (trends) | Line chart with markers | Clean time-series signal; markers make individual years scannable |
| Chart height | 350px | Fits 6 charts in 3 rows without excessive scrolling on a 1440px display |
| Layout | 2-column grid | 3 rows × 2 charts = the full 6 visible in a single scroll on 1080p |
| Chat panel position | Below all charts, full width | Static charts primary; chat is secondary drill-down |
| Sidebar state | Expanded by default | Indicator definitions visible on first load for non-expert viewers |
