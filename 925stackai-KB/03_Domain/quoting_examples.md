# Quoting Examples

Sample quoting scenarios demonstrating the application of the Cottesloe Window Cleaning pricing structure.

## Purpose

These examples illustrate how the [window cleaning pricing structure](window_cleaning_pricing.md) is applied in real-world scenarios. Each example shows the step-by-step calculation process used by the quoting system.

---

## Example 1: Minimum Charge Scenario

### Scenario
Small apartment with 4 small windows, exterior cleaning only, local area (Cottesloe).

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00 (local minimum)
* **Windows:** 4 × $6.00 (exterior only) = $24.00
* **Subtotal:** $114.00
* **Applied Minimum:** $90.00 (Base + Travel minimum)

**Final Quote: $114.00**

*Note: Subtotal exceeds minimum, so full calculation applies.*

---

## Example 2: Standard Residential Home

### Scenario
Single-story house in Cottesloe with:
- 8 standard sash windows (both sides)
- 2 French doors (both sides)
- Standard cleaning level

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00 (local)
* **Sash Windows:** 8 × $10.00 = $80.00
* **French Doors:** 2 × $10.00 = $20.00 (counted as standard panes)

**Final Quote: $190.00**

---

## Example 3: Two-Story Home with Mixed Services

### Scenario
Property in Swanbourne (6km from Cottesloe) with:
- 6 ground floor windows (both sides)
- 4 second-story windows (exterior only, requires WFP)
- 2 large picture windows (both sides)
- Mild cleaning level required

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00 + (1 × $2.00) = $12.00
* **Ground Floor:** 6 × $10.00 = $60.00
* **Second Story:** 4 × $12.00 = $48.00 (exterior only with height surcharge)
* **Large Windows:** 2 × $15.00 = $30.00
* **WFP Surcharge:** $20.00 (for upper-story access)
* **Mild Clean Adjustment:** +10% on window cleaning = +$13.80
* **Subtotal:** $263.80

**Final Quote: $263.80**

---

## Example 4: Weekend Emergency Service

### Scenario
City Beach property (30km round trip) requiring same-day weekend service:
- 6 standard windows (both sides)
- Heavy cleaning required (water stains)
- Weekend surcharge applies

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00 + (25 × $2.00) = $60.00
* **Windows:** 6 × $10.00 = $60.00
* **Heavy Clean Surcharge:** +20% on windows = +$12.00
* **Subtotal:** $212.00
* **Weekend Surcharge:** +30% on entire job = +$63.60
* **Same Day Travel Surcharge:** +25% on travel only = +$15.00

**Final Quote: $290.60**

---

## Example 5: Large Commercial Job

### Scenario
Office building with:
- 40 standard windows (exterior only)
- 8 large picture windows (both sides)
- Light cleaning level
- Regular maintenance discount applies

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00 (local)
* **Standard Windows:** 40 × $6.00 = $240.00
* **Large Windows:** 8 × $15.00 = $120.00
* **Light Clean Discount:** -10% on windows = -$36.00
* **Subtotal:** $414.00
* **Large Job Discount:** -10% (25+ windows) = -$33.40

**Final Quote: $380.60**

---

## Example 6: Heritage Property Special Handling

### Scenario
Heritage-listed home with:
- 12 leadlight windows (counted as 48 small panes)
- Deep frame cleaning required
- Post-construction cleanup (paint removal)

### Calculation
* **Base Fee:** $80.00
* **Travel Fee:** $10.00
* **Leadlight Panes:** 48 × $10.00 = $480.00
* **Deep Frame Cleaning:** 12 × $4.00 = $48.00
* **Post-Construction Surcharge:** +50% on affected panes = +$240.00
* **Subtotal:** $858.00
* **Large Job Discount:** -15% (50+ panes) = -$79.20

**Final Quote: $778.80**

---

## Calculation Logic Summary

The quoting system follows this sequence:

1. **Base Costs:** Apply base fee and travel charges
2. **Window Pricing:** Calculate per-pane costs based on type and size
3. **Service Adjustments:** Apply cleaning level modifiers
4. **Surcharges:** Add any applicable surcharges (height, WFP, urgency)
5. **Time-Based Adjustments:** Apply weekend/holiday surcharges
6. **Discounts:** Apply any eligible discounts (maintenance, large job, senior)
7. **Minimum Validation:** Ensure quote meets minimum charge requirements

For technical implementation details, see the [Quote Calculation Engine](../04_Logic/quote_calculation_engine.md) documentation.
